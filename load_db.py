import sqlite3
import pandas as pd
import os

DB = "ieee_local.db"
TABLE = "enrichment"
CSV = "enrichment_clean_for_dbms.csv"

def preprocess_csv(csv_file):
    """Load, clean, normalize, and prepare CSV for DB"""
    df = pd.read_csv(csv_file)
    df.columns = [c.strip().lower() for c in df.columns]

    # Rename columns
    rename_map = {
        "term": "Term",
        "p-value": "p_value",
        "p_value": "p_value",
        "adj p-value": "adj_p_value",
        "adj_p_value": "adj_p_value",
        "odds ratio": "odds_ratio",
        "odds_ratio": "odds_ratio",
        "combined score": "combined_score",
        "overlap": "Overlap",
        "genes": "Genes"
    }
    df = df.rename(columns=rename_map)

    # Split overlap column
    if "Overlap" in df.columns:
        def split_overlap(val):
            if isinstance(val, str) and "/" in val:
                try:
                    num, den = val.split("/")
                    num, den = int(num), int(den)
                    return num, den, num / den if den != 0 else None
                except:
                    return None, None, None
            return None, None, None
        df[["overlap_num", "overlap_den", "overlap_frac"]] = df["Overlap"].apply(
            lambda x: pd.Series(split_overlap(x))
        )

    # Numeric columns
    numeric_cols = ["p_value", "adj_p_value", "odds_ratio", "combined_score",
                    "overlap_num", "overlap_den", "overlap_frac"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Text columns
    text_cols = ["Term", "Genes", "Overlap"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace("nan", None)
            df[col] = df[col].str.lower()

    # Ensure all expected columns
    expected = ["Term", "p_value", "adj_p_value", "odds_ratio", "combined_score",
                "Overlap", "overlap_num", "overlap_den", "overlap_frac", "Genes"]
    for col in expected:
        if col not in df.columns:
            df[col] = None

    # Drop duplicates
    df = df.drop_duplicates()

    # Drop rows with missing critical field
    df = df.dropna(subset=["p_value"])

    # Clip extreme values
    df["p_value"] = df["p_value"].clip(0,1)
    df["adj_p_value"] = df.get("adj_p_value", pd.Series()).clip(0,1) if "adj_p_value" in df else df.get("adj_p_value")
    df["odds_ratio"] = df.get("odds_ratio", pd.Series()).clip(0,100) if "odds_ratio" in df else df.get("odds_ratio")

    # Min-Max normalize numeric columns
    scaler_cols = ["odds_ratio", "combined_score", "overlap_frac"]
    for col in scaler_cols:
        if col in df.columns and df[col].notna().sum() > 0:
            min_val, max_val = df[col].min(), df[col].max()
            if min_val != max_val:
                df[col] = (df[col] - min_val) / (max_val - min_val)

    return df[expected]

def create_db():
    """Create SQLite table if not exists"""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Term TEXT,
            p_value REAL,
            adj_p_value REAL,
            odds_ratio REAL,
            combined_score REAL,
            Overlap TEXT,
            overlap_num INTEGER,
            overlap_den INTEGER,
            overlap_frac REAL,
            Genes TEXT
        );
    """)
    conn.commit()
    conn.close()

def load_csv_to_db(csv_file=CSV):
    """Load cleaned CSV into DB"""
    df = preprocess_csv(csv_file)
    conn = sqlite3.connect(DB)
    df.to_sql(TABLE, conn, if_exists="append", index=False)
    conn.close()
    print(f"Loaded {len(df)} rows into {DB}")

# ✅ Correct main guard
if __name__ == "__main__":
    create_db()
    if os.path.exists(CSV):
        load_csv_to_db()
    else:
        print(f"Place {CSV} in the folder and run again.")
