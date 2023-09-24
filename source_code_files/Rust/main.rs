// main.rs
//
// Robert Sackmann, 2023-09-24
//
// test: OK
// environment: $ uname -a --> Linux ... 6.2.0-32-generic #32~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug 18 10:40:13 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
//
//
// DEBUG:
//   build: ./dp_knapsack_top-down $ cargo build
//   run:   ./dp_knapsack_top-down $ ./target/debug/dp_knapsack_top-down [no_picks, nopicks, picks_off, picksoff] [no_timer, notimer, timer_off, timeroff]
//
// RELEASE:
//   build: ./dp_knapsack_top-down $ cargo build -r -v  # -r release, -v verbose
//   run:   ./dp_knapsack_top-down $ ./target/release/dp_knapsack_top-down [no_picks, nopicks, picks_off, picksoff] [no_timer, notimer, timer_off, timeroff]
//          have test case files (*.in) in same directory as the Cargo.toml file
//
//
// to do:
//    -
//
//
// 2023-09-24: execution times (Total number of CPU-milliseconds that the process spent in user mode) with picks table activated:
//   $ bash shell script "exe_times_statistics_for_multiple_test_cases" (10x) with test case files (*.in) located in directory: ./test_cases
//     01_WEIGHTS4.in                      0ms
//     02_WEIGHTS24_Kreher&Stinson.in     99ms
//     03_WEIGHTS100_Xu_Xu_et_al.in     8143ms
//     04_WEIGHTS_TODD_16.in               0ms
//     04_WEIGHTS_TODD_17.in               1ms
//     05_WEIGHTS_TODD_18.in               3ms
//     06_WEIGHTS_TODD_19.in             -----  <not enough free available memory>
//     06_WEIGHTS_TODD_20.in             -----  <not enough free available memory>
//     7.in                              -----  <see below: not tested>
//
// 2023-09-24: same, but without picks table activated:
//     01_WEIGHTS4.in                      0ms
//     02_WEIGHTS24_Kreher&Stinson.in     40ms
//     03_WEIGHTS100_Xu_Xu_et_al.in     6907ms
//     04_WEIGHTS_TODD_16.in               0ms
//     04_WEIGHTS_TODD_17.in               0ms
//     05_WEIGHTS_TODD_18.in               0ms
//     06_WEIGHTS_TODD_19.in               0ms
//     06_WEIGHTS_TODD_20.in               4ms
//     7.in                              -----  <stopped manually after many minutes>



use std::{env, fs};
use std::error::Error;
use std::str::FromStr;  // string to integer

use std::time::{Instant};  // https://rust-lang-nursery.github.io/rust-cookbook/datetime/duration.html


mod dp_knapsack_top_down_recursion;  // DP top-down (recursion) is happening here: *.rs


/*
fn print_type_of<T>(_: &T) {
    println!("{}", std::any::type_name::<T>())
}
*/



