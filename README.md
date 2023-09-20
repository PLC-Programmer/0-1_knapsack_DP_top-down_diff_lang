# The 0/1 knapsack problem with dynamic programming with the top-down (recursive) algorithm: comparing execution speeds of programming languages

2023-09-19/20...: a work in progress (WIP)

First batch of programming languages:
* Python: albeit slow, if possible this is my reference for calculating a correct result for an unknown test case
* C++ (with the _g++ -O3_ optimization option)
* C# (release build)
* Rust (release build)

DP = Dynamic Programming

Important things first (with Python see below):

![plot](./diagrams_svg/lang1_WEIGHTS100_Xu_Xu_ex_Python.svg)

 
While C++ is looking good in above diagram, and as many would expect, this test case, which is very different in nature, might come as a shock even:

![plot](./diagrams_svg/lang1_WEIGHTS_TODD_18_ex_Python.svg)


Also with this test case, C++ is also not looking so good with an activated picks table (for backtracking the optimal result if desired):

![plot](./diagrams_svg/lang1_WEIGHTS24_Kreher_Stinson.svg)


In the C++ program I use the **vector data type** for the **picks table** in the recursive function, however in Rust I do the same.

(In the C# program I use the array data type.)

(One might guess that also using the good old array data type might lead to a faster C++ program with some of the test cases.)


   
...

![plot](./diagrams_svg/lang1_WEIGHTS100_Xu_Xu.svg)

...

