# Razorpay Payments Intelligence \& Business Optimization

## Fraud Detection Model — Baseline Evaluation

### 1\. Project Context

This project uses synthetic payment transaction data to demonstrate
business analysis and fraud detection workflows. The data is not actual
Razorpay internal data, and the results must not be interpreted as
Razorpay's real-world performance.

### 2\. Dataset Summary

* Total transactions: 20,000
* Fraud-labelled transactions: 763
* Non-fraud-labelled transactions: 19,237
* Fraud-label prevalence: 3.815%
* Evaluation method: Stratified 75/25 train-test split
* Model: Logistic Regression with class\_weight="balanced"
* Decision threshold: 0.50 (50%)

### 3\. Test-Set Results

* Test transactions: 5,000
* ROC-AUC: 0.7305
* PR-AUC / Average Precision: 0.0925
* Precision at 50% threshold: 8.13%
* Recall at 50% threshold: 61.78%

### 4\. Confusion Matrix

|Actual / Predicted|Non-fraud|Fraud|
|-|-:|-:|
|Non-fraud-labelled|3,476|1,333|
|Fraud-labelled|73|118|

### 5\. Business Interpretation

At the selected 50% probability threshold, the model identified 118 of
191 fraud-labelled test transactions and missed 73. It also flagged
1,333 non-fraud-labelled transactions.

The 8.13% precision indicates that many flagged transactions would
require review without ultimately matching the dataset's fraud label.
The 61.78% recall indicates that the model identified approximately
62% of fraud-labelled test transactions.

The majority-class baseline achieved 96.18% accuracy but zero fraud
recall, demonstrating why accuracy alone is inadequate for this
imbalanced classification problem.

### 6\. Data Quality and Limitations

* Fraud labels matched across the two source CSV files with zero
mismatches across 20,000 transaction IDs.
* Five fraud-related features were identical across both source files.
* The original method used to generate synthetic fraud labels and
indicators has not yet been verified.
* Potential feature leakage has not been ruled out.
* Results are based on a single random stratified split.
* The 50% threshold is a baseline choice, not a proven optimal
operational threshold.
* These results do not establish production readiness or real-world
fraud prevention capability.

### 7\. Recommended Next Steps

1. Document feature provenance and investigate potential leakage.
2. Establish a validation set for model and threshold decisions.
3. Evaluate alert volume and precision-recall trade-offs.
4. Complete SQL-based payment performance analysis.
5. Build a Power BI dashboard and summarize business recommendations.

### 8\. Reproducibility

Baseline model script: src/train\_fraud\_baseline.py
Processed dataset: data/processed/transactions\_enriched.csv

Threshold used for this baseline: 0.50.

## 9\. Feature Provenance Investigation

The project scripts were searched for fraud-label and feature-generation
logic. No label-generation code was identified in the inspected scripts.

The transactions.csv and fraud\_labels.csv files contain matching values
for the following fields across all 20,000 matched transaction IDs:

* new\_device\_flag
* ip\_location\_mismatch
* failed\_attempts\_last\_24h
* transaction\_velocity
* amount\_deviation\_score
* is\_fraud

These checks establish consistency between the source files but do not
establish how the synthetic fraud labels were originally assigned.

### Outstanding Risk

The original dataset-generation method and the timing of feature
calculation remain unverified. Potential target leakage therefore
cannot be ruled out. The baseline metrics should be treated as
exploratory results on synthetic data, not evidence of production
fraud-detection capability.

## 10\. Three-Way Evaluation — Validation Results

### Data Split

* Training set: 12,000 transactions
* Validation set: 4,000 transactions
* Reserved test set: 4,000 transactions
* Random state: 42
* Split strategy: Stratified
* Threshold: 0.50 (50%)

### Validation Metrics

* PR-AUC / Average Precision: 0.1083
* ROC-AUC: 0.7416
* Precision: 8.00%
* Recall: 64.47%

### Validation Confusion Matrix

|Actual / Predicted|Non-fraud|Fraud|
|-|-:|-:|
|Non-fraud-labelled|2,721|1,127|
|Fraud-labelled|54|98|

### Interpretation

At the fixed 50% threshold, the model identified 98 of 152
fraud-labelled validation transactions and missed 54. It also flagged
1,127 non-fraud-labelled transactions.

The validation PR-AUC of 0.1083 is above the fraud-label prevalence
of approximately 3.8%, but the low precision indicates a substantial
potential alert-review burden.

The test set remains reserved for final evaluation. These results are
based on synthetic data, and feature provenance and potential leakage
remain unresolved. They should not be interpreted as production
performance.

This evaluation uses a different split from the original 75/25
baseline; the two sets of metrics should not be compared as if they
were measured on the same test transactions.



11\. Fraud Label and Feature Overlap Audit

Findings



\- `transactions.csv`: 20,000 rows and 20,000 unique transaction IDs.

\- `fraud\_labels.csv`: 20,000 rows and 20,000 unique transaction IDs.

\- All 20,000 transaction IDs matched across the two files.

\- No unmatched transaction IDs were found.

\- Zero mismatches were found for `is\_fraud`, `new\_device\_flag`, `ip\_location\_mismatch`, `failed\_attempts\_last\_24h`, `transaction\_velocity`, and `amount\_deviation\_score`.



Interpretation and Limitations



The audit establishes exact consistency between the transaction and fraud-label files for the fields compared. It does not establish the validity of the fraud labels, the causal direction between features and labels, feature availability at decision time, or the absence of target leakage.



The original fraud-label-generation method and feature-generation timing remain unverified. The dataset is synthetic and must not be presented as actual Razorpay internal data or as evidence of production fraud-detection performance.

