"""
rev.2023-09-25
Knapsack: dynamic programming: top-down (recursive)
Execution times [ms] ("Total number of CPU-seconds
  that the process spent in user mode") for the
  05_WEIGHTS_TODD_18.in test case for the first group
  of programming languages: Python, C++, C#, Rust
- nan (not a number): not enough memory or timeout exceeded
Using the bash script with the Linux time command:
  - exe_times_statistics_for_multiple_test_cases
  - 10 rounds each test case
  - internal timer off: [no_timer, notimer, timer_off, timeroff]
"""

picks_on = [
    ('Python', float('nan')),
    ('C++', 181),
    ('C#', 42),
    ('Rust', 3)
]


picks_off = [
    ('Python', 58),
    ('C++', 0),
    ('C#', 31),
    ('Rust', 0)
]
