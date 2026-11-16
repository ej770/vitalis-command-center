# Vitalis Command Center

An interactive hospital operations dashboard built on **real public data** for Massachusetts General Hospital (CMS Certification Number 220071). It combines weekly HHS bed-capacity reporting with CMS Care Compare quality measures, and adds scenario modelling, forecasting, nurse staffing and a 3D view of the hospital.

Open `index.html` in a browser. It is a single self-contained page; the only network requests are fonts and the three.js library from public CDNs.

## What's in the dashboard

| Area | What it does |
|---|---|
| **Patient flow** | Inpatient census split across Adult Med/Surg, Adult ICU, Pediatric Ward and Peds & Neonatal ICU, with sparklines and week-over-week deltas. |
| **Scenarios** | Real weeks (Omicron peak, ICU at 100%, the 2022 pediatric RSV/flu surge, latest reported) and what-if replays. A week slider and playback cover all 188 reported weeks. |
| **What-if levers** | Admission demand, staffed beds lost, length-of-stay change and flex beds, projected onto the selected unit. |
| **3D hospital** | Six-floor building (three.js): ED, Surgery (operating rooms and recovery bays), Critical Care, two Med/Surg floors and Pediatrics, plus a rooftop helipad. Single patient rooms with private bathrooms, glass-front ICU rooms, curtained ED bays and operating rooms. Hover or click any room for its status, clinical group, day of stay and assigned nurse. The floor selector lifts away the floors above the chosen one. |
| **ED → admission pipeline** | Daily ED arrivals, ED occupancy, admission requests, rooms available for admission (open rooms plus expected discharges) and ED boarders, by day of the week and by unit. |
| **Nurse staffing** | RNs on duty versus needed for each care area and shift (Day, Evening, Night), with actual vs target patient-to-nurse ratios. |
| **Analytics** | Damped Holt trend forecast with an 80% interval and a backtest (MAPE, interval coverage), a unit-by-month occupancy heatmap, and automated insights (percentile position, saturation streaks, seasonality, COVID correlation, forecast risk, anomalies, capacity gap, ED crunch day, worst staffing shift). |
| **Quality** | CMS overall rating, hospital-wide readmission and mortality, sepsis (SEP-1), patient safety indicators, HCAHPS, and ED median length of stay (OP-18b). |
| **AI analyst** | A chat that reads the current dashboard state and can run scenarios. It uses the Claude artifact runtime (`window.claude`), so it works only when the page is opened as a Claude artifact; in a normal browser it shows "Open in Claude to chat". |

## Data sources

All raw API responses are kept in `data/raw/`.

- **HHS:** *COVID-19 Reported Patient Impact and Hospital Capacity by Facility* (healthdata.gov dataset `anag-cw7u`), weekly 7-day averages, Sep 2020 – Apr 2024. Federal reporting ended in May 2024. ED visit counts are reported through Jun 2023.
- **CMS Care Compare provider data:**
  - Timely & Effective Care (`yv7e-xc69`)
  - Complications & Deaths (`ynj2-r877`)
  - Unplanned Hospital Visits (`632h-zaca`)
  - HCAHPS patient survey (`dgck-syfz`)
  - Hospital General Information (`xubh-q36u`)

## Method and assumptions

**Derived units.** HHS reports hospital-level fields, so units are derived:
- Adult Med/Surg = adult inpatient beds − staffed adult ICU beds
- Pediatric Ward = all inpatient − adult inpatient − pediatric ICU
- Peds & Neonatal ICU = total ICU − adult ICU

**ED model.**
- Real inputs: weekly ED visits ÷ 7, and the CMS median ED stay of 298 minutes. Patients in the ED at once = arrivals × stay ÷ 1,440 minutes (Little's law).
- Assumptions, adjustable in the page: ED admit rate (default 24%) and ED treatment spaces (default 80).
- Fixed assumptions: unit mix of ED admissions, average length of stay per unit, and typical published day-of-week profiles for ED arrivals, discharges and elective admissions.

**Nurse staffing.**
- Targets: the Massachusetts ICU staffing law (2014: 1:1 or 1:2) and California Title 22 minimums (Med/Surg 1:5, Pediatrics 1:4, ED 1:4, PACU 1:2, one circulating RN per OR).
- Assumptions: RN schedules, shift fill rates (Day 100%, Evening 94%, Night 86%), 56 ORs, 44 PACU bays, 2.4-hour average cases and surgical volume ratios.

**Illustrative detail.** Room numbers, clinical groups, days of stay and nurse assignments in the 3D view are generated to match the real unit totals. The source data reports totals only. The building layout is also illustrative: the real campus spans several buildings.

This is an independent analysis of public data and is not affiliated with the hospital.

## Rebuild

```bash
python scripts/build.py
```

`scripts/build.py` embeds `data/weeks.json` into `src/dashboard.src.html` and writes `index.html`. `scripts/shape_hhs.py` turns the raw HHS response into `data/weeks.json`.

## Repository layout

```
index.html              built, self-contained dashboard
src/dashboard.src.html  dashboard template (HTML, CSS, JS)
data/weeks.json         shaped weekly HHS data
data/raw/               raw HHS and CMS API responses
scripts/                build and data-shaping scripts
```
