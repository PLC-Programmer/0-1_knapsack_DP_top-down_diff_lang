"""
Knapsack: dynamic programming: top-down (recursive)
Rust program : execution times [ms] for various test cases
nan (not a number): not enough memory or timeout exceeded
"""

picks_on = [
    ('01_WEIGHTS4.in', 6),
    ('02_WEIGHTS24_Kreher_Stinson.in', 162),
    ('03_WEIGHTS100_Xu_Xu_et_al.in', 8206),
    ('04_WEIGHTS_TODD_16.in', 23),
    ('04_WEIGHTS_TODD_17.in', 47),
    ('05_WEIGHTS_TODD_18.in', 87),
    ('06_WEIGHTS_TODD_19.in', float('nan')),
    ('06_WEIGHTS_TODD_20.in', float('nan')),
    ('7.in', float('nan'))
]

picks_off = [
    ('01_WEIGHTS4.in', 0),
    ('02_WEIGHTS24_Kreher_Stinson.in', 55),
    ('03_WEIGHTS100_Xu_Xu_et_al.in', 6940),
    ('04_WEIGHTS_TODD_16.in', 0),
    ('04_WEIGHTS_TODD_17.in', 0),
    ('05_WEIGHTS_TODD_18.in', 0),
    ('06_WEIGHTS_TODD_19.in', 1),
    ('06_WEIGHTS_TODD_20.in', 2),
    ('7.in', float('nan'))
]
