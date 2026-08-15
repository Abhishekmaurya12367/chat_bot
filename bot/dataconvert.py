
# # Claude finished the response
# # explain about the data cleaning in hinglish

# # Data Cleaning kya hota hai (Hinglish mein)
# # Data cleaning ek process hai jisme raw/messy data ko clean, consistent aur usable format mein convert karte hain, taaki analysis ya ML model training ke liye use kar sakein. Isse "data cleansing" ya "data scrubbing" bhi bolte hain.

# # Kyun zaroori hai?
# # Real-world data almost kabhi bhi perfect nahi hota — usme errors, missing values, duplicates, aur inconsistencies hoti hain. Agar aap dirty data pe model train karoge, toh "garbage in, garbage out" wali situation ho jayegi — model ki accuracy aur predictions dono kharab honge.

# # Main Steps
# # 1. Missing Values Handle karna

# # Kabhi data mein blank cells ya NaN values hoti hain
# # Options: unhe drop karo, ya mean/median/mode se fill karo (imputation), ya koi default value daalo
# # 2. Duplicates Remove karna

# # Same record baar-baar aa sakta hai (data collection ya merging ke time)
# # drop_duplicates() (pandas mein) jaise functions se remove karte hain
# # 3. Inconsistent Data Fix karna

# # Jaise ek column mein "Delhi", "delhi", "DELHI" — sab same city hai but different format
# # Standardize karna padta hai (lowercase, trimming spaces, etc.)
# # 4. Outliers Detect aur Handle karna

# # Extreme values jo normal pattern se bahut door hain
# # Box plots, z-score, IQR method se detect karte hain — phir decide karo remove karna hai ya keep
# # 5. Data Type Correction

# # Kabhi numbers string format mein aa jaate hain ("25" instead of 25)
# # Dates alag-alag formats mein ho sakte hain — unhe ek consistent format mein convert karna
# # 6. Wrong/Invalid Entries Fix karna

# # Jaise age = -5, ya email bina "@" ke
# # Validation rules laga ke aise entries ko flag ya correct karna
# # Tools jo commonly use hote hain
# # Python: pandas (dropna(), fillna(), drop_duplicates()), NumPy
# # Libraries: OpenRefine (dedicated data cleaning tool)
# # SQL: bhi basic cleaning ke liye use hota hai (queries se filter/update)
# # Example (Python pandas)
# # python
# import pandas as pd

# df = pd.read_csv("data.csv")

# # Missing values fill karna
# df['age'].fillna(df['age'].mean(), inplace=True)

# # Duplicates remove karna
# df.drop_duplicates(inplace=True)

# # Column names standardize karna
# df.columns = df.columns.str.strip().str.lower()

# # String data clean karna
# df['city'] = df['city'].str.strip().str.title()
# Since aap GenAI/backend ke liye prep kar rahe ho, data cleaning ka concept ML pipelines mein bhi bahut important hai — kyunki model training se pehle yeh step almost hamesha aata hai. Agar chaho toh main pandas ke saath ek chhota hands-on example bhi bana sakta hoon.

# give me the complete code for the data cleaning making bot


# Created a file, ran a command
# Created a file, ran a command
# Code chal raha hai, bas pandas ke naye version mein ek deprecation warning aa rahi thi — usko fix kar deta hoon taaki future-proof rahe.


# Edited a file, ran a command
# Edited a file, ran a command
# Bas ek harmless deprecation warning bacha hai (pandas ke future version ke liye), koi actual error nahi — script clean chal raha hai.


# Presented file
# Presented file
# Ye bot kya karta hai (full pipeline):

# Column names standardize karta hai (lowercase, underscores)
# Duplicate rows remove karta hai
# Text columns clean karta hai (whitespace, casing)
# Data types fix karta hai (numbers/dates auto-detect)
# Missing values fill karta hai (median/mode se, ya drop/zero strategy bhi choose kar sakte ho)
# Outliers detect + handle karta hai (IQR method — clip/remove/flag)
# Email/phone jaise fields validate karta hai
# Cleaned CSV + ek text report (kya-kya kiya) save karta hai
# Run karne ka tarika:

# bash
# python data_cleaning_bot.py input_file.csv
# python data_cleaning_bot.py input_file.xlsx output_file.csv
# Bas pandas, numpy install hone chahiye (pip install pandas numpy openpyxl — openpyxl Excel ke liye).

# Chaho toh isse aur extend kar sakta hoon — jaise ek Streamlit web UI bana doon jahan file upload karo aur browser mein hi cleaned data dikhe. Bataana agar interested ho.


# Data cleaning bot
# PY 






# Claude is AI and can make mistakes. Please double-check responses.
# Data cleaning bot · PY
# """
# =========================================================
# AUTOMATED DATA CLEANING BOT
# =========================================================
# Ye script kisi bhi CSV/Excel file ko automatically clean 
# karta hai aur ek cleaning report generate karta hai.
 
# Usage:
#     python data_cleaning_bot.py input_file.csv
#     python data_cleaning_bot.py input_file.xlsx
 
