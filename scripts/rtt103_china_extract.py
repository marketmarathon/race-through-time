#!/usr/bin/env python3
"""RTT-103 (IQ-16): quarterly capex of the China-listed companies, read from their own filings (RMB, as printed).

Finding list: the private research catalogues' coverage grids (which document covers which quarter). Every figure is
read by this script from the document itself; the research catalogue's own claims are never used as figures.

Baidu: each quarter's results release on sec.gov (6-K exhibit 99.1).
  - 2009 Q2 - 2014 Q4: the narrative sentence "capital expenditures for the <n> quarter of <year> were RMB<x> million|billion"
    (printed to RMB 0.1m below RMB1bn and to RMB1m above).
  - 2015 Q1 onwards: the free-cash-flow reconciliation row "Less: Capital expenditures" (exact; thousands until Q1 2017,
    millions from Q2 2017). Columns: prior-year quarter, previous quarter, current quarter (+ US$ convenience and
    twelve-month columns). From Q3 2018 Baidu Core, iQIYI and Baidu (consolidated) are shown; the consolidated figure
    is used. The prior-year and previous-quarter columns are kept as later observations of those quarters.
Output CSV (data/rtt-103/source/china_observations.csv) columns: see FIELDS.

Usage: rtt103_china_extract.py <private_rtt103_dir> <catalogue_sec_index_csv> <sec_cache_dir> <out_csv> [fetched_dir]
"""
import csv
import gzip
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rtt103_sec_docs import to_text  # noqa: E402

FIELDS = ["company_id", "line", "period_start", "period_end", "duration", "value_local", "currency", "printed_value",
          "printed_units", "metric_name_exact", "source_id", "source_url", "source_sha256", "publication_date",
          "page_table", "quote", "role", "grade", "verified", "notes"]
ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4}
Q_END = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
Q_START = {1: "01-01", 2: "04-01", 3: "07-01", 4: "10-01"}


def blocks(path):
    raw = open(path, encoding="utf-8-sig").read()
    return [list(csv.DictReader(io.StringIO(b))) for b in re.findall(r"```csv\n(.*?)```", raw, flags=re.S)]


def prev_q(y, q, n=1):
    for _ in range(n):
        y, q = (y, q - 1) if q > 1 else (y - 1, 4)
    return y, q


def rmb(amount, unit):
    v = float(amount.replace(",", ""))
    return round(v * (1e9 if unit.lower().startswith("b") else 1e6))


def nums_of(row):
    out = []
    for cell in row.split("|")[1:]:
        c = cell.strip()
        if re.fullmatch(r"[—–-]+", c):
            out.append(0)
            continue
        m = re.search(r"\(\s*([\d,]+)", c)  # capex is printed as an outflow, in parentheses; percentages are not
        if m and "%" not in c:
            out.append(int(m.group(1).replace(",", "")))
    return out


