# Hourly Payment Performance Analysis

## Objective
Identify variation in payment outcomes across the 24 hours of the day.

## Data
Synthetic transaction dataset for a portfolio project. This is not actual Razorpay internal data.

## Method
Transactions were grouped by hour of day. Attempt counts, successful attempts, failed attempts, pending attempts, failure rates, and success rates were calculated.

## Key Findings

| Hour | Total Attempts | Failed Attempts | Failure Rate |
|---|---:|---:|---:|
| 18:00 | 855 | 93 | 10.88% |
| 05:00 | 812 | 85 | 10.47% |
| 03:00 | 831 | 86 | 10.35% |
| 23:00 | 806 | 83 | 10.30% |
| 22:00 | 812 | 83 | 10.22% |
| 14:00 | 929 | 66 | 7.10% |

## Business Interpretation
The 18:00 hour has the highest observed failure rate (10.88%) and the highest failed-attempt count (93). The 14:00 hour has the lowest observed failure rate (7.10%).

The difference between the highest and lowest hourly failure rates is 3.78 percentage points.

## Recommended Follow-up
1. Compare hourly failure patterns by payment app and transaction type.
2. Investigate underlying failure reasons and payment-provider responses.
3. Check whether the pattern persists across dates and days of the week.
4. Avoid attributing the observed pattern to system load without supporting evidence.

## Limitations
These are descriptive results from synthetic data. Hourly associations do not establish causation or represent actual Razorpay performance.
