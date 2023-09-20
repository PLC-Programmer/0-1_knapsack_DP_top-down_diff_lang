# dp_knapsack_top-down.py
"""
Comparing memory safety and execution speed of different programming languages
when solving the same basic algorithm:
Combinatorial Optimization -> knapsack --> input: (mostly) TODD class problems
--> only implement the Dynamic Programming top-down (recursive) approach here
"""
#
# Robert Sackmann, 2023-09-17
#
#
# run in Ubuntu:
#   $ python3 ./dp_knapsack_top-down.py [no_picks, nopicks, picks_off, picksoff]
#
#
# test: OK
# environment:
#   $ uname -a --> Linux ... 6.2.0-32-generic #32~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug 18 10:40:13 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
#   Python 3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0] ($ python3 -V -V)
#
#
# Ubuntu memory: $ free -t  # in [kB]
#
#
# to do:
#  - 
#  -
#
#
# 2023-09-11: execution times with picks table activated (and optimal results printed, but not the huge picks table beyond 01_WEIGHTS4.in):
#     01_WEIGHTS4.in                         2ms
#     02_WEIGHTS24_Kreher&Stinson.in      6832ms
#     03_WEIGHTS100_Xu_Xu_et_al.in      461218ms
#     04_WEIGHTS_TODD_16.in               4027ms
#     04_WEIGHTS_TODD_17.in               9216ms
#     05_WEIGHTS_TODD_18.in                  -----  <not enough free available memory>
#     06_WEIGHTS_TODD_19.in                  -----  <not enough free available memory>
#     06_WEIGHTS_TODD_20.in                  -----  <not enough free available memory>
#     7.in                                   -----  <stopped manually after many minutes>
#
# 2023-09-11: execution times without picks table activated:
#     01_WEIGHTS4.in                         0ms
#     02_WEIGHTS24_Kreher&Stinson.in      3524ms
#     03_WEIGHTS100_Xu_Xu_et_al.in      406398ms
#     04_WEIGHTS_TODD_16.in                 14ms
#     04_WEIGHTS_TODD_17.in                 29ms
#     05_WEIGHTS_TODD_18.in                 58ms
#     06_WEIGHTS_TODD_19.in                115ms
#     06_WEIGHTS_TODD_20.in                224ms
#     7.in                                   -----  <see above>


import datetime
import os  # use os methods
import re  # regular expressions
import numpy as np
import sys  # command line options
import resource
from pympler import asizeof

import os      # watching memory
# import psutil  # watching memory: $ pip install psutil


# global variable:
TIME_CHECK_COUNTER = 30000  # incremental ticks for doing a time duration check in recursive knapsack_rec()
TIME_LIMIT  = 1200  # 20 min in seconds
time_counter = 0  # just ticks without a unit: used in knapsack_rec() + knapsack_rec_picks_off()
MARGIN_OF_SAFETY_BYTES = 500000000  # ~500 megabytes; only a wild guess after some experiments in Ubuntu LTS 22
CLEANUP_FLAG = 0


######################################################################
# user defined functions:

# recursion (top-down) with picks table ON:
def knapsack_rec(v, w, n, W, c_start):
    """
    Values (stored in list `v`)
    Weights (stored in list `w`)
    Total number of distinct items `n`
    Knapsack capacity `W`
    """

    global TIME_CHECK_COUNTER
    global TIME_LIMIT
    global time_counter
    global CLEANUP_FLAG

    # intermediate check for duration:
    if time_counter > TIME_CHECK_COUNTER:
        duration = datetime.datetime.now() - c_start
        duration_in_sec = duration.total_seconds()
        if duration_in_sec > TIME_LIMIT:
            if CLEANUP_FLAG == 0:
                CLEANUP_FLAG = 1
                print("\n  >>> DP top-down: stopping execution due to exceeded time limit of 20 minutes. Cleaning up...")
            return -1e12
        else:
            time_counter = 0


    # base case: Negative capacity
    if W < 0:
        return -1e12  # seems to be faster than -sys.maxsize

    # base case: no items left or capacity becomes 0
    if n < 0 or W == 0:
        return 0

    # Case 1. Include current item `n` in knapsack `v[n]` and recur for
    # remaining items `n-1` with decreased capacity `W-w[n]`
    include = v[n] + knapsack_rec(v, w, n - 1, W - w[n], c_start)

    # Case 2. Exclude current item `v[n]` from the knapsack and recur for
    # remaining items `n-1`
    exclude = knapsack_rec(v, w, n - 1, W, c_start)

    if include > exclude:
        PICKS[n][W] = 1
    else:
        PICKS[n][W] = -1

    time_counter += 1

    # return maximum value we get by including or excluding the current item:
    return max(include, exclude)



