"""Smoke tests: both algorithms and the Streamlit app run on a small dataset."""

import os

os.environ.setdefault("MPLBACKEND", "Agg")

import pandas as pd
from streamlit.testing.v1 import AppTest

import sia_algorithms as sia


def test_gras_on_simulation_3():
    df = pd.read_csv("simulation_3.csv")
    h = sia.gras_hierarchy(sia.matrice_implication(df, "gras"))
    assert len({tuple(c) for c in h}) == 48


def test_optimized_on_simulation_3():
    df = pd.read_csv("simulation_3.csv")
    _, hier = sia.optimized_hierarchy(sia.matrice_implication(df, "optimized"), 0.85)
    assert len(hier) == 36


def test_streamlit_app_runs():
    at = AppTest.from_file("streamlit_app.py", default_timeout=120).run()
    assert not at.exception
