"""
rev.2023-09-22
Knapsack: dynamic programming: top-down (recursive)
C++ program (-O3): execution times [ms]
  ("Total number of CPU-seconds that the process spent in user mode")
- nan (not a number): not enough memory or timeout exceeded
Using the bash script with the Linux time command:
  - exe_times_statistics_for_multiple_test_cases
  - 10 rounds each test case
  - internal timer off: [no_timer, notimer, timer_off, timeroff]
"""

picks_on = [
    ('01_WEIGHTS4.in', 0),
    ('02_WEIGHTS24_Kreher_Stinson.in', 109),
    ('03_WEIGHTS100_Xu_Xu_et_al.in', 3583),
    ('04_WEIGHTS_TODD_16.in', 30),
    ('04_WEIGHTS_TODD_17.in', 84),
    ('05_WEIGHTS_TODD_18.in', 181),
    ('06_WEIGHTS_TODD_19.in', float('nan')),
    ('06_WEIGHTS_TODD_20.in', float('nan')),
    ('7.in', float('nan'))
]

picks_off = [
    ('01_WEIGHTS4.in', 0),
    ('02_WEIGHTS24_Kreher_Stinson.in', 20),
    ('03_WEIGHTS100_Xu_Xu_et_al.in', 2896),
    ('04_WEIGHTS_TODD_16.in', 0),
    ('04_WEIGHTS_TODD_17.in', 0),
    ('05_WEIGHTS_TODD_18.in', 0),
    ('06_WEIGHTS_TODD_19.in', 0),
    ('06_WEIGHTS_TODD_20.in', 0),
    ('7.in', float('nan'))
]
