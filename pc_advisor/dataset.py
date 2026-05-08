import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path

from pc_advisor.models import ComponentSearch, PartMatch
from pc_advisor.config import COMPONENT_TABLES, MAX_SEARCH_RESULTS

load_dotenv()

# ---------------------------------------------------------------------------
# Database loader
# ---------------------------------------------------------------------------
class DatabaseLoader:
    """Creates database connection for files"""
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv("SQL_HOST"),
            user=os.getenv("SQL_USER"),
            password=os.getenv("SQL_PASSWORD"),
            database=os.getenv("SQL_DATABASE")
        )
    def _rows_to_parts(self, rows):
        return [dict(row) for row in rows]
    def search(self, table: str, query: str) -> list[PartMatch]:
        if not query.strip():
            return []
        tokens = query.lower().split()
        where_clause = " AND ".join(["LOWER(name) LIKE %s"] * len(tokens))
        params = [f"%{t}%" for t in tokens]
        sql = f"""
            SELECT *
            FROM `{table}`
            WHERE {where_clause}
            LIMIT %s
        """
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(sql, (*params, MAX_SEARCH_RESULTS))
        rows = cursor.fetchall()
        return [
            PartMatch(
                name=row["name"],
                price=float(row["price"]) if row.get("price") else None,
                data=row
            )
            for row in rows
        ]
    def top(self, table: str) -> list[PartMatch]:
        sql = f"SELECT * FROM `{table}` LIMIT %s"
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(sql, (MAX_SEARCH_RESULTS,))
        rows = cursor.fetchall()
        return [
            PartMatch(
                name=row["name"],
                price=float(row["price"]) if row.get("price") else None,
                data=row
            )
            for row in rows
        ]

# ---------------------------------------------------------------------------
# Dataset search
# ---------------------------------------------------------------------------

def search_dataset(loader: DatabaseLoader, preferences: dict[str, str]) -> list[ComponentSearch]:
    results: list[ComponentSearch] = []

    print("\n" + "=" * 60)
    print("  Searching MySQL database...")
    print("=" * 60)

    for component, preference in preferences.items():
        table = COMPONENT_TABLES.get(component, "")
        cs = ComponentSearch(category=component, user_preference=preference)

        print(f"\n  [{component}]  query: \"{preference or '(any)'}\"")

        if not table:
            cs.error = "No database table mapped."
            results.append(cs)
            continue

        try:
            matches = loader.search(table, preference) if preference else loader.top(table)
            if not matches:
                print("    No matches found.")
                cs.error = "No matches found in database."
            else:
                for m in matches:
                    ps = f"${m.price:,.2f}" if m.price else "Price N/A"
                    print(f"    - {m.name[:55]:55s}  {ps}")
                cs.matches = matches
        except Exception as exc:
            cs.error = str(exc)
            print(f"    ERROR: {exc}")

        results.append(cs)

    return results
