import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

def generate_realistic_data(n_customers=2000, n_transactions=8000):
    """Generate production-grade e-commerce transaction data"""
    customer_ids = np.arange(1, n_customers + 1)
    products = ['Electronics', 'Fashion', 'Home', 'Sports', 'Books', 'Beauty', 'Toys', 'Food']

    transactions = []
    base_date = datetime(2023, 1, 1)

    for _ in range(n_transactions):
        cust_id = np.random.choice(customer_ids)
        days_ago = np.random.randint(0, 730)
        transaction_date = base_date + timedelta(days=days_ago)

        base_amount = np.random.choice([500, 1000, 2000, 5000], p=[0.5, 0.25, 0.15, 0.1])
        amount = base_amount + np.random.normal(0, base_amount * 0.2)
        amount = max(100, amount)

        transactions.append({
            'customer_id': cust_id,
            'transaction_date': transaction_date,
            'amount': round(amount, 2),
            'product_category': np.random.choice(products),
            'order_id': f"ORD{cust_id}{days_ago}{_}"
        })

    df = pd.DataFrame(transactions)
    df = df.sort_values('transaction_date').reset_index(drop=True)
    return df

def clean_data(df):
    """Data cleaning and validation"""
    print("Cleaning data...")
    df = df.drop_duplicates(subset=['order_id'])
    df = df[df['amount'] > 0]
    Q3 = df['amount'].quantile(0.99)
    df = df[df['amount'] <= Q3]
    print(f"  Cleaned: {len(df)} transactions")
    return df

def calculate_rfm(df, reference_date=None):
    """Calculate RFM: Recency, Frequency, Monetary"""
    if reference_date is None:
        reference_date = datetime(2025, 12, 31)

    rfm = df.groupby('customer_id').agg({
        'transaction_date': lambda x: (reference_date - x.max()).days,
        'customer_id': 'count',
        'amount': 'sum'
    }).rename(columns={
        'transaction_date': 'recency',
        'customer_id': 'frequency',
        'amount': 'monetary'
    })

    return rfm

def score_rfm(rfm):
    """Score R, F, M on scale 1-5 (5 is best)"""
    rfm['R_score'] = pd.qcut(rfm['recency'], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')
    rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
    rfm['M_score'] = pd.qcut(rfm['monetary'], q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')

    rfm['R_score'] = rfm['R_score'].astype(int)
    rfm['F_score'] = rfm['F_score'].astype(int)
    rfm['M_score'] = rfm['M_score'].astype(int)

    rfm['rfm_score'] = (rfm['R_score'] + rfm['F_score'] + rfm['M_score']) / 3
    rfm['rfm_segment_code'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

    return rfm

def segment_customers(rfm):
    """Assign customer segments based on RFM"""
    def get_segment(row):
        r, f, m = row['R_score'], row['F_score'], row['M_score']

        if r >= 4 and f >= 4 and m >= 4:
            return 'Champions'
        elif r >= 4 and f >= 3 and m >= 3:
            return 'Loyal Customers'
        elif r >= 3 and f >= 3:
            return 'Potential Loyalists'
        elif r >= 4 and f <= 2:
            return 'Recent Customers'
        elif r <= 2 and f >= 4:
            return 'At Risk'
        elif r <= 2 and f >= 3:
            return 'Cant Lose Them'
        elif r <= 1:
            return 'Lost'
        else:
            return 'Need Attention'

    rfm['segment'] = rfm.apply(get_segment, axis=1)
    return rfm

if __name__ == '__main__':
    print("=" * 70)
    print("RFM SEGMENTATION ANALYSIS - PRODUCTION READY")
    print("=" * 70)

    print("\nGenerating realistic e-commerce data...")
    transactions = generate_realistic_data(n_customers=2000, n_transactions=8000)
    print(f"  Generated: {len(transactions)} transactions from {transactions['customer_id'].nunique()} customers")

    print("\nData processing pipeline...")
    transactions = clean_data(transactions)

    print("\nCalculating RFM metrics...")
    rfm = calculate_rfm(transactions)
    rfm = score_rfm(rfm)
    rfm = segment_customers(rfm)

    rfm = rfm.reset_index()
    rfm['customer_value'] = rfm['monetary'] / rfm['frequency']
    rfm['days_since_purchase'] = rfm['recency']

    year_rev = transactions.pivot_table(index='customer_id', columns=transactions['transaction_date'].dt.year,
                                        values='amount', aggfunc='sum', fill_value=0)
    rfm['revenue_2023'] = rfm['customer_id'].map(year_rev[2023]).round(2)
    rfm['revenue_2024'] = rfm['customer_id'].map(year_rev[2024]).round(2)

    # Reorder columns for Power BI
    rfm = rfm[[
        'customer_id', 'recency', 'frequency', 'monetary',
        'R_score', 'F_score', 'M_score', 'rfm_score', 'rfm_segment_code',
        'segment', 'customer_value', 'days_since_purchase', 'revenue_2023', 'revenue_2024'
    ]]

    os.makedirs('data', exist_ok=True)
    output_file = 'data/rfm_segmentation.csv'
    rfm.to_csv(output_file, index=False)

    print(f"\nRFM data ready: {output_file}")

    print("\n" + "=" * 70)
    print("BUSINESS INSIGHTS")
    print("=" * 70)
    print(f"Total Customers: {len(rfm):,}")
    print(f"Total Revenue: Rs {rfm['monetary'].sum():,.0f}")
    print(f"Avg Customer Lifetime Value: Rs {rfm['monetary'].mean():,.0f}")
    print(f"Date Range: 2023-01-01 to 2024-12-31\n")

    print("CUSTOMER SEGMENTS:")
    for segment in ['Champions', 'Loyal Customers', 'Potential Loyalists', 'Recent Customers', 'At Risk', 'Cant Lose Them', 'Lost']:
        count = len(rfm[rfm['segment'] == segment])
        if count > 0:
            revenue = rfm[rfm['segment'] == segment]['monetary'].sum()
            pct = (count / len(rfm)) * 100
            avg_value = rfm[rfm['segment'] == segment]['monetary'].mean()
            print(f"  {segment:25s}: {count:4d} ({pct:5.1f}%) -> Revenue: Rs {revenue:>12,.0f} | Avg: Rs {avg_value:>8,.0f}")

    print("\n" + "=" * 70)
    print("Ready for Power BI Dashboard")
    print("=" * 70)
