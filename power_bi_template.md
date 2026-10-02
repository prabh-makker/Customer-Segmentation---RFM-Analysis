# Power BI Dashboard Template - RFM Segmentation

## 📋 Dashboard Overview
**Name:** Customer Segmentation - RFM Analysis  
**Data Source:** `rfm_segmentation.csv`  
**Refresh:** Manual or Daily (recommended)

---

## 📊 Page 1: Executive Summary

### Visual 1: KPI Cards (Top Row)
```
┌─────────────┬──────────────┬──────────────┬─────────────┐
│   Total     │    Total     │    Avg CLV   │  Churn Rate │
│ Customers   │  Revenue     │              │             │
│    1,960    │  ₹9.8M       │   ₹5,010    │    13.9%    │
└─────────────┴──────────────┴──────────────┴─────────────┘
```

**Measures to Create in Power BI:**

```dax
Total Customers = COUNTA(rfm_segmentation[customer_id])

Total Revenue = SUM(rfm_segmentation[monetary])

Avg Customer Lifetime Value = AVERAGE(rfm_segmentation[monetary])

Churn Rate % = 
  DIVIDE(
    COUNTIF(rfm_segmentation[segment], "Lost"),
    COUNTA(rfm_segmentation[customer_id]),
    0
  ) * 100
```

### Visual 2: Customer Segments Distribution (Pie Chart)
- **Field:** segment (Categories)
- **Values:** COUNT of customer_id
- **Colors:** 
  - Champions: #2E7D32 (Green)
  - Loyal: #1976D2 (Blue)
  - Potential: #F57C00 (Orange)
  - Recent: #C62828 (Red)
  - At Risk: #D32F2F (Dark Red)
  - Can't Lose: #FF6F00 (Orange-Red)
  - Lost: #757575 (Gray)

### Visual 3: Revenue by Segment (Column Chart)
- **X-Axis:** Segment
- **Y-Axis:** SUM(monetary)
- **Data Label:** Show values
- **Sort:** By revenue descending

### Visual 4: Customer Count by Segment (Bar Chart)
- **X-Axis:** COUNT of customer_id
- **Y-Axis:** Segment
- **Format:** Show percentages

---

## 📈 Page 2: RFM Deep Dive

### Visual 1: RFM Segment Code Heatmap
Create a matrix visual:
- **Rows:** R_score (1-5)
- **Columns:** F_score (1-5)
- **Values:** COUNT of customer_id
- **Color Scale:** Green (high) → Red (low)
- **Data Labels:** Show counts

### Visual 2: Monetary Distribution by Segment (Box Plot Alternative)
Use Scatter chart:
- **X-Axis:** Segment
- **Y-Axis:** monetary
- **Size:** frequency
- **Legend:** R_score

### Visual 3: Recency vs Frequency Scatter
- **X-Axis:** recency (days since purchase)
- **Y-Axis:** frequency (purchase count)
- **Bubble Size:** monetary
- **Color:** segment
- **Tooltip:** customer_id, rfm_score

### Visual 4: Customer Value Distribution (Histogram)
- **X-Axis:** customer_value (binned, 0-10000 range)
- **Y-Axis:** COUNT of customer_id
- **Color:** segment

---

## 🎯 Page 3: Segment Analysis & Actions

### Visual 1: Segment Performance Card Matrix
Create 7 cards (one per segment) with:
```
╔════════════════════════════════╗
║       CHAMPIONS                ║
║  Customers: 293 (14.9%)        ║
║  Revenue: ₹2.6M (26.6%)        ║
║  Avg Value: ₹8,928             ║
║  Recency: 150 days             ║
║  Freq: 6.5 purchases           ║
║                                ║
║  ACTION: Reward loyalty        ║
║  📌 VIP Program                ║
║  📌 Early access               ║
║  📌 Personalized offers        ║
╚════════════════════════════════╝
```

Repeat for each segment with specific KPIs and actions.

### Visual 2: Segment Trends (Table)
Create detailed table with columns:
- Segment
- Customer Count
- % of Base
- Total Revenue
- Avg Lifetime Value
- Avg Recency (days)
- Avg Frequency
- Avg Monetary
- Recommended Action