# Author: Data Cleaning Bot
# =========================================================
# """
 
import pandas as pd
import numpy as np
import re
import sys
import os
from datetime import datetime
 
 
class DataCleaningBot:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.original_shape = None
        self.report = []  # log of every action taken
 
    # -----------------------------------------------------
    # STEP 0: Load File
    # -----------------------------------------------------
    def load_data(self):
        ext = os.path.splitext(self.filepath)[1].lower()
        try:
            if ext == ".csv":
                self.df = pd.read_csv(self.filepath)
            elif ext in [".xlsx", ".xls"]:
                self.df = pd.read_excel(self.filepath)
            else:
                raise ValueError("Sirf .csv, .xlsx, .xls files supported hain.")
        except Exception as e:
            print(f"❌ File load karne mein error: {e}")
            sys.exit(1)
 
        self.original_shape = self.df.shape
        self._log(f"File loaded: {self.filepath}")
        self._log(f"Original shape: {self.original_shape[0]} rows x {self.original_shape[1]} columns")
        return self
 
    def _log(self, message):
        self.report.append(message)
        print(f"  -> {message}")
 
    # -----------------------------------------------------
    # STEP 1: Clean Column Names
    # -----------------------------------------------------
    def clean_column_names(self):
        print("\n[1] Cleaning column names...")
        old_cols = list(self.df.columns)
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(r"[^\w]", "", regex=True)
        )
        self._log(f"Column names standardized: {old_cols} -> {list(self.df.columns)}")
        return self
 
    # -----------------------------------------------------
    # STEP 2: Remove Duplicate Rows
    # -----------------------------------------------------
    def remove_duplicates(self):
        print("\n[2] Removing duplicate rows...")
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        after = len(self.df)
        removed = before - after
        self._log(f"Removed {removed} duplicate rows ({before} -> {after})")
        return self
 
    # -----------------------------------------------------
    # STEP 3: Handle Missing Values
    # -----------------------------------------------------
    def handle_missing_values(self, strategy="auto", threshold=0.5):
        """
        strategy:
          'auto'  -> numeric columns: median, categorical: mode
          'drop'  -> drop rows with any missing value
          'zero'  -> fill numeric with 0, categorical with 'Unknown'
        threshold -> agar kisi column mein missing % > threshold, toh column drop kar do
        """
        print("\n[3] Handling missing values...")
 
        # Drop columns jinme missing values threshold se zyada hain
        missing_pct = self.df.isnull().mean()
        cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
        if cols_to_drop:
            self.df.drop(columns=cols_to_drop, inplace=True)
            self._log(f"Dropped columns with >{int(threshold*100)}% missing data: {cols_to_drop}")
 
        if strategy == "drop":
            before = len(self.df)
            self.df.dropna(inplace=True)
            self._log(f"Dropped {before - len(self.df)} rows with missing values")
 
        else:
            for col in self.df.columns:
                missing_count = self.df[col].isnull().sum()
                if missing_count == 0:
                    continue
 
                if strategy == "zero":
                    if pd.api.types.is_numeric_dtype(self.df[col]):
                        self.df[col] = self.df[col].fillna(0)
                    else:
                        self.df[col] = self.df[col].fillna("Unknown")
                else:  # auto strategy
                    if pd.api.types.is_numeric_dtype(self.df[col]):
                        median_val = self.df[col].median()
                        self.df[col] = self.df[col].fillna(median_val)
                        self._log(f"Column '{col}': filled {missing_count} missing values with median ({median_val})")
                    else:
                        mode_val = self.df[col].mode()
                        fill_val = mode_val[0] if not mode_val.empty else "Unknown"
                        self.df[col] = self.df[col].fillna(fill_val)
                        self._log(f"Column '{col}': filled {missing_count} missing values with mode ('{fill_val}')")
        return self
 
    # -----------------------------------------------------
    # STEP 4: Clean String / Text Columns
    # -----------------------------------------------------
    def clean_text_columns(self):
        print("\n[4] Cleaning text/string columns...")
        text_cols = self.df.select_dtypes(include=["object"]).columns
        for col in text_cols:
            self.df[col] = (
                self.df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )
            # Title case common categorical-looking columns
            if self.df[col].nunique() < 50:
                self.df[col] = self.df[col].str.title()
        self._log(f"Cleaned whitespace/casing in text columns: {list(text_cols)}")
        return self
 
    # -----------------------------------------------------
    # STEP 5: Fix Data Types
    # -----------------------------------------------------
    def fix_data_types(self):
        print("\n[5] Fixing data types...")
        for col in self.df.columns:
            # Try numeric conversion
            if self.df[col].dtype == "object":
                converted = pd.to_numeric(self.df[col], errors="coerce")
                if converted.notnull().mean() > 0.9:  # 90%+ values valid numbers
                    self.df[col] = converted
                    self._log(f"Column '{col}' converted to numeric")
                    continue
 
                # Try date conversion
                if any(k in col.lower() for k in ["date", "time", "dob", "created", "updated"]):
                    try:
                        self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
                        self._log(f"Column '{col}' converted to datetime")
                    except Exception:
                        pass
        return self
 
    # -----------------------------------------------------
    # STEP 6: Detect & Handle Outliers (IQR method)
    # -----------------------------------------------------
    def handle_outliers(self, method="clip"):
        """
        method: 'clip' -> outliers ko boundary values pe cap karo
                'remove' -> outlier rows hata do
                'flag' -> sirf report karo, kuch mat karo
        """
        print("\n[6] Detecting outliers (IQR method)...")
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
 
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
 
            outlier_mask = (self.df[col] < lower) | (self.df[col] > upper)
            n_outliers = outlier_mask.sum()
 
            if n_outliers == 0:
                continue
 
            if method == "clip":
                self.df[col] = self.df[col].clip(lower=lower, upper=upper)
                self._log(f"Column '{col}': {n_outliers} outliers clipped to range [{lower:.2f}, {upper:.2f}]")
            elif method == "remove":
                self.df = self.df[~outlier_mask]
                self._log(f"Column '{col}': {n_outliers} outlier rows removed")
            elif method == "flag":
                self._log(f"Column '{col}': {n_outliers} outliers detected (not modified)")
        return self
 
    # -----------------------------------------------------
    # STEP 7: Validate Common Fields (email, phone, etc.)
    # -----------------------------------------------------
    def validate_common_fields(self):
        print("\n[7] Validating common fields (email, phone)...")
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        phone_pattern = r"^\+?\d{10,13}$"
 
        for col in self.df.columns:
            col_lower = col.lower()
            if "email" in col_lower:
                invalid = ~self.df[col].astype(str).str.match(email_pattern, na=False)
                n_invalid = invalid.sum()
                if n_invalid > 0:
                    self._log(f"Column '{col}': {n_invalid} invalid email formats flagged")
                    self.df[f"{col}_valid"] = ~invalid
 
            if "phone" in col_lower or "mobile" in col_lower:
                cleaned_phone = self.df[col].astype(str).str.replace(r"[^\d+]", "", regex=True)
                invalid = ~cleaned_phone.str.match(phone_pattern, na=False)
                n_invalid = invalid.sum()
                self.df[col] = cleaned_phone
                if n_invalid > 0:
                    self._log(f"Column '{col}': {n_invalid} invalid phone formats flagged")
                    self.df[f"{col}_valid"] = ~invalid
        return self
 
    # -----------------------------------------------------
    # STEP 8: Save Cleaned File + Report
    # -----------------------------------------------------
    def save_output(self, output_path=None):
        print("\n[8] Saving cleaned file and report...")
        base = os.path.splitext(os.path.basename(self.filepath))[0]
        out_dir = os.path.dirname(output_path) if output_path else "."
 
        cleaned_path = output_path or f"{base}_cleaned.csv"
        report_path = os.path.join(out_dir, f"{base}_cleaning_report.txt")
 
        self.df.to_csv(cleaned_path, index=False)
 
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("DATA CLEANING REPORT\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Original file: {self.filepath}\n")
            f.write(f"Original shape: {self.original_shape[0]} rows x {self.original_shape[1]} columns\n")
            f.write(f"Final shape: {self.df.shape[0]} rows x {self.df.shape[1]} columns\n\n")
            f.write("Actions performed:\n")
            f.write("-" * 60 + "\n")
            for i, line in enumerate(self.report, 1):
                f.write(f"{i}. {line}\n")
 
        print(f"\n✅ Cleaned data saved to: {cleaned_path}")
        print(f"✅ Report saved to: {report_path}")
        return cleaned_path, report_path
 
    # -----------------------------------------------------
    # RUN FULL PIPELINE
    # -----------------------------------------------------
    def run_full_pipeline(self, missing_strategy="auto", outlier_method="clip", output_path=None):
        print("=" * 60)
        print("🤖 DATA CLEANING BOT STARTED")
        print("=" * 60)
 
        (
            self.load_data()
            .clean_column_names()
            .remove_duplicates()
            .clean_text_columns()
            .fix_data_types()
            .handle_missing_values(strategy=missing_strategy)
            .handle_outliers(method=outlier_method)
            .validate_common_fields()
        )
 
        cleaned_path, report_path = self.save_output(output_path)
 
        print("\n" + "=" * 60)
        print(f"SUMMARY: {self.original_shape[0]} rows -> {self.df.shape[0]} rows")
        print(f"         {self.original_shape[1]} columns -> {self.df.shape[1]} columns")
        print("=" * 60)
 
        return self.df, cleaned_path, report_path
 
 
# ===========================================================
# COMMAND LINE ENTRY POINT
# ===========================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python data_cleaning_bot.py <input_file.csv/xlsx> [output_file.csv]")
        sys.exit(1)
 
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
 
    bot = DataCleaningBot(input_file)
    bot.run_full_pipeline(
        missing_strategy="auto",   # options: 'auto', 'drop', 'zero'
        outlier_method="clip",     # options: 'clip', 'remove', 'flag'
        output_path=output_file
    )
 
