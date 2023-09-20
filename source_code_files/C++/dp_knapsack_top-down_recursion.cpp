// dp_knapsack_top-down_recursion.cpp
//
// 2023-09-16
//


#include <iostream>
#include <vector>
#include <chrono>
#include <limits.h>  // INT_MIN


using namespace std;

using std::chrono::high_resolution_clock;
using std::chrono::duration;
using std::chrono::duration_cast;


#include <unistd.h>  // sysconf()
#include <sys/sysinfo.h>  // get_avphys_pages()


const long long MARGIN_OF_SAFETY_BYTES = 500000000;  // ~500 megabytes; only a very wild guess after some experiments

const long long TIME_LIMIT_MIN = 60000;  // = 1 min minimum timeout waiting time


class knapsack_recursive{
    vector<int> w;  // weights
    vector<int> v;  // values (prices)

    int T, max_wt;  // current weight capacities
    
    long long timeout_input;  // milliseconds

    vector<int> picks;  // 1dim array as vector (dynamic array) --> can grow dynamically

    long long int_milli_start, int_milli_inter, time_counter;
    int CLEANUP_FLAG;  // for timeout calculation

    // const double TIME_LIMIT = 300000;  // = 5 min
    // const long long TIME_LIMIT = 1200000;  // = 20 min

    const long long TIME_CHECK_COUNTER = 30000;  // tick counter in recursive function for timeout check


    // recursive function:
    int solveKnapsack(
        vector<int>& weight,
        vector<int>& value,
        vector<int>& picks,
        int items,
        int capacity) {

        int include, exclude;

        if (time_counter > TIME_CHECK_COUNTER) {
             auto t_i = high_resolution_clock::now();
             int_milli_inter = duration_cast<std::chrono::milliseconds>(t_i.time_since_epoch()).count();

             double duration = int_milli_inter - int_milli_start;

             if (duration > timeout_input)
             {
                if (CLEANUP_FLAG == 0) {
                    CLEANUP_FLAG = 1;
                    // cout << "\n  >>> Dynamic Programming top-down: stopping execution due to exceeded time limit of 20 minutes. Cleaning up...\n" << endl;
                    cout << "\n  >>> Dynamic Programming top-down: stopping execution due to exceeded time limit of " << timeout_input / TIME_LIMIT_MIN << "minutes. Cleaning up...\n" << endl;
                }

                return INT_MIN;
             }
             else time_counter = 0;
         }

         time_counter++;

         if (capacity < 0) return INT_MIN;
         if (items < 0 || capacity == 0) return 0;

         include = value[items] + solveKnapsack(weight, value, picks, items-1, capacity-weight[items]);

         exclude = solveKnapsack(weight, value, picks, items-1, capacity);

         // building up the (huge) picks table (2dim array):
         if (include > exclude) {
             picks[items*max_wt + capacity] = 1;
         }
         else {
             picks[items*max_wt + capacity] = -1;
         }

        return max(include, exclude);
    }


    // print the optimal weights and the actual total weight of the optimal knapsack:
    int printPicks(
        vector<int>& weight,
        vector<int>& value,
        vector<int>& picks,
        int N,
        int capacity) {

        int act_total_weight = 0;
        int act_total_value = 0;
        int size = capacity;
        int item = N-1;  // item id = 0...N-1

        cout << "\n  Optimal weights as picked by the Dynamic Programming top-down (recursive) algo:" << endl;

        while (item >= 0 && act_total_weight < capacity) {
            if (picks[item*capacity + size] == 1) {
                cout << "    id = " << item << ",  weight = " << weight[item] << ",  value = "<< value[item] << endl;
                act_total_weight += weight[item];
                act_total_value += value[item];
                size -= weight[item];
            }
            item -= 1;
        }

        cout << "  => actual weight of optimal knapsack = " << act_total_weight << endl;
        cout << "  => actual value of optimal knapsack = " << act_total_value << endl;

        return 0;
    }


public:
    int result, result_pr = 0;

