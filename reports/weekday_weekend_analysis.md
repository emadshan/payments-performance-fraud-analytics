# Weekday vs Weekend Payment Analysis

## Objective
Compare payment outcomes between weekdays and weekends.

## Data
Synthetic transaction dataset for a portfolio project; not actual Razorpay internal data.

## Results

| Metric | Weekday | Weekend |
|---|---:|---:|
| Total attempts | 14,372 | 5,628 |
| Successful attempts | 12,678 | 4,950 |
| Failed attempts | 1,304 | 511 |
| Pending attempts | 390 | 167 |
| Failure rate | 9.07% | 9.08% |
| Success rate | 88.21% | 87.95% |

## Business Interpretation
The weekday failure rate is 9.07%, compared with 9.08% on weekends. The difference is only 0.01 percentage points after rounding, so day category alone appears to offer little descriptive separation in this dataset.

Weekdays have more failed attempts in absolute terms because they have a much higher transaction volume.

## Recommended Follow-up
Investigate payment app, transaction type, hour of day, and underlying failure reasons rather than relying on weekday/weekend status alone.

## Limitations
These are descriptive findings from synthetic data. No causal conclusion or claim about actual Razorpay performance is supported.
