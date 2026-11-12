# Sources log

Downloaded 2026-11-11. Raw files are kept out of Git (raw/ is in .gitignore).

| Folder | Source | URL | Coverage | Notes / terms |
|---|---|---|---|---|
| raw/caa | UK CAA, Table 03 All Services (CSV + PDF) | https://www.caa.co.uk/data-and-analysis/uk-aviation-market/airlines/uk-airline-data/ | Jan 2025 to Aug 2026 (20 months) | UK-registered carriers only (e.g. easyJet UK, Ryanair UK are small subsidiaries). Has seat-km available and used, so load factor = used / available. Check CAA licence before publishing. |
| raw/dgca | DGCA monthly air transport statistics, per airline XLSX | https://www.dgca.gov.in (Aviation data and statistics > Domestic Air Transport > Air Traffic > Monthly) | 2025 full year, 2026 Jan to Sep | Domestic block first, international block second in each sheet. SpiceJet 2025 file not listed on the site. Pax load factor defined as PKM / ASKM. |
| raw/company | Emirates Group H1 2026-27 results (page saved to PDF) | https://www.emirates.com/media-centre/ | Apr to Sep 2026 | Press release, 5 Nov 2026. |
| raw/company | Ryanair Oct 2026 traffic (page saved to PDF) | https://corporate.ryanair.com/ | Oct 2026 | Passenger-based load factor. Other months still to add. |
| raw/company | IndiGo Q2 FY26 results press release (page saved to PDF) | https://www.goindigo.in/press-releases/ | Jul to Sep 2025 | Q2 FY27 release still to add (results dated 29 Oct 2026). |

## Added 2026-11-12

| Folder | Source | URL | Coverage | Notes |
|---|---|---|---|---|
| raw/company | Ryanair traffic and load factor table (page saved to PDF) | https://investor.ryanair.com/traffic/ | Monthly guests and load factor, FY24 to Oct 2026 | Replaces the need for separate monthly releases. Load factor is passenger-based. |
| raw/company | Emirates Group H1 2025-26 fast facts (PDF) | https://www.emirates.com/media-centre/ | Apr to Sep 2025 | Comparison base for H1 2026-27. |
| raw/company | IndiGo Q2 FY27 earnings call transcript (PDF, NSE filing) | https://nsearchives.nseindia.com/corporate/Indigo1_04112026174231_Transcript_Q2_FY27.pdf | Jul to Sep 2026 | Results dated 29 Oct 2026. Press release itself not yet saved. |
| raw/caa | CAA Sep and Oct 2026 | n/a | not published yet | Pages redirect as of 12 Nov 2026. Re-check later. |

## Methodology note: matched months (added 12 Nov 2026)
Found while fact-checking the first Power BI build against the raw CSVs. The first dashboard compared Mar to Sep 2026 against Mar to Sep 2025, but Sep 2026 is not published for the UK brands and Air India, so the shock window held 6 months and the baseline 7. Summed capacity looked about 14% lower for those brands. That was a window-length artefact, not a real capacity cut.
Fix: fact_traffic.window flags only months present for the brand in both years (Mar to Aug, 6 months). SpiceJet has no 2025 data and is excluded from every shock comparison. Load factor is always SUM(rpk) / SUM(ask). SQL files already used Mar to Aug and were unaffected.
