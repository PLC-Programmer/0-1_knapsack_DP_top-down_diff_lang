// dp_knapsack_top-down_recursion.cs
//
// Robert Sackmann, 2023-09-14
//


using System.Diagnostics;  // Stopwatch


namespace dp_knapsack_top_down;


class knapsack_recursive
{
    int max_wt;  // current weight capacities
    int[]? picks;  // Consider declaring the field as nullable.

    public static int result = -1;

    static long time_counter;
    static long int_milli_inter;
    Stopwatch? timeout_timer;  // Consider declaring the field as nullable.
    static bool CLEANUP_FLAG;  // for timeout calculation

    // const long TIME_LIMIT = 120000;  // = 2 min
    const long TIME_LIMIT = 1200000;  // = 20 min
    const long TIME_CHECK_COUNTER = 30000;  // tick counter in recursive function for timeout check


    // recursive function:
    int solveKnapsack (
        int[] weight,
        int[] val,
        int[] picks,
        int items,
        int capacity
        ) {

        int include, exclude;

        if (time_counter > TIME_CHECK_COUNTER) {
            if (timeout_timer != null) {
                int_milli_inter = timeout_timer.ElapsedMilliseconds;  // Dereference of a possibly null reference.

                if (int_milli_inter > TIME_LIMIT) {
                   if (CLEANUP_FLAG == false) {
                       CLEANUP_FLAG = true;
                       Console.WriteLine("\n  >>> Dynamic Programming top-down: stopping execution due to exceeded time limit of 20 minutes. Cleaning up...\n");
                   }

                   return Int32.MinValue;
                }
                else {
                    time_counter = 0;
                }
            }
        }

        time_counter++;


        if (capacity < 0) return Int32.MinValue;
        if (items < 0 || capacity == 0) return 0;

        include = val[items] + solveKnapsack(weight, val, picks, items-1, capacity-weight[items]);

        exclude = solveKnapsack(weight, val, picks, items-1, capacity);

        // building up the (huge) picks table (2dim array):
        if (include > exclude) {
            picks[items*max_wt + capacity] = 1;
        }
        else {
            picks[items*max_wt + capacity] = -1;
        }

        return Math.Max(include, exclude);
    }


    int printPicks(
        int[] weight,
        int[] val,
        int[] picks,
        int N,
        int capacity) {

        int act_total_weight = 0;
        int act_total_value = 0;
        int size = capacity;
        int item = N-1;  // item id = 0...N-1

        Console.WriteLine("\n  Optimal weights:");

        while (item >= 0 && act_total_weight < capacity) {
            if (picks[item*capacity + size] == 1) {
                Console.WriteLine("    id = " + item + ",  weight = " + weight[item] + ",  value = " + val[item]);
                act_total_weight += weight[item];
                act_total_value += val[item];
                size -= weight[item];
            }
            item -= 1;
        }

        Console.WriteLine("  => actual weight of optimal knapsack = " + act_total_weight);
        Console.WriteLine("  => actual value of optimal knapsack = " + act_total_value);

        return 0;
    }



