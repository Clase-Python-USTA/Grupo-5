
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CRISP-DM · Data Understanding (seguro) AUTO para bases NNA/TI
- Detecta PII por heurísticas (cabeceras y contenido) y anonimiza.
- Normaliza columnas (quitar tildes/espacios -> guiones bajos).
- Resume / perfila / grafica variables y cruces auto-seleccionados.
Uso:
  python class_du_secure_auto_nna.py --input base.xlsx --sheet BD --sep auto
"""

import argparse, json, os, re, hashlib, unicodedata
from typing import Optional, Union, Dict, Any, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==================
# UTILIDADES GENERALES
# ==================

def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)

def _strip_accents(s: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", str(s)) if not unicodedata.combining(ch))

def normalize_text(s: str) -> str:
    s = _strip_accents(str(s)).strip()
    s = re.sub(r"\s+", " ", s)
    return s

_EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
_PHONE = re.compile(r'\b(?:\+?\d[\s-]?){8,}\b')

def scrub_free_text(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s)
    s = _EMAIL.sub("[EMAIL]", s)
    s = _PHONE.sub("[TEL]", s)
    return normalize_text(s)

def hash_value(val: str, salt: str = "secure_salt_v1") -> str:
    if pd.isna(val) or str(val).strip() == "":
        return ""
    return hashlib.sha256((salt + str(val)).encode("utf-8")).hexdigest()[:12]

def read_any(path: str, sep: Optional[str] = "auto", sheet: Union[int, str, None] = None) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")
    lower = path.lower()
    if lower.endswith((".xls", ".xlsx")):
        return pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
    if lower.endswith(".csv"):
        if sep == "auto":
            for candidate in [",", ";", "\t", "|"]:
                try:
                    df = pd.read_csv(path, sep=candidate)
                    if df.shape[1] > 1:
                        return df
                except Exception:
                    continue
            return pd.read_csv(path)
        return pd.read_csv(path, sep=sep)
    raise ValueError("Unsupported file type. Use .csv or .xlsx")

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    cols2 = []
    for c in out.columns:
        c2 = normalize_text(c)
        c2 = re.sub(r"\s+", " ", c2).strip().replace(" ", "_")
        cols2.append(c2)
    out.columns = cols2
    return out

def safe_filename(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)[:150]

# ==================
# DETECCIÓN PII
# ==================

HEADER_PII_PATTERNS = [
    r'\bNOMBRE\b', r'\bAPELLIDO', r'\bDOC(U|)MENT', r'\bIDENTIFICACI(ON|ÓN)',
    r'\bCEDULA|\bC[EÉ]DULA', r'\bDIREC', r'\bCORREO|\bEMAIL',
    r'\bTELEF', r'\bCELULAR', r'\bFACTURA', r'\bCONTRATO', r'\bCUENTA\b',
    r'\bUSUARIO\b', r'\bCONTACTO', r'\bRESPONSABLE', r'\bACUDIENTE', r'\bM[AE]DICO', r'\bPROFESIONAL'
]
HEADER_HASH_PATTERNS = [
    r'\bENCUESTADOR\b', r'\bENTREVISTADOR\b', r'\bUSUARIO\b', r'\bPROFESIONAL\b'
]
HEADER_FREETEXT_PATTERNS = [
    r'\bOTRO', r'\bOBSERVA', r'\bCOMENT', r'\bDESCRIP', r'\bNOTA'
]

def detect_cols(patterns: List[str], columns: List[str]) -> List[str]:
    acc = []
    for p in patterns:
        rx = re.compile(p, flags=re.IGNORECASE)
        acc.extend([c for c in columns if rx.search(c)])
    # quitar duplicados preservando orden
    seen = set()
    out = []
    for c in acc:
        if c not in seen:
            out.append(c); seen.add(c)
    return out

def pii_config_from_headers(df: pd.DataFrame) -> Dict[str, List[str]]:
    cols = list(df.columns)
    drop_cols = detect_cols(HEADER_PII_PATTERNS, cols)
    hash_cols = detect_cols(HEADER_HASH_PATTERNS, cols)
    freetext_cols = detect_cols(HEADER_FREETEXT_PATTERNS, cols)
    return {"drop": drop_cols, "hash": hash_cols, "freetext": freetext_cols}

def safe_copy(df: pd.DataFrame, cfg: Dict[str, List[str]]) -> pd.DataFrame:
    out = df.copy()
    # Hash
    for c in cfg.get("hash", []):
        if c in out.columns:
            out[c] = out[c].map(lambda v: hash_value(v))
    # Text cleaning
    for c in out.select_dtypes(include=["object", "string"]).columns:
        if c in cfg.get("drop", []):
            continue
        if c in cfg.get("freetext", []):
            out[c] = out[c].map(scrub_free_text)
        else:
            out[c] = out[c].map(normalize_text)
    keep = [c for c in out.columns if c not in cfg.get("drop", [])]
    return out[keep]

# ==================
# PERFILAMIENTO Y GRÁFICOS
# ==================

def data_dictionary(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "column": df.columns,
        "dtype": [str(t) for t in df.dtypes.values],
        "non_null": df.notna().sum().values,
        "nulls": df.isna().sum().values,
        "null_pct": (df.isna().mean().values * 100).round(2),
        "n_unique": df.nunique(dropna=True).values,
    })

def quality_flags(df: pd.DataFrame, high_card_threshold: int = 50, const_threshold: float = 0.99) -> Dict[str, Any]:
    flags: Dict[str, Any] = {}
    const_like = []
    for c in df.columns:
        vc = df[c].value_counts(dropna=True, normalize=True)
        if len(vc) and vc.iloc[0] >= const_threshold:
            const_like.append(c)
    flags["constant_like"] = const_like
    high_card = []
    for c in df.select_dtypes(include=["object", "string"]).columns:
        if df[c].nunique(dropna=True) > high_card_threshold:
            high_card.append(c)
    flags["high_cardinality"] = high_card
    flags["duplicate_rows"] = int(df.duplicated().sum())
    candidate_ids = [c for c in df.columns if df[c].is_unique]
    flags["candidate_ids"] = candidate_ids
    return flags

def plot_missing_bar(df: pd.DataFrame, out_path: str, top: Optional[int] = None) -> None:
    miss = df.isna().mean().sort_values(ascending=False)
    if top: miss = miss.head(top)
    plt.figure(); miss.plot(kind="bar"); plt.title("Porcentaje de valores faltantes por columna")
    plt.ylabel("Proporción"); plt.tight_layout(); plt.savefig(out_path); plt.close()

def plot_correlation(df: pd.DataFrame, out_path: str) -> None:
    num_df = df.select_dtypes(include=[np.number])
    if num_df.shape[1] < 2: return
    corr = num_df.corr(numeric_only=True)
    plt.figure(); plt.imshow(corr.values, interpolation="nearest")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Matriz de correlaciones"); plt.colorbar(); plt.tight_layout()
    plt.savefig(out_path); plt.close()

def bar_top_counts(s: pd.Series, out_path: str, top: int = 20, title: str = "") -> None:
    vc = s.value_counts(dropna=False).head(top)[::-1]
    plt.figure(); vc.plot(kind="barh")
    plt.title(title or (s.name or "Top categorías"))
    plt.xlabel("count"); plt.tight_layout(); plt.savefig(out_path); plt.close()

def bar_top_pairs(df: pd.DataFrame, cols: List[str], out_path: str, top: int = 30, title: str = "") -> None:
    ct = (df.groupby(cols).size().reset_index(name="count").sort_values("count", ascending=False).head(top))
    labels = ct[cols[0]].astype(str) + " | " + ct[cols[1]].astype(str)
    counts = ct["count"].values
    plt.figure(); y = np.arange(len(counts)); plt.barh(y, counts); plt.yticks(y, labels)
    plt.title(title or f"Top pares: {cols[0]} × {cols[1]}"); plt.xlabel("count")
    plt.tight_layout(); plt.savefig(out_path); plt.close()

def vc_to_csv(s: pd.Series, out: str, top: Optional[int] = None) -> None:
    vc = s.value_counts(dropna=False)
    if top: vc = vc.head(top)
    vc.to_csv(out, header=["count"])

# ==================
# AGRUPACIONES AUTO POR PALABRAS CLAVE
# ==================

GROUP_KEYWORDS = {
    "demografia": ["EDAD","SEXO","GENERO","ETNIA","ESTADO_CIVIL","ESCOLARIDAD","OCUPACION","NACIONALIDAD"],
    "territorial_acceso": ["DEPARTAMENTO","MUNICIPIO","LOCALIDAD","BARRIO","ZONA","DIRECCION"],
    "salud_nutricion": ["PESO","TALLA","NUTRIC","GESTACION","SALUD","VACUNA"],
    "educacion": ["COLEGIO","GRADO","ESCOLAR","INASISTENCIA","EDUCACION"],
    "intervencion": ["INTERVENCION","SEGUIMIENTO","CIERRE","REPOSICION","RESULTADOS"],
    "riesgos": ["RIESGO","VIOLENCIA","ABUSO","TRABAJO_INFANTIL","EXPLOTACION"],
}

def auto_group_columns(columns: List[str]) -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = {k: [] for k in GROUP_KEYWORDS.keys()}
    for c in columns:
        for g, keys in GROUP_KEYWORDS.items():
            if any(k in c.upper() for k in keys):
                groups[g].append(c)
    # eliminar grupos vacíos
    return {g: cols for g, cols in groups.items() if cols}

# ==================
# CLI
# ==================

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="CRISP-DM · Data Understanding (seguro AUTO) + figuras")
    ap.add_argument("--input", required=True, help="Ruta al archivo (.xlsx/.csv)")
    ap.add_argument("--sep", default="auto", help="Separador CSV (auto, ',', ';', '\\t', '|')")
    ap.add_argument("--sheet", default=None, help="Hoja Excel (índice o nombre)")
    ap.add_argument("--outdir", default="reports_auto", help="Carpeta de salida (reportes)")
    ap.add_argument("--top", type=int, default=30, help="Top-N para tablas y barras categóricas")
    ap.add_argument("--high_card_threshold", type=int, default=50, help="Umbral alta cardinalidad")
    ap.add_argument("--const_threshold", type=float, default=0.99, help="Umbral cuasi-constante")
    ap.add_argument("--cross", nargs="*", default=None, help="Cruces auto: pasar 2+ nombres de columnas normalizadas")
    return ap.parse_args()

def main() -> None:
    args = parse_args()

    # 1) Carpetas
    fig_dir = os.path.join(args.outdir, "figures")
    fig_groups_dir = os.path.join(fig_dir, "groups")
    fig_cross_dir = os.path.join(fig_dir, "cross")
    ensure_dir(args.outdir); ensure_dir(fig_dir); ensure_dir(fig_groups_dir)
    ensure_dir(fig_cross_dir); ensure_dir("data/interim")
    ensure_dir(os.path.join(args.outdir, "groups")); ensure_dir(os.path.join(args.outdir, "cross"))

    # 2) Cargar
    sheet: Optional[Union[int, str]] = None
    if args.sheet is not None:
        try: sheet = int(args.sheet)
        except ValueError: sheet = args.sheet
    df_raw = read_any(args.input, sep=args.sep, sheet=sheet)
    df = normalize_columns(df_raw)

    # 3) Anonimización / segura (auto)
    cfg = pii_config_from_headers(df)
    df_safe = safe_copy(df, cfg)
    df_safe.to_csv("data/interim/sample_head.csv", index=False)

    # 4) Diccionario / Flags
    dd = data_dictionary(df_safe)
    dd.to_csv(os.path.join(args.outdir, "data_dictionary.csv"), index=False, encoding="utf-8")
    flags = quality_flags(df_safe, high_card_threshold=args.high_card_threshold, const_threshold=args.const_threshold)
    with open(os.path.join(args.outdir, "quality_flags.json"), "w", encoding="utf-8") as f:
        json.dump(flags, f, ensure_ascii=False, indent=2)

    # 5) Resúmenes
    num = df_safe.select_dtypes(include=[np.number])
    if num.shape[1] > 0:
        num.describe().to_csv(os.path.join(args.outdir, "numeric_summary.csv"))
    cat = df_safe.select_dtypes(exclude=[np.number])

    # Categóricas: Top-N CSV
    for c in cat.columns:
        out_csv = os.path.join(args.outdir, f"{safe_filename(c)}_top_value_counts.csv")
        vc_to_csv(df_safe[c], out_csv, top=args.top)

    # 6) Figuras generales
    plot_missing_bar(df_safe, os.path.join(fig_dir, "missing_bar.png"), top=50)
    plot_correlation(df_safe, os.path.join(fig_dir, "corr_matrix.png"))

    # 7) Claves auto por keywords
    groups = auto_group_columns(list(df_safe.columns))
    for gname, cols in groups.items():
        g_csv_dir = os.path.join(args.outdir, "groups", gname)
        g_fig_dir = os.path.join(fig_groups_dir, gname)
        ensure_dir(g_csv_dir); ensure_dir(g_fig_dir)
        for c in cols:
            vc_to_csv(df_safe[c], os.path.join(g_csv_dir, f"{safe_filename(c)}_value_counts.csv"), top=args.top)
            bar_top_counts(df_safe[c], os.path.join(g_fig_dir, f"{safe_filename(c)}.png"), top=args.top, title=f"{gname} · {c}")

    # 8) Cruces si los pasan (nombres ya normalizados)
    if args.cross and len(args.cross) >= 2:
        cols_exist = [c for c in args.cross if c in df_safe.columns]
        if len(cols_exist) >= 2:
            # todas las combinaciones pares adyacentes
            for i in range(len(cols_exist)-1):
                pair = [cols_exist[i], cols_exist[i+1]]
                ct = (df_safe.groupby(pair).size().reset_index(name="count").sort_values("count", ascending=False))
                ct.to_csv(os.path.join(args.outdir, "cross", f"{safe_filename(cols_exist[i] + '_x_' + cols_exist[i+1])}.csv"), index=False)
                bar_top_pairs(df_safe, pair, os.path.join(fig_cross_dir, f"{safe_filename(cols_exist[i] + '_x_' + cols_exist[i+1])}_top_pairs.png"), top=args.top, title=f"Top pares · {pair[0]} × {pair[1]}")

    # 9) Mensaje final
    print("[OK] Data Understanding seguro AUTO + figuras completado.")
    print(f"    Filas x Columnas (post-seguro): {df_safe.shape[0]} x {df_safe.shape[1]}")
    print(f"    Reportes: {os.path.abspath(args.outdir)}")
    print(f"    Figuras: {os.path.abspath(fig_dir)}")

if __name__ == "__main__":
    main()
