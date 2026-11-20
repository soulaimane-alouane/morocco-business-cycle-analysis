from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.filters.hp_filter import hpfilter
from scipy.stats import pearsonr

# Répertoire principal du projet
BASE_DIR = Path(__file__).resolve().parent

# Chemin du fichier de données
DATA_PATH = BASE_DIR / "data" / "macro_annual.csv"

# Importation des données
df = pd.read_csv(DATA_PATH)

# Contrôles initiaux
print("Dimensions :", df.shape)
print("\nColonnes :")
print(df.columns.tolist())

print("\nPremières observations :")
print(df.head())

print("\nValeurs manquantes :")
print(df.isna().sum())

# =========================================================
# ECO202 — Q6 : Filtre Hodrick-Prescott
# =========================================================

LAMBDA_HP = 100

OUTPUT_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

# Séries positives, filtrées en logarithmes
LOG_VARIABLES = {
    "pib": "pib_reel_mdh",
    "consommation": "consommation_menages_volume_mdh",
    "investissement": "investissement_fbc_volume_mdh",
    "exportations": "exportations_volume_mdh",
    "importations": "importations_volume_mdh",
    "ipc": "ipc_moyen_base2006",
}

# Séries en pourcentage, filtrées en niveaux
RATE_VARIABLES = {
    "tib": "tib_nominal_moyen_pct",
    "inflation": "inflation_ipc_annuelle_pct",
    "taux_reel": "taux_reel_expost_approx_pct",
}

# Vérifications avant calcul
assert len(df) == 13, "La base doit contenir 13 années."
assert df["annee"].tolist() == list(range(2007, 2020))

all_columns = list(LOG_VARIABLES.values()) + list(
    RATE_VARIABLES.values()
)

assert not df[all_columns].isna().any().any(), (
    "Valeurs manquantes détectées."
)

assert (df[list(LOG_VARIABLES.values())] > 0).all().all(), (
    "Impossible de calculer le log d'une valeur non positive."
)

# DataFrames de résultats
trends = pd.DataFrame({"annee": df["annee"]})
cycles = pd.DataFrame({"annee": df["annee"]})

def apply_hp(series, log_transform=False):
    """Renvoie tendance et cycle HP."""
    values = series.astype(float)

    if log_transform:
        values = np.log(values)

    cycle, trend = hpfilter(values, lamb=LAMBDA_HP)

    if log_transform:
        cycle = cycle * 100

    return trend, cycle


# Filtrage des variables en logarithmes
for name, column in LOG_VARIABLES.items():
    trend, cycle = apply_hp(df[column], log_transform=True)

    trends[f"trend_{name}"] = trend.to_numpy()
    cycles[f"cycle_{name}"] = cycle.to_numpy()


# Filtrage des taux en niveaux
for name, column in RATE_VARIABLES.items():
    trend, cycle = apply_hp(df[column])

    trends[f"trend_{name}"] = trend.to_numpy()
    cycles[f"cycle_{name}"] = cycle.to_numpy()


# Exports
trends.to_csv(
    TABLES_DIR / "q6_tendances_hp.csv",
    index=False
)

cycles.to_csv(
    TABLES_DIR / "q6_cycles_hp.csv",
    index=False
)

print("\n=== Q6 : Cycles HP ===")
print(cycles.round(3).to_string(index=False))


# =========================================================
# Graphique 1 : Cycle du PIB réel
# =========================================================

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    cycles["annee"],
    cycles["cycle_pib"],
    marker="o",
    linewidth=2,
    label="Cycle du PIB réel"
)

ax.axhline(0, color="black", linewidth=1)
ax.axvspan(2011, 2015, alpha=0.10)

ax.set_title("Maroc : cycle du PIB réel (2007–2019)")
ax.set_xlabel("Année")
ax.set_ylabel("Écart à la tendance HP (%)")
ax.set_xticks(df["annee"])
ax.grid(alpha=0.25)
ax.legend()

fig.tight_layout()
fig.savefig(
    FIGURES_DIR / "q6_cycle_pib.png",
    dpi=200
)

plt.show()


# =========================================================
# Graphique 2 : Cycles des variables réelles
# =========================================================

fig, axes = plt.subplots(
    3, 2, figsize=(12, 10), sharex=True
)

real_variables = [
    "pib",
    "consommation",
    "investissement",
    "exportations",
    "importations",
]

