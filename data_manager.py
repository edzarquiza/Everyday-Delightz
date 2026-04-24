"""
data_manager.py
Handles all Excel read/write operations for Everyday DelightZ.
Database file: everyday_delightz_data.xlsx
"""

import pandas as pd
from pathlib import Path
from datetime import date

DB_FILE = "everyday_delightz_data.xlsx"

# Default values injected when migrating existing sheets that are missing a column
SHEET_DEFAULTS = {
    "pack_sizes": "1,5,10",
}

SHEETS = {
    "ingredients": {
        "columns": ["id", "name", "unit", "cost_per_unit", "stock", "min_stock", "updated_at"],
        "dtypes": {"id": int, "cost_per_unit": float, "stock": float, "min_stock": float}
    },
    "recipes": {
        "columns": ["id", "name", "portion_size", "waste_pct", "default_price",
                    "target_margin_pct", "dough_weight", "pack_sizes"],
        "dtypes": {"id": int, "portion_size": float, "waste_pct": float,
                   "default_price": float, "target_margin_pct": float, "dough_weight": float}
    },
    "recipe_items": {
        "columns": ["id", "recipe_id", "ingredient_id", "qty"],
        "dtypes": {"id": int, "recipe_id": int, "ingredient_id": int, "qty": float}
    },
    "sales": {
        "columns": ["id", "recipe_id", "qty", "price_per_pc", "date", "pack_size"],
        "dtypes": {"id": int, "recipe_id": int, "qty": int, "price_per_pc": float, "pack_size": int}
    },
    "expenses": {
        "columns": ["id", "description", "category", "amount", "date"],
        "dtypes": {"id": int, "amount": float}
    },
    "settings": {
        "columns": ["key", "value"],
        "dtypes": {}
    },
}

SAMPLE_DATA = {
    "ingredients": pd.DataFrame([
        [1, "All-Purpose Flour", "g",  0.065, 5000, 500,  str(date.today())],
        [2, "Sugar",            "g",  0.080, 2000, 300,  str(date.today())],
        [3, "Butter",           "g",  0.450, 800,  200,  str(date.today())],
        [4, "Eggs",             "pcs",12.00, 24,   6,    str(date.today())],
        [5, "Baking Powder",    "g",  0.220, 200,  50,   str(date.today())],
        [6, "Cocoa Powder",     "g",  0.380, 400,  100,  str(date.today())],
        [7, "Chocolate Chips",  "g",  0.720, 600,  150,  str(date.today())],
        [8, "Vanilla Extract",  "ml", 1.200, 100,  20,   str(date.today())],
        [9, "Salt",             "g",  0.020, 500,  50,   str(date.today())],
    ], columns=SHEETS["ingredients"]["columns"]),

    "recipes": pd.DataFrame([
        [1, "Choco Chip Cookies", 40, 5, 35, 60, 927, "1,5,10"],
        [2, "Brownies",           60, 3, 45, 55, 780, "1,5,10"],
    ], columns=SHEETS["recipes"]["columns"]),

    "recipe_items": pd.DataFrame([
        [1,  1, 1, 280], [2,  1, 2, 200], [3,  1, 3, 227],
        [4,  1, 4, 2],   [5,  1, 5, 5],   [6,  1, 7, 200],
        [7,  1, 8, 10],  [8,  1, 9, 3],
        [9,  2, 1, 150], [10, 2, 2, 300], [11, 2, 3, 200],
        [12, 2, 4, 3],   [13, 2, 6, 120], [14, 2, 8, 5],
        [15, 2, 9, 2],
    ], columns=SHEETS["recipe_items"]["columns"]),

    "sales": pd.DataFrame([
        [1, 1, 24, 35, str(date.today()), 6],
        [2, 2, 12, 45, str(date.today()), 12],
    ], columns=SHEETS["sales"]["columns"]),

    "expenses": pd.DataFrame(columns=SHEETS["expenses"]["columns"]),

    "settings": pd.DataFrame([
        ["monthly_goal", "0"],
    ], columns=SHEETS["settings"]["columns"]),
}