    public knapsack_recursive (int[] w, int[] v, int T)
    {
        int n = w.Length;

        max_wt = T;

        ulong picks_alloc = (Convert.ToUInt64(n))*(Convert.ToUInt64(T+1));  // 01_WEIGHTS4.in: (4)*(7+1) = 32

        Console.WriteLine("\n  DP top-down with picks table on: number of elements of picks table = " + picks_alloc);

        // ulong picks_alloc_bytes = picks_alloc * 4;  // speculative!!
        // Console.WriteLine("                                   number of bytes of picks table =    " + picks_alloc_bytes);

        /*
        <gcAllowVeryLargeObjects> element (2023-09-01)
        https://learn.microsoft.com/en-us/dotnet/framework/configure-apps/file-schema/runtime/gcallowverylargeobjects-element?redirectedfrom=MSDN
          The maximum size in any single dimension is 2,147,483,591 (0x7FFFFFC7) for byte arrays and
          arrays of single-byte structures, and 2,146,435,071 (0X7FEFFFFF) for arrays containing other types.
        If not considered --> Unhandled exception. System.OverflowException: Array dimensions exceeded supported range; Aborted (core dumped)

        1 int value takes 4 bytes: https://learn.microsoft.com/de-de/dotnet/api/system.int32?view=net-7.0

        free available memory: do not calculate it here with C#: implicitly assume that there would be always something like 4GB or so for the memory: System.Int32.MaxValue is the most probable limit:

        Test case: 05_WEIGHTS_TODD_18.in:
            max capacity of knapsack = 79691769
            DP top-down with picks table on: number of elements of picks table = 1434451860
                                                number of bytes of picks table =    5737807440
                  (maximum size of arrays of non-single-byte structures [bytes] =    2146435071) --> speculative!!
            DP top-down: start recursion...
            end of recursion.
        */

        try {
            picks = new int[picks_alloc];

            // start timeout timer:
            timeout_timer = Stopwatch.StartNew();

            time_counter = 0;
            CLEANUP_FLAG = false;

            Console.WriteLine("\n  DP top-down: start recursion...");
            result = solveKnapsack(w, v, picks, n-1, max_wt); // n-1, not n: stay within the bounds of the w and v arrays!!
            Console.WriteLine("  end of recursion.");

            timeout_timer.Stop();

            if (CLEANUP_FLAG == false) {
                int result_pr = printPicks(w, v, picks, n, max_wt);
            }
        }
        catch (Exception e) {
            Console.WriteLine("\n  Can't allocate memory for an int array with elements for a picks table of needed size: " + e.Message);
            result = -1;
        }

        if (CLEANUP_FLAG == true) {
            result = -1;
        }
    }
}



class knapsack_recursive_no_picks
{
    int max_wt;  // current weight capacities

    public static int result = -1;

    static long time_counter;
    static long int_milli_inter;
    Stopwatch? timeout_timer;  // Consider declaring the field as nullable.
    static bool CLEANUP_FLAG;  // for timeout calculation

    // const long TIME_LIMIT = 120000;  // = 2 min
    const long TIME_LIMIT = 1200000;  // = 20 min
    const long TIME_CHECK_COUNTER = 30000;  // tick counter in recursive function for timeout check


    // recursive function:
    int solveKnapsack (
        int[] weight,
        int[] val,
        int items,
        int capacity
        ) {

        int include, exclude;

        if (time_counter > TIME_CHECK_COUNTER) {
            if (timeout_timer != null) {
                int_milli_inter = timeout_timer.ElapsedMilliseconds;  // Dereference of a possibly null reference.

                if (int_milli_inter > TIME_LIMIT) {
                   if (CLEANUP_FLAG == false) {
                       CLEANUP_FLAG = true;
                       Console.WriteLine("\n  >>> Dynamic Programming top-down: stopping execution due to exceeded time limit of 20 minutes. Cleaning up...\n");
                   }

                   return Int32.MinValue;
                }
                else {
                    time_counter = 0;
                }
            }
        }

        time_counter++;


        if (capacity < 0) return Int32.MinValue;
        if (items < 0 || capacity == 0) return 0;

        include = val[items] + solveKnapsack(weight, val, items-1, capacity-weight[items]);

        exclude = solveKnapsack(weight, val, items-1, capacity);

        return Math.Max(include, exclude);
    }


    public knapsack_recursive_no_picks (int[] w, int[] v, int T)
    {
        int n = w.Length;

        max_wt = T;

        timeout_timer = Stopwatch.StartNew();

        Console.WriteLine("\n  DP top-down: start recursion...");
        result = solveKnapsack(w, v, n-1, max_wt);  // n-1, not n: stay within the bounds of the w and v arrays!!
        Console.WriteLine("  end of recursion.");

        if (CLEANUP_FLAG == true) {
            result = -1;
        }
    }
}