for ax, name in zip(axes.flat, real_variables):
    ax.plot(
        cycles["annee"],
        cycles[f"cycle_{name}"],
        marker="o"
    )
    ax.axhline(0, color="black", linewidth=1)
    ax.set_title(name.capitalize())
    ax.set_ylabel("Écart (%)")
    ax.grid(alpha=0.25)

# Masquer la dernière case inutilisée
axes.flat[-1].set_visible(False)

for ax in axes[-1]:
    ax.set_xlabel("Année")

fig.suptitle(
    "Maroc : composantes cycliques HP (2007–2019)"
)

fig.tight_layout()
fig.savefig(
    FIGURES_DIR / "q6_cycles_reels.png",
    dpi=200
)

plt.show()

# =========================================================
# Q6 — Complément : IPC et TIB
# =========================================================

# 1. IPC : série observée, tendance HP et cycle

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(10, 7), sharex=True
)

ax1.plot(
    df["annee"],
    df["ipc_moyen_base2006"],
    marker="o",
    label="IPC observé"
)

# La tendance est en logarithmes : on revient
# aux unités de l'indice avec np.exp()
ax1.plot(
    df["annee"],
    np.exp(trends["trend_ipc"]),
    label="Tendance HP (λ = 100)"
)

ax1.set_title("Maroc : IPC et tendance HP (2007–2019)")
ax1.set_ylabel("IPC (base 2006)")
ax1.legend()
ax1.grid(alpha=0.25)

ax2.plot(
    cycles["annee"],
    cycles["cycle_ipc"],
    marker="o"
)

ax2.axhline(0, color="black", linewidth=1)
ax2.axvspan(2011, 2015, alpha=0.10)
ax2.set_xlabel("Année")
ax2.set_ylabel("Écart à la tendance (%)")
ax2.set_xticks(df["annee"])
ax2.grid(alpha=0.25)

fig.tight_layout()
fig.savefig(FIGURES_DIR / "q6_ipc_hp.png", dpi=200)
plt.show()


# 2. TIB : taux observé, tendance HP et cycle

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(10, 7), sharex=True
)

ax1.plot(
    df["annee"],
    df["tib_nominal_moyen_pct"],
    marker="o",
    label="TIB observé"
)

ax1.plot(
    df["annee"],
    trends["trend_tib"],
    label="Tendance HP (λ = 100)"
)

ax1.set_title("Maroc : TIB nominal et tendance HP (2007–2019)")
ax1.set_ylabel("TIB (%)")
ax1.legend()
ax1.grid(alpha=0.25)

ax2.plot(
    cycles["annee"],
    cycles["cycle_tib"],
    marker="o"
)

ax2.axhline(0, color="black", linewidth=1)
ax2.axvspan(2011, 2015, alpha=0.10)
ax2.set_xlabel("Année")
ax2.set_ylabel("Écart (points de %)")
ax2.set_xticks(df["annee"])
ax2.grid(alpha=0.25)

fig.tight_layout()
fig.savefig(FIGURES_DIR / "q6_tib_hp.png", dpi=200)
plt.show()

# =========================================================
# ECO202 — Q8 : Corrélations des composantes cycliques HP
# =========================================================

ALPHA = 0.05

# Variables cycliques disponibles
cycle_columns = [
    col for col in cycles.columns
    if col.startswith("cycle_")
]

cycle_data = cycles[cycle_columns].copy()

# 1. Matrice des corrélations de Pearson
correlation_matrix = cycle_data.corr(method="pearson")

correlation_matrix.to_csv(
    TABLES_DIR / "q8_matrice_correlations.csv"
)

print("\n=== Q8 : Matrice des corrélations ===")
print(correlation_matrix.round(3).to_string())


# 2. Tests des corrélations avec le cycle du PIB
results = []

for variable in cycle_columns:

    if variable == "cycle_pib":
        continue

    sample = cycles[
        ["cycle_pib", variable]
    ].dropna()

    r, p_value = pearsonr(
        sample["cycle_pib"],
        sample[variable]
    )

    results.append({
        "variable": variable,
        "n": len(sample),
        "correlation": r,
        "p_value": p_value,
        "significatif_5pct": p_value < ALPHA
    })


# 3. Tableau de synthèse
q8_results = pd.DataFrame(results)

q8_results.to_csv(
    TABLES_DIR / "q8_tests_pearson_pib.csv",
    index=False
)

print("\n=== Q8 : Corrélations avec le PIB ===")
print(q8_results.round(4).to_string(index=False))