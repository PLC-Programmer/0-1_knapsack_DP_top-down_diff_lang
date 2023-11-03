#!/usr/bin/pwsh -Command
#
# exe_times_statistics_for_multiple_test_cases.ps1
#
# $ chmod 755 exe_times_statistics_for_multiple_test_cases.ps1
#
# Robert Sackmann, 2023-11-02
#
# test:
#   C++: OK
#   Python: OK
#   C#: OK
#   Rust: OK
#
# environment: $ $PSVersionTable -->
#                Linux 6.2.0-35-generic #35~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Oct  6 10:23:26 UTC 2
#                PSVersion 7.3.8
#
# timer run for the:
#   C++ program:    $ ./exe_times_statistics_for_multiple_test_cases.ps1 dp_knapsack_top-down_main pickson 20 timeroff
#                                                                        $args[0]                  $args[1] $args[2] $args[3]
#   Python program: $ ./exe_times_statistics_for_multiple_test_cases.ps1 python3 dp_knapsack_top-down.py pickson timeroff
#                                                                        $args[0] $args[1]               $args[2] $args[3]
#   C# program:     $ ./exe_times_statistics_for_multiple_test_cases.ps1 ./bin/Release/net7.0/linux-x64/dp_knapsack_top-down pickson timeroff
#                                                                        $args[0]                                            $args[1] $args[2]
#   Rust program:   $ ./exe_times_statistics_for_multiple_test_cases.ps1 ./target/release/dp_knapsack_top-down pickson timeroff
#                                                                        $args[0]                              $args[1] $args[2]
#
#
# !! PLACE ONLY TESTABLE TEST CASES INTO DIRECTORY: ./test_cases !! So, no test cases that will lead to timeouts or not enough memory, respectively.
#
#
# C++ example command here to get the "Total number of CPU-seconds that the process spent in user mode": $ /usr/bin/time -f '%U' ./dp_knapsack_top-down_main pickson 20 timeroff
# for the time command see: https://www.man7.org/linux/man-pages/man1/time.1.html (*)
#
#
#  to do:
#    - 
#    - 

$ROUNDS = 10  # n rounds for one test case

$TESTDIR = "./test_cases"

$EXTENSION = "_cpp"

if ($args[0] -eq "python3") {
    $CMD = "/usr/bin/time -f '%U' " + $args[0] + " " + $args[1] + " " + $args[2] + " "+ $args[3]
    $EXTENSION = "_python"
}
else {
    $CMD = "/usr/bin/time -f '%U' ./" + $args[0] + " " + $args[1] + " " + $args[2] + " "+ $args[3]
}

if ($args[0] -match "net") {
    $EXTENSION = "_cs"
}

if ($args[0] -match "target") {
    $EXTENSION = "_rust"
}

$RESULTFILE = "./exe_times_statistics_for_multiple_test_cases_results" + $EXTENSION + ".txt"



"Test command:"
$CMD
"`n!!DO NOT SAVE UNTESTABLE INPUT FILES (TIMEOUT, NOT ENOUGH MEMORY) INTO THE TEST DIRECTORY!! THIS WOULD CAUSE WRONG TEST RESULTS!" | Tee-Object -FilePath $RESULTFILE


$DATE = Get-Date -UFormat "%Y-%m-%d @ %T"
$TZONE = Get-TimeZone
$DATE = "$DATE  $TZONE"  # 2023-11-01 @ 23:46:55  (UTC+01:00) Central European Time (Berlin)

Add-Content -Path $RESULTFILE "`n$DATE"
Add-Content -Path $RESULTFILE  "`nCommand to be run: $CMD"


# list all test case files in test dir:
$in_files = Get-ChildItem $TESTDIR *.in | Select-Object -ExpandProperty Name
"`nInput files with test cases:" | Tee-Object -Append -Path $RESULTFILE
foreach ($n in $in_files) {
    "  $TESTDIR/$n" | Tee-Object -Append -Path $RESULTFILE
}


# delete all potential test cases in cwd:
$CWD = Get-Location
$del_files = Get-ChildItem *.in
foreach ($n in $del_files) {
    Remove-Item -Path $n
}


foreach ($n in $in_files) {
    # copy test case i from TESTDIR into cwd:
    Copy-Item -Path $TESTDIR/$n  -Destination $CWD

    [single]$SUM = 0.0  # milliseconds
    [single[]]$OUTCOME_ARRAY  = @()


    "`n$n"
    "  this test case will do now $ROUNDS rounds..."
    For ($i = 0; $i -lt $ROUNDS; $i++) {
        [string]$user = Invoke-Expression "$CMD 2>&1"

        $outcome = [single]$user.Split(" ")[-1]
        "  round #" + ($i+1) + " --> outcome = " + $outcome + " seconds"
        $OUTCOME_ARRAY += $outcome * 1000.0  # convert to [milliseconds]
        $SUM += $outcome * 1000.0

    }


    "======================="
    Add-Content -Path $RESULTFILE "  ======================="  # only write to result file here

    Add-Content -Path $RESULTFILE "  Test case: $n"  # only write to result file here

    "SUM = " + $SUM + " [milliseconds]"
    Add-Content -Path $RESULTFILE ("    SUM = " + $SUM + " [milliseconds]")  # only write to result file here

    "rounds = " + $ROUNDS
    Add-Content -Path $RESULTFILE ("    rounds = " + $ROUNDS)  # only write to result file here

    [single]$MEAN = ($SUM/$ROUNDS)
    "MEAN = " + $MEAN.ToString('0.00') + ": total number of CPU-milliseconds that the process spent in user mode"
    Add-Content -Path $RESULTFILE ("    MEAN = " + $MEAN.ToString('0.00') + ": total number of CPU-milliseconds that the process spent in user mode")  # only write to result file here


    # variance:
    [single]$SUM_SQUARES = 0.0
    For ($j = 0; $j -lt $ROUNDS; $j++) {
        $SUM_SQUARES = $SUM_SQUARES + [Math]::Pow(($OUTCOME_ARRAY[$j] - $MEAN), 2)
    }
    $VARIANCE = $SUM_SQUARES / ($ROUNDS - 1)
    "VARIANCE = " + $VARIANCE.ToString('0.00') + " [milliseconds]^2"
    Add-Content -Path $RESULTFILE ("    VARIANCE = " + $VARIANCE.ToString('0.00') + " [milliseconds]^2")  # only write to result file here


    # std.dev:
    [single]$STD_DEV = [Math]::sqrt($VARIANCE)
    "STD_DEV = " + $STD_DEV.ToString('0.00') + " [milliseconds]"
    Add-Content -Path $RESULTFILE ("    STD_DEV = " + $STD_DEV.ToString('0.00') + " [milliseconds]")  # only write to result file here

    Remove-Item -Path $n
}


"`n`nTest results have been saved to: " + $RESULTFILE

# end of exe_times_statistics_for_multiple_test_cases.ps1