def baidu(priv, idx, cache):
    cat, cov = blocks(os.path.join(priv, "part03b_china_prompt_baidu_Section_A_file.txt"))[:2]
    out = []
    for c in cov:
        end = c["fiscal_period_end"]
        y, q = int(end[:4]), (int(end[5:7]) - 1) // 3 + 1
        ids = [i.strip() for i in c["quarter_figure_source_ids"].split(";")]
        secs = [i for i in ids if i in idx]
        if not secs:
            continue
        sid = secs[0]
        meta = idx[sid]
        text = to_text(gzip.open(os.path.join(cache, meta["cache_file"])).read())
        pubdate = next((r["publication_date"] for r in cat if r["source_id"] == sid), "")
        base = {"company_id": "baidu", "line": "company_capex", "currency": "CNY", "source_id": sid,
                "source_url": meta["url"], "source_sha256": meta["sha256"], "publication_date": pubdate,
                "grade": "A", "verified": "VERIFIED", "metric_name_exact": "Capital expenditures"}
        rows = [ln for ln in text.split("\n") if re.match(r"less: capital expenditures", ln, re.I)]
        if rows:
            groups = []
            for r in rows:
                n = nums_of(r)
                groups.append(n)
            three = groups[0]
            if len(rows) >= 3 and len(groups[2]) >= 3:          # Q3-Q4 2018: Core, iQIYI, Baidu rows
                cons = groups[2]
                vals, note = cons[:3], "Consolidated 'Baidu' row (Baidu Core and iQIYI shown separately)."
                qrow = rows[2]
            elif len(three) >= 12:                               # 2019+: groups of (Core, iQIYI, Baidu)
                vals, note = [three[2], three[5], three[8]], "Consolidated 'Baidu' column (third of Baidu Core, iQIYI, Baidu)."
                qrow = rows[0]
            else:                                                # 2015 - Q2 2018: single row
                vals, note = three[:3], "Single consolidated row."
                qrow = rows[0]
            scale = 1e3 if max(vals) > 100000 else 1e6
            unit = "RMB thousands" if scale == 1e3 else "RMB millions"
            for k, (yy, qq) in enumerate([prev_q(y, q, 4), prev_q(y, q, 1), (y, q)]):
                out.append(dict(base, period_start=f"{yy}-{Q_START[qq]}", period_end=f"{yy}-{Q_END[qq]}", duration="3M",
                                value_local=int(vals[k] * scale), printed_value=f"({vals[k]:,})", printed_units=unit,
                                page_table="Reconciliation from net cash provided by operating activities to free cash flow, row 'Less: Capital expenditures'",
                                quote=qrow[:300], role="current" if k == 2 else ("prior_year_comparative" if k == 0 else "previous_quarter_comparative"),
                                notes=note + (" Comparative column in a later release." if k < 2 else "")))
            # twelve-month figures in Q4 releases
            fyv, fyrow = None, None
            if q == 4:
                if len(three) >= 12 and len(rows) > 1 and len(groups[-1]) >= 6:      # 2019+: separate twelve-month row
                    fyv, fyrow = groups[-1][5], rows[-1]
                elif len(rows) >= 3 and len(groups[2]) >= 7:                          # 2018: consolidated row
                    fyv, fyrow = groups[2][5], rows[2]
                elif len(three) >= 5:                                                 # 2015-2017: single row
                    fyv, fyrow = three[4], rows[0]
            if fyv:
                out.append(dict(base, period_start=f"{y}-01-01", period_end=f"{y}-12-31", duration="12M",
                                value_local=int(fyv * scale), printed_value=f"({fyv:,})", printed_units=unit,
                                page_table="Free cash flow reconciliation, twelve months", quote=fyrow[:300], role="annual",
                                notes="Consolidated twelve-month figure."))
            continue
        if q == 4:
            for s in re.split(r"(?<=\.)\s+", text.replace("\n", " ")):
                if not re.search(r"(full year|in %d\b).{0,60}capital expenditures|capital expenditures in %d" % (y, y), s, re.I):
                    continue
                amts = re.findall(r"RMB\s*([\d.,]+)\s*(million|billion)", s)
                if not amts:
                    continue
                # "net operating cash inflow and capital expenditures ... were RMB<x> and RMB<y>, respectively": capex is the second
                amt = amts[1] if ("operating cash inflow and capital expenditures" in s.lower() and len(amts) > 1) else amts[-1] if "operating cash inflow" in s.lower().split("capital expenditures")[0] and len(amts) > 1 and "respectively" in s else amts[0]
                if "capital expenditures in %d were" % y in s.lower() and "operating cash inflow in" in s.lower():
                    amt = amts[-1]
                out.append(dict(base, period_start=f"{y}-01-01", period_end=f"{y}-12-31", duration="12M",
                                value_local=rmb(*amt), printed_value=f"RMB{amt[0]} {amt[1]}",
                                printed_units=f"RMB {amt[1]}s (rounded as printed)", page_table="Results release text",
                                quote=s.strip()[:300], role="annual", notes="Full-year narrative figure, rounded as printed."))
                break
        for s in re.split(r"(?<=\.)\s+", text.replace("\n", " ")):
            m = re.search(r"capital expenditures (?:for|in) the (\w+) quarter of (\d{4}) were\s*RMB\s*([\d.,]+)\s*(million|billion)", s, re.I)
            m2 = re.search(r"net operating cash inflow and capital expenditures for the (\w+) quarter of (\d{4}) were\s*RMB\s*[\d.,]+\s*(?:million|billion)"
                           r".*?and\s*RMB\s*([\d.,]+)\s*(million|billion)", s, re.I)
            m = m2 or m  # the combined sentence names operating cash first and capex second
            m3 = re.search(r"capital expenditures were\s*RMB\s*([\d.,]+)\s*(million|billion)", s, re.I)
            if m:
                if (int(m.group(2)), ORD[m.group(1).lower()]) != (y, q):
                    continue
                amt, unit_ = m.group(3), m.group(4)
            elif m3:  # 2018: "Net operating cash inflow was ... and capital expenditures were RMB 2.0 billion" (quarter of the release)
                amt, unit_ = m3.group(1), m3.group(2)
            else:
                continue
            out.append(dict(base, period_start=f"{y}-{Q_START[q]}", period_end=end, duration="3M",
                            value_local=rmb(amt, unit_), printed_value=f"RMB{amt} {unit_}",
                            printed_units=f"RMB {unit_}s (rounded as printed)", page_table="Results release text (cash flow paragraph)",
                            quote=s.strip()[:300], role="current", notes="Narrative figure, rounded as printed."))
            break
        else:
            out.append(dict(base, period_start=f"{y}-{Q_START[q]}", period_end=end, duration="3M", value_local="",
                            printed_value="", printed_units="", page_table="", quote="", role="current", verified="NOT FOUND",
                            notes="No capex sentence or table row found in this SEC document."))
    return out


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]


