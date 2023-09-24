"""
rev.2023-09-24
Knapsack: dynamic programming: top-down (recursive)
Rust program: execution times [ms]
  ("Total number of CPU-seconds that the process spent in user mode")
- nan (not a number): not enough memory or timeout exceeded
Using the bash script with the Linux time command:
  - exe_times_statistics_for_multiple_test_cases
  - 10 rounds each test case
  - internal timer off: [no_timer, notimer, timer_off, timeroff]
"""

picks_on = [
    ('01_WEIGHTS4.in', 0),
    ('02_WEIGHTS24_Kreher_Stinson.in', 99),
    ('03_WEIGHTS100_Xu_Xu_et_al.in', 8143),
    ('04_WEIGHTS_TODD_16.in', 0),
    ('04_WEIGHTS_TODD_17.in', 1),
    ('05_WEIGHTS_TODD_18.in', 3),
    ('06_WEIGHTS_TODD_19.in', float('nan')),
    ('06_WEIGHTS_TODD_20.in', float('nan')),
    ('7.in', float('nan'))
]

picks_off = [
    ('01_WEIGHTS4.in', 0),
    ('02_WEIGHTS24_Kreher_Stinson.in', 40),
    ('03_WEIGHTS100_Xu_Xu_et_al.in', 6907,
    ('04_WEIGHTS_TODD_16.in', 0),
    ('04_WEIGHTS_TODD_17.in', 0),
    ('05_WEIGHTS_TODD_18.in', 0),
    ('06_WEIGHTS_TODD_19.in', 0),
    ('06_WEIGHTS_TODD_20.in', 4),
    ('7.in', float('nan'))
]
