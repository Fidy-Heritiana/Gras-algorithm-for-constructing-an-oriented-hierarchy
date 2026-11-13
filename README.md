# Comparison of Gras's algorithm and an optimized algorithm
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Fidy-Heritiana/Gras-algorithm-for-constructing-an-oriented-hierarchy/blob/main/demo.ipynb)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Fidy-Heritiana/Gras-algorithm-for-constructing-an-oriented-hierarchy/main?labpath=demo.ipynb)
[![Streamlit app](https://img.shields.io/badge/Streamlit-Live%20app-FF4B4B?logo=streamlit&logoColor=white)](https://gras-oriented-hierarchy.streamlit.app/)
[![CI](https://github.com/Fidy-Heritiana/Gras-algorithm-for-constructing-an-oriented-hierarchy/actions/workflows/ci.yml/badge.svg)](https://github.com/Fidy-Heritiana/Gras-algorithm-for-constructing-an-oriented-hierarchy/actions/workflows/ci.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24185484.svg)](https://doi.org/10.5281/zenodo.24185484)

The two algorithms presented here enable the construction of a directed hierarchy, a data analysis model in statistical implicative analysis (SIA), in the form of a classification. The first is Gras's algorithm. It was presented by this author, the founder of SIA, in several of his works. The second algorithm proposes another, more efficient method of constructing it.

To test both algorithms, use the simulated datasets `simulation_1.csv` to `simulation_20.csv` (from 10 to 200 variables) at the root of this repository. Click a badge above to run `demo.ipynb` in your browser, without installing anything. An interactive web application is also available: https://gras-oriented-hierarchy.streamlit.app/

## The article in brief

Gras's algorithm builds an oriented hierarchy in cubic time. The article studies oriented hierarchies as combinatorial objects, which can be enumerated with analytic combinatorics (on average they contain 3/2 blocks). It then uses the correspondence between the statistical implication graph and the hierarchy to build it through a lattice and a topological sort, in at most quadratic time. Experiments on 20 simulated data sets (10 to 200 variables) show that the optimized algorithm becomes faster than Gras's algorithm beyond a few dozen variables.

A longer summary, with the main formulas, is in [ARTICLE_SUMMARY.md](ARTICLE_SUMMARY.md).
You may consult the following article for further understanding:
## Associated Publication

**Title:** Combinatorial and Algorithmic Analysis of Oriented Hierarchies in Implicative Statistical Analysis  
**Authors:** Andrianarivony Fidy Heritiana, Vlady Ravelomanana  
**Journal:** Annals of Mathematics and Artificial Intelligence  
**Publisher:** Springer Nature  
**Year:** 2025  
**DOI:** 10.1007/s10472-025-10001-1  
**Link:** https://link.springer.com/article/10.1007/s10472-025-10001-1

**Abstract:**  
This paper introduces a novel and more efficient method for constructing oriented hierarchies within the framework of Statistical Implicative Analysis. The primary focus of this study is the computational complexity of the original algorithm proposed by Gras, whose cubic time complexity is established in this work. To address this limitation, a detailed combinatorial analysis of hierarchical structures is performed, leveraging tools from analytic combinatorics. This methodology facilitates the enumeration of the number of possible configurations as a function of input size and enables the investigation of both the depth and width characteristics of the hierarchy’s block structure. This study then proposes a reconstruction algorithm based on a formal correspondence between the statistical implication graph and the oriented hierarchy. The proposed method achieves quadratic worst-case complexity, thereby resulting in a substantial improvement in computational performance. Moreover, the analytic framework also makes it possible to characterise the average-case behaviour of the algorithm. The findings of the comparative computational experiments demonstrate the clear advantage of the proposed method over Gras’s algorithm, both in terms of execution time and overall algorithmic efficiency.

**Keywords:** Implicative Statistical Analysis, Oriented Hierarchies, Algorithm Analysis, Combinatorics, Order Theory

