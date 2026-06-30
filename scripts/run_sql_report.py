from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "fraud_investigation.db"
REPORTS_DIR = PROJECT_ROOT / "reports"

REPORTS = {
    "MODEL DECISION PERFORMANCE REPORT": "model_decision_performance.sql",
    "OPERATIONAL COST PERFORMANCE REPORT": "operational_cost_performance.sql",
    "PRECISION / RECALL @ K REPORT": "precision_recall_at_k.sql",
    "TOP OPERATIONAL RISKS REPORT": "top_operational_risks.sql",
}


def run_query(sql_file: str) -> pd.DataFrame:
    sql_path = PROJECT_ROOT / "sql" / sql_file

    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    with open(sql_path, "r", encoding="utf-8") as file:
        query = file.read()

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        df = pd.read_sql_query(query, connection)
    finally:
        connection.close()

    return df


def print_report(title: str, df: pd.DataFrame) -> None:
    print(f"\n{title}\n")
    print(df.to_string(index=False))


def save_report(sql_file: str, df: pd.DataFrame) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    output_filename = sql_file.replace(".sql", ".csv")
    output_path = REPORTS_DIR / output_filename

    df.to_csv(output_path, index=False)

    return output_path


if __name__ == "__main__":
    for title, sql_file in REPORTS.items():
        try:
            report_df = run_query(sql_file)
            output_path = save_report(sql_file, report_df)

            print(f"\nSaved CSV: {output_path}")
            print_report(title, report_df)

        except Exception as error:
            print(f"\n{title}\n")
            print(f"Could not generate report: {error}")