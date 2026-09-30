# ML Monitoring & Data Drift Detection System

A modular machine learning monitoring project that detects **data
drift** between reference data and simulated production data using the
**Kolmogorov-Smirnov (KS) test** and **Population Stability Index
(PSI)**.

The project is built around a bank customer churn dataset and includes a
Streamlit dashboard for viewing drift results.

------------------------------------------------------------------------

## Overview

Machine learning models can become less reliable after deployment when
the data they receive changes over time.

For example, a churn model may have been trained when customers had
relatively low transaction amounts. If customer transaction behavior
changes significantly later, the production data may no longer resemble
the data used during model development.

This project monitors that change:

``` text
Historical Dataset
       |
       v
Prepare Reference + Production Data
       |
       v
Compare Feature Distributions
       |
       +----> KS Test
       |
       +----> PSI
       |
       v
Drift Report
       |
       v
Streamlit Dashboard
```

------------------------------------------------------------------------

## Features

-   Modular Python project structure
-   Reference vs production data comparison
-   Data drift detection using:
    -   Kolmogorov-Smirnov (KS) test
    -   Population Stability Index (PSI)
-   Automated generation of reference and simulated production datasets
-   CSV drift report
-   Streamlit monitoring dashboard
-   Uses `uv` for Python dependency management

------------------------------------------------------------------------

## Project Structure

``` text
ml-monitoring-system/
│
├── data/
│   ├── raw/
│   │   └── BankChurners.csv
│   ├── reference/
│   │   └── reference_data.csv
│   └── production/
│       └── production_data.csv
│
├── reports/
│   └── drift_report.csv
│
├── src/
│   ├── __init__.py
│   ├── prepare_data.py
│   ├── run_monitoring.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   └── loader.py
│   │
│   └── drift/
│       ├── __init__.py
│       ├── ks_test.py
│       ├── psi.py
│       ├── detector.py
│       └── report.py
│
├── app.py
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── README.md
└── uv.lock
```

> Generated datasets inside `data/reference/` and `data/production/` do
> not need to be committed to GitHub. They are recreated by
> `prepare_data.py`.

------------------------------------------------------------------------

## How It Works

### 1. Raw Data

The project starts with the bank customer churn dataset:

``` text
data/raw/BankChurners.csv
```

The monitoring system currently uses these numerical features:

-   `Customer_Age`
-   `Credit_Limit`
-   `Total_Trans_Amt`
-   `Total_Trans_Ct`
-   `Avg_Utilization_Ratio`

------------------------------------------------------------------------

### 2. Reference Data

Reference data represents the distribution that the monitoring system
considers the baseline.

It is generated from the original dataset.

``` text
BankChurners.csv
       |
       v
Reference Data
```

------------------------------------------------------------------------

### 3. Production Data

The project does not have access to a real production stream, so
`prepare_data.py` creates a simulated production dataset.

A controlled change is introduced into `Total_Trans_Amt`:

``` python
production["Total_Trans_Amt"] *= 1.5
```

This intentionally creates a distribution shift so that the monitoring
system has drift to detect.

------------------------------------------------------------------------

## Drift Detection

### Kolmogorov-Smirnov Test

The KS test compares the distributions of reference and production data.

The project uses a significance threshold of:

``` text
0.05
```

The interpretation used by the monitoring code is:

``` text
p-value < 0.05
        |
        v
Statistical evidence of distribution difference
        |
        v
Drift detected
```

The KS test provides:

-   KS statistic
-   p-value
-   drift flag

------------------------------------------------------------------------

### Population Stability Index

PSI measures the degree of distributional change between reference and
production data.

The project calculates a PSI score for each monitored feature.

Together, KS and PSI provide two different views of distribution shift:

``` text
KS  -> statistical evidence of difference
PSI -> magnitude of distribution shift
```

------------------------------------------------------------------------

## Installation

### Prerequisites

-   Python 3.10+
-   `uv`
-   Bank churn dataset

Clone the repository and move into the project directory:

``` bash
cd ml-monitoring-system
```

Install dependencies:

``` bash
uv sync
```

If dependencies have not yet been added, they can be installed with:

