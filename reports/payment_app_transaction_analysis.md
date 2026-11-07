# Payment App × Transaction Type Analysis

## Objective
Identify payment app and transaction type combinations with elevated
payment failure rates.

## Data
This analysis uses a synthetic transaction dataset for a portfolio
project. It is not actual Razorpay internal data.

## Method
- Group transactions by payment app and transaction type.
- Calculate attempt counts, successful attempts, failed attempts,
  pending attempts, failure rate, success rate, and average amount.
- Include only combinations with at least 50 attempts.
- Rank combinations by failure rate.

## Key Findings

| Payment App | Transaction Type | Attempts | Failed | Failure Rate |
|---|---|---:|---:|---:|
| PhonePe | Bill Payment | 875 | 114 | 13.03% |
| Amazon Pay | EMI | 135 | 17 | 12.59% |
| Paytm | Recharge | 375 | 41 | 10.93% |
| PhonePe | P2M | 2,090 | 219 | 10.48% |
| WhatsApp Pay | Bill Payment | 118 | 12 | 10.17% |

## Business Interpretation
PhonePe + Bill Payment has the highest failure rate among the listed
combinations. PhonePe + P2M has a larger absolute number of failures,
making it another important area for investigation.

## Recommended Follow-up
1. Investigate failure reasons and payment status transitions.
2. Compare failure rates by hour, device type, and user city tier.
3. Check whether the observed patterns persist across time periods.
4. Avoid attributing failures to a payment app without supporting
   evidence about the underlying causes.

## Limitations
These findings are descriptive and based on synthetic data. They do
not establish causation or represent actual Razorpay performance.
