# GO Trading Strategy Suggestions

Three candidate strategies derived from the supply–demand fundamental analysis (AIB Activity Statistics) and the Argus-assessed price term structure.

---

## 1. Seasonal Inventory Cycle — Calendar Spread

**Signal source:** GO_Fundamentals.ipynb — aggregate inventory time series.

**Observation:** Issuance peaks in Q2–Q3 (hydro snowmelt, solar irradiance) while cancellations cluster around compliance deadlines (typically Q1–Q2 of the following year). This produces a predictable inventory *build* in summer and *draw* in winter/spring.

**Trade construction:** Calendar spread on production-year contracts:
- **Long** near-year production GOs during the draw phase (Q4–Q1), when inventory declines and scarcity premiums rise.
- **Short** near-year production GOs during the build phase (Q2–Q3), when fresh issuance floods the market and prices soften.

**Edge:** Captures the mean-reverting seasonal premium without directional price exposure. The position profits from the predictable widening and narrowing of the front/back production-year spread driven by physical certificate lifecycle timing.

---

## 2. Technology Basis Trade — Wind/Solar vs. Any Renewable

**Signal source:** GO_Price_Data.ipynb — technology premium $\Delta_k(t) = P_k(t) - P_{\text{Any Renewable}}(t)$.

**Observation:** The technology premium is persistent but time-varying. When issuance of a specific technology surges (e.g., a strong wind year), the corresponding basis compresses as supply outpaces incremental demand for that label. Conversely, supply shortfalls widen the premium.

**Trade construction:** Spread trade between a technology-specific contract and the Any Renewable EU benchmark:
- **Long the basis** (long Wind/Solar, short Any Renewable) when rolling issuance momentum for that technology is decelerating or below trend.
- **Short the basis** when issuance momentum is accelerating or above trend.

**Edge:** Market-neutral position whose P&L is driven by relative supply dynamics observable in near-real-time from AIB monthly statistics, before the broader market reprices.

---

## 3. Cross-Border Flow Imbalance — Long Deficit / Short Surplus

**Signal source:** GO_Fundamentals.ipynb — net cross-border position and country-level inventory.

**Observation:** Structural flow patterns are rigid: Norway exports ~600M GOs cumulatively, Germany imports ~1000M. Deficit countries (DE, NL, AT) must continuously import, creating persistent demand-side pressure. Surplus countries (NO, SE, ES) face structural oversupply of domestically-sourced certificates.

**Trade construction:** Relative-value position across regional/origin contract types:
- **Long** certificates demanded by deficit countries (e.g., Hydro Nordic, which flows south to satisfy German/Dutch compliance demand).
- **Short** certificates abundant in surplus countries or the generic Any Renewable benchmark.

Scale the position based on the rate of inventory drawdown in importing countries — acceleration signals tightening and spread widening.

**Edge:** Exploits the inelasticity of compliance-driven import demand combined with the physical constraint that cross-border transfer takes time. When deficit-country inventories draw faster than historical norms, the premium for importable certificate types widens before new export supply can respond.

---

## General Notes

- All strategies are spread/relative-value by construction, limiting directional exposure to the overall GO price level.
- Signals are derived from publicly available AIB monthly statistics with a ~1 month reporting lag.
- Execution assumes access to OTC or exchange-traded GO forward contracts differentiated by production year, technology, and/or origin.
