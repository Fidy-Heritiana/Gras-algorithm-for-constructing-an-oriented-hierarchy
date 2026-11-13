# The article in detail

**Combinatorial and algorithmic analysis of oriented hierarchies in statistical implicative analysis**
*Annals of Mathematics and Artificial Intelligence* (Springer Nature), 2025.
DOI: [10.1007/s10472-025-10001-1](https://doi.org/10.1007/s10472-025-10001-1)

This page summarises the article and shows where each part is implemented in this repository.

## 1. Context

**Statistical implicative analysis (SIA)** is an exploratory method for binary data, introduced by Régis Gras. It looks for rules of the form "if *a*, then *b*" that are true in most cases, not always. For two binary variables *x* and *y*, the **implication intensity** measures how unlikely it is to observe so few counterexamples (objects with *x* but not *y*) if the variables were independent. With the Poisson approximation,

$$\varphi(x\to y)=1-\sum_{k=0}^{m_{x\wedge\bar y}}\frac{\lambda^k}{k!}e^{-\lambda},\qquad \lambda=\frac{m_x\,m_{\bar y}}{m},$$

where *m* is the number of objects, *m<sub>x</sub>* the number of objects with *x*, and *m<sub>x∧ȳ</sub>* the number of counterexamples.

The **quasi-implication** relation keeps *x → y* when *m<sub>x</sub> ≤ m<sub>y</sub>* and *φ(x → y) ≥ α*, for a threshold *α* in (0.5, 1) chosen by the analyst. Its graph is the **statistical implication graph**.

An **oriented hierarchy** goes one step further: it organises rules into rules about rules (meta-implications) such as *(a → b) → (c → d)*. It is a family of nested **classes**, each class being an *ordered* sequence of variables, for example *(d, b, a, f)* obtained by concatenating *(d, b)* and *(a, f)*. The quality of a class is measured by its **cohesion**: for a pair,

$$\operatorname{coh}(a,b)=\Bigl(1-\bigl[-p\log_2 p-(1-p)\log_2(1-p)\bigr]^2\Bigr)^{1/2}\ \text{ if } p=\varphi(a\to b)\ge 0.5,\ \text{ and } 0 \text{ otherwise,}$$

and for a class of order *r*, the geometric mean of the cohesions of its pairs.

## 2. The problem: Gras's algorithm is cubic

Gras's algorithm starts from the single variables (cohesion 1) and, at each level, keeps the concatenation of two existing classes with the greatest cohesion. It stops when every possible concatenation has zero cohesion. Counting its operations gives

$$s_n = n+\sum_{i=1}^{k}(n-i+1)(n-i)=O(n^3).$$

For large data sets this cost is a serious limit, and the article is the first, to the authors' knowledge, to study it.

## 3. Combinatorial analysis of oriented hierarchies

The article treats oriented hierarchies as combinatorial objects and counts them with analytic combinatorics.

- **Classes are words.** The classes that can be formed on *n* variables form a monoid under concatenation, with ⌊*e*·*n*!⌋ elements.
- **Binary hierarchies.** A binary hierarchy is either a single variable or the concatenation of two binary hierarchies, so *H<sub>b</sub>(z) = z + H<sub>b</sub>(z)²*, that is $H_b(z)=\frac{1-\sqrt{1-4z}}{2}$. The number of binary hierarchies on *n* variables involves the Catalan number *C<sub>n−1</sub>*.
- **Oriented hierarchies.** An oriented hierarchy is a set of binary hierarchies (its blocks), hence *H(z) = exp(H<sub>b</sub>(z))*. Equivalently, for a set of *n* variables,

$$H_n=\sum_{P\in\mathrm{Part}(E)}\ \prod_{j=1}^{m} n_j!\,C_{n_j-1},$$

with *H<sub>n</sub>* = 1, 3, 19, 193, 2721, 49171 for *n* = 1, …, 6, and already 28,875,761,731 for *n* = 10.

- **Number of blocks.** The bivariate series *H(z, u) = exp(u H<sub>b</sub>(z))* counts hierarchies by size and by number of blocks. Singularity analysis at *z = 1/4* shows that the number of blocks has mean **3/2**, variance 1/2 and standard deviation √2/2, with factorial moments (2*r*+1)/2<sup>*r*</sup>. This distribution is determined by its moments (Carleman's criterion). In practice, an oriented hierarchy has one or two blocks: the variables tend to be all linked.
- **Consequences for the algorithms.** The average height of a hierarchy is of order √*n* (2√(2π*n*/3)), and it has on average *n* − 3/2 arcs.
- **Simulation.** Hierarchies are generated at random with a **Boltzmann sampler**: the number of blocks follows a Poisson law of parameter *H<sub>b</sub>(x)*, and each binary hierarchy is a leaf with probability *x / H<sub>b</sub>(x)* and otherwise the concatenation of two independent ones. On 500 runs with target size 100, just under 80% of the hierarchies have one block and about 20% have two.

## 4. A correspondence between the graph and the hierarchy

Cohesion is an increasing function of the implication intensity on [0.5, 1). Ordering pairs by intensity or by cohesion is therefore the same thing, and a statistical implication graph determines an oriented hierarchy: the first class of order 2 is the pair with the greatest intensity, the order of the implications gives the order of the variables in a class, and two classes cannot share a prefix or a suffix without one containing the other.

A **naive algorithm** exploits this correspondence directly: repeatedly take the largest remaining intensity *M[i][j]*, record the implication *i → j*, and delete row *i*, column *j* and the symmetric entry *M[j][i]*. It is still cubic.

## 5. The optimized algorithm

For a variable *x*, let *P<sub>x</sub> = {t : t → x}* be its **class of premises** and *G<sub>x</sub> = {t : x → t}* its **class of consequents**.

1. **Premises and consequents.** The article proves that the premise classes, with the empty set, form a lower semi-lattice, that the consequent classes, with the whole set, form an upper semi-lattice, and that their union is a **lattice** with between *n* and 2*n* classes. (One step relies on a proposition supported by a numerical simulation; an analytic proof remains to be established.)
2. **Topological sorting.** The classes are ordered by inclusion with Kahn's algorithm.
3. **Adjustment.** Classes that violate the nesting axiom of an oriented hierarchy (two classes must be nested or disjoint) are removed, and every single variable is added as an elementary class.

The cost is **O(*n*²) in the worst case**, and linear in the most favourable case, against O(*n*³) for Gras's algorithm. The threshold *α* controls how dense the implication graph, and therefore the hierarchy, is.

## 6. Computational experiments

Both algorithms were run on twenty simulated data sets with 10 to 200 variables (steps of 10).

- **Running time.** Gras's algorithm is slightly faster only on the smallest data sets. For *n* = 200 it needs 77.3 s against 16.7 s for the optimized algorithm. Between *n* = 100 and *n* = 200, the fitted exponent of *T(n) ∼ c·n<sup>k</sup>* is *k* ≈ 2.83 for Gras (cubic behaviour) and *k* ≈ 1.9 for the optimized algorithm (close to quadratic).
- **Number of classes.** Section 6.2 of the article compares the number of classes produced by both algorithms on the five largest data sets, for *α* from 0.5 to 0.9. For the optimized algorithm the result depends on the threshold, which lets the user target the most selective rules.

## 7. Conclusion and open questions

The article gives the first complexity analysis of the construction of oriented hierarchies, a combinatorial description of these structures, and a lattice-based algorithm that is quadratic in the worst case. Open directions are validation on real data by experts of the field, a choice of *α* guided by applications, and algorithms below quadratic cost.

## Where to find it in this repository

| Article | Repository |
| --- | --- |
| Gras's algorithm (Section 3.3 to 3.4) | `Gras_Algorithm.ipynb`, function `gras_hierarchy` in `sia_algorithms.py` |
| Optimized algorithm (Section 5.3) | `Optimized_Algorithm.ipynb`, function `optimized_hierarchy` in `sia_algorithms.py` |
| Simulated data (Section 6) | `simulation_1.csv` to `simulation_20.csv` (10 to 200 variables) |
| Try both algorithms online | `demo.ipynb` (Colab or Binder) and the [Streamlit application](https://gras-oriented-hierarchy.streamlit.app/) |
