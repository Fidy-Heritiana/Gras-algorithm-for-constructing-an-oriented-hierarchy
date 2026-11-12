from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

import sia_algorithms as sia

DOSSIER = Path(__file__).resolve().parent
REPO_URL = "https://github.com/Fidy-Heritiana/Gras-algorithm-for-constructing-an-oriented-hierarchy"
MAX_VARIABLES = 50
MAX_LIGNES = 5000

st.set_page_config(page_title="Oriented hierarchies (SIA)", page_icon="🌳", layout="wide")

st.title("Gras's algorithm and the optimized algorithm")
st.markdown(
    "Construction of an **oriented hierarchy** in statistical implicative analysis. "
    f"Interactive companion to the [GitHub repository]({REPO_URL}) and to the article "
    "*Combinatorial and Algorithmic Analysis of Oriented Hierarchies in Implicative "
    "Statistical Analysis* (Annals of Mathematics and Artificial Intelligence)."
)

# ----------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------


def valider_csv(df):
    """Return an error message, or None if the table can be used."""
    if df.shape[1] < 2 or df.shape[1] > MAX_VARIABLES:
        return f"The table must have between 2 and {MAX_VARIABLES} columns (it has {df.shape[1]})."
    if df.shape[0] < 2 or df.shape[0] > MAX_LIGNES:
        return f"The table must have between 2 and {MAX_LIGNES} rows (it has {df.shape[0]})."
    if df.isnull().any().any():
        return "The table contains missing values."
    if not all(pd.api.types.is_numeric_dtype(t) or pd.api.types.is_bool_dtype(t) for t in df.dtypes):
        return "All columns must be numeric (0 or 1)."
    if not set(np.unique(df.values)).issubset({0, 1}):
        return "All values must be 0 or 1."
    if len(set(df.columns)) != df.shape[1]:
        return "Column names must be distinct."
    return None


@st.cache_data(show_spinner=False)
def charger_simulation(numero):
    return pd.read_csv(DOSSIER / f"simulation_{numero}.csv")


# ----------------------------------------------------------------------
# Computations (cached)
# ----------------------------------------------------------------------


@st.cache_data(show_spinner=False)
def calcul_gras(df):
    mat = sia.matrice_implication(df, "gras")
    try:
        h, t = sia.chronometre(sia.gras_hierarchy, mat)
    except UnboundLocalError:
        # no class with a positive cohesion: only the single variables remain
        h, t = [[v] for v in df.columns], 0.0
    # the loop of the notebook appends its last class a second time: each class is kept once
    return list(dict.fromkeys(tuple(c) for c in h)), t


@st.cache_data(show_spinner=False)
def calcul_optimise(df, alpha):
    mat = sia.matrice_implication(df, "optimized")
    (G, hier), t = sia.chronometre(sia.optimized_hierarchy, mat, alpha)
    return mat, G, [tuple(c) for c in hier], t


@st.cache_data(show_spinner=False)
def benchmark(alpha):
    lignes = []
    for k in range(1, 7):
        d = charger_simulation(k)
        _, tg = sia.chronometre(sia.gras_hierarchy, sia.matrice_implication(d, "gras"))
        _, to = sia.chronometre(
            sia.optimized_hierarchy, sia.matrice_implication(d, "optimized"), alpha
        )
        lignes.append({"variables": d.shape[1], "Gras (s)": tg, "Optimized (s)": to})
    return pd.DataFrame(lignes)


def tableau_classes(classes, nom, fleche):
    lignes = [
        {"algorithm": nom, "size": len(c), "class": fleche.join(str(v) for v in c)}
        for c in classes
        if len(c) >= 2
    ]
    return pd.DataFrame(lignes, columns=["algorithm", "size", "class"])


# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------

st.sidebar.header("Data")
source = st.sidebar.radio("Dataset", ["Simulated dataset", "My own CSV file"])

if source == "Simulated dataset":
    numero = st.sidebar.slider("simulation_<k>.csv", 1, 8, 3)
    df = charger_simulation(numero)
    nom_donnees = f"simulation_{numero}.csv"
    st.sidebar.caption(f"{df.shape[0]} observations, {df.shape[1]} variables.")
else:
    fichier = st.sidebar.file_uploader("CSV file with 0/1 columns", type="csv")
    st.sidebar.caption(
        f"One row per observation, one column per variable, values 0 or 1. "
        f"At most {MAX_VARIABLES} variables and {MAX_LIGNES} rows."
    )
    if fichier is None:
        st.info("Upload a CSV file in the sidebar, or switch to a simulated dataset.")
        st.stop()
    try:
        df = pd.read_csv(fichier)
    except Exception:
        st.error("This file could not be read as a CSV table.")
        st.stop()
    erreur = valider_csv(df)
    if erreur:
        st.error(erreur)
        st.stop()
    nom_donnees = fichier.name

