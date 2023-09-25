# The 0/1 knapsack problem with dynamic programming with the top-down (recursive) algorithm: comparing execution speeds of programming languages

2023-09-19/20/22/23/24/25...: a work in progress (WIP)

First batch of programming languages:
* **Python**: albeit slow, if possible this is my reference for calculating a correct result for an unknown test case
* **C++** (with the _g++ -O3_ optimization option; gcc version 11.4.0 has been used here)
* **C#** (release build)
* **Rust** (release build)

DP = Dynamic Programming

Important things first (with Python included see below at https://github.com/PLC-Programmer/0-1_knapsack_DP_top-down_diff_lang#diagrams-of-the-individual-programming-languages ):

![plot](./diagrams_svg_resized/lang1_WEIGHTS100_Xu_Xu_ex_Python_resized.svg)

<rev.2023-09-25: mass tested with script: 10 rounds for each test case, arithmetic mean, using Linux time command>

This project is a spin-off from this project: https://github.com/PLC-Programmer/knapsack_Axiotis-Tzamos, where only Algo 3 is used here: https://github.com/PLC-Programmer/knapsack_Axiotis-Tzamos#algo-3----15-winner-dp-top-down 


## The odd case of the implementation with C++

While C++ is looking good in above diagram, and as many would expect, this test case, which is very different in nature, might come as a shock even:

![plot](./diagrams_svg_resized/lang1_WEIGHTS_TODD_18_ex_Python_resized.svg)

<rev.2023-09-25: mass tested with script: 10 rounds for each test case, arithmetic mean, using Linux time command>

However, with the (famous) _02_WEIGHTS24_Kreher&Stinson.in_ test case (https://github.com/PLC-Programmer/knapsack_Axiotis-Tzamos#02_weights24_kreherstinsonin) the program in C++ can compare in speed with its counterpart in Rust with an activated picks table (for backtracking the optimal result if desired):

![plot](./diagrams_svg_resized/lang1_WEIGHTS24_Kreher_Stinson_ex_Python_resized.svg)

<rev.2023-09-25: mass tested with script: 10 rounds for each test case, arithmetic mean, using Linux time command>

In the C++ program I use the **vector data type** for the **picks table** in the recursive function:

```
class knapsack_recursive...
    ...
    vector<int> picks;  // 1dim array as vector (dynamic array) --> can grow dynamically
    ...
    int solveKnapsack(
        ...
        vector<int>& picks,
        ...
        ) {
        ...
        // building up the (huge) picks table (2dim array):
        if (include > exclude) {
            picks[items*max_wt + capacity] = 1;
        }
        else {
            picks[items*max_wt + capacity] = -1;
        }        
        ...
    }
```

However in Rust I do the same:

```
fn solve_knapsack_picks_on(
    ...
    &Vec<u32>,
    ...) -> i32 {
    ...
    // building up the (huge) picks table (2dim array):
    // unsafe due to using MAX_WT:
    unsafe {
        if include > exclude {
            picks[_items * MAX_WT + capacity as usize] = 1;
        }
        else {
            picks[_items * MAX_WT + capacity as usize] = -1;
        }
    }
    ...
}
```

In the C# program I use the array data type:

```
class knapsack_recursive {
    ...
    int[]? picks;  // Consider declaring the field as nullable.
    ...
    int solveKnapsack (
        ...
        int[] picks,
        ...) {
        ...
        // building up the (huge) picks table (2dim array):
        if (include > exclude) {
            picks[items*max_wt + capacity] = 1;
        }
        else {
            picks[items*max_wt + capacity] = -1;
        }
        ...
    }
    ...
}
```

One might guess that also using the good old array data type might lead to a faster C++ program with some of the test cases...

## Diagrams of the individual programming languages

Since the other test cases can be computed much faster (if possible in my environment) than test case _03_WEIGHTS100_Xu_Xu_et_al.in_:

![plot](./diagrams_svg_resized/lang1_WEIGHTS100_Xu_Xu_resized.svg)

<rev.2023-09-24: mass tested with script: 10 rounds for each test case, arithmetic mean, using Linux time command>

\
...this test case is omitted from the diagrams of the individual programming languages:

![plot](./diagrams_svg_resized/python_ex_Xu_Xu_resized.svg)

<rev.2023-09-23, Python: mass tested with script: 10 rounds for each test case, arithmetic mean, using Linux time command>

\
![plot](./diagrams_svg_resized/cpp_ex_Xu_Xu_resized.svg)

<rev.2023-09-22, C++: mass tested with script: 10 rounds for each test case, arithmetic mean, using Linux time command; g++ -O3 compiled>

\
![plot](./diagrams_svg_resized/cs_ex_Xu_Xu_resized.svg)

<rev.2023-09-23, C#: mass tested with script: 10 rounds for each test case, arithmetic mean, using Linux time command>

\
![plot](./diagrams_svg_resized/rust_ex_Xu_Xu_resized.svg)

<rev.2023-09-24, Rust: mass tested with script: 10 rounds for each test case, arithmetic mean, using Linux time command>

## Environment

Hardware:

* CPU: Intel Core i7-11700K, 3.60GHz (11th gen.)

* mainboard: GigaByte Z590 GAMING X, rev.0

* RAM: DDR4, 16GB, 3200-16 Vengeance LPX

Operating system:

* _$ uname -a_ --> _Linux ... 6.2.0-32-generic #32~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug 18 10:40:13 UTC 2 x86_64 x86_64 x86_64_

### Used compiler or builder versions, respectively

* **Python**: _$ python3 -V -V_ --> _Python 3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0]_

* **C++**: _$ g++ --version_ --> _g++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0_

* **C#**:

  _$ dotnet --list-sdks_ --> _7.0.111 [/usr/lib/dotnet/sdk]_

  _$ dotnet --list-runtimes_ -->

    _Microsoft.AspNetCore.App 7.0.11 [/usr/lib/dotnet/shared/Microsoft.AspNetCore.App]_

    _Microsoft.NETCore.App 7.0.11 [/usr/lib/dotnet/shared/Microsoft.NETCore.App]_

* **Rust**:

  _$ cargo -V_ --> _cargo 1.66.1_

  _$ rustc -V_ --> _rustc 1.66.1 (90743e729 2023-01-10) (built from a source tarball)_


## C++: g++ compiler options for speed optimization

Apparently the choice of options for (speed) optimization has a huge influence on the performance of a compiled C++ program with g++: https://gcc.gnu.org/onlinedocs/gcc-11.4.0/gcc/Optimize-Options.html

Well, at least with the presented computational task here.

Compile the C++ source code with command: _$ g++ [options] ./dp_knapsack_top-down_main.cpp -o dp_knapsack_top-down_main_

I experimented with these optimization options on test case _03_WEIGHTS100_Xu_Xu_et_al.in_:

* -O0 (or no -O option) -- Reduce compilation time and make debugging produce the expected results. This is the default.

* -O, -O1 -- Optimize.

* -O2 -- Optimize even more.

* -O3 -- Optimize yet more  // this option has been used for all C++ results presented here; option -Ofast looks a little bit faster here; however I guess I should keep _strict standards compliance_ for now

* -Os -- Optimize for size.

* -Ofast -- Disregard strict standards compliance.

![plot](./diagrams_svg_resized/cpp_gpp_WEIGHTS100_Xu_Xu_resized.svg)

 
## Case testing for execution times

So far I have implemented three simple procedures:

(a) running with internal timers (done within the source code)

Run in Linux (Ubuntu) like this:

* Python: _$ python3 ./dp_knapsack_top-down.py [no_picks, nopicks, picks_off, picksoff] [no_timer, notimer, timer_off, timeroff]_
* C++: _$ ./dp_knapsack_top-down_main [no_picks, nopicks, picks_off, picksoff] **[20]** [no_timer, notimer, timer_off, timeroff]_
* C#: _$ ./bin/Release/net7.0/linux-x64/dp_knapsack_top-down [no_picks, nopicks, picks_off, picksoff] [no_timer, notimer, timer_off, timeroff]_
* Rust: _$ ./target/release/dp_knapsack_top-down [no_picks, nopicks, picks_off, picksoff] [no_timer, notimer, timer_off, timeroff]_ --> have the test case files (_*.in_) in same directory as the _Cargo.toml_ file

Default options are:
* _pickson_ for example (for an activated picks table)
* (only in C++: a user modifiable timeout timer; this is a fixed setting of 20 minutes with the other languages)
* _timeron_ for example (for an activated internal execution timer)
 
This procedure is probably not really useful for meaningful test statistics.

Time measurement concepts differ from one programming language to the other, at least with my implementations. However, an internal timer is useful in my opinion to compare one test case with another **processed with a program written in the same programming language**. This is why this is the original timing implementation and will stay as a feature: https://github.com/PLC-Programmer/knapsack_Axiotis-Tzamos

\
(b) bash script for **one individual test case** file (*.in) in the current working directory (cwd): _exe_times_statistics_for_one_test_case_in_cwd_

See examples and further information from here ("bash shell scripts"): https://github.com/PLC-Programmer/0-1_knapsack_DP_top-down_diff_lang/tree/main/bash_shell_scripts_mass_testing

\
(c) bash script for **mass testing** of several test cases: _exe_times_statistics_for_multiple_test_cases_

The test case files (_*.in_) are to be saved in the test case directory: _./test_cases_

See examples and further information from here ("bash shell scripts"): https://github.com/PLC-Programmer/0-1_knapsack_DP_top-down_diff_lang/tree/main/bash_shell_scripts_mass_testing
