# GO Analysis Repository — Handover Documentation

## Overview

This repository contains the quantitative analysis framework for the European Guarantee of Origin (GO) market. It combines ENTSO-E generation data, AIB certificate lifecycle statistics, and Argus price assessments to produce a comprehensive view of GO supply, demand, inventory, cross-border flows, and pricing dynamics.

---

## Repository Structure

```
├── GO_Price_Data.ipynb              # Argus GO price term structure and technology premium analysis
├── GO_Fundamental_Overview.ipynb    # AIB supply/demand/inventory/flow analysis
├── Hydro/
│   ├── Hydro_Balance.ipynb          # Nordic hydro balance forecasts (PointConnect)
│   └── Hydro_Generation.ipynb       # ENTSO-E hydro generation vs GO issuance comparison
├── Solar/
│   └── Solar_Generation.ipynb       # ENTSO-E solar generation vs GO issuance comparison
├── Wind/
│   └── Wind_Generation.ipynb        # ENTSO-E wind generation vs GO issuance comparison
├── Trading_Strategies.md            # Three candidate trading strategies
├── functions/
│   ├── __init__.py
│   └── sql_data.py                  # Database query interface (SQL Server via SQLAlchemy)
├── GO_All_Statistics_1.csv          # AIB Activity Statistics (part 1)
├── GO_All_Statistics_2.csv          # AIB Activity Statistics (part 2)
├── pyproject.toml                   # Python project dependencies
└── poetry.lock
```

Each notebook follows a consistent structure:
1. **Imports** — library and database interface loading
2. **Parameters** — user-adjustable constants (curve IDs, file paths, date ranges)
3. **Analysis** — data collection, processing, visualisation, and conclusions

---

## The GO Market

### What is a Guarantee of Origin?

A Guarantee of Origin (GO) is an electronic certificate proving that 1 MWh of electricity was generated from a specific energy source. GOs are the legally mandated instrument under EU Directive 2018/2001 for electricity origin disclosure to end consumers. They are issued, transferred, and cancelled within the AIB (Association of Issuing Bodies) European Energy Certificate System (EECS).

### Certificate Lifecycle

| Event | Description |
|-------|-------------|
| **Issuance** | A GO is created for 1 MWh of eligible production. Producers have up to 12 months post-production to request issuance. |
| **Transfer** | Intra-registry ownership change between account holders. |
| **Export/Import** | Cross-border transfer between national registries via the AIB Hub. |
| **Cancellation** | The GO is consumed — typically by a supplier disclosing the origin of electricity to an end consumer. Cancellation is irreversible. |
| **Expiry** | GOs not cancelled within 12 months of production are automatically removed. |
| **Withdrawal** | Administrative removal from the system. |

### Market Structure

- **Supply** is driven by renewable generation eligible for GO issuance. Norway and Sweden (hydro) dominate, followed by wind (ES, DE merchant share, FR, DK) and solar (DE merchant share, ES, IT, NL).
- **Demand** is driven by compliance cancellations — suppliers must disclose origin to consumers. Germany and the Netherlands are the largest net importers due to the *Doppelvermarktungsverbot* (double marketing prohibition under the German EEG), which prevents EEG-subsidised generators from obtaining GOs.
- **Inventory** is the running stock of live certificates in the system. Seasonal build/draw cycles are driven by the timing mismatch between issuance (peaks Q2–Q3) and cancellation (peaks Q1–Q2 of the following year).
- **Pricing** is assessed by Argus Media for four benchmark contracts: Wind EU, Solar EU, Hydro Nordic, and Any Renewable EU, each differentiated by production year.

### Key Regulatory Constraints

- **Double marketing prohibition (DE):** Generators receiving EEG feed-in tariffs or market premiums cannot simultaneously obtain GOs. This excludes the majority of German renewables from the GO system, making Germany a structural net importer.
- **12-month validity:** GOs expire 12 months after production if not cancelled, creating a natural inventory drain and urgency for timely cancellation.
- **12-month issuance window:** Producers can delay issuance up to 12 months post-production. Nordic hydro producers routinely exploit this for strategic timing.

---

## Data Sources

### 1. InCo SQL Server Database

Accessed via `functions/sql_data.py` using SQLAlchemy + ODBC Driver 18.

