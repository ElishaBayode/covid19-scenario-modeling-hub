## Summary of results
Differences across scenarios are driven by vaccination coverage level and timing. Relative to the no-vaccination counterfactual (Scenario A), all vaccination scenarios reduce cumulative hospitalizations and deaths, and the optimistic-coverage scenarios (D, E) avert substantially more than the moderate-coverage scenarios (B, C). Adding a semi-annual spring campaign for high-risk individuals (C, E) noticeably reduces the size of the Summer 2026 wave; because that campaign prevents summer infections, it can leave slightly more susceptibility going into the following winter, so for some locations the winter 2026-27 peak of the semi-annual scenarios is not lower than the annual-only scenarios even though cumulative burden is. Vaccination is protective in cumulative burden in every location (A has the highest cumulative hospitalizations and deaths everywhere). The projections show both a summer and a winter peak in the 2026-27 season, with more pronounced summer activity in southern states.

## Explanation of observed dynamics given model assumptions
Dynamics are driven by the combination of (i) per-group seasonal forcing fit to the observed 2025-26 curve, (ii) depletion and replenishment of susceptibility (infection- and vaccine-induced immunity lost at a single weekly rate combining waning and immune escape), and (iii) the group-specific vaccination schedule of each scenario. The seasonal structure, re-applied by week number, generates a high likelihood of both a summer and a winter peak. Because the vaccine is concentrated in the 65+ group, which accounts for the majority of hospitalizations, changes to vaccination have their largest effect on hospitalizations through that group.

## Model assumptions: please describe:
### Number/type of immune classes considered
We use a single all-or-nothing protected/susceptible split per group. For each of three population groups we track a protected fraction P_g(t); the susceptible fraction is s_g = 1 - P_g. Individuals enter the protected state through infection or vaccination and leave it (return to susceptible) at a single exponential weekly rate that combines waning and immune escape. We do not use a multi-level immune ladder; protection is binary within each group, with the vaccine contributing to protection scaled by its effectiveness against infection.

### Initial distribution of susceptibility (if available)
The initial susceptible fraction at the start of the projection period (June 8, 2025) is a hyperparameter sampled uniformly over [0.30, 0.70], shared across the three groups. Samples are weighted by how well the resulting free-run reproduces the observed calibration curve, so the effective initial-susceptibility distribution is data-informed.

### Initial variant characteristics (transmissibility of variants at t=0, and how uncertainty or non-identifiability was handled)
A single variant is modeled. Intrinsic transmissibility (two weekly transmission rates β1, β2, corresponding to k=2, J=1) is estimated per group by non-negative regression on the susceptibility-adjusted incidence over the calibration window. Immune escape is not modeled as discrete variants but folded into the constant weekly immunity-loss rate. Uncertainty and non-identifiability are handled by Latin-hypercube sampling over the remaining hyperparameters and importance-resampling by calibration fit.

### Details about calibration of immunity at t=0 (calibration period considered, assumptions about/fitting of past immune escape and waning immunity, is the same calibration process used for all scenarios?)
The initial immune fraction (1 - initial susceptibility) is a sampled hyperparameter at the projection start (June 2025), not carried over from a prior round. Calibration uses data from June 2025 to June 2026. Goodness of fit is evaluated on the free-run driven by the **actual observed vaccination** — before any scenario is generated — since the scenario projections are counterfactuals and are not expected to match reality. The same calibrated parameters are used for all five scenarios (paired simulations); scenarios differ only in their vaccination schedule. Past immune escape and waning are represented jointly by the sampled weekly immunity-loss rate.

### Details about modeling of immune escape after t=0 (including what is the level of immune escape considered, whether a stepwise or continuous escape was considered and how immune escape affects infection- and vaccine-induced immunity)
Immune escape is continuous and is combined with immunity waning into a single weekly loss-of-immunity rate ω, sampled over [0.020, 0.055] per week (equivalent to a median immunity duration of roughly 3-10 months, encompassing waning plus roughly 20-50% per year escape). We do not distinguish infection-induced from vaccine-induced immunity, so escape affects both identically.

### Assumptions regarding waning immunity against infection and symptoms (including values used for the duration and level of protection against infection or symptomatic disease, whether a point estimate was used or a range, and distribution used)
Immunity against infection is lost at the single weekly exponential rate ω described above (sampled range [0.020, 0.055]/week; median duration ~3-10 months). Vaccine effectiveness against infection at administration is sampled uniformly over [0.35, 0.57] (per round guidance) and scales the susceptibility reduction from each dose. Protection is all-or-nothing and decays by returning individuals to the fully susceptible state.

