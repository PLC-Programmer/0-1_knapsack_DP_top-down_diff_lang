// Program.cs
//
// Robert Sackmann, 2023-09-23
//
//
// test:
// environment: $ uname -a --> Linux ... 6.2.0-32-generic #32~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug 18 10:40:13 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
//              $ dotnet --info --> 7.0.111 [/usr/lib/dotnet/sdk],
//                                  Microsoft.AspNetCore.App 7.0.11 [/usr/lib/dotnet/shared/Microsoft.AspNetCore.App]
//                                  Microsoft.NETCore.App 7.0.11 [/usr/lib/dotnet/shared/Microsoft.NETCore.App]
//
//
// ini:   $ ./C#/dotnet new console -n dp_knapsack_top-down --use-program-main
//
// build a development candidate:
// build:   ./C#/dp_knapsack_top-down $ dotnet build
// run:     ./C#/dp_knapsack_top-down $ ./bin/Debug/net7.0/dp_knapsack_top-down [no_picks, nopicks, picks_off, picksoff] [no_timer, notimer, timer_off, timeroff]
//
// build a release candidate:
// build:   ./C#/dp_knapsack_top-down $ dotnet publish -c Release -r linux-x64 --no-self-contained
// run:     ./C#/dp_knapsack_top-down $ ./bin/Release/net7.0/linux-x64/dp_knapsack_top-down [no_picks, nopicks, picks_off, picksoff] [no_timer, notimer, timer_off, timeroff]
//
//
// to do:
//   -
//
//
// 2023-09-23: execution times (Total number of CPU-milliseconds that the process spent in user mode) with picks table activated:
//   $ bash shell script "exe_times_statistics_for_multiple_test_cases" (10x) with test case files (*.in) located in directory: ./test_cases
//     01_WEIGHTS4.in                    34ms
//     02_WEIGHTS24_Kreher&Stinson.in   172ms
//     03_WEIGHTS100_Xu_Xu_et_al.in    8989ms
//     04_WEIGHTS_TODD_16.in             35ms
//     04_WEIGHTS_TODD_17.in             35ms
//     05_WEIGHTS_TODD_18.in             42ms
//     06_WEIGHTS_TODD_19.in             ----  <Array dimensions exceeded supported range.>
//     06_WEIGHTS_TODD_20.in             ----  <Array dimensions exceeded supported range.>
//     7.in                              ----  <stopped manually after many minutes>
//
// 2023-09-21: same, but without picks table activated:
//     01_WEIGHTS4.in                    28ms
//     02_WEIGHTS24_Kreher&Stinson.in    88ms
//     03_WEIGHTS100_Xu_Xu_et_al.in    8529ms
//     04_WEIGHTS_TODD_16.in             32ms
//     04_WEIGHTS_TODD_17.in             34ms
//     05_WEIGHTS_TODD_18.in             31ms
//     06_WEIGHTS_TODD_19.in             36ms
//     06_WEIGHTS_TODD_20.in             37ms
//     7.in                              ----  <see above: not tested>


using System;
using System.IO;  // Directory, DirectoryInfo
using System.Diagnostics;  // ProcessStartInfo(), Process()



namespace dp_knapsack_top_down;


using static knapsack_recursive;           // class in another source file *.cs
using static knapsack_recursive_no_picks;  // class in another source file *.cs


public static class Globals
{
    public const int NBR_FILES = 20;
}


