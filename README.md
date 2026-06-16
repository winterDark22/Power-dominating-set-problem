# Greedy Heuristics for the Power Dominating Set (PDS) Problem

Undergraduate thesis project — Department of Computer Science and Engineering, BUET.

## Authors
- Sadia Tabassum (1905091)
- Md. Azizul Haque Nadim (1905059)

**Supervisor:** Abu Wasif, Associate Professor, CSE, BUET

---

## Problem Overview

The **Power Dominating Set (PDS)** problem asks for a minimum set of vertices that can observe an entire graph under two rules:
1. **Domination rule** — a selected vertex observes itself and all neighbors
2. **Zero-forcing (propagation) rule** — an observed vertex with exactly one unobserved neighbor forces that neighbor to be observed

It models the optimal placement of **Phasor Measurement Units (PMUs)** in electrical grids for full observability. The problem is NP-hard on general graphs.

---

## What This Repo Contains

```
├── pds_greedy_heuristic.ipynb   # Main notebook — all heuristics, experiments, results
├── datasets/                    # Benchmark instances (BCSPWR, IEEE, PEGASE, RTE)
└── results/                     # CSV exports of solution sizes, runtimes, optimality gaps
```

---

## Heuristics Implemented

| ID | Name | Description |
|----|------|-------------|
| H1 | Degree Greedy | Selects vertex with highest degree at each step |
| H2 | Effective Degree Greedy | Selects vertex maximizing newly observed vertices |
| H3 | Neighbor Count Greedy | Prioritizes vertices by unobserved neighbor count |
| H4 | Semi-Greedy (GRASP-style) | Randomized construction from a restricted candidate list |
| H5 | Twin-Guided Greedy | Seeds from near-twin vertices before greedy phase |

All heuristics are paired with a **post-processing pruning stage** that removes redundant PMUs after construction.

---

## Pruning Methods

- **Naive pruner** — single-pass, tries removing each PMU one by one
- **Fort-based pruner** — uses fort structure to identify removable vertices, reducing closure-set computations by ~50% on large grids

---

## Benchmark Results

Evaluated on **29 power-network instances** spanning:
- BCSPWR series (01–10)
- IEEE standard cases (14, 30, 57, 118, 300 bus)
- PEGASE cases
- Illinois 200
- RTE French grid (up to **9,241 buses**)

**Key finding:** H2 (effective-degree greedy) achieves the lowest optimality gap — **~1.67% average** on large instances after pruning — compared to certified optima from Bläsius & Göttlicher (Algorithmica, 2025).

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

## Key References

- Haynes et al., *Domination in Graphs Applied to Electric Power Networks*, SIAM J. Discrete Math (2002)
- Bläsius & Göttlicher, *Exact Algorithms for the Power Dominating Set Problem*, Algorithmica (2025)
- Jovanovic & Voss, *Fixed set search applied to the power dominating set problem*, Expert Systems (2020)
- Laguna, *GRASP for the power dominating set problem*, Mathematical Programming Computation (2025)
