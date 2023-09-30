// dp_knapsack_top-down_main_array.cpp
//
// Robert Sackmann, 2023-09-30
//
// test: OK
// environment: $ uname -a --> Linux ... 6.2.0-32-generic #32~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug 18 10:40:13 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
//
//
// compile: $ g++ -O3 ./dp_knapsack_top-down_main_array.cpp -o dp_knapsack_top-down_main_array
// run:     $ ./dp_knapsack_top-down_main_array [no_picks, nopicks, picks_off, picksoff] [20] [no_timer, notimer, timer_off, timeroff]
//
//
// to do:
//    -
//    -
//


#include <chrono>
#include <iostream>
#include <vector>
#include <dirent.h>
#include <stdio.h>
#include <unistd.h>  // getcwd()
#include <regex.h>
#include <string.h>
#include <limits.h>  // INT_MIN, PATH_MAX
#include <sys/resource.h>  // temporary increase of stack size

// #include "./dp_knapsack_top-down_recursion.cpp"
#include "./dp_knapsack_top-down_recursion_array.cpp"


using namespace std;

using std::chrono::high_resolution_clock;
using std::chrono::duration;


const char* INPUTFILES = "./";
const rlim_t kStackSize = 64 * 1024 * 1024;  // min stack size = 16 MB; type long unsigned int

const int NBR_FILES = 20;


// needed for qsort of file names:
int string_cmp(const void * a, const void * b ) {
    const char * pa = (const char *) a;
    const char * pb = (const char *) b;

    return strcmp(pa,pb);
}


