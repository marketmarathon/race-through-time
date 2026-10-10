**What the sources say.**
- UN SDG metadata for indicator 5.5.1(a), the IPU being custodian (https://unstats.un.org/sdgs/metadata/files/Metadata-05-05-01a.pdf, read on the runner): "The proportion of seats held by women in national parliaments, currently as of 1 January of reporting year". Its table of dates: "2020 – Present As at 1 January"; "2013 – 2019 As at 1 February"; "2003, 2005 – 2007, 2009 - 2012 As at 31 January"; "2008 As at 29 January"; "2001, 2004 As at 30 January"; "2002 As at 4 February"; "1999 As at 5 February"; "1998, 2000 As at 25 January"; "1997 As at 1 January".
- World Bank WDI source note (metadata, and data.worldbank.org as Cowork saw it): "For the year of 1998, the data is as of August 10, 1998." WDI gives no date for any other year, and every per-value WDI footnote is empty.

**Test against the IPU's own archived monthly rankings** (archive.ipu.org, read on the runner, run 38030108879; rows in `fetch_2026-10-10_run38030108879_archive/page_excerpts/`). WDI value (one decimal) against the IPU ranking of the stated date:

| WDI year | Country | WDI | IPU ranking, same country | Matches |
|---|---|---|---|---|
| 1997 | Mexico; Sweden | 14.2; 40.4 | 1 Jan 1997: 14.2; 40.4 | 1 Jan 1997 |
| 1998 | Mexico | 17.4 | 25 Jan 1998: 14.2 · 10 Aug 1998: 17.4 | **10 Aug 1998** (WDI's note), not the SDG table's 25 January |
| 2003 | Rwanda | 48.8 | election "09 2003" (IPU 31 Jan 2007 row); 31 Jan 2003 ranking shows Sweden first | after Rwanda's September 2003 election |
| 2006 | UAE; Nepal | 5.0; 5.9 | 31 Jan 2007: 22.5; 17.3 | neither (WDI shows the position before those changes) |
| 2007 | Sweden; Mexico; UAE; Nepal | 47.0; 23.2; 22.5; 17.3 | 31 Jan 2008: 47.0; 23.2; 22.5; 17.3 | **31 Jan 2008** (the following January) |
| 2012 | Rwanda; Mexico; Saudi Arabia; UAE; Kuwait | 56.2; 36.8; 0.0; 17.5; 6.2 | 1 Jan 2013: 56.3; 36.8; 0.0; 17.5; 6.2 | **1 Jan 2013** (the following January) |
| 2013 | Rwanda; Saudi Arabia; Mexico; Kuwait | 63.8; 19.9; 36.8; 6.2 | 1 Feb 2014: 63.8; 19.9; 37.4; 4.6 | mixed: Rwanda after its September 2013 election, Kuwait before its July 2013 election |
| 2017 | Rwanda; Sweden; Mexico; UAE; Saudi Arabia; Kuwait | 61.2; 43.6; 42.6; 22.5; 19.9; 3.1 | 1 Jan 2018: 61.3; 43.6; 42.6; 22.5; 19.9; 3.1 | **1 Jan 2018** (the following January); Nepal differs (WDI 29.6, IPU 3.6 provisional) |
| 2018 | Mexico; Sweden; Kuwait | 48.2; 46.1; 3.1 | 1 Jan 2019: 48.2; 47.3; 4.6 | mixed: Mexico after its July 2018 election, Sweden and Kuwait not the 1 Jan 2019 figure |
| 2019 | UAE; Sweden; Kuwait | 50.0; 47.3; 4.6 | 1 Jan 2019: 22.5; 47.3; 4.6 | mixed: UAE after its October 2019 election, Sweden and Kuwait equal the 1 Jan 2019 figure |

**Finding (Claude, DEC-621; an inference from the table, not a quote).** A WDI year is **not** one fixed date. Most tested values describe the position late in the WDI year or at the start of the next (2007, 2012, 2017 match the following January's ranking; Rwanda 2003 and 2013, Mexico 2018 and the UAE 2019 already include that year's election), but some match an earlier ranking (Kuwait 2013, 2018; Sweden 2019). 1998 is 10 August 1998, as WDI says; the SDG table's dates do not describe the WDI years. The missing final years fit "late in the year" too (Kuwait no 2024 figure after the May 2024 dissolution; Nepal no 2025 figure; Bangladesh no 2024 figure after the August 2024 dissolution), with exceptions (Afghanistan and Myanmar keep a 2021 figure). Because no single date is supported, **no date should be printed with the year** (question 2). The two sources disagree on 1998 (SDG table 25 January, WDI 10 August); WDI's own note is the one that matches its value.
