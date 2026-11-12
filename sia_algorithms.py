"""
Oriented hierarchies in statistical implicative analysis (SIA).

This module gathers, as functions, the code of the two notebooks of the
repository:

* Gras_Algorithm.ipynb       -> gras_hierarchy
* Optimized_Algorithm.ipynb  -> optimized_hierarchy

The logic is the one of the notebooks. The notebooks remain the reference.
"""

import math
import time

import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import poisson


# ----------------------------------------------------------------------
# Implication matrix
# ----------------------------------------------------------------------

def intensite_implication(n_x, n_y, n_xy, n, variante="optimized"):
    """
    Implication intensity of x => y.

    variante="gras"      : convention of Gras_Algorithm.ipynb (0 if n_y == n).
    variante="optimized" : convention of Optimized_Algorithm.ipynb (0 if n_x > n_y).
    """
    lamb = n_x * (n - n_y) / n
    if variante == "gras":
        if n_y == n:
            return 0
    else:
        if n_x > n_y:
            return 0
    return 1 - poisson.cdf(n_xy, lamb)


def matrice_implication(donnees, variante="optimized"):
    """
    Implication matrix of a binary table (path of a CSV file or DataFrame).
    """
    df = pd.read_csv(donnees) if isinstance(donnees, str) else donnees
    n = len(df)
    attributs = df.columns
    taille = len(attributs)

    matrice = pd.DataFrame(np.zeros((taille, taille)), index=attributs, columns=attributs)

    for i, x in enumerate(attributs):
        for j, y in enumerate(attributs):
            n_x = df[x].sum()
            n_y = df[y].sum()
            n_xy = ((df[x] == 1) & (df[y] == 0)).sum()
            matrice.iloc[i, j] = intensite_implication(n_x, n_y, n_xy, n, variante)
    return matrice


# ----------------------------------------------------------------------
# Gras's algorithm
# ----------------------------------------------------------------------

def cohesion_2(p):
    if p < 0.5 or p <= 0 or p >= 1:
        return 0
    elif p == 1:
        return 1
    else:
        try:
            H = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
            return (1 - H**2) ** 0.5
        except ValueError:
            return 0


def cohesion(C, matrice):
    if len(C) == 1:
        return 1
    r = len(C)
    produit = 1
    liste = list(C)
    for i in range(r):
        for j in range(i + 1, r):
            a, b = liste[i], liste[j]
            produit *= cohesion_2(matrice.loc[a, b])
    return produit ** (2 / (r * (r - 1)))


def gras_hierarchy(mat):
    """Gras's algorithm. Returns the list h of the classes, in order of construction."""
    E = mat.index
    h = []

    for i in E:
        h.append([i])
    classes = h.copy()
    m = 1
    while m > 0:
        candidat = []
        for i in classes:
            for j in classes:
                if set(i) & set(j) == set([]):
                    candidat.append(i + j)

        maxi = 0
        for clas in candidat:
            if cohesion(clas, mat) > maxi:
                maxi = cohesion(clas, mat)
                meilleur_clas = clas
        h.append(meilleur_clas)
        classes.append(meilleur_clas)
        for a in classes:
            for b in classes:
                if a + b == meilleur_clas:
                    if a in classes:
                        classes.remove(a)
                    if b in classes and b != a:
                        classes.remove(b)
        m = maxi
    return h


# ----------------------------------------------------------------------
# Optimized algorithm
# ----------------------------------------------------------------------

def graphe_implication(matrice, alpha):
    """Directed graph of implications: i -> j if matrice.loc[i, j] > alpha."""
    G = nx.DiGraph()
    for i in matrice.index:
        for j in matrice.columns:
            if matrice.loc[i, j] > alpha:
                G.add_edge(i, j, weight=matrice.loc[i, j])
    return G


def dessiner_graphe(G, ax=None, taille_noeuds=700, taille_police=12, poids=True):
    """Draw the implication graph (same layout as in the notebook)."""
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42, k=1.5)
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=taille_noeuds, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=taille_police, font_family="sans-serif", ax=ax)
    if poids:
        edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, ax=ax)
    ax.set_title("Implication graph: phi(i -> j) > alpha")
    ax.axis("off")
    return ax


def consequent(G):
    resultats = {}
    for i in G.nodes:
        atteints = nx.descendants(G, i)
        resultats[i] = sorted(atteints)
        resultats[i].append(i)
    return resultats


def premisse(G):
    G_transpose = G.reverse(copy=True)
    resultats = {}
    for i in G.nodes:
        antecedents = nx.descendants(G_transpose, i)
        resultats[i] = sorted(antecedents)
        resultats[i].append(i)
    return resultats


def treillis(G):
    consequents = consequent(G)
    antecedents = premisse(G)
    list_antecedents = list(antecedents.values())
    list_consequents = list(consequents.values())
    concatenate = list_antecedents + list_consequents
    for x in G.nodes:
        concatenate.append([x])  # singleton class {x}
    return concatenate


def tri_topologique(resultats):
    E_arcs = []
    resultats = [tuple(sorted(C)) for C in resultats]
    resultats = list(set(resultats))
    in_degre = {C: 0 for C in resultats}

    for Ci in resultats:
        for Cj in resultats:
            if Ci != Cj and set(Ci).issubset(set(Cj)) and len(Ci) < len(Cj):
                E_arcs.append((Ci, Cj))
                in_degre[Cj] += 1

    S = sorted([C for C in resultats if in_degre[C] == 0], key=len)
    L = []

    while S:
        Ci = S.pop(0)
        L.append(Ci)
        for arc in E_arcs[:]:
            if arc[0] == Ci:
                Cj = arc[1]
                E_arcs.remove(arc)
                in_degre[Cj] -= 1
                if in_degre[Cj] == 0:
                    S.append(Cj)
        S = sorted(S, key=len)

    return [list(C) for C in L]


def hierarchie_orientee(resultats):
    l = resultats
    retire = []
    for Ci in l:
        for Cj in l:
            if len(Ci) < len(Cj) and set(Ci) & set(Cj) != set() and set(Ci) & set(Cj) != set(Ci):
                retire.append(Cj)
    return [classe for classe in l if classe not in retire]


def optimized_hierarchy(mat, alpha=0.85):
    """Optimized algorithm. Returns (graph G, oriented hierarchy)."""
    G = graphe_implication(mat, alpha)
    T = treillis(G)
    return G, hierarchie_orientee(tri_topologique(T))


# ----------------------------------------------------------------------
# Helper for comparisons
# ----------------------------------------------------------------------

def chronometre(f, *args, **kwargs):
    """Return (result, elapsed seconds)."""
    t0 = time.perf_counter()
    res = f(*args, **kwargs)
    return res, time.perf_counter() - t0
