// dp_knapsack_top_down_recursion.rs
//
// Robert Sackmann, 2023-09-13
//


use std::cmp;
use subprocess::Exec;  // Exec::shell() --> "free -t"
use std::str::FromStr;  // string to integer
use std::time::{Instant};
use once_cell::sync::Lazy;


// globals:
static mut MAX_WT: usize = 0;  // unsafe {}

const MARGIN_OF_SAFETY_BYTES: usize = 500_000_000;  // ~500MB

// const TIME_LIMIT: u128 = 120000;  // = 2 min
const TIME_LIMIT: u128 = 1200000;  // = 20 min
const TIME_CHECK_COUNTER: usize = 30000;  // tick counter in recursive function for timeout check

static mut INT_MILLI_START: Lazy<Instant> = Lazy::new(Instant::now);  // unsafe {}, INT for interval

static mut TIME_COUNTER: usize = 0;     // unsafe {}
static mut CLEANUP_FLAG: bool = false;  // unsafe {}



// recursive function with picks OFF:
fn solve_knapsack_picks_off(weight: &Vec<u32>, val: &Vec<u32>, items: i32, capacity: i32) -> i32 {

    unsafe {
      if TIME_COUNTER > TIME_CHECK_COUNTER {

          let duration = INT_MILLI_START.elapsed().as_millis();

           if duration > TIME_LIMIT {
              if CLEANUP_FLAG == false {
                  CLEANUP_FLAG = true;
                  println!("\n  >>> Dynamic Programming top-down: stopping execution due to exceeded time limit of 20 minutes. Cleaning up...\n");
              }
              return i32::MIN;
           }
           else {TIME_COUNTER = 0;}
       }
       TIME_COUNTER += 1;
    }


    if capacity < 0 {return i32::MIN;}
    if items < 0 || capacity == 0 {return 0;}

    let _items = items as usize;  // usize for indexing

    let include = val[_items] as i32 + solve_knapsack_picks_off(&weight, &val, items - 1, capacity - (weight[_items] as i32));

    let exclude = solve_knapsack_picks_off(&weight, &val, items - 1, capacity);

    return cmp::max(include, exclude);
}



// recursive function with picks ON:
fn solve_knapsack_picks_on(weight: &Vec<u32>, val: &Vec<u32>, picks: &mut Vec<i32>, items: i32, capacity: i32) -> i32 {

     unsafe {
      if TIME_COUNTER > TIME_CHECK_COUNTER {

          let duration = INT_MILLI_START.elapsed().as_millis();

           if duration > TIME_LIMIT {
              if CLEANUP_FLAG == false {
                  CLEANUP_FLAG = true;
                  println!("\n  >>> Dynamic Programming top-down: stopping execution due to exceeded time limit of 20 minutes. Cleaning up...\n");
              }
              return i32::MIN;
           }
           else {TIME_COUNTER = 0;}
       }
       TIME_COUNTER += 1;
    }


    if capacity < 0 {return i32::MIN;}
    if items < 0 || capacity == 0 {return 0;}

    let _items = items as usize;  // usize for indexing

    let include = val[_items] as i32 + solve_knapsack_picks_on(&weight, &val, picks, items - 1, capacity - (weight[_items] as i32));

    let exclude = solve_knapsack_picks_on(&weight, &val, picks, items - 1, capacity);

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

    return cmp::max(include, exclude);
}



// "main" function here (alternative #1):
pub fn picks_off(w: Vec<u32>, v: Vec<u32>, t: u32) -> i32 {

    let n = w.len();  // usize

    // start timeout timer:
    unsafe {
        *INT_MILLI_START = Instant::now();
        TIME_COUNTER = 0;
        CLEANUP_FLAG = false;
    }

    println!("\n  DP top-down: start recursion with picks table off...");
    let mut result = solve_knapsack_picks_off(&w, &v, (n - 1) as i32, t as i32);
    println!("  end of recursion.");

    unsafe {
        if CLEANUP_FLAG == true {result = -1;}
    }

    return result;
}



// "main" function here (alternative #2):
pub fn picks_on(w: Vec<u32>, v: Vec<u32>, t: u32) -> i32 {

    let n = w.len();  // usize

    unsafe {
        MAX_WT = t as usize;  // current weight capacities
    }

    let picks_alloc: usize;

    // number of elements of picks table:
    picks_alloc = (n) * (t as usize + 1);  // usize; 01_WEIGHTS4.in: (4)*(7+1) = 32
    println!("\n  DP top-down with picks table on: number of elements of picks table = {}", picks_alloc);

    // one i32 element takes 4 bytes in memory:
    //   https://doc.rust-lang.org/std/vec/struct.Vec.html#method.with_capacity
    let picks_alloc_bytes = picks_alloc * 4;

    let mem = {Exec::shell("free -t")}.capture().expect("nothing captured!").stdout_str();
    let mem_v = mem.split_whitespace().collect::<Vec<_>>();

    let free_available_memory = usize::from_str(mem_v[9]).unwrap() * 1024 as usize;  // kB --> bytes
    println!("  free available memory [bytes] = {}", free_available_memory);

    if picks_alloc_bytes > (free_available_memory as usize - MARGIN_OF_SAFETY_BYTES) {
        println!("\n  recursion is not starting here: it may run out of free available memory including some safety margin!");

        return -1;
    }
    else {
        // DON't EXECUTE THIS COMMAND WITHOUT CHECKING FOR ENOUGH MEMORY:
        let mut picks: Vec<i32> = vec![0; picks_alloc];

        // start timeout timer:
        unsafe {
            *INT_MILLI_START = Instant::now();
            TIME_COUNTER = 0;
            CLEANUP_FLAG = false;
        }

        println!("\n  DP top-down: start recursion...");
        let mut result = solve_knapsack_picks_on(&w, &v, &mut picks, (n - 1) as i32, t as i32);
        println!("  end of recursion.");

        unsafe {
            if CLEANUP_FLAG == true {result = -1;}
            else {print_picks(&w, &v, &picks, n, t as usize);}
        }

        return result;
    }
}



fn print_picks(weight: &Vec<u32>, val: &Vec<u32>, picks: &Vec<i32>, n: usize, capacity: usize) {

    let mut act_total_weight: u32 = 0;
    let mut act_total_value: u32 = 0;
    let mut size = capacity as usize;
    let mut item = (n - 1) as usize;  // item id = 0...N-1

    println!("\n  Optimal weights:");

    while act_total_weight < (capacity as u32) {

        if picks[item * capacity + size] == 1 {
            println!("    id = {}, weight = {},  value = {}", item, weight[item], val[item]);

            act_total_weight += weight[item];
            act_total_value += val[item];

            size -= weight[item] as usize;
        }

        item -= 1;
        if item == 0 {  // comparison is useless due to type limits
            break;
        }
    }

    println!("  => actual weight of optimal knapsack = {}", act_total_weight);
    println!("  => actual value of optimal knapsack = {}", act_total_value);

    // just an extra effort:
    print_picks_table(&picks, n, capacity);
}



fn print_picks_table(picks: &Vec<i32>, n: usize, capacity: usize) {

    if n > 10 || capacity > 10 {
        println!("  Picks table is too big to print here in detail. Returning...");
        return;
    }

    println!("\n  picks table in detail: horizontal = increasing weight capacity of knapsack, vertical = weight item:");

    // loop over items:
    for i in 0..n {

        print!("   ");
        // loop over capacity:
        for j in 0..capacity+1 {
            // using a format string: always 2 digits per value for spacing reasons: -1, 0, +1:
            print!(" {:2}", picks[i * capacity + j as usize]);
        }
        println!();
    }
}
