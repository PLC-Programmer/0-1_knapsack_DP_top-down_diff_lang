2023-10-23: so far I only made a similar PowerShell script for testing an individual test case (with multiple runs and result output to console)

### PowerShell scripts

ps = PowerShell

Now floating point arithmetic is supported!

#### Install PowerShell in Linux

This worked for me in Ubuntu 22 LTS:

2023: Getting Started with PowerShell in Linux [Beginner Guide]: https://www.tecmint.com/install-powershell-in-linux/

```
$ sudo apt-get install -y wget apt-transport-https software-properties-common
$ wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb"
$ sudo dpkg -i packages-microsoft-prod.deb
$ sudo apt-get update
$ sudo apt-get install -y powershell
```

Before running a ps script make it executable:
```
$ chmod 755 ./exe_times_statistics_for_one_test_case_in_cwd.ps1
```

Put this statement into the first line of a ps script:

```
#!/usr/bin/pwsh -Command
```

<br/>

#### exe_times_statistics_for_one_test_case_in_cwd.ps1

https://github.com/PLC-Programmer/0-1_knapsack_DP_top-down_diff_lang/blob/main/PowerShell_scripts_mass_testing/exe_times_statistics_for_one_test_case_in_cwd.ps1

This script is **only useful with having only one test case file** (*.in) in the cwd (current working directory) or relevant directory, respectively of the to be tested program. Shell commands for testing the program in (here only for _pickson_, otherwise take _picksoff_ for example):

* Python: _$ ./exe_times_statistics_for_one_test_case_in_cwd.ps1 python3 dp_knapsack_top-down.py pickson timeroff_
* C++: _$ ./exe_times_statistics_for_one_test_case_in_cwd.ps1 dp_knapsack_top-down_main pickson **20** timeroff_
* C#: _$ ./exe_times_statistics_for_one_test_case_in_cwd.ps1 ./bin/Release/net7.0/linux-x64/dp_knapsack_top-down pickson timeroff_
* Rust: _$ ./exe_times_statistics_for_one_test_case_in_cwd.ps1 ./target/release/dp_knapsack_top-down pickson timeroff_

Example output for a Python test case:

![plot](./exe_times_statistics_for_one_test_case_in_cwd.ps1_python_WEIGHTS24_Kreher_Stinson_2023-10-23.png)


### Shut the internal execution timer off

Also use these scripts **only** with the activated option to bypass the internal execution timer of the to be tested program: [no_timer, notimer, timer_off, timeroff].
Then also provide a [pickson, picksoff] option before ([no_picks, nopicks, picks_off, picksoff]), for example:

_$ python3 ./dp_knapsack_top-down.py pickson timeroff_

I haven't provided elaborated user arguments evaluation for my programs.

 
### Linux time command

These scripts use the Linux _time_ command, here for the C++ program for example:

_$ /usr/bin/time -f '%U' ./dp_knapsack_top-down_main pickson 20 timeroff_

(*) see: https://www.man7.org/linux/man-pages/man1/time.1.html

This seemingly odd mechanism of these scripts leave the computer programs in the different programming languages almost untouched.
                                          
However, I had to add the option (as a second or third user argument, respectively) to not use the internal execution timer: [no_timer, notimer, timer_off, timeroff]
