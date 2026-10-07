#!/usr/bin/env python3
"""RTT-101 (IQ-15): extract pointers from Wikipedia pages fetched by the runner (CC BY-SA 4.0, grade C pointers).

Usage: rtt101_extract_wiki.py RUNNER_DIR [RUNNER_DIR ...]   (writes into data/rtt-101/source/)
Outputs:
  wiki_pages.csv           every page used: title, revision id, page sha256
  wiki_season_tables.csv   season, position, team code, linked club article, club_id, relegated flag, season dates
  wiki_window_rows.csv     every row of the per-window transfer lists that involves one of the 51 PL clubs:
                           window, date, player, from/to (linked article + club_id), fee text as the list states it,
                           and each citation (url, publisher, date). A Transfermarkt citation is never stored (DEC-236).
Nothing is interpreted beyond the page's own text; fees stay as text here (the build parses them)."""
import csv, glob, hashlib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rtt101_lib as L  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "rtt-101", "source")
MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                       "september", "october", "november", "december"], 1)}


def load_pages(dirs):
    pages = {}
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(d, "wiki__*"))):
            raw = open(f, "rb").read()
            j = json.loads(raw)
            if "parse" not in j:
                continue
            p = j["parse"]
            pages[p["title"]] = {"revid": p["revid"], "wikitext": p["wikitext"], "sha256": hashlib.sha256(raw).hexdigest()}
    return pages


def link_target(cell):
    m = re.search(r"\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]", cell)
    if not m:
        return "", re.sub(r"\{\{[^}]*\}\}", "", cell).strip()
    return m.group(1).strip(), (m.group(2) or m.group(1)).strip()


def unwrap_templates(cell):
    """Resolve templates from the innermost out: {{sort|key|shown}} -> shown, {{sortname|First|Last|...}} -> First Last,
    anything else (flags, notes) -> nothing."""
    def rep(m):
        parts = [p.strip() for p in m.group(1).split("|")]
        name = parts[0].lower()
        args = [p for p in parts[1:] if "=" not in p]
        if name.replace(" ", "") == "#invoke:sort" and args:
            if args[0].lower() == "name" and len(args) >= 3:
                return f"{args[1]} {args[2]}"
            return args[-1]
        if name == "sort" and args:
            return args[-1]
        if name == "sortname" and len(args) >= 2:
            return f"{args[0]} {args[1]}"
        return ""
    prev = None
    while prev != cell:
        prev = cell
        cell = re.sub(r"\{\{([^{}]*)\}\}", rep, cell)
    return cell