    knapsack_recursive(vector<int>& w, vector<int>& v, int T, long long timeout_input) : w(w), v(v), T(T), timeout_input(timeout_input) {
        int n = w.size();

        max_wt = T;

        // number of elements of picks table:
        // 2023-09-10: only n * (T+1) elements needed (not (n+1) * (T+1))
        long long picks_alloc = (static_cast<long long>(n)) * (static_cast<long long>(T)+1);


        cout << "\n  DP top-down with picks table on: number of elements of picks table = " << picks_alloc << endl;

        int size_int = sizeof(int);  // vector<int> picks;
        long long picks_alloc_bytes = picks_alloc * static_cast<long long>(size_int);
        cout << "                                   number of bytes of picks table =    " << picks_alloc_bytes << endl;

        // Test case: ./06_WEIGHTS_TODD_19.in: picks_alloc = (19 + 1) * (167772154 + 1) = 3355443100 (elements of type int)
        //   => 3355443100 * 4 bytes = 13421772400 bytes = ~13.4 gigabytes <-- picks_alloc_bytes
        // https://convertlive.com/u/convert/bytes/to/gigabytes

        // Test case: ./06_WEIGHTS_TODD_18.in: picks_alloc_bytes = 6056574520 = ~6.06 gigabytes

        // If an exception is thrown for any reason, these functions have no effect (strong exception safety guarantee). Although not explicitly specified, std::length_error is thrown if the capacity required by the new vector would exceed max_size().
        // from: https://en.cppreference.com/w/cpp/container/vector/resize
        //
        // https://stackoverflow.com/questions/23678678/c-vector-catch-resize-memory-leak
        // this doesn't work with 06_WEIGHTS_TODD_19.in: the recursion is starting, only to see after some while: Segmentation fault (core dumped):
        //   try
        //   {
        //       picks.resize(picks_alloc,0);
        //   }
        //   catch (const bad_alloc& ba)
        //   {
        //       cerr << "\nMemory Exhaustion! Leaving this test case..." << endl;
        //   }

        long long avl_pages = get_avphys_pages();  // available physical page count
        long long page_size = sysconf(_SC_PAGE_SIZE);
        long long avl_page_size_bytes = avl_pages * page_size;
        cout << "                                   avl_page_size_bytes =               " << avl_page_size_bytes << " (available free memory in bytes)" << endl;

        long long net_free_memory_guess = avl_page_size_bytes - MARGIN_OF_SAFETY_BYTES;
        cout << "  available free memory after applying a margin of safety =            " << net_free_memory_guess << endl;


        if (picks_alloc_bytes > net_free_memory_guess) {
            cerr << "\n  recursion is not starting here: it may run out of free available memory including some safety margin!" << endl;

            result = -1;
        }
        else {
            picks.resize(picks_alloc,0);

            // start timeout timer:
            auto t_start = high_resolution_clock::now();
            int_milli_start = duration_cast<std::chrono::milliseconds>(t_start.time_since_epoch()).count();

            time_counter = 0;
            CLEANUP_FLAG = 0;

            cout << "\n  DP top-down: start recursion..." << endl;
            result = solveKnapsack(w, v, picks, n-1, max_wt);  // n-1, not n: stay within the bounds of the w, v arrays!!
            cout << "  end of recursion." << endl;

            if (CLEANUP_FLAG == 1) {
                result = -1;
            }
            else {
                result_pr = printPicks(w, v, picks, n, max_wt);
            }
        }
    }
};



class knapsack_recursive_no_picks{
    vector<int> w;  // weights
    vector<int> v;  // values (prices)

    int T, max_wt;  // current weight capacities
    
    long long timeout_input;  // milliseconds

    long long int_milli_start, int_milli_inter, time_counter;
    int CLEANUP_FLAG;  // for timeout calculation

    // const double TIME_LIMIT = 300000;  // = 5 min
    // const long long TIME_LIMIT = 1200000;  // = 20 min

    const long long TIME_CHECK_COUNTER = 30000;  // millisecond counter in recursive function for timeout check


    // recursive function:
    int solveKnapsack(
        vector<int>& weight,
        vector<int>& value,
        int items,
        int capacity) {

        int include, exclude;

        if (time_counter > TIME_CHECK_COUNTER) {
            auto t_i = high_resolution_clock::now();
            int_milli_inter = duration_cast<std::chrono::milliseconds>(t_i.time_since_epoch()).count();

            double duration = int_milli_inter - int_milli_start;

            if (duration > timeout_input)
            {
                if (CLEANUP_FLAG == 0) {
                    CLEANUP_FLAG = 1;
                    // cout << "\n  >>> Dynamic Programming top-down: stopping execution due to exceeded time limit of 20 minutes. Cleaning up...\n" << endl;
                    cout << "\n  >>> Dynamic Programming top-down: stopping execution due to exceeded time limit of " << timeout_input / TIME_LIMIT_MIN << "minutes. Cleaning up...\n" << endl;
                }

                return INT_MIN;
            }
            else time_counter = 0;
        }

        time_counter++;

        if (capacity < 0) return INT_MIN;
        if (items < 0 || capacity == 0) return 0;

        include = value[items] + solveKnapsack(weight, value, items-1, capacity-weight[items]);

        exclude = solveKnapsack(weight, value, items-1, capacity);

        return max(include, exclude);
    }


public:
    int result, result_pr = 0;

    knapsack_recursive_no_picks(vector<int>& w, vector<int>& v, int T, long long timeout_input) : w(w), v(v), T(T), timeout_input(timeout_input) {
        int n = w.size();

        max_wt = T;

        auto t_start = high_resolution_clock::now();
        int_milli_start = duration_cast<std::chrono::milliseconds>(t_start.time_since_epoch()).count();

        time_counter = 0;
        CLEANUP_FLAG = 0;

        cout << "\n  DP top-down: start recursion with picks table off..." << endl;
        result = solveKnapsack(w, v, n-1, max_wt);  // n-1, not n: stay within the bounds of the w, v arrays!!
        cout << "  end of recursion." << endl;

        if (CLEANUP_FLAG == 1) result = -1;
    }
};
