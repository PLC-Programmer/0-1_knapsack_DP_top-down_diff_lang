#!/usr/bin/pwsh -Command
#
# exe_times_statistics_for_one_test_case_in_cwd.ps1
#
# Robert Sackmann, 2023-10-23
#
# test:
#   C++: OK
#   Python: OK
#   C#: OK
#   Rust: OK
#
# environment: $ $PSVersionTable -->
#                Linux 6.2.0-34-generic #34~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Sep  7 13:12:03 UTC 2
#                PSVersion 7.3.8
#
# timer run for the:
#   C++ program:    $ ./exe_times_statistics_for_one_test_case_in_cwd.ps1 dp_knapsack_top-down_main pickson 20 timeroff
#                                                                         $args[0]                  $args[1] $args[2] $args[3]
#   Python program: $ ./exe_times_statistics_for_one_test_case_in_cwd.ps1 python3 dp_knapsack_top-down.py pickson timeroff
#                                                                         $args[0]                        $args[1] $args[2]
#   C# program:     $ ./exe_times_statistics_for_one_test_case_in_cwd.ps1 ./bin/Release/net7.0/linux-x64/dp_knapsack_top-down pickson timeroff
#                                                                         $args[0]                                            $args[1] $args[2]
#   Rust program:   $ ./exe_times_statistics_for_one_test_case_in_cwd.ps1 ./target/release/dp_knapsack_top-down pickson timeroff
#                                                                         $args[0]                              $args[1] $args[2]
#
#
# C++ example command here to get the "Total number of CPU-seconds that the process spent in user mode": $ /usr/bin/time -f '%U' ./dp_knapsack_top-down_main pickson 20 timeroff
# for the time command see: https://www.man7.org/linux/man-pages/man1/time.1.html
#
#
#  to do:
#    -
#    -

$ROUNDS = 10  # n rounds for one test case

if ($args[0] -eq "python3") {
    $CMD = "/usr/bin/time -f '%U' " + $args[0] + " " + $args[1] + " " + $args[2] + " "+ $args[3]
}
else {
    $CMD = "/usr/bin/time -f '%U' ./" + $args[0] + " " + $args[1] + " " + $args[2] + " "+ $args[3]
}

"Test command:"
$CMD
# list all *.in files in the cwd (current working directory), even though this script is only meant for only one test case file in the cwd:
"`nTest case file(s) in current working directory (though only one test case is meant to be tested here):"
$in_files = Get-ChildItem . *.in | Select-Object -ExpandProperty Name
"  $in_files"
"`nThis test case will do now $ROUNDS rounds..."


[single]$SUM = 0.0  # milliseconds

[single[]]$OUTCOME_ARRAY  = @()


For ($i = 0; $i -lt $ROUNDS; $i++) {

    [string]$user = Invoke-Expression "$CMD 2>&1"
    # "user = " + $user
    <#
    user =  Temporary increase of stack sizerl.rlim_cur = 8388608  After change: rl.rlim_cur = 67108864   Sorted list of input files with test cases:   ./02_WEIGHTS24_Kreher&Stinson.in  Answer of -1 means that no optimal value is known or no optimal value could be computed within the time limit.   Test case: ./02_WEIGHTS24_Kreher&Stinson.in   timeout waiting time = 20min    DP top-down with picks table on: number of elements of picks table = 153700344                                    number of bytes of picks table =    614801376                                    avl_page_size_bytes =               7801462784 (available free memory in bytes)   available free memory after applying a margin of safety =            7301462784    DP top-down: start recursion...   end of recursion.    Optimal weights as picked by the Dynamic Programming top-down (recursive) algo:     id = 23,  weight = 169684,  value = 369261     id = 22,  weight = 224916,  value = 466257     id = 21,  weight = 264724,  value = 577243     id = 15,  weight = 951111,  value = 2067538     id = 12,  weight = 610856,  value = 1252836     id = 10,  weight = 853665,  value = 1844992     id = 9,  weight = 903959,  value = 1902996     id = 5,  weight = 44328,  value = 97426     id = 4,  weight = 467902,  value = 943972     id = 3,  weight = 729069,  value = 1523970     id = 1,  weight = 799601,  value = 1677009     id = 0,  weight = 382745,  value = 825594   => actual weight of optimal knapsack = 6402560   => actual value of optimal knapsack = 13549094   Dynamic programming top-down (recursive) was completed with answer = 13549094   The expected maximum value of the optimal knapsack is 13549094 0.09
    #>

    $outcome = [single]$user.Split(" ")[-1]
    "  round #" + ($i+1) + " --> outcome = " + $outcome + " seconds"

    $OUTCOME_ARRAY += $outcome * 1000.0  # convert to [milliseconds]
    $SUM += $outcome * 1000.0
}

"======================="
"SUM = " + $SUM + " [milliseconds]"
"rounds = " + $ROUNDS

[single]$MEAN = ($SUM/$ROUNDS)
"MEAN = " + $MEAN.ToString('0.00') + ": total number of CPU-milliseconds that the process spent in user mode"


# variance:
[single]$SUM_SQUARES = 0.0
For ($j = 0; $j -lt $ROUNDS; $j++) {
    $SUM_SQUARES = $SUM_SQUARES + [Math]::Pow(($OUTCOME_ARRAY[$j] - $MEAN), 2)
}
$VARIANCE = $SUM_SQUARES / ($ROUNDS - 1)
"VARIANCE = " + $VARIANCE.ToString('0.00') + " [milliseconds]^2"


# std.dev:
[single]$STD_DEV = [Math]::sqrt($VARIANCE)
"STD_DEV = " + $STD_DEV.ToString('0.00') + " [milliseconds]"


# end of exe_times_statistics_for_one_test_case_in_cwd.ps1