class DataManager:
    def __init__(self, db_path: str = DB_FILE):
        self.db_path = Path(db_path)
        self._ensure_db()

    # ── Internal helpers ────────────────────────────────────────────
    def _ensure_db(self):
        """Create the Excel file with sample data if it doesn't exist, or migrate existing."""
        if not self.db_path.exists():
            with pd.ExcelWriter(self.db_path, engine="openpyxl") as writer:
                for sheet, df in SAMPLE_DATA.items():
                    df.to_excel(writer, sheet_name=sheet, index=False)
        else:
            try:
                xf = pd.ExcelFile(self.db_path, engine="openpyxl")
                existing_sheets = xf.sheet_names
                all_sheets = {s: pd.read_excel(self.db_path, sheet_name=s, engine="openpyxl")
                              for s in existing_sheets}
                changed = False

                for sheet, spec in SHEETS.items():
                    if sheet not in all_sheets:
                        all_sheets[sheet] = SAMPLE_DATA[sheet].copy()
                        changed = True
                    else:
                        df = all_sheets[sheet]
                        for col in spec["columns"]:
                            if col not in df.columns:
                                df[col] = SHEET_DEFAULTS.get(col, None)
                                changed = True
                        all_sheets[sheet] = df

                if changed:
                    with pd.ExcelWriter(self.db_path, engine="openpyxl") as writer:
                        for s, df in all_sheets.items():
                            df.to_excel(writer, sheet_name=s, index=False)
            except Exception:
                pass

    def _read(self, sheet: str) -> pd.DataFrame:
        try:
            df = pd.read_excel(self.db_path, sheet_name=sheet, engine="openpyxl")
            if df.empty:
                return pd.DataFrame(columns=SHEETS[sheet]["columns"])
            return df
        except Exception:
            return pd.DataFrame(columns=SHEETS[sheet]["columns"])

    def _write_sheet(self, sheet: str, df: pd.DataFrame):
        """Write a single sheet, preserving all other sheets."""
        try:
            all_sheets = {}
            try:
                xf = pd.ExcelFile(self.db_path, engine="openpyxl")
                for s in xf.sheet_names:
                    all_sheets[s] = pd.read_excel(self.db_path, sheet_name=s, engine="openpyxl")
            except Exception:
                pass
            all_sheets[sheet] = df
            with pd.ExcelWriter(self.db_path, engine="openpyxl") as writer:
                for s, sdf in all_sheets.items():
                    sdf.to_excel(writer, sheet_name=s, index=False)
        except Exception as e:
            raise RuntimeError(f"Failed to write sheet '{sheet}': {e}")

    def _next_id(self, df: pd.DataFrame) -> int:
        if df.empty or "id" not in df.columns:
            return 1
        return int(df["id"].max()) + 1

    # ── INGREDIENTS ─────────────────────────────────────────────────
    def get_ingredients(self) -> pd.DataFrame:
        df = self._read("ingredients")
        if not df.empty:
            for col, dtype in SHEETS["ingredients"]["dtypes"].items():
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(dtype)
        return df

    def add_ingredient(self, name, unit, cost_per_unit, stock, min_stock):
        df = self.get_ingredients()
        new_row = {
            "id": self._next_id(df), "name": name, "unit": unit,
            "cost_per_unit": float(cost_per_unit), "stock": float(stock),
            "min_stock": float(min_stock), "updated_at": str(date.today()),
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self._write_sheet("ingredients", df)

    def update_ingredient(self, ing_id, name, unit, cost_per_unit, stock, min_stock):
        df = self.get_ingredients()
        idx = df[df["id"] == ing_id].index
        if not idx.empty:
            df.loc[idx[0], ["name", "unit", "cost_per_unit", "stock", "min_stock", "updated_at"]] = [
                name, unit, float(cost_per_unit), float(stock), float(min_stock), str(date.today())
            ]
        self._write_sheet("ingredients", df)

    def delete_ingredient(self, ing_id):
        df = self.get_ingredients()
        df = df[df["id"] != ing_id]
        self._write_sheet("ingredients", df)

    # ── RECIPES ─────────────────────────────────────────────────────
    def get_recipes(self) -> pd.DataFrame:
        df = self._read("recipes")
        if not df.empty:
            for col, dtype in SHEETS["recipes"]["dtypes"].items():
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(dtype)
            if "pack_sizes" not in df.columns:
                df["pack_sizes"] = "1,5,10"
            else:
                df["pack_sizes"] = df["pack_sizes"].fillna("1,5,10").astype(str)
        return df

    def add_recipe(self, name, portion_size, waste_pct, default_price,
                   target_margin_pct, dough_weight, ingredients: list,
                   pack_sizes: str = "1,5,10"):
        df = self.get_recipes()
        new_id = self._next_id(df)
        new_row = {
            "id": new_id, "name": name,
            "portion_size": float(portion_size), "waste_pct": float(waste_pct),
            "default_price": float(default_price), "target_margin_pct": float(target_margin_pct),
            "dough_weight": float(dough_weight), "pack_sizes": str(pack_sizes),
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self._write_sheet("recipes", df)

        ri_df = self.get_recipe_items()
        new_rows = []
        for item in ingredients:
            new_rows.append({
                "id": self._next_id(ri_df) + len(new_rows),
                "recipe_id": new_id,
                "ingredient_id": int(item["ingredient_id"]),
                "qty": float(item["qty"]),
            })
        if new_rows:
            ri_df = pd.concat([ri_df, pd.DataFrame(new_rows)], ignore_index=True)
            self._write_sheet("recipe_items", ri_df)

    def update_recipe(self, recipe_id, name, portion_size, waste_pct, default_price,
                      target_margin_pct, dough_weight, ingredients: list,
                      pack_sizes: str = None):
        df = self.get_recipes()
        idx = df[df["id"] == recipe_id].index
        if not idx.empty:
            cols = ["name", "portion_size", "waste_pct", "default_price",
                    "target_margin_pct", "dough_weight"]
            vals = [name, float(portion_size), float(waste_pct),
                    float(default_price), float(target_margin_pct), float(dough_weight)]
            if pack_sizes is not None:
                cols.append("pack_sizes")
                vals.append(str(pack_sizes))
            df.loc[idx[0], cols] = vals
        self._write_sheet("recipes", df)

        ri_df = self.get_recipe_items()
        ri_df = ri_df[ri_df["recipe_id"] != recipe_id]
        new_rows = []
        for item in ingredients:
            new_rows.append({
                "id": self._next_id(ri_df) + len(new_rows),
                "recipe_id": recipe_id,
                "ingredient_id": int(item["ingredient_id"]),
                "qty": float(item["qty"]),
            })
        if new_rows:
            ri_df = pd.concat([ri_df, pd.DataFrame(new_rows)], ignore_index=True)
        self._write_sheet("recipe_items", ri_df)

    def delete_recipe(self, recipe_id):
        df = self.get_recipes()
        df = df[df["id"] != recipe_id]
        self._write_sheet("recipes", df)
        ri_df = self.get_recipe_items()
        ri_df = ri_df[ri_df["recipe_id"] != recipe_id]
        self._write_sheet("recipe_items", ri_df)

    # ── RECIPE ITEMS ────────────────────────────────────────────────
    def get_recipe_items(self, recipe_id=None) -> pd.DataFrame:
        df = self._read("recipe_items")
        if not df.empty:
            for col, dtype in SHEETS["recipe_items"]["dtypes"].items():
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(dtype)
        if recipe_id is not None and not df.empty:
            df = df[df["recipe_id"] == recipe_id]
        return df

    # ── SALES ────────────────────────────────────────────────────────
    def get_sales(self) -> pd.DataFrame:
        df = self._read("sales")
        if not df.empty:
            if "pack_size" not in df.columns:
                df["pack_size"] = 1
            for col, dtype in SHEETS["sales"]["dtypes"].items():
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(dtype)
        return df

    def add_sale(self, recipe_id, qty, price_per_pc, sale_date, pack_size=1):
        df = self.get_sales()
        new_row = {
            "id": self._next_id(df), "recipe_id": int(recipe_id),
            "qty": int(qty), "price_per_pc": float(price_per_pc),
            "date": str(sale_date), "pack_size": int(pack_size),
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self._write_sheet("sales", df)

    def delete_sale(self, sale_id):
        df = self.get_sales()
        df = df[df["id"] != sale_id]
        self._write_sheet("sales", df)

    # ── EXPENSES ─────────────────────────────────────────────────────
    def get_expenses(self) -> pd.DataFrame:
        df = self._read("expenses")
        if not df.empty:
            for col, dtype in SHEETS["expenses"]["dtypes"].items():
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(dtype)
        return df

    def add_expense(self, description, category, amount, exp_date):
        df = self.get_expenses()
        new_row = {
            "id": self._next_id(df), "description": description,
            "category": category, "amount": float(amount), "date": str(exp_date),
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self._write_sheet("expenses", df)

    def delete_expense(self, exp_id):
        df = self.get_expenses()
        df = df[df["id"] != exp_id]
        self._write_sheet("expenses", df)

    # ── SETTINGS ─────────────────────────────────────────────────────
    def get_setting(self, key: str, default=None):
        df = self._read("settings")
        if df.empty or "key" not in df.columns:
            return default
        row = df[df["key"] == key]
        return row.iloc[0]["value"] if not row.empty else default

    def set_setting(self, key: str, value: str):
        df = self._read("settings")
        if df.empty or "key" not in df.columns:
            df = pd.DataFrame(columns=SHEETS["settings"]["columns"])
        if key in df["key"].values:
            df.loc[df["key"] == key, "value"] = str(value)
        else:
            df = pd.concat([df, pd.DataFrame([{"key": key, "value": str(value)}])], ignore_index=True)
        self._write_sheet("settings", df)
