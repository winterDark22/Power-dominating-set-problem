# Greedy Heuristics for the Power Dominating Set (PDS) Problem

Undergraduate thesis project — Department of Computer Science and Engineering, BUET.

## Authors
- Sadia Tabassum
- Azizul Haque Nadim — [GitHub](https://github.com/nadimat-sham)

**Supervisor:** Abu Wasif, Associate Professor, CSE, BUET

---

## Problem Overview

The **Power Dominating Set (PDS)** problem asks for a minimum set of vertices S ⊆ V that observes an entire graph G = (V, E) under two exhaustively applied rules:

1. **Domination rule** — every vertex in S and every neighbor of S is observed: N[S] is observed.
2. **Propagation rule** — if an observed vertex has exactly one unobserved neighbor, that neighbor becomes observed (repeated until no rule applies).

S is a **power dominating set** if all of V is observed after exhaustive application. The goal is to find a minimum such set, called the **power domination number** γ_P(G).

This models the optimal placement of **Phasor Measurement Units (PMUs)** in electrical grids for full observability. PMUs are expensive, but Kirchhoff's and Ohm's laws allow some buses to be inferred for free — which is exactly what the propagation rule captures.

The PDS problem is **NP-hard** even on bipartite, chordal, and planar graphs (Haynes et al., 2002), and strongly inapproximable in general (Aazami, 2008).

---

## Repository Structure

```
├── pds_greedy_heuristic.ipynb   # Main notebook — all heuristics, experiments, results
├── datasets/                    # Benchmark instances (BCSPWR, IEEE, PEGASE, RTE)
├── results/                     # CSV exports of solution sizes, runtimes, optimality gaps
├── extended_abstract.pdf        # Extended abstract
└── 1905059_1905091_defense.pdf  # Defense presentation slides
```

---

## Pipeline

```
Input graph G = (V, E)
        │
        ▼
Greedy construction (H1 / H2 / H3 / H4 / H5)
        │
        ▼
Post-processing pruning (naive or fort-based)
        │
        ▼
Minimal PDS  S
```

All heuristics share a single fast **O(m) observation engine** that applies domination and propagation rules incrementally, processing each edge O(1) times per closure.

---

## Heuristics Implemented

| ID | Name | Selection Rule |
|----|------|----------------|
| H1 | Degree greedy | Highest static degree vertex |
| H2 | Effective-degree greedy | Vertex with the most currently unobserved neighbors, recomputed at each step |
| H3 | Multi-hop greedy | Weighted count of neighbors at distances 1, 2, and 3 |
| H4 | Effective multi-hop greedy | Multi-hop score restricted to unobserved vertices only |
| H5 | Near-twin-guided greedy | Two-phase: seeds from near-twin vertices by degree, then completes with degree-based greedy |

**Generic scheme:** start with S = ∅; while not all vertices are observed, add the vertex with the best score; recompute the observation closure.

### Note on H5 — Near-Twins

Two vertices u, v are **near-twins** if they are adjacent and their neighborhoods differ in only a few vertices. The intuition is that twin classes are redundancy hotspots. In practice, H5 performs poorly on real power grid instances — near-twin seeding leads to over-commitment of local PMUs and results in larger solutions than H2.

---

## Pruning Methods

Greedy solutions contain redundant PMUs. The pruning stage tests each v ∈ S: if S \ {v} still observes all of V, drop v.

### Naive Pruner
Re-runs the full O(m) observation routine for every candidate vertex.

### Fort-Based Pruner
Uses the concept of a **fort** (Smith & Hicks, 2022): a non-empty set F ⊆ V where every vertex outside F has either 0 or ≥ 2 neighbors in F. A fort is a "hard core" that propagation cannot enter from outside — every PDS must place or dominate into each fort.

When a removal fails, the unobserved remainder is a fort — cache it. A vertex that is the sole PMU covering a cached fort is essential: lock it and skip future re-checks.

**Both pruners reach identical minimal sizes.** The fort-based pruner skips ~50% of closure calls, giving ~1.8–2× wall-clock speedup on the largest grids.

---

## Benchmark

Evaluated on **29 power-network instances** spanning:

| Dataset | Cases | Size range |
|---------|-------|------------|
| BCSPWR (SuiteSparse / Harwell–Boeing) | 01–10 | n = 39 to 5,300 |
| Bus admittance cases | 494, 662, 685, 1138 bus | — |
| IEEE standard cases | 14, 30, 57, 118, 300 bus + Illinois 200 | — |
| PEGASE European cases | 1354, 2869, 9241 bus | — |
| RTE French grid | 1888, 1951, 2848, 2868, 6468, 6470 bus | up to 9,241 buses |

---

## Key Results

### Construction quality (raw, un-pruned, single-run)

H2 dominates on every instance. On BCSPWR10 (n = 5,300), solution sizes range from 366 (H2) to 4,465 (H3) — a factor of ~12×.

### Pruning is the great equalizer

After pruning, all five constructors converge to a narrow band (< 5% spread). On BCSPWR10: 327–343. **The pruning stage, not the construction strategy, determines the final solution size.** H2 still yields the smallest pruned set on most graphs.

### Optimality gap vs. certified optima

%Dev = 100 · (|S| − γ_P) / γ_P, compared against certified optima from Bläsius & Göttlicher (2025):

| Instance | γ_P | H1 | H2 | H3 | H4 | H5 |
|----------|-----|-----|-----|------|-----|------|
| IEEE118 | 8 | 25.00 | 12.50 | 25.00 | 0.00 | 25.00 |
| illinois200 | 20 | 5.00 | 0.00 | 45.00 | 0.00 | 5.00 |
| pegase1354 | 176 | 3.41 | 0.57 | 42.61 | 1.14 | 2.84 |
| case1888rte | 235 | 4.68 | 1.28 | 52.77 | 2.13 | 12.34 |
| case2848rte | 352 | 3.41 | 0.85 | 58.81 | 0.85 | 14.77 |
| case6470rte | 745 | 7.65 | 1.21 | 64.83 | 1.21 | 12.89 |
| pegase9241 | 811 | 10.60 | 4.81 | 51.05 | 5.92 | 13.19 |
| **Average** | | **8.54** | **3.03** | **48.58** | **1.61** | **12.29** |

**H2 achieves the lowest average optimality gap (~3.03%). H4 is second (~1.61% average but higher on large RTE instances). H3 is far off.**

### Fort-based pruning speedup (H2 solutions)

| Instance | Naive (s) | Fort (s) | Speedup |
|----------|-----------|----------|---------|
| BCSPWR10 | 10.24 | 5.56 | 1.84× |
| case1951rte | 1.74 | 0.75 | 2.34× |
| pegase2869 | 3.47 | 1.74 | 1.99× |
| case6468rte | 17.54 | 9.02 | 1.94× |

---

## Setup

```bash
# Clone the repo
git clone https://github.com/winterDark22/Power-dominating-set-problem
cd Power-dominating-set-problem

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install numpy pandas networkx matplotlib pandapower scipy

# Open notebook
jupyter notebook pds_greedy_heuristic.ipynb
```

---

## References

1. Haynes et al., *Domination in Graphs Applied to Electric Power Networks*, SIAM J. Discrete Math., 2002.
2. Brueni & Heath, *The PMU Placement Problem*, SIAM J. Discrete Math., 2005.
3. Aazami, *Hardness Results and Approximation Algorithms for Some Problems on Graphs*, PhD thesis, 2008.
4. Binkele-Raible & Fernau, *An Exact Exponential Time Algorithm for Power Dominating Set*, Algorithmica, 2012.
5. Jovanovic & Voss, *Greedy/GRASP Heuristics for the Power Dominating Set Problem*, Expert Systems with Applications, 2020.
6. Smith & Hicks, *Optimal Sensor Placement in Power Grids: Fort-based Branch-and-Cut*, Networks, 2022.
7. Bläsius & Göttlicher, *An Efficient Algorithm for Power Dominating Set*, Algorithmica, 2025.
8. Laguna, *Multiparent Path Relinking: An Application to the Power Dominating Set Problem*, Mathematical Programming Computation, 2025.
