# Agricultural NDVI Sensor Reliability Analysis

## Project Overview

This project aim is to analyse agricultural parcel metadata and NDVI (Normalized difference vegetation index) sensor readings to evaluate:

- data quality,
- sensor reliability,
- explain the findings,
- and overall quality before any modeling or time series analysis.

This pipeline cleans, validates, and merges both datasets into a final time-series dataset suitable for analysis.

---

# 1. Data Quality Audit

| Column              | Issue Identified                                       | Prevalence                                                    | Decision       | Justification                                                                         |
| ------------------- | ------------------------------------------------------ | ------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------- |
| parcel_id           | Parcel inconsistency between metadata and readings     | 3 parcels absent in readings and 2 absent in metadata         | Preserve + Isolate           | Preserved separately and because of mismatches, merge prunes orphan parcel ids |
| crop_type           | Imbalanced crop distribution                           | Sugarcane represents ~70% of parcels                          | Preserve       | Reflects real distribution considering the counts                         |
| sowing_date         | Stored as string                                       | Entire column                                                 | Repair         | Required datetime conversion for temporal analysis                                    |
| date                | Multiple date formats                                  | 3 formats detected                                            | Repair         | Standardized parsing required for consistency                           |
| ndvi_value          | Invalid biological values outside [-1, 1]              | 104 invalid records                                                   | Flag + Exclude | Impossible values will distort vegetation analysis                      |
| sensor_status       | Whitespace, casing inconsistencies, and missing values | 137 missing values detected                                   | Repair         | Standardization for proper categorising     |
| parcel coverage (orphan parcel_id)   | Incomplete temporal coverage                           | Compared to the other parcels with ~135 records, Parcels 098 and 099 has only ~20 records each, roughly 15% of the volume | Preserve + Isolate         | Preserved for future interpretation, deployment                            |
| temporal continuity (orphan parcel_id) | Large temporal gaps                                    | 90-day and 63-day discontinuities detected for Parcels 098 and 099 respectively                   | Preserve + Isolate         |     Temporal discontinuities were preserved because they may represent real or testing outages, ingestion failures

---

# 2. Pipeline Approach

The pipeline performs the following steps:

1. Loaded parcel metadata and sensor readings
2. Standardized date formats
3. Cleaned sensor status labels
4. Flagged invalid NDVI observations
5. Separated rogue parcel records with metadata inconsistencies
6. Preserved degraded but potentially usable observations
7. Merged metadata and sensor readings into a unified parcel-date time-series dataset
8. Exported cleaned dataset as: `data/cleaned_parcel_timeseries.csv`
9. Exported final analysis dataset as: `data/analysis_dataset.csv`


---

# 3. Quick Analysis - Crop-Level NDVI Stats

| crop_type | mean_ndvi_before | mean_ndvi_after | n_parcels |
| --------- | ---------------- | --------------- | --------- |
| soybean   | 0.215545	               | 0.316259              | 4        |
| sugarcane | 0.230894               | 0.355916              | 19        |
| wheat     | 0.215500               | 0.322548                 | 2        |

### Interpretation

NDVI values generally increase after sowing, indicating expected vegetation growth activity following crop establishment.

It was asked to ignore the bad `sensor_status` observations, only  CORRUPTED NDVI readings were removed and isolated from the final analysis. DEGRADED and UNKNOWN sensor states were preserved (for before and after NDVI analysis) when NDVI values remained plausible, because operational instability may still contain importaant informattion regarding the sensors useful for vegetation signals.

The increase in post sowing NDVI across all crop categories aligns with expected vegetation development following crop establishment, suggesting that the trusted subset retained biologically meaningful signals despite inconsistencies in the raw system.

Sugarcane shows the highest post-sowing NDVI increase and also dominates the dataset with 19 parcels, while soybean and wheat contain only 4 and 2 parcels respectively. As a result, the soybean and wheat aggregates are less statistically stable and more sensitive to parcel-level variation.

---

# 4. Production-Readiness Reflection

## If the dataset became 100× larger

### Changes I would make

1. Move preprocessing into modular production pipelines.
2. Partition time-series data by date and parcel for scalable processing
3. Introduce automated validation checks for NDVI ranges, date consistency, sensor status and orphan parcels and metadata mismatches.

---

## What I would monitor

* Percentage of invalid NDVI readings
* Missing sensor status frequency
* Temporal continuity gaps of indicidual parcels
* Daily ingestion row counts
* Data drift over quarters, mainly NDVI avg
* Sudden spikes in degraded or discarded sensor states
* Crop-wise observation imbalance and shrinking parcel representation
* The status transition change is in proportion
* Flatlining of sensor measurements
---

## Most likely silent failure

The most likely silent failure would be gradual sensor degradation producing biologically plausible NDVI values. These records may pass standard range validation checks while still reducing the reliability of downstream vegetation analysis.

This becomes particularly important for smaller crop groups such as wheat and soybean, where a small number of unreliable parcels could disproportionately influence aggregate NDVI trends due to limited parcel representation.

---

# Reading Notebooks

Read notebooks sequentially from 01 to 07 as labeled, since each notebook progressively builds on the findings, preprocessing decisions, and analytical outputs of the previous stage.

# Tech Used

Python 3.12

pandas

numpy

matplotlib

seaborn

VS Code

Excel

codex - used for logics, charts, output validation, comments AND README refinement.

[Normalized Difference Vegetation Index (NDVI)](https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index) - domain reference for vegetation health interpretation