### Assumptions regarding waning immunity against severe disease (including whether immunity against severe disease, conditional on infection, is fixed vs declines over time; and if it wanes, specify how)
We model protection against infection only. Severe outcomes are derived from infections via fixed group-specific severity, so we do not separately track or wane protection against severe disease given infection. Consequently, all vaccine benefit against hospitalization operates through reduced infection.

### Assumptions regarding boosting effect from multiple infections
None explicitly. With an all-or-nothing protected fraction per group, reinfections are represented implicitly through the return of previously-infected individuals to the susceptible pool via waning/escape.

### Is vaccination assumed to prevent infection and/or transmissibility?
Infection only. Vaccination reduces susceptibility (via VE against infection); it has no separately-modeled effect on onward transmissibility or on severity given infection.

### Describe the process used to set or calibrate disease severity, ie P(hosp given current infection) and P(death given current infection) details. What are the datasets used for calibration of the death targets?
Reported hospitalizations (NHSN) are treated directly as the modeled incidence signal for each group. Group-specific relative severities (low-risk 1, high-risk 3, 65+ 11) convert infections to hospitalizations and also split the observed 0-64 hospitalization series into high- and low-risk components; the overall hospitalization-per-infection scale is a sampled hyperparameter fit by calibration. These relative severities give the 65+ group approximately 65% of hospitalizations, matching the data. Deaths are modeled as an outcome of hospitalizations (a non-negative least-squares regression of observed deaths on lagged total hospitalizations, lags 0-3 weeks, deaths lagging hospitalizations by about two weeks, ratio about 5.5%), fit per location and applied to every hospitalization trajectory. Deaths are calibrated to the SMH-provided death target (NCHS-based) and are modeled at the overall (all-ages) level only.

### Describe seasonality implementation, e.g., whether seasonality varies by geography, what is the function used to model seasonal forcing, and which datasets are used to fit seasonal parameters
Seasonality is a week-of-year multiplicative factor on transmission, bounded to [0.5, 2], fit **separately for each group** (three seasonality adjustments per location) so that the model's free-run reproduces the observed 2025-26 curve; the same week-of-year multipliers are then applied to future weeks. Seasonality is location-specific because every location is calibrated independently. Parameters are fit to the NHSN hospitalization target data.

### What is the calibration period used to fit the model? How is the period of low reporting in hospitalization data in May-Nov 2024 handled?
The calibration period is June 2025 to June 2026 (the projection start onward), fit to hospitalizations (NHSN) and deaths (NCHS). Because calibration uses only data from mid-2025 onward, the May-November 2024 low-reporting period is entirely outside the fitting window and does not affect the model.

### Details about modeling of age-specific outcomes, including assumptions on age-specific parameters (e.g., susceptibility, infection hospitalization risk or fatality risk, VE)
The population is modeled in three groups: low-risk (18-64 low-risk plus children 0.5-17), high-risk (18-64 high-risk), and 65+ (treated as high-risk/eligible). Susceptibility and immunity are tracked per group. Hospitalization risk per infection is group-specific via the relative severities above; deaths are all-ages only. Infection susceptibility is assumed equal across groups apart from differences induced by vaccination. VE against infection is assumed equal across groups (per round guidance).

### Details about modeling of high-risk individuals, e.g., susceptibility and infection hospitalization risk or infection fatality risk, VE
The 18-64 age band is split into low-risk and high-risk. High-risk individuals have a relative hospitalization severity three times that of low-risk individuals (used both to split observed 0-64 hospitalizations and to convert infections to hospitalizations). The 65+ group is treated as entirely high-risk/eligible. High-risk individuals of any age are the target of the semi-annual spring 2026 campaign in Scenarios C and E. VE is assumed equal for high- and low-risk groups.

### Is empirical data on human mobility or contact patterns used in the model?
None. Groups are calibrated independently and combined by summation; the final model does not use an explicit between-group contact matrix or empirical mobility data. It estimates the contact matrtix from data.

### Is there a background level of non pharmaceutical interventions?
None.

### Is importation from other countries considered?
None.

### Other updates in model assumptions from previous rounds (e.g., demographic dynamics, immune escape, severity)
This is an independent, simplified SIkJalpha implementation prepared for Round 20; it is not a continuation of a prior-round model. Key simplifications relative to a full model: a single variant with immune escape folded into the weekly immunity-loss term; reported hospitalizations treated directly as the case/incidence signal; three age/risk groups calibrated independently and summed (no explicit contact matrix); vaccine benefit against hospitalization operating only through reduced infection.