int main(int argc, char* argv[]) {
    // temporarily increase the stack size from 8MB to 64MB (in Ubuntu 22.04.3 LTS) to try to prevent segmentation faults:
    struct rlimit rl;
    int result = getrlimit(RLIMIT_STACK, &rl);
    if (result == 0)
    {
        printf("\nTemporary increase of stack size");
        printf("rl.rlim_cur = %lu \n", rl.rlim_cur);  // %lu for unsigned long

        if (rl.rlim_cur < kStackSize)
        {
            rl.rlim_cur = kStackSize;
            result = setrlimit(RLIMIT_STACK, &rl);
            if (result != 0)
            {
                fprintf(stderr, "setrlimit returned result = %d\n", result);
                return 1;
            }
            else printf("After change: rl.rlim_cur = %lu \n", rl.rlim_cur);  // %lu for unsigned long
        }
    }
    else {
        printf("\ncannot access stack size... leaving...");
        return 1;
    }


    bool picks_on = true;  // default: with picks table activated
    bool exe_timer_on = true;  // default: with internal execution timer activated
    
    long long TIME_LIMIT = 1200000;  // = 20 min default setting

    if (argc > 1) {
        if (strcmp(argv[1], "no_picks") == 0 ||
            strcmp(argv[1], "nopicks") == 0 ||
            strcmp(argv[1], "picks_off") == 0 ||
            strcmp(argv[1], "picksoff") == 0)
        {
            picks_on = false;  // no picks table to be activated
        }
        
        if (argv[2] != NULL)
        {
            long long TIME_LIMIT_a = stoi(argv[2]) * 60000;  // user set timeout waiting time in [min] --> milliseconds
            TIME_LIMIT = max(TIME_LIMIT_MIN, TIME_LIMIT_a);  // have a minimum of 1 minute
        }

        if (strcmp(argv[3], "no_timer") == 0 ||
            strcmp(argv[3], "notimer") == 0 ||
            strcmp(argv[3], "timer_off") == 0 ||
            strcmp(argv[3], "timeroff") == 0)
        {
            exe_timer_on = false;  // no internal execution timer to be activated
        } 
        
    }
    

    char cwd[PATH_MAX];
    DIR *d;
    char* buffer;
    buffer = getcwd(cwd, sizeof(cwd));  // https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/getcwd-wgetcwd?view=msvc-170
    d = opendir(cwd);
    struct dirent *dir;

    regex_t regex;
    int reti = regcomp(&regex, "\\.in$", REG_EXTENDED);

    char file_name[NBR_FILES][PATH_MAX];
    int i = 0;

    if (d && !reti) {  // regular expression compiled OK
        while ((dir = readdir(d)) != NULL) {
          char file_path[PATH_MAX];
          char* temp_name = dir->d_name;
          reti = regexec(&regex, temp_name, 0, NULL, 0);
          if (!reti) {  // pattern match
              strcpy(file_path, INPUTFILES);
              strcat(file_path, temp_name);
              strcpy(file_name[i], file_path);
              i++;
          }
        }
        closedir(d);

        if (i == 0) {
            printf("\nNo input files *.in could be found in directory %s\n", cwd);
            return 1;
        }
    }
    else if (!d) {
        printf("\nCannot open directory %s!\n", cwd);
        return 1;
    }

    int nbr_files = i;  // number of input files with test cases

    // sort alphabetically char *file_name[]:
    qsort(file_name, nbr_files, sizeof(file_name[0]), string_cmp);

    printf("\nSorted list of input files with test cases:");
    for (int i = 0; i < nbr_files; i++) {
        printf("\n  %s", file_name[i]);
    }


    // service announcement:
    printf("\n\nAnswer of -1 means that no optimal value is known or no optimal value could be computed within the time limit.\n");




    // changes: loop over input files with test cases:
    for (int h = 0; h < nbr_files; h++)
    {
        printf("\n\nTest case: %s", file_name[h]);

        FILE *in_file;
        in_file = fopen(file_name[h], "r");  // open file with relative path
        if(in_file == NULL){
            printf("\nCan't open input file!\n");
            return 1;
        }

        char line[128];
        int n, T, optimal_profit = -1;
        // n = number of weights
        // T = max.capacity of knapsack
        // optimal_profit = the expected optimal value of the optimal knapsack

        // line 0 is special: int n, T, optimal_profit to be expected here:
        if (fgets(line, sizeof(line), in_file) != NULL)
        {
            if (sscanf(line, "%d %d %d", &n, &T, &optimal_profit) != 3) {
                printf("\n1/ Something went wrong while reading numbers of the test case!\n");
                return 1;
            }
        }

        vector<int> v(n), w(n);  // values (prices), weights

        int i = 0;
        // reading values and related weights:
        while (fgets(line, sizeof(line), in_file) != NULL)
        {
            if (sscanf(line, "%d %d", &v[i], &w[i]) != 2) {
                printf("\n2/ Something went wrong while reading numbers of the test case!\n");
                return 1;
            }
            i++;
        }


        cout << "\n  timeout waiting time = " << TIME_LIMIT / TIME_LIMIT_MIN << "min" << endl;


        ////////////////////////////////////////////////////////////////////////////
        //
        // Dynamic Programming top-down (recursive) procedure:

        if (picks_on == true) {
            if (exe_timer_on == true ) {               
                auto t1 = high_resolution_clock::now();
                knapsack_recursive td_knaps(w, v, T, TIME_LIMIT);
                auto t2 = high_resolution_clock::now();
                duration<double, std::milli> time_dp_top_down = t2 - t1;
                
                cout << "  Dynamic programming top-down (recursive) was completed with answer = " << td_knaps.result << " and execution time = " << time_dp_top_down.count() << "ms" << endl;
            }
            else {
                knapsack_recursive td_knaps(w, v, T, TIME_LIMIT);
                
                cout << "  Dynamic programming top-down (recursive) was completed with answer = " << td_knaps.result << endl;
            }
        }

        else {
            if (exe_timer_on == true ) {               
                auto t1 = high_resolution_clock::now();
                knapsack_recursive_no_picks td_knaps(w, v, T, TIME_LIMIT);
                auto t2 = high_resolution_clock::now();
                duration<double, std::milli> time_dp_top_down = t2 - t1;
                
                cout << "  Dynamic programming top-down (recursive) was completed with answer = " << td_knaps.result << " and execution time = " << time_dp_top_down.count() << "ms" << endl;
            }
            else {
                knapsack_recursive_no_picks td_knaps(w, v, T, TIME_LIMIT);

                cout << "  Dynamic programming top-down (recursive) was completed with answer = " << td_knaps.result << endl;
            }
        }

        cout << "  The expected maximum value of the optimal knapsack is " << optimal_profit << endl;

        //
        ////////////////////////////////////////////////////////////////////////////


        fclose(in_file);
    }


    regfree(&regex);

    return 0;
}
