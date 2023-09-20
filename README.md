# The 0/1 knapsack problem with dynamic programming with the top-down (recursive) algorithm: comparing execution speeds of programming languages

2023-09-19/20...: a work in progress (WIP)

First batch of programming languages:
* Python: albeit slow, if possible this is my reference for calculating a correct result for an unknown test case
* C++ (with the _g++ -O3_ optimization option as my best guess so far)
* C# (release build)
* Rust (release build)

DP = Dynamic Programming

Important things first (with Python included see below at https://github.com/PLC-Programmer/0-1_knapsack_DP_top-down_diff_lang#diagrams-of-the-individual-programming-languages ):

![plot](./diagrams_svg/lang1_WEIGHTS100_Xu_Xu_ex_Python.svg)
 
This is a spin-off project from this one: https://github.com/PLC-Programmer/knapsack_Axiotis-Tzamos, where only Algo 3 is used here: https://github.com/PLC-Programmer/knapsack_Axiotis-Tzamos#algo-3----15-winner-dp-top-down 
  

## The odd case of the implementation with C++

While C++ is looking good in above diagram, and as many would expect, this test case, which is very different in nature, might come as a shock even:

![plot](./diagrams_svg/lang1_WEIGHTS_TODD_18_ex_Python.svg)

Also with this test case, C++ is also not looking so good with an activated picks table (for backtracking the optimal result if desired):

![plot](./diagrams_svg/lang1_WEIGHTS24_Kreher_Stinson.svg)

In the C++ program I use the **vector data type** for the **picks table** in the recursive function, however in Rust I do the same.

(In the C# program I use the array data type.)

(One might guess that also using the good old array data type might lead to a faster C++ program with some of the test cases.)

## Diagrams of the individual programming languages

Since the other test cases can be computed much faster (if possible in my environment) than test case _03_WEIGHTS100_Xu_Xu_et_al.in_:

![plot](./diagrams_svg/lang1_WEIGHTS100_Xu_Xu.svg)

...this test case is omitted from these diagrams:

![plot](./diagrams_svg/python.svg)

![plot](./diagrams_svg/cpp.svg)

![plot](./diagrams_svg/cs.svg)

![plot](./diagrams_svg/rust.svg)



...

