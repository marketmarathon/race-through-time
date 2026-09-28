# RTT-002 driver nationality — comparison report

Written by `python scripts/rtt002_nationality.py` (deterministic). Output: `data/rtt-002/driver_nationality.csv` (SHA-256 `a41c3d4690db17fb71f177332330e71f9e14a6b2b05e2a932978562601fe4812`).

- Primary source: the flag in each driver's row of Wikipedia's "List of Formula One Grand Prix winners", revision 1376824402 (the revision recorded in `data/rtt-002/source/README.md`), retrieved 2026-09-28T18:10:25Z. Codes mapped to ISO 3166-1 alpha-3 with Luke's table (UK→GBR, GER→DEU, NED→NLD, SUI→CHE, MON→MCO; others unchanged).
- Cross-check: Wikidata P1532 (country for sport) on each driver's item; where an item has no P1532, P27 (country of citizenship). Retrieved 2026-09-28T18:12:55Z.
- Extraction: `scripts/extract_nationality.browser.js`, run in Luke's Chrome by Claude in Cowork, because Wikimedia answered this cloud environment with HTTP 429 (Claude Code's own requests on 28 Sep 2026, 17:59–18:2x UTC: Wikipedia API 429 on every content request, Wikidata API 429 on every request; not worked around).

## Checks

- PASS: every drivers.csv driver has exactly one source row, matched by page ID — 116 rows, 116 drivers; missing none, extra none
- PASS: every Wikipedia wins value equals career_totals.csv — 116/116 equal; differences none
- PASS: every Wikipedia flag code maps to a known ISO 3166-1 alpha-3 code — unknown: none

## Result

116 drivers; primary value found for 116; Wikidata agrees for 113, disagrees for 3, other 0.

| Compared on | Result | Drivers |
|---|---|---|
| P1532 | AGREE | 34 |
| P1532 | DISAGREE | 2 |
| P27 (no P1532) | AGREE | 79 |
| P27 (no P1532) | DISAGREE | 1 |

## Disagreements and missing values (for Luke; not resolved — the CSV keeps the Wikipedia value)

| Driver | ID | Result | Compared on | Evidence |
|---|---|---|---|---|
| Luigi Fagioli | `wp1212766` | DISAGREE | P27 (no P1532) | Wikipedia flag ITA → ITA (Italy); Wikidata Q173038 (revision 2517179183): P1532 none; P27 Q172579 Kingdom of Italy |
| Phil Hill | `wp341545` | DISAGREE | P1532 | Wikipedia flag USA → USA (United States); Wikidata Q3112 (revision 2544076670): P1532 Q786 Dominican Republic; P27 Q30 United States |
| Jim Clark | `wp181892` | DISAGREE | P1532 | Wikipedia flag UK → GBR (United Kingdom); Wikidata Q3137 (revision 2530072898): P1532 Q22 Scotland; P27 Q145 United Kingdom |

Several Wikidata values, one of which matches (counted as AGREE, listed for completeness):

- Michael Schumacher: P1532 lists Luxembourg, Germany; one of them is Germany, so it counts as AGREE
- Eddie Irvine: P1532 lists United Kingdom, Ireland; one of them is United Kingdom, so it counts as AGREE

## Historical flag variants in the Wikipedia source (for the record; DEC-035: today's design is drawn for everyone)

The Wikipedia rows below show a dated flag variant (the flag of that year). The video draws today's flag for these drivers too.

| Driver | Wikipedia code | Variant |
|---|---|---|
| Johnnie Parsons | USA | 1912 |
| Lee Wallard | USA | 1912 |
| Troy Ruttman | USA | 1912 |
| Bill Vukovich | USA | 1912 |
| Bob Sweikert | USA | 1912 |
| Pat Flaherty | USA | 1912 |
| Sam Hanks | USA | 1912 |
| Jimmy Bryan | USA | 1912 |
| Rodger Ward | USA | 1912 |
| Jim Rathmann | USA | 1959 |
| Emerson Fittipaldi | BRA | 1968 |
| Jody Scheckter | ZAF | 1928 |
| Carlos Pace | BRA | 1968 |
| Nelson Piquet | BRA | 1968 |