class Program
{
    static int Main(string[] args)
    {
        int result = -1;

        long stopped_time;

        int n, max_wt, optimal_profit, nbr_files;


        bool picks_on = true;  // default: with picks table activated
        bool exe_timer_on = true;  // default: with internal execution timer activated

        if (args.Length > 0) {
            if (args[0] == "no_picks" || args[0] == "nopicks" || args[0] == "picks_off" || args[0] == "picksoff" )
            {
                picks_on = false;  // no picks table to be activated
            }

            if (args.Length > 1) {
                if (args[1] == "no_timer" || args[1] == "notimer" || args[1] == "timer_off" || args[1] == "timeroff" )
                {
                    exe_timer_on = false;  // no internal execution timer to be activated
                }
            }
        }


        // get names of files with test cases:
        string path = Directory.GetCurrentDirectory();  // OK
        DirectoryInfo di = new DirectoryInfo(path);

        bool check = false;
        nbr_files = 0;
        string[] input_files = new string[Globals.NBR_FILES];  // arrays cannot be resized dynamically
        foreach (var fi in di.GetFiles("*.in"))
        {
            input_files[nbr_files++] = fi.Name;
            check = true;
        }

        if (!check) {
            Console.WriteLine("Cannot open any input file *.in in directory: " + path);
            return 1;
        }

        // potentially shrink input_files:
        Array.Resize(ref input_files, nbr_files);

        // sort input files:
        //
        Console.WriteLine("\nSorted list of input files with test cases:");
        input_files = input_files.OrderBy( s => s ).ToArray();
        foreach (var fi in input_files)
        {
            Console.WriteLine("  " + fi);
        }

        // service announcement:
        Console.WriteLine("\nAnswer of -1 means that no optimal value is known or no optimal value could be computed within the time limit.");

        // loop over input files with test cases:
        for (int h = 0; h < nbr_files; h++)
        {
            Console.WriteLine("\n\nTest case: " + input_files[h]);

            StreamReader infile = new StreamReader(input_files[h]);

            string? line;  // Converting null literal or possible null value to non-nullable type.

            line = infile.ReadLine();

            // first line is special:
            //   number of weight items, max capacity, expected max value:
            if (line != null) {  // Dereference of a possibly null reference.
                string[] first_line = line.Split(new char[] {' '}, StringSplitOptions.RemoveEmptyEntries);
                n = int.Parse(first_line[0]);
                max_wt = int.Parse(first_line[1]);
                optimal_profit = int.Parse(first_line[2]);
            }
            else {
                Console.WriteLine("\n  Can't read parameters from first line of input file!");
                break;
            }

            Console.WriteLine("  number of weight items = " + n);
            Console.WriteLine("  max capacity of knapsack = " + max_wt);

            int[] v = new int[n];
            int[] w  = new int[n];

            // reading in v + w:
            int i = 0;
            while ((line = infile.ReadLine()) != null)
            {
                // expect multi-space separation here:
                string[] chunks = line.Split(new char[] {' '}, StringSplitOptions.RemoveEmptyEntries);

                v[i] = int.Parse(chunks[0]);
                w[i]  = int.Parse(chunks[1]);
                i++;
            }


            ////////////////////////////////////////////////////////////////////////////
            //
            // Dynamic Programming top-down (recursive) procedure:

            if (picks_on is true) {
                if (exe_timer_on is true) {
                    ProcessStartInfo startInfo = new ProcessStartInfo()
                    {
                        FileName = "/bin/bash",
                        Arguments = "-c \"date +'%s%3N'\"",  // milliseconds since 1970-01-01 00:00:00 UTC
                        RedirectStandardOutput = true
                    };

                    Process proc = new Process() { StartInfo = startInfo, };
                    proc.Start();
                    var t1 = proc.StandardOutput.ReadToEnd();

                    knapsack_recursive ks_rec = new knapsack_recursive(w, v, max_wt);  // function in another source file
                    result = knapsack_recursive.result;

                    proc.Start();
                    var t2 = proc.StandardOutput.ReadToEnd();
                    stopped_time = Convert.ToInt64(t2) - Convert.ToInt64(t1);  // in milliseconds

                    Console.WriteLine("\n  Dynamic programming top-down (recursive) was completed with answer = " + result + " and execution time = " + stopped_time + "ms");
                }
                else {
                    knapsack_recursive ks_rec = new knapsack_recursive(w, v, max_wt);  // function in another source file
                    result = knapsack_recursive.result;
                    Console.WriteLine("\n  Dynamic programming top-down (recursive) was completed with answer = " + result);
                }
            }
            else {
                if (exe_timer_on is true) {
                    ProcessStartInfo startInfo = new ProcessStartInfo()
                    {
                        FileName = "/bin/bash",
                        Arguments = "-c \"date +'%s%3N'\"",  // milliseconds since 1970-01-01 00:00:00 UTC
                        RedirectStandardOutput = true
                    };

                    Process proc = new Process() { StartInfo = startInfo, };
                    proc.Start();
                    var t1 = proc.StandardOutput.ReadToEnd();

                    knapsack_recursive_no_picks ks_rec = new knapsack_recursive_no_picks(w, v, max_wt);  // function in another source file
                    result = knapsack_recursive_no_picks.result;

                    proc.Start();
                    var t2 = proc.StandardOutput.ReadToEnd();
                    stopped_time = Convert.ToInt64(t2) - Convert.ToInt64(t1);  // in milliseconds

                    Console.WriteLine("\n  Dynamic programming top-down (recursive) was completed with answer = " + result + " and execution time = " + stopped_time + "ms");
                }
                else {
                    knapsack_recursive_no_picks ks_rec = new knapsack_recursive_no_picks(w, v, max_wt);  // function in another source file
                    result = knapsack_recursive_no_picks.result;
                    Console.WriteLine("\n  Dynamic programming top-down (recursive) was completed with answer = " + result);
                }
            }

            Console.WriteLine("  The expected maximum value of the optimal knapsack is " + optimal_profit);

            //
            ////////////////////////////////////////////////////////////////////////////


            infile.Close();
        }

        return 0;
    }
}
