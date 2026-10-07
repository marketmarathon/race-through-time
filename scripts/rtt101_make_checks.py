#!/usr/bin/env python3
"""RTT-101 (IQ-15): build the runner job that checks cited sources (Tier 2 scripted check; also Tier 1 and the
Tier 3 sample where a source URL exists). For each fee-bearing transfer and each evidence row with a fetchable URL,
the runner looks for the figure (several spellings) within 400 characters of the player's surname.
Usage: rtt101_make_checks.py [MAX_ITEMS]   -> data/rtt-101/runner_job.json"""
import csv, hashlib, json, re, sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 4500
T = {t["transfer_id"]: t for t in csv.DictReader(open("data/rtt-101/transfers.csv", encoding="utf-8"))}
E = list(csv.DictReader(open("data/rtt-101/fee_evidence.csv", encoding="utf-8")))


def needles(amount, cur):
    a = float(amount)
    out = []
    if a >= 1e6:
        m = a / 1e6
        s = [f"{m:g}"] + ([f"{m:.1f}", f"{m:.2f}"] if m != int(m) else [])
        for x in dict.fromkeys(s):
            if cur == "GBP":
                out += [f"£{x}m", f"£{x} m", f"£{x} million", f"£{x}million", f"£{x}mn", f"£{x}M", f"£{x}-million", f"pounds {x}m", f"pounds {x} million", f"{x} million pounds", f"{x}m pounds"]
            elif cur == "EUR":
                out += [f"€{x}m", f"€{x} m", f"€{x} million", f"€{x}million", f"€{x}M", f"{x} million euros", f"{x}m euros", f"€{x}-million", f"EUR{x}m", f"EUR {x}m"]
            elif cur == "USD":
                out += [f"${x}m", f"${x} million", f"{x} million dollars", f"US${x}m"]
    sym = {"GBP": "£", "EUR": "€", "USD": "$"}.get(cur, "")
    out += [f"{sym}{int(a):,}", f"{sym}{int(a):,}".replace(",", ".")] if sym else []
    if cur == "GBP" and a < 1e6:
        out += [f"£{a / 1e3:g}k", f"£{a / 1e3:g},000", f"£{a / 1e3:g}K"]
    return list(dict.fromkeys(out))


items, seen = [], set()
order = sorted(T.values(), key=lambda t: ({"1": 0, "2": 1, "3": 2}.get(t["tier"], 3), -float(t["fee_gbp"] or 0)))
by_t = {}
for e in E:
    by_t.setdefault(e["transfer_id"], []).append(e)
for t in order:
    if not t["fee_gbp"] or float(t["fee_gbp"]) <= 0 or (t["tier"] == "3" and t["tier3_sample"] != "yes"):
        continue
    surname = re.sub(r"\(.*?\)", "", t["player"]).strip().split(" ")[-1]
    for e in by_t.get(t["transfer_id"], []):
        if not e["amount"] or not e["currency"]:
            continue
        urls = [e["url"]] if e["origin"] == "research_lead" else e["cited_urls"].split()
        for u in urls[:2]:
            if not u.startswith("http") or "wikipedia.org" in u or "transfermarkt" in u.lower():
                continue
            cid = hashlib.sha256(f"{t['transfer_id']}|{u}|{e['amount']}|{e['currency']}".encode()).hexdigest()[:16]
            if cid in seen:
                continue
            seen.add(cid)
            items.append({"id": cid, "url": u, "near": surname, "needles": needles(e["amount"], e["currency"]),
                          "transfer_id": t["transfer_id"], "amount": e["amount"], "currency": e["currency"], "tier": t["tier"]})
print(len(items), "check items;", sum(1 for i in items if i["tier"] == "1"), "tier 1;", sum(1 for i in items if i["tier"] == "2"), "tier 2;",
      sum(1 for i in items if i["tier"] == "3"), "tier 3 sample")
items = items[:MAX]
json.dump({"delay": 0.8, "check": items}, open("data/rtt-101/runner_job.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