def long_date(iso):
    y, m, d_ = iso.split("-")
    return f"{MONTHS[int(m) - 1]} {int(d_)}, {y}"


def baba_scope(label):
    l_ = label.lower()
    if "licensed copyrights" in l_:
        return "capex_plus_intangibles_and_licensed_copyrights"
    if "intangible" in l_:
        return "capex_plus_intangible_assets"
    return "capex_ppe_incl_land_use_rights_and_cip"


class Docs:
    """Text of a catalogue source: the runner's fetched copy (issuer PDF/HTML) or the container's sec.gov copy."""

    def __init__(self, idx, cache, fetched):
        self.idx, self.cache, self.fetched, self.fet = idx, cache, fetched, {}
        if fetched:
            import json
            for m in json.load(open(os.path.join(fetched, "manifest.json")))["documents"]:
                if m.get("ok") and m.get("kept_file"):
                    for sid in m["source_ids"]:
                        self.fet[sid] = m

    def get(self, sid):
        if sid in self.fet:
            m = self.fet[sid]
            t = open(os.path.join(self.fetched, m["kept_file"]), encoding="utf-8", errors="replace").read()
            if m["kept_file"].endswith(".html"):
                t = to_text(t.encode())
            return t, m["url"], m["sha256"], "issuer document fetched on a GitHub runner" + (" (PDF; text by pdftotext)" if m.get("is_pdf") else "")
        if sid in self.idx:
            r = self.idx[sid]
            raw = gzip.open(os.path.join(self.cache, r["cache_file"])).read()
            if raw[:5] == b"%PDF-":
                import subprocess
                import tempfile
                with tempfile.NamedTemporaryFile(suffix=".pdf") as tf:
                    tf.write(raw)
                    tf.flush()
                    txt = subprocess.run(["pdftotext", "-layout", tf.name, "-"], capture_output=True).stdout.decode("utf-8", "replace")
                return txt, r["url"], r["sha256"], "sec.gov (PDF exhibit; text by pdftotext)"
            return to_text(raw), r["url"], r["sha256"], "sec.gov"
        return None, None, None, None


