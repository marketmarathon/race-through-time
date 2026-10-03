## Summary for Luke

**What the race shows (January 1994 – September 2026, all devices).** Four leaders:

1. **Mosaic** leads from the start: 97.22% of GVU's January 1994 survey respondents named it as their main browser, and still 68% (all Mosaic versions together) in the October–November 1994 survey.
2. **Netscape** takes over somewhere between November 1994 and April 1996. There is **no figure in that gap**, so the month the straight line crosses (June 1995 in the data) is only where two lines meet and must not be shown as a date. By April 1996 Netscape has 83.3% of the hosts visiting the Illinois EWS server.
3. **Internet Explorer** first leads in **October 1998**, an observed month (EWS: Microsoft 49.1%, Netscape 48.3%). It peaks at about 96% in August 2002 (StatMarket 95.97% on 26 August 2002).
4. **Chrome** first leads in **May 2012**, also observed (StatCounter all platforms: Chrome 29.15%, IE 28.87%), and has led every month since. In September 2026 the board is Chrome 66.45%, Safari 18.2%, Edge 6.03%, Firefox 2.79%, Samsung Internet 2.31% and Opera 1.77%.

**How sure we are, part by part.**
- **2009 – 2026 (StatCounter): solid.** Every monthly value is the StatCounter export cell, checked by script. These are page views on StatCounter's member sites, not people.
- **1996 – 2000 (Illinois EWS): verified, but narrow.** Every month April 1996 – December 2000 was checked at its archived page. It is one university server's visiting hosts, not the whole web, which is why it is shown as an estimate.
- **2001 – April 2007 (StatMarket, then OneStat): verified snapshots.** 9 StatMarket and 64 OneStat figures, each read in the archived release, joined by straight lines.
- **May 2007 – December 2008 (W3Counter): verified monthly.**
- **1994 (GVU surveys): verified, weakest.** A self-selected online survey of early web users, mostly in North America.
- **The joins between sources are where the race is least reliable.** The sources measure different things, so the lines across the hand-overs show large moves that are really changes of measure: IE goes from 75.4% (EWS, December 2000) to 87.71% (StatMarket, February 2001), and from 85.81% (OneStat, January 2007) to 67.1% (W3Counter, May 2007). In June 2007 the two trackers were 19 points apart for the same browser (OneStat 85.81%, W3Counter 66.9%). This follows your decisions (DEC-152, DEC-153), but it is the main thing a sharp viewer could challenge.

**What Claude verified and how.** StatCounter and GVU were fetched by a GitHub runner, because this container's network blocks every source site. Eight EWS months came from the runner too. The web archive then blocked the runner with "too many requests", so Claude in Cowork checked the remaining 480 pre-2009 figures in your Chrome on 3 Oct 2026.
- Cowork's browser tool could not return page SHA-256 hashes, so those rows record the exact archive capture URL instead (`observations.csv` `url`; `page_sha256` empty).
- Rows checked by the runner do carry page hashes.
- The 384 cross-check figures (W3Schools, XiTi, Net Applications, TheCounter) remain UNVERIFIED. They are never on screen and only appear in the seam table.

<!-- QUESTIONS -->
## Questions for Luke (each with Claude's recommendation)

1. **Browser families (DEC-155).** Mosaic versions added together; Netscape 1–9 as one; Edge separate from IE; Firefox separate from the Mozilla Suite. Two further calls:
   - StatCounter's "Edge" and "Edge Legacy" are added together as one Edge bar. Because of this, September 2026 shows Edge at 6.03%, not StatCounter's headline 6.02%.
   - StatCounter's "IE Mobile" stays a separate bar.

   *Recommendation: accept both.*
2. **Hand-over rule (DEC-156).** Each source uses only its own figures. A straight line joins the last figure of one source to the first of the next. Cross-check sources are never shown. *Recommendation: accept.*
3. **Browsers a source does not report (DEC-157, refined in DEC-162).**
   - A line is drawn only between two figures of the same browser from the same source, or across a hand-over when both sides report it.
   - A single release that leaves a browser out does not break that source's line. Example: OneStat's 2004 releases omit Netscape.
   - Consequences:
     - MacWeb (3% on 16 Nov 1994) never appears at a month end.
     - Lynx and Mosaic stop in June 1997, when EWS stops listing them.
     - Netscape stops in January 2007.
     - Chrome first appears in January 2009, because W3Counter's tables do not list it.
     - Opera first appears in November 2004. StatMarket's single Opera figure (0.33% on 25 Oct 2001) has no neighbouring Opera figure to join, and OneStat gave Opera only by version until November 2004.

   *Recommendation: accept.*
4. **Dates (DEC-158).**
   - GVU's first survey (announced 17 January 1994, "posted on the Web for a month") is dated 31 January 1994.
   - OneStat releases are dated on their release day.
   - Monthly reports are dated at the month end.

   *Recommendation: accept.*
5. **"Other" is never a bar (DEC-159).** *Recommendation: accept.*
6. **EWS "Mosaic" includes Internet Explorer until May 1996.**
   - Following the source, the Mosaic bar falls from 13.4% (May 1996) to 3.4% (June 1996).
   - Internet Explorer then appears from nowhere at 11.0%.

   *Recommendation: keep the source as published and, in the player session, propose a short on-screen note (a new feature, so your approval first, DEC-069).*
7. **Netscape overtaking Mosaic.** It happens on the 1994–96 hand-over line (June 1995 in the data), which has no figure. *Recommendation: no dated callout; if a callout is wanted, word it "between late 1994 and spring 1996 (estimate)".*
8. **The big moves at the hand-overs.** IE +12 points across 2000–01 and −19 points across 2007, as the measure changes. *Recommendation: accept, as you decided (DEC-153), and name the source on screen at each era as planned. Optional extra: a short "new source" marker at each hand-over (a new feature, DEC-069).*
9. **GVU's terms.** GVU's copyright notice says the recipient "may not derive income for the Georgia Tech Research Corporation information itself" and must acknowledge GTRC (`reference/rights_ledger.md`). *Recommendation: credit GVU / Georgia Tech on screen and in the description. Decide whether you are comfortable that a monetised video does not "derive income for the information itself". This is not legal advice, and Isle of Man law has not been checked.*
10. **Terms for EWS, StatMarket, OneStat and W3Counter: NOT FOUND.** *Recommendation: we use only a few published percentages as facts, with the source named; accept, or ask Cowork to look for terms pages.*
11. **Disagreements.**
    - StatMarket's 1999–2000 figures are 10–17 points higher for IE than EWS in the same months.
    - OneStat's 3 February 2003 release has a second table with an unstated measure. It is not used.
    - OneStat's 28 July 2003 release prints two Mozilla values (0.51 and 1.6). Neither is used.

    *Recommendation: as handled (never averaged); listed below.*
12. **GVU April 1995 (Netscape 54%) stays UNVERIFIED.** It exists only in a secondary source, and GVU's own April 1995 survey pages have no browser chart. *Recommendation: leave it out.*
