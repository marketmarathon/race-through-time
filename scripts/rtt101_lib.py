#!/usr/bin/env python3
"""RTT-101 (IQ-15) shared helpers: club-name matching and fee-text parsing.

Fee parsing never guesses: text it cannot read exactly returns None (NOT FOUND), and qualifiers such as
"up to", "rising to", "potential", "reported", "believed" are reported separately (DEC-237 (e), (g))."""
import csv, os, re, unicodedata, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ALIASES = os.path.join(HERE, "..", "data", "rtt-101", "source", "club_aliases.csv")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = s.replace("&", " and ")
    s = re.sub(r"\b(a\.?f\.?c\.?|f\.?c\.?)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


_club_index = None


def club_index():
    global _club_index
    if _club_index is None:
        idx = {}
        for r in csv.DictReader(open(ALIASES, encoding="utf-8")):
            names = [r["display_name"], r["wikipedia_title"], r["club_id"].replace("_", " ")]
            names += [n for n in r["other_names"].split("|") if n and "(" not in n]
            for n in names:
                idx.setdefault(norm(n), r["club_id"])
        idx[norm("Wimbledon F.C.")] = "wimbledon_fc"
        for bad in ("afc wimbledon", "milton keynes dons", "mk dons"):
            idx[bad] = None  # never Wimbledon FC (identity rule)
        _club_index = idx
    return _club_index


def club_id(name):
    """PL club_id for a club name, or None if it is not one of the 51 PL clubs (or is AFC Wimbledon / MK Dons)."""
    n = norm(name)
    idx = club_index()
    if n in idx:
        return idx[n]
    return None


UNITS = {"m": 1e6, "mn": 1e6, "million": 1e6, "mil": 1e6, "k": 1e3, "thousand": 1e3, "bn": 1e9, "billion": 1e9}
CUR = [("£", "GBP"), ("€", "EUR"), ("$", "USD"), ("us$", "USD"), ("pounds", "GBP"), ("pound", "GBP"), ("euros", "EUR"),
       ("euro", "EUR"), ("eur", "EUR"), ("gbp", "GBP"), ("usd", "USD"), ("dollars", "USD")]
QUAL = {"up_to": r"\b(up to|rising to|could rise|potential(ly)?|as much as|maximum|could reach|could exceed|in total)\b",
        "reported": r"\b(reported(ly)?|believed|thought to be|understood|around|about|approximately|in the region of|some|estimated|undisclosed|c\.)\b",
        "plus": r"(\+|\bplus\b|add-ons|add ons)"}

NUM = r"(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)"


GUAR = [r"(?:initial|guaranteed|fixed|up-front|upfront|basic)\s+(?:fee\s+)?(?:of\s+)?(?:club[- ]record\s+fee\s+of\s+)?((?:£|€|\$)\s?[\d.,]+\s*(?:m|mn|million|bn|billion)?)",
        r"((?:£|€|\$)\s?[\d.,]+\s*(?:m|mn|million)?)\s+(?:up front|upfront|guaranteed|fixed)",
        r"((?:£|€|\$)\s?[\d.,]+\s*(?:m|mn|million)?)\s*(?:\(|,)?\s*(?:plus|\+|with)\s+(?:a\s+further\s+|another\s+|up\s+to\s+(?:another\s+|a\s+further\s+)?)?(?:£|€|\$)\s?[\d.,]+\s*(?:m|mn|million)?\s+(?:in\s+)?(?:potential\s+)?(?:add-ons|add ons|bonuses|performance|variable|instalments?)"]


def guaranteed_part(text):
    """The guaranteed amount when the text separates it from add-ons (DEC-237 (e)); None if not stated."""
    low = (text or "").lower().replace("pounds ", "£")
    for rx in GUAR:
        m = re.search(rx, low)
        if m:
            p = parse_fee(m.group(1), _plain=True)
            if p["amount"] is not None:
                return p
    return None


def parse_fee(text, _plain=False):
    """Return dict(amount, currency, qualifiers, kind) for the FIRST money amount in text, or kind for free/loan/undisclosed.
    amount is a float in currency units; None when not exactly readable."""
    t = (text or "").strip()
    low = t.lower()
    out = {"amount": None, "currency": None, "qualifiers": [], "kind": "fee"}
    for q, rx in QUAL.items():
        if re.search(rx, low):
            out["qualifiers"].append(q)
    if not t or low in ("not found", "n/a", "-", "—", "?"):
        out["kind"] = "none"; return out
    if re.fullmatch(r"(free|free transfer|nominal|released|end of contract|bosman)\b.*", low) and not re.search(r"\d", low):
        out["kind"] = "free"; out["amount"] = 0.0; out["currency"] = "GBP"; return out
    if re.search(r"combined|joint fee|for both players|together with", low):
        out["qualifiers"].append("combined")  # a fee for more than one player is never one deal's fee
    if "undisclosed" in low and not re.search(r"\d", low):
        out["kind"] = "undisclosed"; return out
    if re.fullmatch(r"(loan|on loan|season-long loan|loan return|end of loan|loaned)\b.*", low) and not re.search(r"\d", low):
        out["kind"] = "loan_no_fee"; return out
    low = re.sub(r"\b(pounds?|stg|gbp)\s?(?=\d)", "£", low)
    low = re.sub(r"\b(euros?|eur)\s?(?=\d)", "€", low)
    m = re.search(r"(£|€|\$|us\$)\s?" + NUM + r"\s*(bn|billion|m|mn|million|mil|k|thousand)?\b", low)
    if m:
        cur = {"£": "GBP", "€": "EUR", "$": "USD", "us$": "USD"}[m.group(1)]
        n = float(m.group(2).replace(",", ""))
        unit = m.group(3)
    else:
        m = re.search(NUM + r"\s*(bn|billion|m|mn|million|mil|k|thousand)?\s*(pounds|pound|euros|euro|eur|gbp|usd|dollars)\b", low)
        if not m:
            return out
        n = float(m.group(1).replace(",", ""))
        unit = m.group(2)
        cur = {"pounds": "GBP", "pound": "GBP", "gbp": "GBP", "euros": "EUR", "euro": "EUR", "eur": "EUR",
               "usd": "USD", "dollars": "USD"}[m.group(3)]
    if unit:
        n *= UNITS[unit]
    elif n < 1000:
        return out  # "£7" with no unit is ambiguous: NOT FOUND, never guessed
    out["amount"] = round(n, 2)
    out["currency"] = cur
    if not _plain:
        g = guaranteed_part(t)
        if g and (g["amount"] != out["amount"] or g["currency"] != out["currency"]):
            out["amount"], out["currency"] = g["amount"], g["currency"]
            out["qualifiers"] = [q for q in out["qualifiers"] if q != "up_to"] + ["guaranteed_part"]
            return out
    # "up to £X" applies only when the qualifier comes before the first amount ("£12m rising to £15m" = £12m guaranteed)
    if "up_to" in out["qualifiers"] and not re.search(QUAL["up_to"], low[:m.start()]):
        out["qualifiers"] = [q for q in out["qualifiers"] if q != "up_to"] + ["max_later"]
    return out


# publisher grade of a cited page (DEC-254): club or league site A; quality press B; databases C; anything else D
B = ("bbc.co.uk", "bbc.com", "theguardian.com", "guardian.co.uk", "observer", "skysports.com", "sky.com", "independent.co.uk",
     "the-independent.com", "telegraph.co.uk", "thetimes.co.uk", "timesonline", "reuters.com", "uefa.com", "nytimes.com",
     "theathletic.com", "espn.", "ft.com", "pa.media")
A = ("premierleague.com", "fc.com", "fc.co.uk", "arsenal.com", "mancity.com", "manutd.com", "tottenhamhotspur.com", "nufc.co.uk",
     "evertonfc.com", "whufc.com", "avfc.co.uk", "lcfc.com", "wolves.co.uk", "afcb.co.uk", "brightonandhovealbion.com", "cpfc.co.uk",
     "fulhamfc.com", "nottinghamforest.co.uk", "brentfordfc.com", "leedsunited.com", "burnleyfootballclub.com", "sunderlandafc.com",
     "ipswichtown.co.uk", "coventrycity.co.uk", "hullcitytigers.com", "londonstockexchange.com", "juventus.com", "realmadrid.com",
     "fcbarcelona.com", "slbenfica.pt", "sporting.pt", "bvb.de", "psg.fr")
C = ("soccerbase.com", "wikipedia.org", "worldfootball.net")


def grade_of(url):
    h = urllib.parse.urlparse(url).netloc.lower()
    if any(x in h for x in C):
        return "C"
    if any(x in h for x in A):
        return "A"
    if any(x in h for x in B):
        return "B"
    return "D"


# words before a figure that mean it is not this deal's guaranteed fee (a maximum, valuation, offer or another figure)
NOTFEE = re.compile(r"(combined|up to|could be worth|could rise|could reach|rising to|rise to|potentially|valued|valuation|similar to|demanding|"
                    r"\bbid\b|\boffer|asking for|wanted|rejected|in excess of|more than|over)\W*(a\s+|an\s+|about\s+|around\s+)?$", re.I)