## By country (primary value; flag = flag-icons file, today's design)

| Country | ISO alpha-3 | Flag file | Drivers |
|---|---|---|---|
| United Kingdom | GBR | `gb` | 21: Mike Hawthorn, Stirling Moss, Peter Collins, Tony Brooks, Innes Ireland, Graham Hill, Jim Clark, John Surtees, Jackie Stewart, Peter Gethin, James Hunt, John Watson, Nigel Mansell, Damon Hill, Johnny Herbert, David Coulthard, Eddie Irvine, Jenson Button, Lewis Hamilton, George Russell, Lando Norris |
| Italy | ITA | `it` | 16: Giuseppe Farina, Luigi Fagioli, Alberto Ascari, Piero Taruffi, Luigi Musso, Giancarlo Baghetti, Lorenzo Bandini, Ludovico Scarfiotti, Vittorio Brambilla, Riccardo Patrese, Elio de Angelis, Michele Alboreto, Alessandro Nannini, Giancarlo Fisichella, Jarno Trulli, Kimi Antonelli |
| United States | USA | `us` | 15: Johnnie Parsons, Lee Wallard, Troy Ruttman, Bill Vukovich, Bob Sweikert, Pat Flaherty, Sam Hanks, Jimmy Bryan, Rodger Ward, Jim Rathmann, Phil Hill, Dan Gurney, Richie Ginther, Mario Andretti, Peter Revson |
| France | FRA | `fr` | 14: Maurice Trintignant, François Cevert, Jean-Pierre Beltoise, Jacques Laffite, Patrick Depailler, Jean-Pierre Jabouille, René Arnoux, Didier Pironi, Alain Prost, Patrick Tambay, Jean Alesi, Olivier Panis, Pierre Gasly, Esteban Ocon |
| Germany | DEU | `de` | 7: Wolfgang von Trips, Jochen Mass, Michael Schumacher, Heinz-Harald Frentzen, Ralf Schumacher, Sebastian Vettel, Nico Rosberg |
| Brazil | BRA | `br` | 6: Emerson Fittipaldi, Carlos Pace, Nelson Piquet, Ayrton Senna, Rubens Barrichello, Felipe Massa |
| Australia | AUS | `au` | 5: Jack Brabham, Alan Jones, Mark Webber, Daniel Ricciardo, Oscar Piastri |
| Finland | FIN | `fi` | 5: Keke Rosberg, Mika Häkkinen, Kimi Räikkönen, Heikki Kovalainen, Valtteri Bottas |
| Argentina | ARG | `ar` | 3: Juan Manuel Fangio, José Froilán González, Carlos Reutemann |
| Austria | AUT | `at` | 3: Jochen Rindt, Niki Lauda, Gerhard Berger |
| Sweden | SWE | `se` | 3: Jo Bonnier, Ronnie Peterson, Gunnar Nilsson |
| Belgium | BEL | `be` | 2: Jacky Ickx, Thierry Boutsen |
| Canada | CAN | `ca` | 2: Gilles Villeneuve, Jacques Villeneuve |
| Mexico | MEX | `mx` | 2: Pedro Rodríguez, Sergio Pérez |
| New Zealand | NZL | `nz` | 2: Bruce McLaren, Denny Hulme |
| Spain | ESP | `es` | 2: Fernando Alonso, Carlos Sainz Jr. |
| Switzerland | CHE | `ch` | 2: Jo Siffert, Clay Regazzoni |
| Colombia | COL | `co` | 1: Juan Pablo Montoya |
| Monaco | MCO | `mc` | 1: Charles Leclerc |
| Netherlands | NLD | `nl` | 1: Max Verstappen |
| Poland | POL | `pl` | 1: Robert Kubica |
| South Africa | ZAF | `za` | 1: Jody Scheckter |
| Venezuela | VEN | `ve` | 1: Pastor Maldonado |
