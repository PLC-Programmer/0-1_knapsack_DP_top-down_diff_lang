"""
rev.2023-09-26
Knapsack: dynamic programming: top-down (recursive)
Execution times [ms] ("Total number of CPU-seconds
  that the process spent in user mode") for the
  04_WEIGHTS_TODD_16/17/18.in test cases
  for the C++ and Rust programs with picks table on
- nan (not a number): not enough memory or timeout exceeded
Using the bash script with the Linux time command:
  - exe_times_statistics_for_multiple_test_cases
  - 10 rounds each test case
  - internal timer off: [no_timer, notimer, timer_off, timeroff]
"""

# C++, picks on:
lang1 = [
    ('04_WEIGHTS_TODD_16.in', 30),
    ('04_WEIGHTS_TODD_17.in', 84),
    ('05_WEIGHTS_TODD_18.in', 181),
]


# Rust, picks on:
lang2 = [
    ('04_WEIGHTS_TODD_16.in', 0),
    ('04_WEIGHTS_TODD_17.in', 1),
    ('05_WEIGHTS_TODD_18.in', 3),
]
