# Razorpay Payments Intelligence & Business Optimization
## Executive Business Analysis Report

**Role:** Business Analyst — Portfolio Project  
**Data:** Synthetic payment transaction dataset  
**Period:** January–December 2024  
**Status:** Exploratory analysis; not actual Razorpay internal data

---

## 1. Executive Summary

This project analyzes 20,000 synthetic payment transactions to identify payment performance patterns, investigate failure rates, and evaluate an exploratory fraud-detection model.

The SQL analysis examines performance by transaction type, payment app, app–transaction-type combination, hour of day, and weekday versus weekend. A separate machine-learning workflow evaluates fraud-labelled transactions.

The analysis identifies specific areas for further investigation, but the synthetic dataset does not establish actual Razorpay performance or the causes of payment failures.

## 2. Dataset Overview

- Total transactions: 20,000
- Date range: 1 January 2024 to 30 December 2024
- Successful transactions: 17,628 (88.14%)
- Failed transactions: 1,815 (9.08%)
- Pending transactions: 557 (2.79%)
- Fraud-labelled transactions: 763 (3.82%)

Percentages may not sum to exactly 100% because of rounding.

## 3. Payment Performance

### By transaction type

| Transaction Type | Attempts | Failed | Failure Rate |
|---|---:|---:|---:|
| Bill Payment | 3,033 | 306 | 10.09% |
| Recharge | 2,063 | 191 | 9.26% |
| P2M | 7,014 | 646 | 9.21% |
| P2P | 4,881 | 435 | 8.91% |
| EMI | 1,628 | 130 | 7.99% |
| Subscription | 1,381 | 107 | 7.75% |

Bill Payment has the highest failure rate, while P2M has the highest transaction volume and the highest number of failed attempts.

### By payment app

| Payment App | Attempts | Failed | Failure Rate |
|---|---:|---:|---:|
| PhonePe | 5,864 | 582 | 9.92% |
| GPay | 6,438 | 593 | 9.21% |
| Paytm | 3,738 | 330 | 8.83% |
| Amazon Pay | 1,584 | 135 | 8.52% |
| BHIM | 1,595 | 120 | 7.52% |
| WhatsApp Pay | 781 | 55 | 7.04% |

PhonePe has the highest app-level failure rate. GPay has the highest number of failures, reflecting its larger transaction volume.

### App and transaction-type combinations

| Payment App | Transaction Type | Attempts | Failed | Failure Rate |
|---|---|---:|---:|---:|
| PhonePe | Bill Payment | 875 | 114 | 13.03% |
| Amazon Pay | EMI | 135 | 17 | 12.59% |
| Paytm | Recharge | 375 | 41 | 10.93% |
| PhonePe | P2M | 2,090 | 219 | 10.48% |
| WhatsApp Pay | Bill Payment | 118 | 12 | 10.17% |

PhonePe + Bill Payment is a priority for investigation because it has the highest failure rate among these combinations. PhonePe + P2M also merits attention because of its higher absolute failure count.

## 4. Time-Based Analysis

### Hour of day

- Highest observed failure rate: 18:00, at 10.88% (93 failures from 855 attempts).
- Lowest observed failure rate: 14:00, at 7.10% (66 failures from 929 attempts).
- Difference: 3.78 percentage points.

These results identify periods worth investigating. They do not demonstrate that system load or peak-hour traffic causes failures.

### Weekday versus weekend

| Metric | Weekday | Weekend |
|---|---:|---:|
| Attempts | 14,372 | 5,628 |
| Failed attempts | 1,304 | 511 |
| Failure rate | 9.07% | 9.08% |
| Success rate | 88.21% | 87.95% |

Failure rates are nearly identical. Day category alone does not meaningfully distinguish failure outcomes in this dataset.

## 5. Fraud Model Evaluation

The exploratory logistic regression model uses a class-weighted pipeline and a threshold of 0.50. The final evaluation uses a held-out test set of 4,000 rows.

| Metric | Held-out test result |
|---|---:|
| PR-AUC | 0.0839 |
| ROC-AUC | 0.7181 |
| Precision | 7.86% |
| Recall | 59.48% |
| F1-score | 0.1388 |
| True positives | 91 |
| False positives | 1,067 |
| False negatives | 62 |
| True negatives | 2,780 |

At this threshold, the model identifies 91 of 153 fraud-labelled test cases, misses 62, and flags 1,067 non-fraud-labelled transactions.

The low precision means that only about 8 in every 100 flagged transactions are fraud-labelled. The model is not production-ready.

Feature provenance and the process used to generate fraud labels remain unverified. The results are exploratory and cannot establish real-world fraud-detection effectiveness.

## 6. Business Recommendations

1. **Investigate Bill Payment failures.** Examine failure reasons, payment status transitions, and relevant provider responses.
2. **Prioritize high-volume problem areas.** Review P2M and PhonePe + P2M because they account for many failed attempts.
3. **Investigate app–transaction combinations.** Compare underlying failure codes before recommending app-specific interventions.
4. **Examine hourly patterns.** Compare failure rates across dates, apps, and transaction types before drawing operational conclusions.
5. **Improve fraud-label governance.** Verify label-generation logic, feature timing, and possible target leakage before further model development.
6. **Define an operational threshold only with business costs.** Fraud review capacity, false-positive costs, and missed-fraud costs should inform any future threshold choice.

## 7. Limitations

- All transaction data is synthetic and does not represent actual Razorpay internal performance.
- Observed associations do not establish causation.
- Fraud-label validity and feature provenance have not been established.
- Fraud-model precision is low and requires further investigation.
- Findings should be validated on reliable, appropriately governed data before operational use.

## 8. Project Deliverables

- PostgreSQL analysis views and SQL scripts.
- Payment performance and time-based analysis reports.
- Fraud baseline, threshold analysis, and held-out test evaluation.
- A foundation for a Power BI dashboard and a reproducible GitHub portfolio project.

---

**Conclusion:** The project demonstrates SQL-based KPI analysis, data investigation, exploratory machine learning, and business-oriented recommendations. The findings are intended for portfolio demonstration and further investigation, not production decision-making.