fn main() -> Result<(), Box<dyn Error>> {

    // picks table or not?
    let args: Vec<String> = env::args().collect();

    let mut picks_on: bool = true;  // default: with picks table activated
    let mut exe_timer_on: bool = true;  // default: with internal execution timer activated


    if args.len() > 1 {
        if args[1] == "no_picks" || args[1] == "nopicks" || args[1] == "picks_off" || args[1] == "picksoff"
        {
            picks_on = false;  // no picks table to be activated
        }

        if args.len() > 2 {
            if args[2] == "no_timer" || args[2] == "notimer" || args[2] == "timer_off" || args[2] == "timeroff"
            {
                exe_timer_on = false;  // no internal execution timer to be activated
            }
        }

    }


    // collect input files *.in with test cases in cwd (current working directory): type = std::path::PathBuf
    let cwd = env::current_dir()?;  // ? == success or not?
    println!("Current directory is: {}", cwd.display());


    // type = alloc::vec::Vec<alloc::string::String>
    // mut to be sorted later on:
    let mut full_file_names = fs::read_dir(&cwd)  // vector of strings with full file paths; only reference to &cwd given, not moving it
        .unwrap()
        .filter_map(Result::ok)
        .filter(|f| f.file_type().expect("no files here!").is_file())  // get only files
        // filter file names for *.in:
        .filter_map(|d| d.path().to_str()
          .and_then(|f| if f.ends_with(".in") {Some(d)} else {None}))
        .map(|entry| entry.path().to_string_lossy().into_owned())
        .collect::<Vec<_>>();

    // leave program when no input files could have been found in the cwd:
    let nbr_files = full_file_names.len();

    if nbr_files < 1 {
        println!("Cannot open any input file *.in in directory: {}", cwd.display());
        return Ok(())
    };


    // sort full file names:
    full_file_names.sort();

    // get only file names from full_file_names[]: declare a vector of strings:
    let mut file_names: Vec<String> = vec![String::new(); nbr_files];

    println!("\nSorted list of input files with test cases:");

    for i in 0..nbr_files {
        // split full path name:
        let v: Vec<&str> = full_file_names[i].split('/').collect();
        let v_last = v.last().expect("full_file_names[i]: Vec<&str> has no last element!").to_string();  // last element of vector
        println!("  {}", &v_last);
        file_names[i] = v_last;  // ownership of v_last moved to here
    }


    // service announcement:
    println!("\nAnswer of -1 means that no optimal value is known or no optimal value could be computed within the time limit.");


    // loop over collected input files with test cases:
    for i in 0..nbr_files {
        println!("\n\nTest case: {}", file_names[i]);

        let contents = fs::read_to_string(&file_names[i]).expect("something went wrong reading this input file!");
        // print_type_of(&contents);  // alloc::string::String

        // break contents into individual lines:
        let input_lines: Vec<&str> = contents.lines().collect();  // this can be CRLF (panick!) or LF (OK)!!
        // Test case: 01_WEIGHTS4.in
        // [src/main.rs:149] &first_line = [
        //     "4",
        //     "7",
        //     "9\r", <<<<<<
        // ]

        // first line is special: &str type here; consider more than one white space!
        let first_line = input_lines[0].split_whitespace().collect::<Vec<_>>();

        // number of weight items, max capacity, expected max value:
        let n = u32::from_str(first_line[0]).unwrap();

        let max_wt = u32::from_str(first_line[1]).unwrap();

        // expected max value could be -1 if unknown yet => u32 => i32!!!
        //   thread 'main' panicked at 'called `Result::unwrap()` on an `Err` value: ParseIntError { kind: InvalidDigit }', src/main.rs:142:59
        let optimal_profit = i32::from_str(first_line[2]).unwrap();

        println!("  number of weight items = {}", &n);
        println!("  max capacity of knapsack = {}", &max_wt);

        let mut v: Vec<u32> = vec![0; n.try_into().unwrap()];
        let mut w: Vec<u32> = vec![0; n.try_into().unwrap()];

        // reading in v + w:
        let nbr_lines = input_lines.len();  // type: usize

        // assert n here just for fun:
        assert_eq!(n, (nbr_lines - 1) as u32);  // in panic case: thread 'main' panicked at 'assertion failed: `(left == right)`....
        // dbg!(&n);
        // dbg!(&nbr_lines);

        for h in 1..nbr_lines {
            // expect multi-space separation here:
            let chunks = input_lines[h].split_whitespace().collect::<Vec<_>>();

            v[h-1] = u32::from_str(chunks[0]).unwrap();
            w[h-1] = u32::from_str(chunks[1]).unwrap();
        }
        // dbg!(&v);


        ////////////////////////////////////////////////////////////////////////////
        //
        // Dynamic Programming top-down (recursive) procedure:

        // start stopwatch here:

        let result;

        if exe_timer_on {  // true
            let start = Instant::now();

            if picks_on {
                // function in another source file:
                result = dp_knapsack_top_down_recursion::picks_on(w, v, max_wt);
            }
            else {
                // function in another source file:
                result = dp_knapsack_top_down_recursion::picks_off(w, v, max_wt);
            }

            let duration = start.elapsed().as_millis();
            println!("\n  Dynamic programming top-down (recursive) was completed with answer = {} and execution time = {}ms", result, duration );
        }
        else {
            if picks_on {
                result = dp_knapsack_top_down_recursion::picks_on(w, v, max_wt);
            }
            else {
                result = dp_knapsack_top_down_recursion::picks_off(w, v, max_wt);
            }

            println!("\n  Dynamic programming top-down (recursive) was completed with answer = {}", result);
        }

        println!("  The expected maximum value of the optimal knapsack is {}", optimal_profit);

        //
        ////////////////////////////////////////////////////////////////////////////
    }

    Ok(())
}
