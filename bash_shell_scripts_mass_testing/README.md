Here are two bash shell scripts for mass testing for the execution times (here the "Total number of CPU-seconds that the process spent in user mode" (*)) for the programs in the different programming languages (Python, C++, C#, Rust, ...).

\
(a) _exe_times_statistics_for_one_test_case_in_cwd_ (755)

This script is **only useful with having only one test case file** (*.in) in the cwd (current working directory) or relevant directory, respectively of the to be tested program.

\
(b) _exe_times_statistics_for_multiple_test_cases_ (755)

This script takes all test cases (*.in) from directory _./test_cases_ and copies them one by one into the cwd or relevant directory, respectively of the to be tested program.

It will produce a log file (_exe_times_statistics_for_multiple_test_cases_results.txt_) with simple test statistics.

\
Most important: **DO NOT SAVE UNTESTABLE INPUT FILES (TIMEOUT, NOT ENOUGH MEMORY) INTO THE TEST DIRECTORY! THIS WOULD CAUSE WRONG TEST RESULTS!**

So preselect your test cases files when mass testing.

\
These scripts use the Linux time command (here for the C++ program): _$ /usr/bin/time -f '%U' ./dp_knapsack_top-down_main pickson 20 timeroff_

(*) see: https://www.man7.org/linux/man-pages/man1/time.1.html

The seemingly odd mechanism of these scripts leave the computer programs in the different programming languages almost untouched.
                                          
However, I had to add the option (as a third user argument) to not use the internal execution timer: [no_timer, notimer, timer_off, timeroff]

2023-09-21: only the C++ program has this third option for now...
 
\
Of course, these test scripts could have been also done in Python for example to get better and easier control of the testing procedure (bash doesn't support floating point arithmetic for example).

But for now, using the Linux _time_ command, which apparently provides a precision of only +/-10 milliseconds, is good enough for me.

\
Check Linux mode (755) to make these scripts executable.
