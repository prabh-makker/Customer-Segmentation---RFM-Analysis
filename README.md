# Customer Segmentation - RFM Analysis

**Production-Ready E-Commerce Customer Segmentation using RFM (Recency, Frequency, Monetary) Analysis**

## 📊 Project Overview

This project implements a complete RFM analysis pipeline for customer segmentation. The data is ready for Power BI dashboard creation to drive business decisions on customer retention and revenue optimization.

### Key Metrics
- **Total Customers**: 1,960
- **Total Revenue**: ₹9,820,510
- **Average Customer Lifetime Value**: ₹5,010
- **Date Range**: 2023-01-01 to 2024-12-31

## 📋 Customer Segments

| Segment | Count | % of Base | Revenue | Avg Value | Action |
|---------|-------|----------|---------|-----------|--------|
| **Champions** | 293 | 14.9% | ₹2.6M | ₹8,928 | Reward loyalty, upsell premium |
| **Loyal Customers** | 176 | 9.0% | ₹915K | ₹5,202 | Personalized offers |
| **Potential Loyalists** | 359 | 18.3% | ₹2.0M | ₹5,676 | Engagement programs |
| **Recent Customers** | 234 | 11.9% | ₹744K | ₹3,179 | First purchase follow-up |
| **At Risk** | 189 | 9.6% | ₹1.3M | ₹6,913 | Win-back campaigns |
| **Can't Lose Them** | 159 | 8.1% | ₹724K | ₹4,556 | Immediate intervention |
| **Lost** | 272 | 13.9% | ₹635K | ₹2,333 | Re-engagement offers |

## 🛠️ Tech Stack

- **Python 3.x**: Data processing & RFM calculation
- **Pandas & NumPy**: Data manipulation
- **Power BI**: Interactive dashboard & visualization

## 📁 Project Structure

```
C/
├── rfm_analysis.py          # Main RFM calculation script
├── requirements.txt         # Python dependencies
├── data/
│   └── rfm_segmentation.csv # Ready for Power BI (1,960 customers)
└── README.md               # This file
```

## 🚀 How to Use

### 1. Generate Fresh Data
```bash
python3 rfm_analysis.py
```
This will:
- Generate realistic e-commerce transaction data
- Clean and validate the data
- Calculate RFM metrics for each customer
- Segment customers into 7 business-driven categories
- Export `data/rfm_segmentation.csv`

### 2. Connect to Power BI

**Step 1**: Open Power BI Desktop  
**Step 2**: Get Data → Text/CSV  
**Step 3**: Select `data/rfm_segmentation.csv`  
**Step 4**: Load the data

### 3. Power BI Dashboard Recommendations

#### Key Visuals to Build:

1. **Customer Segment Distribution**
   - Card visuals for each segment count & revenue
   - Pie chart: % of customers by segment

2. **RFM Score Matrix**
   - Scatter plot: Frequency vs Monetary (color by Recency)
   - Heatmap: R×F×M scores

3. **Revenue Analysis**
   - Bar chart: Revenue by segment
   - Gauge: Revenue vs target by segment

4. **Customer Health Metrics**
   - KPI cards: Total customers, avg lifetime value, churn rate
   - Trend: Segment size over time (if historical data available)

5. **Slicers**
   - Segment dropdown
   - Customer ID search
   - RFM Score range

## 📊 CSV Columns Explained

| Column | Description |
|--------|-------------|
| `customer_id` | Unique customer identifier |
| `recency` | Days since last purchase (0=most recent) |
| `frequency` | Total number of purchases |
| `monetary` | Total amount spent (₹) |
| `R_score` | Recency score (1-5, 5=best) |
| `F_score` | Frequency score (1-5, 5=best) |
| `M_score` | Monetary score (1-5, 5=best) |
| `rfm_score` | Average of R, F, M scores |
| `rfm_segment_code` | Numeric segment code (e.g., "555") |
| `segment` | Business segment name |
| `customer_value` | Avg transaction value (₹) |
| `days_since_purchase` | Same as recency |

## 🎯 Business Insights & Recommendations

### Immediate Actions by Segment

**Champions (14.9% of base, 26.6% of revenue)**
- Highest value customers
- Focus: Retention & upselling
- Tactics: VIP programs, early access to new products

**At Risk (9.6% of base, 13.3% of revenue)**
- High lifetime value but haven't purchased recently
- Focus: Win-back campaigns
- Tactics: Personalized discounts, "We miss you" emails

**Lost (13.9% of base, 6.5% of revenue)**
- Haven't purchased in long time
- Focus: Re-engagement
- Tactics: Seasonal offers, product recommendations

**Recent Customers (11.9% of base, 7.6% of revenue)**
- New but not yet loyal
- Focus: Convert to repeat buyers
- Tactics: Cross-sell, loyalty rewards introduction

## 📈 RFM Segmentation Logic

```
Champions        → R≥4, F≥4, M≥4
Loyal Customers  → R≥4, F≥3, M≥3
Potential        → R≥3, F≥3
Recent           → R≥4, F≤2
At Risk          → R≤2, F≥4
Can't Lose       → R≤2, F≥3
Lost             → R≤1
```

## 🔧 Customization

Edit `rfm_analysis.py` to:
- Change customer/transaction count: `generate_realistic_data(n_customers=2000, n_transactions=8000)`
- Adjust segment thresholds in `segment_customers()` function
- Modify RFM scoring logic in `score_rfm()` function

## 📄 Data Generation

The dataset is synthetically generated with:
- ✅ Realistic purchase patterns (power-law distribution)
- ✅ 2-year historical data (2023-2024)
- ✅ Multiple product categories
- ✅ Varied customer purchase frequencies & amounts
- ✅ No personally identifiable information

Perfect for portfolio demonstrations and business case studies.

---

**Ready for Power BI!** 🚀 Import `rfm_segmentation.csv` and start building your dashboard.
