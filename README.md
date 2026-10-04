# Customer Segmentation - RFM Analysis

Python builds RFM scores and 8 customer segments from synthetic e-commerce transactions. A 2-page Power BI dashboard reads the result.

![Page 1](screenshots/page1-where-your-customers-stand.jpg)
![Page 2](screenshots/page2-insights-actions.jpg)

## Files

| File | What |
|---|---|
| `rfm_analysis.py` | Generates transactions, scores R/F/M (1-5), assigns segments, writes the CSV |
| `data/rfm_segmentation.csv` | 1,960 customers, 14 columns |
| `RFM_Customer_Segmentation_Dashboard.pbix` | The dashboard |
| `screenshots/` | Both dashboard pages |

## Run

```bash
pip install -r requirements.txt
python rfm_analysis.py
```

Then open the `.pbix`. It points at the CSV by absolute path, so repoint it once: Home > Transform data > Data source settings > Change source.

## Segments

Champions, Loyal Customers, Potential Loyalists, Recent Customers, Need Attention, At Risk, Cant Lose Them, Lost.

## Dashboard

**Page 1, Where Your Customers Stand:** 4 KPI cards (customers, active %, avg lifetime value, revenue), customers / revenue / avg value by segment, segment table, key insights.

**Page 2, The Insights & Actions:** segment slicer, customers by recency band / purchases / avg value, R x F heatmap, scorecard (priority action, health score, status, trend), 4 segment cards, monetary band charts.

## Key measures

```
Active Customer % = DIVIDE(CALCULATE(COUNTROWS(rfm_segmentation),
    NOT(rfm_segmentation[segment] IN {"At Risk", "Cant Lose Them", "Lost"})),
    COUNTROWS(rfm_segmentation))

Health Score = ROUND(AVERAGEX(rfm_segmentation, VALUE(rfm_segmentation[rfm_score])) / 5 * 10, 1)

Health Status = SWITCH(TRUE(), [Health Score] >= 7, "Healthy", [Health Score] >= 5, "Watch", "Critical")

Trend = (2024 revenue - 2023 revenue) / 2023 revenue, from revenue_2023 and revenue_2024
```

"Active" excludes the three at-risk segments because every customer in the data is at least 366 days since last purchase, so a recency cutoff would match nobody.

Data is synthetic (fixed seed 42).