# recursion (top-down) with picks table OFF:
def knapsack_rec_picks_off(v, w, n, W, c_start):
    """
    Values (stored in list `v`)
    Weights (stored in list `w`)
    Total number of distinct items `n`
    Knapsack capacity `W`
    """

    global TIME_CHECK_COUNTER
    global TIME_LIMIT
    global time_counter
    global CLEANUP_FLAG

    # intermediate check for duration:
    if time_counter > TIME_CHECK_COUNTER:
        duration = datetime.datetime.now() - c_start
        duration_in_sec = duration.total_seconds()
        if duration_in_sec > TIME_LIMIT:
            if CLEANUP_FLAG == 0:
                CLEANUP_FLAG = 1
                print("\n  >>> DP top-down: stopping execution due to exceeded time limit of 20 minutes. Cleaning up...")
            return -1e12
        else:
            time_counter = 0


    # base case: Negative capacity
    if W < 0:
        return -1e12  # seems to be faster than -sys.maxsize

    # base case: no items left or capacity becomes 0
    if n < 0 or W == 0:
        return 0

    # Case 1. Include current item `n` in knapsack `v[n]` and recur for
    # remaining items `n-1` with decreased capacity `W-w[n]`
    include = v[n] + knapsack_rec_picks_off(v, w, n - 1, W - w[n], c_start)

    # Case 2. Exclude current item `v[n]` from the knapsack and recur for
    # remaining items `n-1`
    exclude = knapsack_rec_picks_off(v, w, n - 1, W, c_start)

    time_counter += 1

    # return maximum value we get by including or excluding the current item
    return max(include, exclude)



def print_picks(weights, capacity, picks, n):
    """
    print the optimal weights and the actual weight of the optimal knapsack:
    """
    item = n-1  # item id = 0...n-1
    size = capacity
    print("\n  optimal weights:")
    ACT_WEIGHT = 0
    opt_weights = []
    while item >= 0:
        if picks[item][size] == 1:
            print("  ", weights[item])
            ACT_WEIGHT += weights[item]
            opt_weights.append(weights[item])
            size -=weights[item]
            item -= 1
        else:
            item -= 1

    print("  => actual weight of optimal knapsack:", ACT_WEIGHT)

    opt_indices = np.argwhere(np.isin(weights, opt_weights))
    opt_indices = list(opt_indices.flatten())
    print("  optimal indices [0...n-1]:", opt_indices)


    if n < 10 and capacity < 10:
        print("  picks:")
        for k in range(n):
            stringA = "    "
            for l in range(capacity+1):
              stringA = stringA + " " +  "%2d" % picks[k][l]  # format later for -1, 0 , +1
            print(stringA)



######################################################################
# main part of program starts here:

