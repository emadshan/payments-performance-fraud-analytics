\# Payments Performance \& Fraud Analytics



An end-to-end data analytics portfolio project exploring payment performance, transaction failures, and fraud detection using SQL, PostgreSQL, Python, and Scikit-learn.



> \*\*Project note:\*\* This is an independent portfolio project using synthetic payment data. It is not affiliated with or based on confidential internal data from Razorpay.



\## Project Overview



The project analyses 20,000 payment transactions to understand payment performance, identify failure-prone segments, investigate transaction patterns, and develop a baseline fraud-detection model.



The analysis combines SQL-based business intelligence with Python-based data quality checks, feature engineering, and machine learning evaluation.



\## Tools \& Technologies



\- \*\*Database:\*\* PostgreSQL

\- \*\*Programming:\*\* Python

\- \*\*Libraries:\*\* Pandas, NumPy, Scikit-learn, Matplotlib

\- \*\*Analytics:\*\* SQL, exploratory data analysis, KPI analysis

\- \*\*Machine Learning:\*\* Logistic Regression, classification metrics, threshold analysis

\- \*\*Version Control:\*\* Git and GitHub



\## Key Business Findings



| Metric | Result |

|---|---:|

| Total payment attempts | 20,000 |

| Successful transactions | 17,628 |

| Failed transactions | 1,815 |

| Pending transactions | 557 |

| Overall success rate | 88.14% |

| Overall failure rate | 9.08% |



\### Payment Failure Analysis



\- Bill Payment recorded a failure rate of approximately 10.09%.

\- PhonePe Bill Payment transactions recorded a 13.03% failure rate.

\- This segment had 114 failed attempts, representing approximately ₹1.09 lakh in failed transaction value out of ₹7.77 lakh in attempted value.



These figures represent transaction values, not confirmed revenue losses.



\## Fraud Detection Model



A Logistic Regression baseline was evaluated on a held-out test dataset.



| Evaluation Metric | Result |

|---|---:|

| ROC-AUC | 0.7181 |

| PR-AUC | 0.0839 |

| Precision | 7.86% |

| Recall | 59.48% |

| F1-score | 0.1388 |



Threshold analysis examined the trade-off between precision and recall.



\*\*Model limitation:\*\* The model has relatively low precision, and fraud-label and feature provenance require further validation. It is an experimental baseline and is not suitable for production deployment.



\## Business Recommendations



\- Investigate failure patterns in Bill Payment transactions.

\- Examine payment-app and transaction-type combinations with elevated failure rates.

\- Monitor payment performance across different time periods.

\- Further validate fraud labels and features before operationalising fraud detection.



\## Project Structure



\- `data/` — Raw and processed datasets (excluded from public repository).

\- `reports/` — Business analysis and model evaluation reports.

\- `sql/` — PostgreSQL queries and KPI analysis.

\- `src/` — Python scripts for auditing, feature engineering and modelling.

\- `notebooks/` — Exploratory analysis notebooks.

\- `dashboard/` — Power BI dashboard files.



\## Project Status



\- \[x] Data auditing and quality checks

\- \[x] SQL payment performance analysis

\- \[x] Transaction feature investigation and reconstruction

\- \[x] Fraud detection baseline

\- \[x] Model evaluation and threshold analysis

\- \[x] Business analysis reports

\- \[ ] Complete Power BI dashboard

\- \[ ] Dashboard screenshots and documentation



\## Disclaimer



All data used in this project is intended for portfolio and educational purposes. Findings are based on the synthetic dataset and should not be interpreted as actual payment processor performance or real-world fraud statistics.

