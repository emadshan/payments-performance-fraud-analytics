# Fraud Model — Final Held-Out Test Evaluation

## Evaluation protocol

- Dataset: synthetic transaction data, not actual Razorpay internal data.
- Model: class-weighted Logistic Regression.
- Random state: 42.
- Split: 60% training, 20% validation, 20% held-out test.
- Threshold: 0.50, fixed before final test evaluation.
- The model was fitted on training data only.
- The reserved test set was evaluated once for this report.

## Final test metrics

| Metric | Result |
|---|---:|
| Test rows | 4,000 |
| Fraud-labelled test rows | 153 |
| Test fraud prevalence | 3.82% |
| Threshold | 0.50 |
| PR-AUC | 0.0839 |
| ROC-AUC | 0.7181 |
| Precision | 0.0786 |
| Recall | 0.5948 |
| F1 | 0.1388 |

## Confusion matrix

| Actual / Predicted | Non-fraud | Fraud |
|---|---:|---:|
| Non-fraud-labelled | 2780 | 1067 |
| Fraud-labelled | 62 | 91 |

## Interpretation cautions

These results estimate performance on a held-out portion of the supplied synthetic dataset. They do not establish performance on real Razorpay transactions or production fraud patterns.

The original fraud-label-generation method, feature-generation timing, and potential target leakage remain unresolved. Results should therefore be treated as exploratory rather than production evidence.

The threshold was not selected using test results. No threshold comparison was performed on the test set.