def alibaba(priv, docs):
    cat, cov = blocks(os.path.join(priv, "part04b_china_prompt_alibaba_Section_A_file.txt"))[:2]
    pub = {r["source_id"]: r["publication_date"] for r in cat}
    out = []
    amt = r"RMB\s?([\d,]+)\s?million"
    for c in cov:
        end = c["fiscal_period_end"]
        ids = [i.strip() for i in c["quarter_figure_source_ids"].split(";")]
        found = False
        for sid in ids:
            t, url, sha, how = docs.get(sid)
            if t is None:
                continue
            j = re.sub(r"\s+", " ", t)
            base = {"company_id": "alibaba", "currency": "CNY", "source_id": sid, "source_url": url, "source_sha256": sha,
                    "publication_date": pub.get(sid, ""), "grade": "A" if "sec.gov" in url else "B", "verified": "VERIFIED"}
            ld = long_date(end)
            y, mth = int(end[:4]), int(end[5:7])
            start = f"{y}-{mth - 2:02d}-01"  # quarter ends in March, June, September or December
            # 1) "Capital expenditures in the quarter ended <date> were RMB x million ..., compared to RMB y million in the same quarter of <y-1>"
            m = re.search(r"Capital expenditures in the quarter ended " + re.escape(ld) + r" were " + amt + r"[^.]*?(?:compared to " + amt + r" in the same quarter of (\d{4}))?", j)
            label, val, quote = None, None, None
            if m:
                label, val, quote = "Capital expenditures", m.group(1), m.group(0)
            else:
                for km in re.finditer(re.escape("During the quarter ended " + ld), j):
                    k = km.start()
                    nxt = j.find("During ", k + 30)
                    seg = j[k: nxt if nxt > 0 else k + 3000]
                    if "investing activities" not in seg[:200]:
                        continue  # the operating-activities paragraph starts the same way
                    m2 = re.search(r"(capital expenditures?(?: and (?:acquisition of )?intangible assets(?: and licensed copyrights)?)?) (?:of|were) " + amt, seg, re.I)
                    if m2:
                        label, val, quote = m2.group(1), m2.group(2), seg[max(0, m2.start() - 60): m2.end() + 140]
                        break
            if val:
                scope = baba_scope(label)
                out.append(dict(base, line="company_capex", period_start=start, period_end=end, duration="3M",
                                value_local=int(val.replace(",", "")) * 10 ** 6, printed_value=f"RMB{val} million",
                                printed_units="RMB millions", metric_name_exact=label[0].upper() + label[1:],
                                page_table="Results announcement, liquidity / investing activities discussion",
                                quote=quote[:300], role="current", notes=f"scope={scope}; source: {how}."))
                mc = re.search(r"Capital expenditures in the quarter ended " + re.escape(ld) + r" were " + amt + r" \(US\$[\d,]+ million\), compared to " + amt + r" in the same quarter of (\d{4})", j)
                if mc:
                    py = f"{int(mc.group(3))}-{end[5:]}"
                    out.append(dict(base, line="company_capex", period_start=f"{int(start[:4]) - 1}{start[4:]}", period_end=py,
                                    duration="3M", value_local=int(mc.group(2).replace(",", "")) * 10 ** 6,
                                    printed_value=f"RMB{mc.group(2)} million", printed_units="RMB millions",
                                    metric_name_exact="Capital expenditures", page_table="Results announcement (prior-year comparative)",
                                    quote=mc.group(0)[:300], role="prior_year_comparative",
                                    notes=f"scope={baba_scope('Capital expenditures')}; comparative in a later release; source: {how}."))
                found = True
            # fiscal-year totals in March-quarter releases
            for fm in re.finditer(r"Capital expenditures in fiscal year (\d{4}) were " + amt, j):
                out.append(dict(base, line="company_capex", period_start=f"{int(fm.group(1)) - 1}-04-01", period_end=f"{fm.group(1)}-03-31",
                                duration="12M", value_local=int(fm.group(2).replace(",", "")) * 10 ** 6, printed_value=f"RMB{fm.group(2)} million",
                                printed_units="RMB millions", metric_name_exact="Capital expenditures", page_table="Results announcement",
                                quote=fm.group(0), role="annual", notes=f"scope={baba_scope('x')}; source: {how}."))
            fy = re.search(r"During fiscal year (\d{4}), net cash (?:used in|provided by) investing activities.{0,900}?(capital expenditures?(?: and (?:acquisition of )?intangible assets(?: and licensed copyrights)?)?) of " + amt, j)
            if fy:
                out.append(dict(base, line="company_capex", period_start=f"{int(fy.group(1)) - 1}-04-01", period_end=f"{fy.group(1)}-03-31",
                                duration="12M", value_local=int(fy.group(3).replace(",", "")) * 10 ** 6, printed_value=f"RMB{fy.group(3)} million",
                                printed_units="RMB millions", metric_name_exact=fy.group(2)[0].upper() + fy.group(2)[1:],
                                page_table="Results announcement, fiscal-year investing activities", quote=fy.group(0)[-300:], role="annual",
                                notes=f"scope={baba_scope(fy.group(2))}; source: {how}."))
            # prospectus (F-1 / 424B4) totals
            for pm in re.finditer(r"In the three months ended (June 30, 2014), our capital expenditures totaled " + amt, j):
                out.append(dict(base, line="company_capex", period_start="2014-04-01", period_end="2014-06-30", duration="3M",
                                value_local=int(pm.group(2).replace(",", "")) * 10 ** 6, printed_value=f"RMB{pm.group(2)} million",
                                printed_units="RMB millions", metric_name_exact="Capital expenditures", page_table="Prospectus, Capital Expenditures",
                                quote=pm.group(0), role="current", notes=f"scope={baba_scope('x')}; source: {how}."))
                found = True
            for pm in re.finditer(r"nine months ended December 31, 2013, our capital expenditures totaled " + amt + r", " + amt + r".{0,40}?and " + amt, j):
                for (ps, pe, v) in (("2011-04-01", "2012-03-31", pm.group(1)), ("2012-04-01", "2013-03-31", pm.group(2)), ("2013-04-01", "2013-12-31", pm.group(3))):
                    out.append(dict(base, line="company_capex", period_start=ps, period_end=pe, duration="12M" if pe.endswith("03-31") else "9M",
                                    value_local=int(v.replace(",", "")) * 10 ** 6, printed_value=f"RMB{v} million", printed_units="RMB millions",
                                    metric_name_exact="Capital expenditures", page_table="F-1, Capital Expenditures", quote=pm.group(0)[:300],
                                    role="annual" if pe.endswith("03-31") else "ytd", notes=f"scope={baba_scope('x')}; source: {how}."))
            m3 = re.search(r"fiscal years? 2012, (?:fiscal year )?2013 and (?:the nine months ended December 31, 2013|2014), our capital expenditures totaled " + amt + r", " + amt + r"(?: \(US\$[\d,]+ million\))? and " + amt, j)
            if m3 and "2014" in m3.group(0) and "nine months" not in m3.group(0):
                out.append(dict(base, line="company_capex", period_start="2013-04-01", period_end="2014-03-31", duration="12M",
                                value_local=int(m3.group(3).replace(",", "")) * 10 ** 6, printed_value=f"RMB{m3.group(3)} million",
                                printed_units="RMB millions", metric_name_exact="Capital expenditures", page_table="Prospectus, Capital Expenditures",
                                quote=m3.group(0)[:300], role="annual", notes=f"scope={baba_scope('x')}; source: {how}."))
            if found:
                break
        if not found and c["status"] != "NOT PUBLIC":
            out.append({"company_id": "alibaba", "line": "company_capex", "period_end": end, "duration": "3M", "value_local": "",
                        "verified": "NOT FOUND", "role": "current", "notes": "No quarterly capex sentence found in the listed documents."})
    return out


