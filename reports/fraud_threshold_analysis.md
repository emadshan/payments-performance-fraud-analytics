# Fraud Detection Threshold Analysis

## Scope and methodology

* Dataset: synthetic transaction data; not actual Razorpay internal data.
* Model: class-weighted logistic regression with the same feature pipeline as the validation baseline.
* Training set: 60% of the full dataset.
* Validation set: 20% of the full dataset.
* Reserved test set: 20%; not used for fitting, threshold selection, or evaluation.
* Thresholds compared: 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80.
* The 0.50 threshold remains the baseline; no final threshold is selected automatically.

## Validation metrics

* Validation PR-AUC: 0.1083
* Validation ROC-AUC: 0.7416
* Validation fraud-labelled rows: 152 of 4,000

|Threshold|Precision|Recall|F1|TP|FP|FN|TN|Alerts|
|-:|-:|-:|-:|-:|-:|-:|-:|-:|
|0.20|0.0412|0.9934|0.0792|151|3510|1|338|3661|
|0.30|0.0529|0.9276|0.1001|141|2524|11|1324|2665|
|0.40|0.0666|0.8026|0.1230|122|1709|30|2139|1831|
|0.50|0.0800|0.6447|0.1423|98|1127|54|2721|1225|
|0.60|0.0930|0.4868|0.1561|74|722|78|3126|796|
|0.70|0.1185|0.3421|0.1760|52|387|100|3461|439|
|0.80|0.1436|0.1908|0.1638|29|173|123|3675|202|

## Baseline threshold (0.50)

* Precision: 0.0800
* Recall: 0.6447
* F1: 0.1423
* True positives: 98
* False positives: 1127
* False negatives: 54
* Total alerts: 1225

## Interpretation cautions

Lower thresholds typically increase the number of alerts and may catch more fraud-labelled cases, but can increase false positives. Higher thresholds typically reduce alerts but may miss more fraud-labelled cases. Use the measured results above rather than assuming these effects for any particular threshold.

Threshold choice should reflect review capacity and the relative costs of missed fraud versus false alerts. These results do not establish production performance: the dataset is synthetic and label-generation methodology, feature timing, and potential target leakage remain unresolved.

The reserved test set must remain untouched until the threshold and evaluation approach have been finalized.



Business Implications and Operational Trade-offs



Alert Review Workload



At the baseline threshold of 0.50, the model generated 1,225 alerts across 4,000 validation transactions. Of these, 98 were fraud-labelled true positives and 1,127 were non-fraud-labelled false positives. The resulting precision of 8.00% indicates a substantial alert-review burden.



Threshold Trade-off



Increasing the threshold to 0.70 reduced the alert count to 439 and improved precision to 11.85%. However, recall fell to 34.21%, meaning that 100 of the 152 fraud-labelled validation cases were missed. This illustrates the trade-off between reducing review workload and detecting more positive cases.



Recommended Decision



Retain 0.50 as the baseline for comparison. Do not designate an operational threshold until review capacity, the relative costs of false positives and false negatives, and appropriate validation criteria have been established. Any threshold selection must be completed using validation data before the reserved test set is evaluated once for final assessment.



Limitations



The dataset is synthetic and is not actual Razorpay internal data. Fraud-label validity, feature-generation timing, and potential target leakage remain unresolved. These metrics are exploratory and do not establish production effectiveness.