if __name__ == "__main__":

    picks_on = True  # default: with picks table activated
    if len(sys.argv) > 1:
        # search for: no_picks, nopicks, picks_off, picksoff
        opt_pattern = r'no_picks|nopicks|picks_off|picksoff'
        result = re.search(opt_pattern, sys.argv[1])
        picks_on = not(bool(result))


    input_files = os.listdir()

    # sort input_files before further processing (needed in Linux, not Windows):
    input_files.sort()

    FLAG1 = False

    # going through all input files:
    for i,file in enumerate(input_files):

        re1 = re.match(r"\S*\.in", file)  # \S matches any non-whitespace character

        if re1:
            print("\n\ninput file =", file)

            # open and process this input file:
            f = None
            try:
                f = open(file, "r")
                FLAG1 = True
            except IOError as e:
                print(f"Couldn't open input file ({e})")

            # first line is special:
            #   number of weight items, max capacity, expected max value:
            line_1 = f.readline()
            # print(line_1)

            pars = line_1.split(" ")
            N = int(pars[0])
            CAPACITY = int(pars[1])
            OPTIMAL_PROFIT = int(pars[2])
            PRICES = []
            WEIGHTS = []

            print("  number of weight items =", N)
            print("  max capacity of knapsack =", CAPACITY)

            # read both columns: value + weight
            for j in range(N):
                line_1 = f.readline()

                # there's still a "\n" attached to it:
                line_1 = line_1.rstrip()

                # value and weight can be seperated by more than one space char:
                chunks = re.split(' +', line_1)

                PRICES.append(int(chunks[0]))
                WEIGHTS.append(int(chunks[1]))


            a = datetime.datetime.now()

            if picks_on:
                picks_alloc = N * (CAPACITY+1)  # number of elements of picks table
                print("\n  DP top-down with picks table on: number of elements of picks table =", picks_alloc)

                mem = os.popen('free -t').readlines()[1].split()[1:]
                free_available_memory = int(mem[2]) * 1024  # kB --> bytes
                print("  free available memory [bytes] =", free_available_memory, flush = True)

                picks_alloc_bytes_est = picks_alloc * 10  # this is only a rough estimates from below (*)

                if picks_alloc_bytes_est > (free_available_memory - MARGIN_OF_SAFETY_BYTES):
                    print("  recursion is not starting here: it may run out of free available memory including some safety margin!", flush = True)
                    MAX_VALUE = -1

                else:
                    # DON't EXECUTE THIS COMMAND WITHOUT CHECKING FOR ENOUGH MEMORY:
                    #   THIS COMMAND MAY TAKE MINUTES!
                    PICKS = [[0 for x in range(CAPACITY+1)] for y in range(N)]  # range(N): create a sequence of numbers from 0 to N-1; type is list

                    CLEANUP_FLAG = 0
                    c = datetime.datetime.now()
                    MAX_VALUE = knapsack_rec(PRICES, WEIGHTS, len(WEIGHTS)-1, CAPACITY, c)

                    if CLEANUP_FLAG == 0:
                        print_picks(WEIGHTS, CAPACITY, PICKS, N)

                    # print("  str(PICKS) =", str(PICKS))
                    # 01_WEIGHTS4.in: str(PICKS) = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

                    # size of list of lists:
                    # PICKS_size = asizeof.asizeof(PICKS)
                    # print("  size of picks table [bytes]   =", PICKS_size)
                    # 01_WEIGHTS4.in: size of PICKS [bytes] = 592
                    # 02_WEIGHTS24_Kreher&Stinson.in: size of PICKS [bytes] = 1334917712 = ~1.24GB
                    # ...
                    # 05_WEIGHTS_TODD_18.in: size of PICKS [bytes] = 11877383936 <-- number of elements of picks table = 1434451860
                    #   => 11877383936 bytes / 1434451860 elements = ~8.28 bytes / element (*)

            else:
                CLEANUP_FLAG = 0
                c = datetime.datetime.now()
                print("\n  recursion is starting with picks table off...")
                MAX_VALUE = knapsack_rec_picks_off(PRICES, WEIGHTS, len(WEIGHTS)-1, CAPACITY, c)

            b = datetime.datetime.now()
            delta = b - a

            if CLEANUP_FLAG == 1:
                MAX_VALUE = -1

            print("\n  => max value of knapsack =", MAX_VALUE)
            print("  => expected max value of optimal knapsack =", OPTIMAL_PROFIT)

            print("\n  elapsed time in milliseconds:", int(delta.total_seconds() * 1000))  # milliseconds

            f.close()

    if FLAG1 is False:
        print("\ncould not open any input file *.in in local directory!")

# end of dp_knapsack_top-down.py