MON = {m.lower(): i + 1 for i, m in enumerate(MONTHS)}
DUR_MONTHS = {"three": 3, "six": 6, "nine": 9, "year": 12}


def month_back(end, months):
    y, m = int(end[:4]), int(end[5:7])
    m0 = m - months + 1
    while m0 <= 0:
        m0 += 12
        y -= 1
    return f"{y}-{m0:02d}-01"


def tencent(priv, docs):
    """'Other Financial Information' table: row 'Capital expenditures (d)' and its note (the definition in force)."""
    cat = blocks(os.path.join(priv, "part02b_china_prompt_tencent_Section_A_file.txt"))[0]
    out = []
    for r in cat:
        if not r["source_type"].startswith("HKEX results announcement") and not r["source_type"].startswith("Annual report") \
                and not r["source_type"].startswith("Interim report"):
            continue
        t, url, sha, how = docs.get(r["source_id"])
        if not t:
            continue
        lines = t.split("\n")
        for i, ln in enumerate(lines):
            if not re.match(r"\s*Capital expenditures\s*(\(\w\))?\s+[\d(]", ln):
                continue
            vals = [int(x.replace(",", "")) for x in re.findall(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+)(?![\w.%])", ln.split("expenditures", 1)[1])]
            vals = [v for v in vals if not (len(vals) > 5 and v < 10)]  # drop a footnote letter turned digit, if any
            head = lines[max(0, i - 25): i]
            years_ln = next((h for h in reversed(head) if re.fullmatch(r"\s*(20\d\d\s+){1,7}20\d\d\s*", h)), None)
            dates_ln = next((h for h in reversed(head) if len(re.findall(r"\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December)", h)) >= 1
                             and not re.search(r"[a-z]{4,} [a-z]{4,} [a-z]{4,}", h.replace("ended", ""))), None)
            label_ln = next((h for h in reversed(head) if re.search(r"(Three|Six|Nine) months ended|Year ended", h)), "")
            unit = "thousands" if any("in thousands" in h for h in head) else "millions"
            if not years_ln or not dates_ln:
                break
            years = re.findall(r"20\d\d", years_ln)
            dates = re.findall(r"(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December)", dates_ln)
            di = max(k for k, h in enumerate(head) if h is dates_ln)
            found_g = []
            for h in head[max(0, di - 6): di + 1]:  # labels can sit on one or several lines above the dates
                for gm in re.finditer(r"(Three|Six|Nine) months ended|(Year) ended", h):
                    found_g.append((gm.start(), (gm.group(1) or gm.group(2)).lower()))
            groups = [g for _, g in sorted(found_g)]
            # a 'Year ended 31 December' label carries its own date: repeat it for both of its columns
            if len(dates) < len(years) and "year" in groups:
                k = groups.index("year")
                pos = sum(3 if g == "three" else 2 for g in groups[:k])
                dates = dates[:pos] + [("31", "December")] * (len(years) - len(dates)) + dates[pos:]
            if len(years) != len(vals) or len(dates) != len(years):
                out.append({"company_id": "tencent", "line": "company_capex", "period_end": r["publication_date"], "duration": "?",
                            "value_local": "", "verified": "PARSE_FAILED", "role": "unparsed", "source_id": r["source_id"],
                            "source_url": url, "quote": ln.strip()[:200],
                            "notes": f"columns: {len(years)} years, {len(dates)} dates, {len(vals)} values; groups {groups}"})
                break
            if not groups:
                groups = ["three"]
            durs = []
            for g in groups:
                durs += [g] * (3 if g == "three" and len(years) >= 3 else 2 if g != "three" else len(years))
            if len(durs) != len(years):
                durs = (["three"] * len(years)) if len(groups) == 1 else durs[:len(years)]
            note = ""
            for k2 in range(i, min(len(lines), i + 40)):
                if re.match(r"\s*\(d\)\s*Capital expenditures", lines[k2]) or re.match(r"\s*\(\w\)\s*Capital expenditure", lines[k2]):
                    note = " ".join(x.strip() for x in lines[k2:k2 + 5])
                    note = re.split(r"\s\(\w\)\s", note)[0][:400]
                    break
            for k3, (dd, mm) in enumerate(dates):
                end = f"{years[k3]}-{MON[mm.lower()]:02d}-{int(dd):02d}"
                dm = DUR_MONTHS[durs[k3]]
                out.append({"company_id": "tencent", "line": "company_capex", "period_start": month_back(end, dm), "period_end": end,
                            "duration": f"{dm}M", "value_local": vals[k3] * (1000 if unit == "thousands" else 10 ** 6), "currency": "CNY",
                            "printed_value": f"{vals[k3]:,}", "printed_units": f"RMB {unit}", "metric_name_exact": "Capital expenditures",
                            "source_id": r["source_id"], "source_url": url, "source_sha256": sha, "publication_date": r["publication_date"],
                            "page_table": "Other Financial Information, row 'Capital expenditures'", "quote": ln.strip()[:200],
                            "role": f"column {k3 + 1} of {len(years)}", "grade": "A", "verified": "VERIFIED",
                            "notes": f"definition note: {note}" if note else "definition note not found next to the table"})
            break
    return out


def main():
    priv, idx_csv, cache, out_csv = sys.argv[1:5]
    fetched = sys.argv[5] if len(sys.argv) > 5 else ""
    idx = {}
    for r in csv.DictReader(open(idx_csv)):
        for sid in r["source_ids"].split(";"):
            idx[sid] = r
    docs = Docs(idx, cache, fetched)
    rows = baidu(priv, idx, cache) + alibaba(priv, docs) + tencent(priv, docs)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
