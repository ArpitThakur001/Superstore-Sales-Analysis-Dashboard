import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "SampleSuperstore.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path, encoding="latin-1")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

    numeric_columns = ["Sales", "Quantity", "Discount", "Profit"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.drop_duplicates().reset_index(drop=True)
    df = df.dropna(subset=["Order ID", "Order Date", "Sales", "Profit"])

    df["Category"] = df["Category"].astype(str).str.strip()
    df["Region"] = df["Region"].astype(str).str.strip()

    if "Profit" in df.columns and "Sales" in df.columns:
        df["Profit Margin"] = (df["Profit"] / df["Sales"]).fillna(0)

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M")

    return df


def save_csv(df: pd.DataFrame, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / name
    df.to_csv(path, index=False)
    return path


def print_summary(df: pd.DataFrame) -> None:
    print("Superstore Sales Analysis")
    print("-------------------------")
    print(f"Total records: {len(df):,}")
    print(f"Total sales: {df['Sales'].sum():,.2f}")
    print(f"Total profit: {df['Profit'].sum():,.2f}")
    print(f"Total orders: {df['Order ID'].nunique():,}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print("\nMissing values by column:")
    print(df.isnull().sum())

    print("\nTop sales by category:")
    print(df.groupby("Category")["Sales"].sum().sort_values(ascending=False))

    print("\nProfit by region:")
    print(df.groupby("Region")["Profit"].sum().sort_values(ascending=False))

    if "State" in df.columns:
        print("\nTop 10 states by sales:")
        print(df.groupby("State")["Sales"].sum().sort_values(ascending=False).head(10))

    print("\nMonthly sales trend:")
    if "Month" in df.columns:
        monthly = df.groupby("Month")["Sales"].sum().sort_index()
        print(monthly.head(12))


def save_summaries(df: pd.DataFrame) -> None:
    save_csv(df, "cleaned_superstore.csv")
    save_csv(df.groupby("Category")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False), "sales_by_category.csv")
    save_csv(df.groupby("Region")["Profit"].sum().reset_index().sort_values(by="Profit", ascending=False), "profit_by_region.csv")
    if "State" in df.columns:
        save_csv(df.groupby("State")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False).head(10), "top_states_by_sales.csv")
    save_csv(df.groupby("Month")["Sales"].sum().reset_index().sort_values(by="Month"), "monthly_sales_trend.csv")


def main() -> None:
    try:
        df = load_data(DATA_FILE)
    except FileNotFoundError as error:
        print(error)
        return

    cleaned = clean_data(df)
    print_summary(cleaned)
    save_summaries(cleaned)

    print(f"\nSaved cleaned data and summary files to: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