def player_name(cell):
    cell = unwrap_templates(re.sub(r"<ref.*?(</ref>|/>)", "", cell, flags=re.S))
    links = re.findall(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", cell)
    links = [l for l in links if not l[0].lower().startswith(("file:", "image:"))]
    if links:
        return (links[-1][1] or links[-1][0]).strip()
    return re.sub(r"'{2,}|[{}|\[\]]", "", cell).strip()


def player_link(cell):
    m = re.search(r"\{\{\s*#invoke:\s*sort\s*\|\s*name\s*\|([^|}]+)\|([^|}]+)((?:\|[^|}]*)*)\}\}", cell, re.I)
    if m:
        extra = [x.strip() for x in m.group(3).split("|") if x.strip() and "=" not in x and "," not in x]
        return extra[0] if extra else f"{m.group(1).strip()} {m.group(2).strip()}"
    m = re.search(r"\{\{\s*sortname\s*\|([^|}]+)\|([^|}]+)(?:\|([^|}]+))?", cell, re.I)
    if m:
        return (m.group(3) or f"{m.group(1).strip()} {m.group(2).strip()}").strip()
    links = [l for l in re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", cell) if not l.lower().startswith(("file:", "image:"))]
    return links[-1].strip() if links else ""


def parse_date(cell, default_year=None):
    m = re.search(r"\{\{\s*dts\s*\|(?:format=\w+\s*\|)?\s*(\d{4})\s*\|\s*(\d{1,2})\s*\|\s*(\d{1,2})", cell, re.I)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    m = re.search(r"\{\{\s*dts\s*\|(?:format=\w+\s*\|)?\s*(\d{1,2}) (\w+) (\d{4})", cell, re.I)
    if m and m.group(2).lower() in MONTHS:
        return f"{int(m.group(3)):04d}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    t = re.sub(r"\{\{[^}]*\}\}|'''|''|<[^>]+>", " ", cell)
    m = re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", t)
    if m and m.group(2).lower() in MONTHS:
        return f"{int(m.group(3)):04d}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    m = re.search(r"([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})", t)
    if m and m.group(1).lower() in MONTHS:
        return f"{int(m.group(3)):04d}-{MONTHS[m.group(1).lower()]:02d}-{int(m.group(2)):02d}"
    return ""


def cite_fields(body):
    f = {}
    for k in ("url", "publisher", "work", "website", "newspaper", "date", "title"):
        m = re.search(r"\|\s*" + k + r"\s*=\s*([^|}]*)", body)
        if m:
            f[k] = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", m.group(1)).strip()
    if "url" not in f:
        m = re.search(r"\[(https?://\S+)", body)
        if m:
            f["url"] = m.group(1)
    return f


def named_refs(w):
    refs = {}
    for m in re.finditer(r"<ref\s+name\s*=\s*\"?([^\">/]+?)\"?\s*>(.*?)</ref>", w, re.S):
        refs[m.group(1).strip()] = cite_fields(m.group(2))
    return refs


def cell_refs(cell, refs):
    out = []
    for m in re.finditer(r"<ref(?:\s+name\s*=\s*\"?([^\">/]+?)\"?)?\s*(/>|>(.*?)</ref>)", cell, re.S):
        if m.group(3) is not None:
            out.append(cite_fields(m.group(3)))
        elif m.group(1):
            out.append(refs.get(m.group(1).strip(), {"url": "", "title": f"named ref {m.group(1).strip()} (not found)"}))
    return out


def fee_text(cell):
    t = re.sub(r"<ref[^>]*/>|<ref.*?</ref>", "", cell, flags=re.S)
    t = re.sub(r"\{\{\s*(ntsh|nts|sort)\s*\|[^}|]*\}\}", "", t, flags=re.I)
    t = re.sub(r"\{\{\s*efn.*?\}\}", "", t, flags=re.I | re.S)
    t = re.sub(r"\{\{\s*(GBP|EUR|USD|currency)\s*\|([^}|]*)[^}]*\}\}", lambda m: {"gbp": "£", "eur": "€", "usd": "$"}.get(m.group(1).lower(), "") + m.group(2), t, flags=re.I)
    t = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", t)
    t = t.replace("&nbsp;", " ").replace("'''", "").replace("''", "")
    t = re.sub(r"<br\s*/?>", "; ", t)
    t = re.sub(r"<[^>]+>|\{\{[^}]*\}\}", "", t)
    return re.sub(r"\s+", " ", t).strip()


def split_cells(s):
    """Split a table line on '||' only outside {{templates}} and [[links]]."""
    parts, cur, depth, i = [], "", 0, 0
    while i < len(s):
        two = s[i:i + 2]
        if two in ("{{", "[["):
            depth += 1; cur += two; i += 2; continue
        if two in ("}}", "]]") and depth:
            depth -= 1; cur += two; i += 2; continue
        if two == "||" and depth == 0:
            parts.append(cur); cur = ""; i += 2; continue
        cur += s[i]; i += 1
    parts.append(cur)
    return parts


def split_rows(table):
    rows = []
    for chunk in re.split(r"\n\|-[^\n]*", table):
        cells = []
        for line in chunk.split("\n"):
            s = line.strip()
            if not s or s.startswith(("{|", "|}", "!", "|+")):
                continue
            if s.startswith("|"):
                cells.extend(split_cells(s[1:]))
            elif cells:
                cells[-1] += "\n" + line
        if cells:
            rows.append(cells)
    return rows


def strip_attr(cell):
    m = re.match(r"\s*((?:rowspan|colspan|style|align|class|data-sort-value)\s*=\s*\"?[^|\"]*\"?\s*)+\|(?!\|)", cell)
    attrs = m.group(0) if m else ""
    rs = re.search(r"rowspan\s*=\s*\"?(\d+)", attrs)
    return cell[len(attrs):], int(rs.group(1)) if rs else 1


def window_rows(title, page):
    w = page["wikitext"]
    refs = named_refs(w)
    out = []
    for tm in re.finditer(r"\{\|.*?\n\|\}", w, re.S):
        table = tm.group(0)
        head = " ".join(re.findall(r"!\s*([^\n]+)", table[:600])).lower()
        if "moving from" not in head and "from" not in head:
            continue
        hdr = []
        for hl in re.findall(r"^!(.*)$", table, re.M):
            hdr += [re.sub(r"^[^|]*\|(?!\|)", "", h).strip().lower() for h in hl.split("!!")]
        hdr = [h for h in hdr if h][:8]
        def col(*keys):
            for k in keys:
                for n, h in enumerate(hdr):
                    if h.startswith(k):
                        return n
            return None
        ci = {"date": col("date"), "name": col("name", "player"), "from": col("moving from", "from"),
              "to": col("moving to", "to"), "fee": col("fee")}
        loan_table = any(h.startswith(("end date", "date to", "until")) for h in hdr)
        if ci["fee"] is None and ci["name"] is not None and ci["from"] is not None and ci["to"] is not None:
            ci["date"] = 0
            ci["fee"] = "LOAN" if loan_table else "NONE"
        elif None in (ci["name"], ci["from"], ci["to"], ci["fee"]):
            continue  # not a transfer table (e.g. released players: no "moving to" column)
        width = len(hdr) if len(hdr) >= 5 else 5
        carry_date, carry_left = "", 0
        for cells in split_rows(table):
            vals = []
            date_here = False
            for i, c in enumerate(cells):
                c2, rs = strip_attr(c)
                if i == 0 and parse_date(c2) and len(cells) >= width:
                    date_here = True
                    carry_date, carry_left = parse_date(c2), rs
                vals.append(c2)
            if date_here:
                vals = vals[1:]
                carry_left -= 1
            elif carry_left > 0 and len(vals) == width - 1:
                carry_left -= 1
            elif len(vals) >= width:
                d = parse_date(vals[0]); vals = vals[1:]
                carry_date = d or carry_date
            if len(vals) < width - 1:
                continue
            off = 1 if ci["date"] == 0 else 0
            name, frm, to = (vals[ci[k] - off] for k in ("name", "from", "to"))
            fee = {"LOAN": "Loan", "NONE": "(no fee column)"}.get(ci["fee"]) if isinstance(ci["fee"], str) else vals[ci["fee"] - off]
            ft, fn = link_target(frm)
            tt, tn = link_target(to)
            fid, tid = L.club_id(ft) or L.club_id(fn), L.club_id(tt) or L.club_id(tn)
            if "milton keynes" in (ft + fn + tt + tn).lower() or "afc wimbledon" in (ft + fn + tt + tn).lower():
                fid = fid if "wimbledon" not in (ft + fn).lower() else None
                tid = tid if "wimbledon" not in (tt + tn).lower() else None
            if not (fid or tid):
                continue
            cites = cell_refs(fee, refs) + cell_refs(name, refs) + cell_refs(to, refs)
            tm_only = bool(cites) and all("transfermarkt" in (c.get("url", "") + c.get("website", "") + c.get("work", "")).lower() for c in cites)
            cites = [c for c in cites if "transfermarkt" not in (c.get("url", "") + c.get("website", "") + c.get("work", "")).lower()]
            out.append({"window": title.replace("List of English football transfers ", ""), "page": title,
                        "revid": page["revid"], "date": carry_date, "player": player_name(name), "player_article": player_link(name),
                        "from_article": ft, "from_name": fn, "from_club_id": fid or "",
                        "to_article": tt, "to_name": tn, "to_club_id": tid or "", "fee_text": fee_text(fee),
                        "citation_only_transfermarkt": "yes" if tm_only else "no",
                        "cite_urls": " ".join(c.get("url", "") for c in cites if c.get("url")),
                        "cite_publishers": " | ".join((c.get("publisher") or c.get("work") or c.get("website") or c.get("newspaper") or "") for c in cites),
                        "cite_dates": " | ".join(c.get("date", "") for c in cites)})
    # bullet-list layout (e.g. summer 2004, winter 2003-04): ";date" then "*[[Player]] from [[A]] to [[B]], fee"
    cur_date = ""
    for line in w.split("\n"):
        s = line.strip()
        if s.startswith(";"):
            cur_date = parse_date(s[1:]) or cur_date
            continue
        m = re.match(r"\*(.*?)\bfrom\b(.*?)\bto\b(.*?),(.*)$", s)
        if not m or not cur_date:
            continue
        name, frm, to, fee = m.groups()
        ft, fn = link_target(frm)
        tt, tn = link_target(to)
        fid, tid = L.club_id(ft) or L.club_id(fn), L.club_id(tt) or L.club_id(tn)
        if not (fid or tid):
            continue
        cites = [c for c in cell_refs(fee, refs) if "transfermarkt" not in (c.get("url", "") + c.get("website", "") + c.get("work", "")).lower()]
        out.append({"window": title.replace("List of English football transfers ", ""), "page": title,
                    "revid": page["revid"], "date": cur_date, "player": player_name(name), "player_article": player_link(name),
                    "from_article": ft, "from_name": fn, "from_club_id": fid or "",
                    "to_article": tt, "to_name": tn, "to_club_id": tid or "", "fee_text": fee_text(fee),
                    "citation_only_transfermarkt": "no",
                    "cite_urls": " ".join(c.get("url", "") for c in cites if c.get("url")),
                    "cite_publishers": " | ".join((c.get("publisher") or c.get("work") or c.get("website") or "") for c in cites),
                    "cite_dates": " | ".join(c.get("date", "") for c in cites)})
    return out


def club_season_rows(title, page):
    """One-sided In/Out tables of a 1992-2002 club-season page; the page's club is the other side."""
    m = re.match(r"(\d{4}–(?:\d{2}|2000)) (.+) season$", title)
    if not m:
        return []
    own = L.club_id(m.group(2))
    if not own:
        return []
    w = page["wikitext"]
    refs = named_refs(w)
    out = []
    for tm in re.finditer(r"\{\|.*?\n\|\}", w, re.S):
        table = tm.group(0)
        before = w[max(0, tm.start() - 600):tm.start()]
        heads = re.findall(r"^=+\s*(.*?)\s*=+\s*$", before, re.M)
        ctx = (" ".join(heads[-2:]) + " " + before[-200:]).lower()
        hdr = []
        for hl in re.findall(r"^!(.*)$", table, re.M):
            hdr += [re.sub(r"^[^|]*\|(?!\|)", "", h).strip().lower() for h in hl.split("!!")]
        hdr = [h for h in hdr if h]
        if not any(h.startswith("fee") for h in hdr):
            continue

        def col(pred):
            for n, h in enumerate(hdr):
                if pred(h):
                    return n
            return None
        c_name = col(lambda h: h in ("name", "player"))
        c_fee = col(lambda h: h.startswith("fee"))
        c_date = col(lambda h: h.startswith("date"))
        c_from = col(lambda h: h in ("from", "transferred from", "previous club", "club from"))
        c_to = col(lambda h: h in ("to", "transferred to", "new club", "club to"))
        c_club = col(lambda h: h == "club")
        if c_name is None:
            continue
        if c_from is not None:
            direction, c_other = "in", c_from
        elif c_to is not None:
            direction, c_other = "out", c_to
        elif c_club is not None and re.search(r"\b(in|arrivals|incoming|signings)\b", ctx) and not re.search(r"\b(out|departures|outgoing)\b", ctx[-120:]):
            direction, c_other = "in", c_club
        elif c_club is not None and re.search(r"\b(out|departures|outgoing|sold)\b", ctx):
            direction, c_other = "out", c_club
        else:
            continue
        last_head = (heads[-1] if heads else "").lower()
        cap = re.search(r"^\|\+(.*)$", table, re.M)
        loan = "loan" in last_head or bool(cap and "loan" in cap.group(1).lower())
        ncols = max(c_name, c_fee, c_other, c_date or 0) + 1
        carry_date, carry_left = "", 0
        for cells in split_rows(table):
            vals, spans = [], []
            for c in cells:
                c2, rs = strip_attr(c)
                vals.append(c2)
                spans.append(rs)
            if len(vals) == ncols - 1 and c_date == 0 and carry_left > 0:
                vals = [""] + vals
                carry_left -= 1
                date = carry_date
            elif len(vals) >= ncols:
                date = parse_date(vals[c_date]) if c_date is not None else ""
                if not date and c_date is not None:
                    plain = re.sub(r"\{\{[^}]*\}\}", " ", vals[c_date]).replace("'", " ")
                    mm = re.search(r"([A-Za-z]+)\s+(\d{4})", plain)
                    if mm and mm.group(1).lower() in MONTHS:
                        date = f"{mm.group(2)}-{MONTHS[mm.group(1).lower()]:02d}"
                if c_date == 0 and spans[0] > 1:
                    carry_date, carry_left = date, spans[0] - 1
            else:
                continue
            ot, on = link_target(vals[c_other])
            oid = L.club_id(ot) or L.club_id(on)
            low = (ot + on).lower()
            if "wimbledon" in low and ("afc" in low or "milton" in low):
                oid = None
            ftxt = fee_text(vals[c_fee]) or ""
            if loan and "loan" not in ftxt.lower():
                ftxt = ("Loan " + ftxt).strip()
            cites = [c for c in cell_refs(" ".join(vals), refs)
                     if "transfermarkt" not in (c.get("url", "") + c.get("website", "") + c.get("work", "")).lower()]
            frm = (ot, on, oid) if direction == "in" else ("", m.group(2), own)
            to = ("", m.group(2), own) if direction == "in" else (ot, on, oid)
            out.append({"window": f"club-season {m.group(1)}", "page": title, "revid": page["revid"], "date": date,
                        "player": player_name(vals[c_name]), "player_article": player_link(vals[c_name]), "from_article": frm[0], "from_name": frm[1], "from_club_id": frm[2] or "",
                        "to_article": to[0], "to_name": to[1], "to_club_id": to[2] or "", "fee_text": ftxt,
                        "citation_only_transfermarkt": "no", "cite_urls": " ".join(c.get("url", "") for c in cites if c.get("url")),
                        "cite_publishers": " | ".join((c.get("publisher") or c.get("work") or c.get("website") or "") for c in cites),
                        "cite_dates": " | ".join(c.get("date", "") for c in cites)})
    return out


def season_tables(pages):
    code_map = {}
    for t, p in pages.items():
        for c, art in re.findall(r"\|\s*name_([A-Z]{3})\s*=\s*\[\[([^\]|]+)", p["wikitext"]):
            if t.endswith("Premier League") and t[:4].isdigit() and int(t[:4]) >= 2015 and c not in code_map:
                code_map[c] = art
    rows = []
    for t in sorted(pages):
        if not re.fullmatch(r"\d{4}–(\d{2}|2000) (FA )?Premier League", t):
            continue
        p = pages[t]; w = p["wikitext"]
        dm = re.search(r"\|\s*dates\s*=(.*?)\n\s*\|\s*\w+\s*=", w, re.S)
        dates = ""
        if dm:
            d0 = re.sub(r"<ref.*?(</ref>|/>)", "", dm.group(1), flags=re.S)
            d0 = re.sub(r"\{\{\s*nowrap\s*\|", "", d0, flags=re.I)
            d0 = re.sub(r"\{\{[^{}]*\}\}|<[^>]+>|\}\}", "", d0)
            m2 = re.search(r"\d{1,2}\s+[A-Za-z]+\s+(\d{4}\s*)?[–-]\s*\d{1,2}\s+[A-Za-z]+\s+\d{4}", re.sub(r"\s+", " ", d0))
            dates = m2.group(0) if m2 else re.sub(r"\s+", " ", d0).strip()
        i = w.lower().find("{{#invoke:sports table")
        j = w.find("\n}}", i)
        blk = w[i:j if j > i else i + 25000]
        names = dict(re.findall(r"\|\s*name_([A-Z]{3})\s*=\s*\[\[([^\]|]+)", w))
        order = []
        m = re.search(r"\|\s*team_order\s*=([^\n]*)", blk)
        if m:
            order = [x.strip() for x in m.group(1).split(",") if x.strip()]
        else:
            for n, c in re.findall(r"\|\s*team(\d+)\s*=\s*([A-Z]{3})", blk):
                if c not in order:
                    order.append(c)
        positions = "no (table auto-sorted on the page)" if re.search(r"auto_generate_standings\s*=\s*y", blk) else "yes"
        if not order:
            order = sorted(names); positions = "no (table not yet ordered)"
        rel = {int(n) for n in re.findall(r"\|\s*result(\d+)\s*=\s*REL", blk)}
        for pos, c in enumerate(order, 1):
            art = names.get(c) or code_map.get(c, "")
            rows.append({"season": t.split(" ")[0], "position": pos if positions == "yes" else "", "team_code": c,
                         "club_article": art, "club_id": L.club_id(art) or "", "relegated_flag": "yes" if pos in rel else "",
                         "season_dates_infobox": dates, "page": t, "revid": p["revid"]})
    return rows


def main():
    pages = load_pages(sys.argv[1:])
    with open(os.path.join(OUT, "wiki_pages.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["title", "revid", "api_response_sha256", "url"])
        for t in sorted(pages):
            w.writerow([t, pages[t]["revid"], pages[t]["sha256"], "https://en.wikipedia.org/w/index.php?oldid=%s" % pages[t]["revid"]])
    st = season_tables(pages)
    with open(os.path.join(OUT, "wiki_season_tables.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(st[0])); w.writeheader(); w.writerows(st)
    wins = []
    for t in sorted(pages):
        if t.startswith("List of English football transfers"):
            w = pages[t]["wikitext"]
            body = re.sub(r"<ref.*?</ref>|<ref[^>]*/>", "", w, flags=re.S)
            body = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", body)
            body = re.sub(r"\[\[File:.*?\]\]\]?|\{\{[^{}]*\}\}", " ", body)
            sent = ""
            for sentence in re.split(r"(?<=[a-z0-9)])\.\s", body[:6000]):
                if "window" in sentence and len(re.findall(r"\b\d{1,2}(?:st|nd|rd|th)? (?:January|February|March|April|May|June|July|August|September|October|November|December)", sentence)) >= 2:
                    sent = re.sub(r"\s+", " ", sentence).strip(); break
            ds = re.findall(r"(\d{1,2})(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)(?:\s+(\d{4}))?", sent)
            yr = re.findall(r"\d{4}", sent)
            dd = []
            for d, mo, y in ds:
                y = y or (yr[-1] if yr else "")
                if y:
                    dd.append(f"{y}-{MONTHS[mo.lower()]:02d}-{int(d):02d}")
            wins.append({"window": t.replace("List of English football transfers ", ""), "page": t, "revid": pages[t]["revid"],
                         "open_date": dd[0] if len(dd) >= 2 else "", "close_date": dd[1] if len(dd) >= 2 else "",
                         "lead_sentence": sent[:300]})
    with open(os.path.join(OUT, "wiki_windows.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(wins[0])); wr.writeheader(); wr.writerows(wins)
    rows = []
    for t in sorted(pages):
        if t.startswith("List of English football transfers"):
            rows += window_rows(t, pages[t])
    with open(os.path.join(OUT, "wiki_window_rows.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    cs = []
    for t in sorted(pages):
        if t.endswith(" season"):
            cs += club_season_rows(t, pages[t])
    if cs:
        with open(os.path.join(OUT, "wiki_club_season_rows.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(cs[0])); w.writeheader(); w.writerows(cs)
    print(len(pages), "pages;", len(st), "club-season rows;", len(rows), "window rows with a PL-history club;", len(cs), "club-season page rows")


if __name__ == "__main__":
    main()