### Visual 3: At-Risk Customers Alert
Filter: segment = "At Risk" OR segment = "Can't Lose Them"
Columns:
- customer_id
- monetary (sorted descending)
- recency
- frequency
- segment
- rfm_score

---

## 🔧 Page 4: Data Dictionary & Filters

### Slicers (All Pages)

**Slicer 1: Segment Filter**
- Field: segment
- Type: Buttons or Dropdown
- Multi-select: ON

**Slicer 2: RFM Score Range**
- Field: rfm_score (binned: 1-2, 2-3, 3-4, 4-5)
- Type: Slider

**Slicer 3: Monetary Range**
- Field: monetary (binned: 0-2000, 2000-5000, 5000-10000, 10000+)
- Type: Buttons

### Data Dictionary Table
```
Column Name          | Description
─────────────────────┼──────────────────────────────
customer_id          | Unique customer identifier
recency              | Days since last purchase
frequency            | Total number of purchases
monetary             | Total amount spent (₹)
R_score              | Recency score (1-5)
F_score              | Frequency score (1-5)
M_score              | Monetary score (1-5)
rfm_score            | Average of R, F, M
segment              | Customer segment name
customer_value       | Avg transaction value
```

---

## 🎨 Design Specifications

### Color Palette
```
Champions:        #2E7D32 (Dark Green)
Loyal:            #1976D2 (Blue)
Potential:        #F57C00 (Orange)
Recent:           #C62828 (Red)
At Risk:          #D32F2F (Dark Red)
Can't Lose:       #FF6F00 (Orange-Red)
Lost:             #757575 (Gray)

Background:       #F5F5F5 (Light Gray)
Accent:           #1976D2 (Primary Blue)
Text:             #333333 (Dark Gray)
```

### Typography
- **Title:** 28px, Bold, #1976D2
- **Subtitle:** 16px, Regular, #666666
- **Labels:** 12px, Regular, #333333
- **Values:** 14px, Bold, #1976D2

---

## 📋 Step-by-Step Setup Instructions

### Step 1: Import Data
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Select `rfm_segmentation.csv`
4. Click Load

### Step 2: Create Measures
In Power BI, go to Model → New Measure and paste each DAX formula

### Step 3: Create Visuals
For each visual, follow the specifications above:
- Select data fields
- Choose visual type
- Apply colors and formatting
- Add titles and data labels

### Step 4: Create Pages
1. Duplicate page for each section
2. Rename pages (Executive Summary, RFM Deep Dive, etc.)
3. Add slicers to each page

### Step 5: Publish
File → Publish → Select workspace

---

## 📊 Sample DAX Formulas

```dax
// Total Revenue
Total Revenue = SUM(rfm_segmentation[monetary])

// Customers by Segment
Segment Count = COUNTIF(rfm_segmentation[segment], SELECTEDVALUE(rfm_segmentation[segment]))

// Revenue Share %
Revenue % = 
  DIVIDE(
    SUM(rfm_segmentation[monetary]),
    CALCULATE(SUM(rfm_segmentation[monetary]), ALL(rfm_segmentation)),
    0
  ) * 100

// Avg Recency by Segment
Avg Recency = AVERAGEIF(rfm_segmentation[segment], SELECTEDVALUE(rfm_segmentation[segment]), rfm_segmentation[recency])

// Churn Risk Customers
Churn Risk Count = 
  COUNTIF(rfm_segmentation[segment], "Lost") + 
  COUNTIF(rfm_segmentation[segment], "Can't Lose Them")

// High Value Customers
High Value Count = COUNTIF(rfm_segmentation[M_score], 5)

// Active Customers (recency < 90 days)
Active Customers = COUNTIF(rfm_segmentation[recency], "<90")
```

---

## 🚀 Dashboard Tips

✅ **Interactivity:** Use slicers for segment-wise filtering  
✅ **Drill-down:** Add detail tables with customer-level data  
✅ **Alerts:** Highlight At-Risk and Lost segments in red  
✅ **Mobile:** Design reports to be mobile-responsive  
✅ **Refresh:** Set automatic daily refresh from CSV  

---

## 📱 Mobile View
Ensure visuals are responsive:
- Use vertical layout for mobile
- Simplify complex charts
- Keep titles and KPIs visible

---

**Ready to build in Power BI Desktop!** 🎯
