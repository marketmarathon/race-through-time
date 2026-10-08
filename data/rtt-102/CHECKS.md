# RTT-102 checks (written by scripts/build_rtt102_dataset.py)

- **K01 PASS** Every on-screen value rests on a VERIFIED figure with its URL and the wording seen at source. 137 points used; problems: none
- **K02 PASS** No averaging: each published month shows one printed figure exactly; each other month is the straight line between its two points. 203 series rows; mismatches: none; used values not printed: none
- **K03 PASS** No point or bar before the site's start date. problems: none
- **K04 PASS** One address per assistant per month. problems: none
- **K05 PASS** DeepSeek: deepseek.com only; never deepseek.com + chat.deepseek.com. 13 DeepSeek points used; problems: none
- **K06 PASS** No forecast: projections (Similarweb's June 2024 and October 2023 projections) are never used. projection rows ['M040', 'M062'], all excluded
- **K07 PASS** data_version set on every point and every series row. problems: none
- **K08 PASS** No extrapolation beyond a bar's first or last published point. problems: none
- **K09 PASS** Only eligible VERIFIED figures are used; UNVERIFIED and NOT FOUND never. problems: none
- **K10 PASS** Leftover conflicts use no figure until Luke decides. 2 leftovers; problems: none
- **K11 PASS** Le Chat and uncounted sites (Bing Chat in bing.com, Grok in x.com) have no bar. none on the board
