"""
rev.2023-09-23
Knapsack: dynamic programming: top-down (recursive)
C# program: execution times [ms]
  ("Total number of CPU-seconds that the process spent in user mode")
- nan (not a number): not enough memory or timeout exceeded
Using the bash script with the Linux time command:
  - exe_times_statistics_for_multiple_test_cases
  - 10 rounds each test case
  - internal timer off: [no_timer, notimer, timer_off, timeroff]
"""

picks_on = [
    ('01_WEIGHTS4.in', 34),
    ('02_WEIGHTS24_Kreher_Stinson.in', 172),
    ('03_WEIGHTS100_Xu_Xu_et_al.in', 8989),
    ('04_WEIGHTS_TODD_16.in', 35),
    ('04_WEIGHTS_TODD_17.in', 35),
    ('05_WEIGHTS_TODD_18.in', 42),
    ('06_WEIGHTS_TODD_19.in', float('nan')),
    ('06_WEIGHTS_TODD_20.in', float('nan')),
    ('7.in', float('nan'))
]

picks_off = [
    ('01_WEIGHTS4.in', 28),
    ('02_WEIGHTS24_Kreher_Stinson.in', 88),
    ('03_WEIGHTS100_Xu_Xu_et_al.in', 8529),
    ('04_WEIGHTS_TODD_16.in', 32),
    ('04_WEIGHTS_TODD_17.in', 34),
    ('05_WEIGHTS_TODD_18.in', 31),
    ('06_WEIGHTS_TODD_19.in', 36),
    ('06_WEIGHTS_TODD_20.in', 37),
    ('7.in', float('nan'))
]
