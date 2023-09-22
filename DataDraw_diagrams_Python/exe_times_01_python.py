"""
rev.2023-09-22
Knapsack: dynamic programming: top-down (recursive)
Python program: execution times [ms]
  ("Total number of CPU-seconds that the process spent in user mode")
- nan (not a number): not enough memory or timeout exceeded
Using the bash script with the Linux time command:
  - exe_times_statistics_for_multiple_test_cases
  - 10 rounds each test case
  - internal timer off: [no_timer, notimer, timer_off, timeroff]
"""

picks_on = [
    ('01_WEIGHTS4.in', 263),
    ('02_WEIGHTS24_Kreher_Stinson.in', 7582),
    ('03_WEIGHTS100_Xu_Xu_et_al.in', 462407),
    ('04_WEIGHTS_TODD_16.in', 5108),
    ('04_WEIGHTS_TODD_17.in', 10917),
    ('05_WEIGHTS_TODD_18.in', float('nan')),
    ('06_WEIGHTS_TODD_19.in', float('nan')),
    ('06_WEIGHTS_TODD_20.in', float('nan')),
    ('7.in', float('nan'))
]

picks_off = [
    ('01_WEIGHTS4.in', 257),
    ('02_WEIGHTS24_Kreher_Stinson.in', 3801),
    ('03_WEIGHTS100_Xu_Xu_et_al.in', 403686),
    ('04_WEIGHTS_TODD_16.in', 327),
    ('04_WEIGHTS_TODD_17.in', 324),
    ('05_WEIGHTS_TODD_18.in', 370),
    ('06_WEIGHTS_TODD_19.in', 435),
    ('06_WEIGHTS_TODD_20.in', 526),
    ('7.in', float('nan'))
]