| Data | Table | Description |
|------|-------|-------------|
| ENTSO-E generation curves | `pub.Timeseries1_v02` | Hourly MW production by country/zone and technology (hydro RoR, reservoir, wind onshore/offshore, solar) |
| Hydro balance forecasts | `pub.Timeseries1_v02` | Nordic hydro balance deviation from normal (GWh) |
| Curve metadata | `pub.dimMetadata` | Curve names, IDs, and deprecation status |
| GO prices | `pub.Argus_Certificate_Price` | Argus midpoint assessments by contract code and production year |

### 2. AIB Activity Statistics (CSV)

Two CSV files (`GO_All_Statistics_1.csv`, `GO_All_Statistics_2.csv`) manually downloaded from https://www.aib-net.org/facts/eecs-go-statistics. These contain monthly certificate volumes by country, energy source, and event type. Data dimensions include:
- Production-date view (volumes indexed by when electricity was produced)
- Transaction-date view (volumes indexed by when the certificate event occurred)
- Lifecycle events: issue, cancel, expire, transfer, export, import, withdraw

### 3. ENTSO-E Transparency Platform (via InCo)

Generation data is sourced from ENTSO-E and stored in the InCo database. Each country/zone has dedicated curve IDs for each generation type. The curve ID mappings are hardcoded in the Parameters section of each generation notebook.

---

## Known Data Gaps

Several AIB member countries lack ENTSO-E generation curves in the internal database:

| Technology | Missing Countries | Reason |
|------------|-------------------|--------|
| **Hydro** | CY, IS, LU | Negligible or no hydro capacity |
| **Solar** | CY, IS, LU, RS | No curves available; RS has minimal solar |
| **Wind** | CY, IS, LU, RS | No curves available |
| **All** | IE (offshore), GR (RoR) | Partial coverage — only some generation types available |

Additionally:
- **Germany (DE):** ENTSO-E hydro data only covers a subset of TSO regions (Amprion, TransnetBW, TenneT, no 50Hertz reservoir), leading to GO factors > 1 for hydro.
- **Switzerland (CH):** ENTSO-E data captures only a portion of total hydro production, resulting in an apparent GO factor of ~2.5×.
- **Netherlands (NL):** Significant distribution-level wind and solar capacity is invisible to ENTSO-E (which only sees TenneT/TSO-connected generation), causing GO issuance to exceed reported generation.

These gaps do not affect the fundamental analysis (AIB statistics are complete), but they limit the generation-vs-issuance comparison to countries with adequate ENTSO-E coverage.

---

## Trading Strategies

The file `Trading_Strategies.md` describes three candidate relative-value strategies derived from the analysis:

### 1. Seasonal Inventory Cycle — Calendar Spread

Exploits the predictable seasonal pattern of GO inventory (build in Q2–Q3 from issuance surge, draw in Q4–Q1 from cancellation demand). The trade is long near-year production GOs during the draw phase and short during the build phase, capturing the mean-reverting seasonal premium via a calendar spread.

### 2. Technology Basis Trade — Wind/Solar vs. Any Renewable

Trades the technology premium $\Delta_k(t) = P_k(t) - P_{\text{Any Renewable}}(t)$. When rolling issuance momentum for a specific technology decelerates (supply tightens), go long the basis; when it accelerates (supply floods), go short. Signal is derived from AIB monthly statistics with ~1 month lag.

### 3. Cross-Border Flow Imbalance — Long Deficit / Short Surplus

Exploits the structural rigidity of cross-border flow patterns. Deficit countries (DE, NL, AT) must continuously import certificates, creating persistent demand pressure. The trade is long certificates demanded by deficit countries (e.g., Hydro Nordic) and short the generic benchmark, scaled by the rate of inventory drawdown in importing countries.

All three strategies are spread/relative-value by construction, limiting directional exposure to the overall GO price level.

---

## Getting Started

1. Ensure Python dependencies are installed: `poetry install`
2. Verify database connectivity (requires ODBC Driver 18 for SQL Server and network access to `inco-bisql.database.windows.net`)
3. Open any notebook and run cells sequentially — parameters are in the second section of each notebook and can be adjusted as needed
4. The `functions/` folder contains the shared database query interface used by all notebooks
