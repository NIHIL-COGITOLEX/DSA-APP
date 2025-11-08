# data_loader.py
import glob
import pandas as pd
from typing import List, Tuple, Dict
from utils import normalize_headers

def glob_default_files(patterns: List[str]) -> List[str]:
    paths = []
    for pat in patterns:
        paths.extend(glob.glob(pat))
    return sorted(set(paths))

def load_multiple_excel(files_or_paths: List[str]) -> Tuple[pd.DataFrame, List[Dict]]:
    frames = []
    manifest = []
    for path in files_or_paths:
        try:
            if str(path).lower().endswith(".csv"):
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path)
            name = str(path)
        except Exception:
            df, name = pd.DataFrame(), str(path)
        if isinstance(df, pd.DataFrame) and not df.empty:
            ndf = normalize_headers(df)
            frames.append(ndf)
            manifest.append({"file": name, "rows": int(len(ndf)), "cols": int(len(ndf.columns)), "columns": list(map(str, ndf.columns))})
        else:
            manifest.append({"file": name, "rows": 0, "cols": 0, "columns": []})
    if frames:
        return pd.concat(frames, ignore_index=True), manifest
    return pd.DataFrame(), manifest

def safe_load_companies_and_pincodes() -> Tuple[pd.DataFrame, List[Dict], pd.DataFrame, List[Dict]]:
    company_patterns = ["company_listings_part*.xlsx", "company_listings*.xlsx", "company_listings*.csv"]
    pincode_patterns = ["pincode_listings_part*.xlsx", "pincode_listings*.xlsx", "pincode_listings*.csv"]

    company_files = glob_default_files(company_patterns)
    pincode_files = glob_default_files(pincode_patterns)

    if not company_files:
        # return empty df + empty manifest but keep object
        company_df, comp_manifest = pd.DataFrame(), []
    else:
        company_df, comp_manifest = load_multiple_excel(company_files)

    if not pincode_files:
        pincode_df, pin_manifest = pd.DataFrame(), []
    else:
        pincode_df, pin_manifest = load_multiple_excel(pincode_files)

    # Normalize fallback for common column naming
    if "BANK" in pincode_df.columns and "BANK_NAME" not in pincode_df.columns:
        pincode_df = pincode_df.rename(columns={"BANK": "BANK_NAME"})

    return company_df, comp_manifest, pincode_df, pin_manifest