st.sidebar.header("Optimized algorithm")
alpha = st.sidebar.slider("Threshold alpha", 0.50, 0.99, 0.85, 0.01)
st.sidebar.caption("There is an arrow i → j when the implication intensity of i ⇒ j exceeds alpha.")

# ----------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------

with st.spinner("Computing..."):
    h, t_gras = calcul_gras(df)
    mat_opt, G, hier, t_opt = calcul_optimise(df, alpha)

tab_res, tab_graph, tab_time = st.tabs(["Results", "Graph and matrix", "Runtime comparison"])

with tab_res:
    st.subheader(nom_donnees)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Variables", df.shape[1])
    c2.metric("Gras: classes", len(h))
    c3.metric("Optimized: classes", len(hier))
    c4.metric("Speed-up", f"x{t_gras / t_opt:.0f}" if t_opt > 0 and t_gras > 0 else "-")

    st.write(
        f"Running time of the algorithms (without building the implication matrix): "
        f"**Gras {t_gras:.3f} s**, **optimized {t_opt:.3f} s**."
    )

    tg = tableau_classes(h, "Gras", " → ")
    to = tableau_classes(hier, "Optimized", ", ")
    left, right = st.columns(2)
    with left:
        st.markdown(f"**Gras**: {len(tg)} classes with at least 2 variables")
        st.dataframe(tg[["size", "class"]], hide_index=True)
    with right:
        st.markdown(f"**Optimized**: {len(to)} classes with at least 2 variables")
        st.dataframe(to[["size", "class"]], hide_index=True)

    st.download_button(
        "Download the classes (CSV)",
        pd.concat([tg, to]).to_csv(index=False).encode("utf-8"),
        file_name="classes.csv",
        mime="text/csv",
    )
    st.caption(
        "A class of Gras's algorithm is an ordered chain of variables. A class of the optimized "
        "algorithm is listed with its variables sorted. Classes made of a single variable are counted "
        "in the totals but not listed."
    )

with tab_graph:
    left, right = st.columns(2)
    with left:
        st.markdown("**Implication matrix** (optimized convention)")
        fig, ax = plt.subplots(figsize=(5.5, 4.8))
        im = ax.imshow(mat_opt.values, cmap="viridis", vmin=0, vmax=1)
        if mat_opt.shape[0] <= 30:
            ax.set_xticks(range(mat_opt.shape[0]), mat_opt.columns, rotation=90, fontsize=7)
            ax.set_yticks(range(mat_opt.shape[0]), mat_opt.index, fontsize=7)
        fig.colorbar(im, ax=ax, label="implication intensity")
        st.pyplot(fig)
        plt.close(fig)
    with right:
        st.markdown(f"**Implication graph** (arrow i → j when intensity > {alpha})")
        n_noeuds = G.number_of_nodes()
        if n_noeuds == 0:
            st.info("No arrow for this threshold: try a smaller alpha.")
        elif n_noeuds > 40:
            st.info(f"The graph has {n_noeuds} vertices: too many to draw. Choose a smaller dataset.")
        else:
            fig, ax = plt.subplots(figsize=(6.5, 5.5))
            sia.dessiner_graphe(
                G,
                ax=ax,
                taille_noeuds=700 if n_noeuds <= 20 else 350,
                taille_police=10 if n_noeuds <= 20 else 7,
                poids=G.number_of_edges() <= 30,
            )
            st.pyplot(fig)
            plt.close(fig)
        st.caption(f"{n_noeuds} vertices, {G.number_of_edges()} arrows.")

with tab_time:
    st.write(
        "Both algorithms on `simulation_1.csv` to `simulation_6.csv` (10 to 60 variables), "
        "with the threshold alpha chosen in the sidebar."
    )
    if st.button("Run the benchmark"):
        st.session_state["bench_alpha"] = alpha

    if "bench_alpha" in st.session_state:
        with st.spinner("Running..."):
            temps = benchmark(st.session_state["bench_alpha"])
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.plot(temps["variables"], temps["Gras (s)"], marker="o", label="Gras")
        ax.plot(temps["variables"], temps["Optimized (s)"], marker="s", label="Optimized")
        ax.set_yscale("log")
        ax.set_xlabel("number of variables")
        ax.set_ylabel("time (s), log scale")
        ax.legend()
        ax.grid(alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
        st.dataframe(temps.round(4), hide_index=True)

st.divider()
st.caption(f"Source code, notebooks and data: {REPO_URL}")
