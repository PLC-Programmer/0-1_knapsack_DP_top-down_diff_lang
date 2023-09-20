"""
Knapsack: dynamic programming: top-down (recursive)
C++ program: execution times [ms] for the 03_WEIGHTS100_Xu_Xu_et_al.in test case
with different g++ optimization options
nan (not a number): not enough memory or timeout exceeded
"""

picks_on = [
    ('g++, g++ -O0', 17092),  # default
    ('g++ -O, O1', 7847),
    ('g++ -Os', 7595),
    ('g++ -O2', 7286),
    ('g++ -O3', 3969),
    ('g++ -Ofast', 3552),
]
