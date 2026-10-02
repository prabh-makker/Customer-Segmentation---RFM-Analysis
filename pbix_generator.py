"""
Power BI Companion Script
Generates enriched data and configuration for Power BI dashboards
"""

import pandas as pd
import json
from datetime import datetime

def add_power_bi_measures(csv_path='data/rfm_segmentation.csv'):
    """Add calculated fields and measures for Power BI"""

    print("📊 Loading RFM data...")
    df = pd.read_csv(csv_path)

    print("🔧 Adding Power BI measures...")

    # Segment grouping for easier analysis
    def get_segment_group(segment):
        if segment in ['Champions', 'Loyal Customers']:
            return 'High Value'
        elif segment in ['Potential Loyalists', 'Recent Customers']:
            return 'Growth'
        elif segment in ['At Risk', 'Can\'t Lose Them']:
            return 'At Risk'
        else:
            return 'Lost'

    df['segment_group'] = df['segment'].apply(get_segment_group)

    # Risk level
    def get_risk_level(segment):
        if segment in ['Lost', 'Can\'t Lose Them']:
            return 'High'
        elif segment == 'At Risk':
            return 'Medium'
        elif segment == 'Recent Customers':
            return 'Low'
        else:
            return 'None'

    df['risk_level'] = df['segment'].apply(get_risk_level)

    # Monetization potential
    def get_potential(f_score, m_score):
        if f_score >= 4 and m_score >= 4:
            return 'Very High'
        elif f_score >= 3 and m_score >= 3:
            return 'High'
        elif f_score >= 2 or m_score >= 2:
            return 'Medium'
        else:
            return 'Low'

    df['monetization_potential'] = df.apply(
        lambda row: get_potential(row['F_score'], row['M_score']),
        axis=1
    )

    # Engagement score (custom metric)
    df['engagement_score'] = (
        (df['F_score'] * 0.4) +  # Frequency: 40%
        (df['R_score'] * 0.4) +  # Recency: 40%
        (df['M_score'] * 0.2)    # Monetary: 20%
    ).round(2)

    # Customer lifecycle stage
    def get_lifecycle(r, f, m):
        if r <= 2 and f <= 2:
            return 'Dormant'
        elif r >= 4 and f <= 2:
            return 'New'
        elif r >= 4 and f >= 3:
            return 'Active'
        elif r <= 2 and f >= 3:
            return 'Inactive'
        else:
            return 'Regular'

    df['lifecycle_stage'] = df.apply(
        lambda row: get_lifecycle(row['R_score'], row['F_score'], row['M_score']),
        axis=1
    )

    # Priority for action
    def get_action_priority(segment, recency):
        if segment in ['At Risk', 'Can\'t Lose Them']:
            return 'Urgent'
        elif segment == 'Lost':
            return 'High'
        elif segment == 'Recent Customers':
            return 'Medium'
        else:
            return 'Low'

    df['action_priority'] = df.apply(
        lambda row: get_action_priority(row['segment'], row['recency']),
        axis=1
    )

    # ROI Category (for investment decision)
    def get_roi_category(segment, monetary):
        if segment == 'Champions' and monetary > 8000:
            return 'High ROI'
        elif segment in ['Loyal Customers', 'Potential Loyalists']:
            return 'Medium-High ROI'
        elif segment == 'At Risk' and monetary > 5000:
            return 'Critical (Win-back)'
        elif segment == 'Recent Customers':
            return 'Growth Potential'
        else:
            return 'Low ROI'

    df['roi_category'] = df.apply(
        lambda row: get_roi_category(row['segment'], row['monetary']),
        axis=1
    )

    # Save enriched data
    enriched_file = 'data/rfm_segmentation_powerbi.csv'
    df.to_csv(enriched_file, index=False)
    print(f"✅ Enriched data saved: {enriched_file}")

    return df

def generate_dax_formulas():
    """Generate DAX measure definitions"""

    dax_measures = {
        "Total_Customers": "COUNTA(rfm_segmentation[customer_id])",

        "Total_Revenue": "SUM(rfm_segmentation[monetary])",

        "Avg_CLV": "AVERAGE(rfm_segmentation[monetary])",

        "Churn_Rate_Percent": """
DIVIDE(
    COUNTIF(rfm_segmentation[segment], "Lost"),
    COUNTA(rfm_segmentation[customer_id]),
    0
) * 100
        """,

        "At_Risk_Count": """
COUNTIF(rfm_segmentation[segment], "At Risk") +
COUNTIF(rfm_segmentation[segment], "Can't Lose Them")
        """,

        "At_Risk_Revenue": """
CALCULATE(
    SUM(rfm_segmentation[monetary]),
    OR(
        rfm_segmentation[segment] = "At Risk",
        rfm_segmentation[segment] = "Can't Lose Them"
    )
)
        """,

        "Champions_Revenue": """
CALCULATE(
    SUM(rfm_segmentation[monetary]),
    rfm_segmentation[segment] = "Champions"
)
        """,

        "Avg_Order_Value": "AVERAGE(rfm_segmentation[customer_value])",

        "High_Value_Customers": "COUNTIF(rfm_segmentation[M_score], 5)",

        "Active_Customers": "COUNTIF(rfm_segmentation[recency], '<90')",

        "Revenue_Share_Percent": """
DIVIDE(
    SUM(rfm_segmentation[monetary]),
    CALCULATE(SUM(rfm_segmentation[monetary]), ALL(rfm_segmentation)),
    0
) * 100
        """,

        "Customer_Concentration": """
DIVIDE(
    SUM(rfm_segmentation[monetary]),
    COUNTA(rfm_segmentation[customer_id]),
    0
        """,

        "Repeat_Purchase_Rate": """
DIVIDE(
    COUNTIF(rfm_segmentation[frequency], '>1'),
    COUNTA(rfm_segmentation[customer_id]),
    0
) * 100
        """
    }

    return dax_measures