``` bash
uv add pandas numpy scipy streamlit
```

------------------------------------------------------------------------

## Dataset Setup

Place the dataset at:

``` text
data/raw/BankChurners.csv
```

The project expects the following columns:

``` text
Customer_Age
Credit_Limit
Total_Trans_Amt
Total_Trans_Ct
Avg_Utilization_Ratio
```

------------------------------------------------------------------------

## Running the Project

### Step 1 --- Prepare the data

Run:

``` bash
uv run python -m src.prepare_data
```

This creates:

``` text
data/reference/reference_data.csv
data/production/production_data.csv
```

------------------------------------------------------------------------

### Step 2 --- Run drift monitoring

Run:

``` bash
uv run python -m src.run_monitoring
```

The system compares the reference and production distributions and
creates:

``` text
reports/drift_report.csv
```

The terminal also displays the drift results.

------------------------------------------------------------------------

### Step 3 --- Start the Streamlit dashboard

Run:

``` bash
uv run streamlit run app.py
```

The dashboard displays:

-   Overall monitoring status
-   Number of monitored features
-   Number of features with detected drift
-   Feature-level KS results
-   PSI scores
-   Drift report

------------------------------------------------------------------------

## Example Monitoring Output

A generated report contains columns similar to:

  Feature                   KS Statistic   P-Value KS Drift      PSI
  ----------------------- -------------- --------- ---------- ------
  Customer_Age                      0.03      0.72 False        0.01
  Credit_Limit                      0.04      0.51 False        0.02
  Total_Trans_Amt                   0.42    0.0001 True         0.58
  Total_Trans_Ct                    0.05      0.32 False        0.03
  Avg_Utilization_Ratio             0.03      0.61 False        0.02

The exact values depend on the generated datasets.

------------------------------------------------------------------------

## Module Responsibilities

  -----------------------------------------------------------------------
  File                                Responsibility
  ----------------------------------- -----------------------------------
  `prepare_data.py`                   Loads the raw dataset and creates
                                      reference and simulated production
                                      datasets

  `loader.py`                         Provides CSV loading functionality

  `ks_test.py`                        Runs the two-sample KS test

  `psi.py`                            Calculates PSI

  `detector.py`                       Runs drift detection across all
                                      monitored features

  `report.py`                         Creates and saves the drift report

  `run_monitoring.py`                 Main monitoring pipeline

  `app.py`                            Streamlit dashboard
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## Design Philosophy

The project keeps the monitoring components separate so that each
responsibility has its own module.

``` text
Data Preparation
      |
      v
Data Loading
      |
      v
Drift Detection
      |
      +---- KS Test
      |
      +---- PSI
      |
      v
Reporting
      |
      v
Dashboard
```

This makes the system easier to understand, test, maintain, and extend.

------------------------------------------------------------------------

## Current Scope

The current implementation focuses on **data drift**.

Data drift answers:

> "Has the distribution of the input data changed compared with the
> reference data?"

It does not yet establish that model performance has degraded.

A future monitoring system can additionally include:

-   Prediction drift
-   Model performance monitoring
-   Accuracy
-   Precision
-   Recall
-   ROC-AUC
-   Historical drift trends
-   Automated alerts
-   Model retraining triggers

------------------------------------------------------------------------

## Why This Project Matters

In a real machine learning system, training a model is only one part of
the lifecycle.

After deployment, the data distribution can change.

A monitoring system helps identify these changes early so that the team
can investigate whether the model needs attention, recalibration, or
retraining.

This project demonstrates the basic architecture of an ML monitoring
pipeline:

``` text
Data
  ↓
Reference Baseline
  ↓
Production Monitoring
  ↓
Statistical Tests
  ↓
Drift Report
  ↓
Dashboard
```

------------------------------------------------------------------------

## Tech Stack

-   **Python**
-   **Pandas**
-   **NumPy**
-   **SciPy**
-   **Streamlit**
-   **uv**
-   **Statistical drift detection**

------------------------------------------------------------------------

## Author

Built as an ML engineering / machine learning monitoring project focused
on understanding model lifecycle monitoring and data drift detection.
