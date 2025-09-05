import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

DB_FILE = 'results.db'


def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM results", conn)
    conn.close()
    return df


def main():
    df = load_data()
    print(df.head())

    print("=== Summary ===")
    print("Workers:", df['worker_id'].nunique())
    print("Total rows processed:", df['rows_processed'].sum())
    print("Total sales:", df['total_sales'].sum())
    print("Overall average price:", df['avg_price'].mean())

    # ========== Parallelization Insights ==========

    # Bar plot: Rows processed by worker
    plt.figure(figsize=(8, 5))
    sns.barplot(x='worker_id', y='rows_processed', data=df)
    plt.title("Rows Processed by Each Worker")
    plt.xlabel("Worker ID")
    plt.ylabel("Rows Processed")
    plt.tight_layout()
    plt.savefig("rows_by_worker.png")
    plt.show()

    # Average price with min/max error bars per worker
    plt.figure(figsize=(10, 6))
    x = np.arange(len(df['worker_id']))
    plt.bar(x, df['avg_price'], yerr=[df['avg_price'] - df['min_price'], df['max_price'] - df['avg_price']], capsize=5)
    plt.xticks(x, df['worker_id'])
    plt.title("Average Price with Min/Max Error Bars by Worker")
    plt.xlabel("Worker")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.savefig("price_error_bars_by_worker.png")
    plt.show()

    # ========== Business Insights Visualizations ==========

    print("\n--- Business Data EDA ---")
    df_sales = pd.read_csv('sales.csv')

    # Convert to datetime
    df_sales['Order Date'] = pd.to_datetime(df_sales['Order Date'])
    df_sales['Year'] = df_sales['Order Date'].dt.year

    # Set as index
    df_sales.set_index('Order Date', inplace=True)

    # Resample by month and drop last (possible incomplete) month
    monthly_sales = df_sales['Total Revenue'].resample('M').sum()[:-1]

    # 3-month rolling average smoothing
    monthly_sales_rolling = monthly_sales.rolling(window=3).mean()

    plt.figure(figsize=(10, 5))
    monthly_sales_rolling.plot(title="Monthly Sales (3-Month Rolling Average)")

    # Highlight peak month with adjusted text position
    peak_month = monthly_sales.idxmax()
    peak_value = monthly_sales.max()
    plt.axvline(peak_month, color='red', linestyle='--', alpha=0.7)

    # Position text slightly above the peak value and inside the plot area
    ymax = plt.gca().get_ylim()[1]
    text_y = min(peak_value * 1.05, ymax * 0.95)
    plt.text(peak_month, text_y, f'Peak: {int(peak_value):,}', color='red', fontsize=9, ha='center', va='bottom',
             backgroundcolor='white')

    plt.ylabel("Total Revenue")
    plt.xlabel("Month")
    plt.tight_layout()
    plt.savefig("monthly_sales_rolling.png")
    plt.show()

    # Yearly sales bar chart
    yearly_sales = df_sales.groupby('Year')['Total Revenue'].sum()

    plt.figure(figsize=(8, 5))
    yearly_sales.plot(kind='bar', title='Yearly Sales', color='skyblue')
    plt.ylabel("Total Revenue")
    plt.xlabel("Year")
    plt.tight_layout()
    plt.savefig("yearly_sales.png")
    plt.show()


if __name__ == "__main__":
    main()