def generate_pbix_config():
    """Generate Power BI configuration JSON"""

    config = {
        "dashboard_name": "Customer Segmentation - RFM Analysis",
        "data_source": "rfm_segmentation_powerbi.csv",
        "pages": [
            {
                "page_name": "Executive Summary",
                "description": "High-level business metrics and segment overview",
                "visuals": [
                    {
                        "type": "KPI Card",
                        "title": "Total Customers",
                        "measure": "Total_Customers",
                        "format": "Number",
                        "position": "Top-Left"
                    },
                    {
                        "type": "KPI Card",
                        "title": "Total Revenue",
                        "measure": "Total_Revenue",
                        "format": "Currency",
                        "position": "Top-Center"
                    },
                    {
                        "type": "KPI Card",
                        "title": "Avg CLV",
                        "measure": "Avg_CLV",
                        "format": "Currency",
                        "position": "Top-Right"
                    },
                    {
                        "type": "KPI Card",
                        "title": "Churn Rate",
                        "measure": "Churn_Rate_Percent",
                        "format": "Percent",
                        "position": "Top-Far-Right"
                    },
                    {
                        "type": "Pie Chart",
                        "title": "Customers by Segment",
                        "category": "segment",
                        "value": "customer_id (count)",
                        "position": "Middle-Left"
                    },
                    {
                        "type": "Column Chart",
                        "title": "Revenue by Segment",
                        "category": "segment",
                        "value": "monetary (sum)",
                        "position": "Middle-Center"
                    },
                    {
                        "type": "Gauge",
                        "title": "Active Customers",
                        "measure": "Active_Customers",
                        "target": "Total_Customers",
                        "position": "Middle-Right"
                    }
                ]
            },
            {
                "page_name": "RFM Deep Dive",
                "description": "Detailed RFM analysis and score distributions",
                "visuals": [
                    {
                        "type": "Matrix",
                        "title": "RFM Score Heatmap",
                        "rows": "R_score",
                        "columns": "F_score",
                        "values": "customer_id (count)",
                        "position": "Top"
                    },
                    {
                        "type": "Scatter Chart",
                        "title": "Recency vs Frequency",
                        "x_axis": "recency",
                        "y_axis": "frequency",
                        "bubble_size": "monetary",
                        "color": "segment",
                        "position": "Bottom-Left"
                    },
                    {
                        "type": "Histogram",
                        "title": "Customer Value Distribution",
                        "field": "customer_value",
                        "bins": 10,
                        "position": "Bottom-Right"
                    }
                ]
            },
            {
                "page_name": "Segment Analysis",
                "description": "Segment-level insights and recommended actions",
                "visuals": [
                    {
                        "type": "Multi-card",
                        "title": "Segment Performance",
                        "filter": "segment",
                        "metrics": ["customer_count", "revenue", "avg_value", "recommended_action"]
                    },
                    {
                        "type": "Table",
                        "title": "Detailed Segment Analysis",
                        "columns": ["segment", "customer_count", "revenue", "avg_clv", "avg_recency", "recommended_action"]
                    },
                    {
                        "type": "Alert Table",
                        "title": "High-Priority Customers",
                        "filter": "action_priority = 'Urgent'",
                        "columns": ["customer_id", "segment", "monetary", "recency", "action_priority"]
                    }
                ]
            },
            {
                "page_name": "Data Dictionary",
                "description": "Column definitions and filter slicers",
                "slicers": [
                    {
                        "type": "Dropdown",
                        "field": "segment",
                        "title": "Filter by Segment"
                    },
                    {
                        "type": "Slider",
                        "field": "rfm_score",
                        "title": "RFM Score Range"
                    },
                    {
                        "type": "Buttons",
                        "field": "lifecycle_stage",
                        "title": "Customer Lifecycle"
                    }
                ]
            }
        ],
        "color_scheme": {
            "Champions": "#2E7D32",
            "Loyal Customers": "#1976D2",
            "Potential Loyalists": "#F57C00",
            "Recent Customers": "#C62828",
            "At Risk": "#D32F2F",
            "Can't Lose Them": "#FF6F00",
            "Lost": "#757575"
        }
    }

    return config

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 POWER BI PREPARATION SCRIPT")
    print("=" * 70)

    # Generate enriched data
    df_enriched = add_power_bi_measures()

    print("\n📋 Generating DAX formulas...")
    dax = generate_dax_formulas()
    dax_file = 'config/dax_measures.json'
    import os
    os.makedirs('config', exist_ok=True)
    with open(dax_file, 'w') as f:
        json.dump(dax, f, indent=2)
    print(f"✅ DAX measures saved: {dax_file}")

    print("\n📊 Generating Power BI configuration...")
    config = generate_pbix_config()
    config_file = 'config/pbix_config.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✅ Configuration saved: {config_file}")

    print("\n" + "=" * 70)
    print("✨ POWER BI IS READY!")
    print("=" * 70)
    print("\n📌 Next Steps:")
    print("1. Open Power BI Desktop")
    print("2. Get Data → Text/CSV")
    print("3. Select 'data/rfm_segmentation_powerbi.csv'")
    print("4. Copy-paste DAX measures from 'config/dax_measures.json'")
    print("5. Follow dashboard layout from 'config/pbix_config.json'")
    print("6. Refer to 'power_bi_template.md' for visual specifications")
    print("\n🎨 Color scheme and formulas are ready in config files!")
    print("=" * 70)
