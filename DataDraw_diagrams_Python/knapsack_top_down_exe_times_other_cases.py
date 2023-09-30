# knapsack_top_down_exe_times_other_cases.py
"""
Diagram the execution times of the dynamic programming top-down (recursive)
algorithm for different test cases and coded in different programming languages
using the DataDraw Python library
"""
#
# Robert Sackmann, 2023-09-30
#
#
# sources:
#   http://datadraw.org/
#   https://github.com/pepprseed/datadraw-examples/blob/main/examples1.py
#
#
#
# put sampled execution times into same directory: ./DataDraw_diagrams
#
#
# test in Spyder: Python 3.8.10, Win11: OK
#
#
# code analysis: 8.75/10 (30.9.2023, Spyder)
#
#
# to do:
#  -
#  -


import math
import re
# import string
from datadraw import DataDraw, write_svgfile


def run_all():
    """ run diagrams and return the result svg objects in a dict """
    bar_diagram = BarsDiagram()
    svgset1 = {}

    # method for a set of test cases for two languages:
    # svgset1['lang1_WEIGHTS_TODD_16_17_18_cpp_rust']  = \
    #     bar_diagram.lang_pair(import_str='exe_times_WEIGHTS_TODD_16_17_18_cpp_rust',
    #     language_pair='C++ vs Rust -- TODD class problems',
    #     pickstable='on')

    svgset1['lang1_WEIGHTS_TODD_16_17_18_cpp_array_rust']  = \
        bar_diagram.lang_pair(import_str='exe_times_WEIGHTS_TODD_16_17_18_cpp_array_rust',
        language_pair='C++ vs Rust -- C++ array vs Rust vector',
        pickstable='on')



    # method for a set of test cases for two implementations of the same language:
    # svgset1['exe_times_02_cpp_array_vs_vector']  = \
    #     bar_diagram.lang_alter(import_str='exe_times_02_cpp_array_vs_vector',
    #     diagram_title='C++: picks table: vector vs array')

    # svgset1['exe_times_02_cpp_array_vs_vector_TODD']  = \
    #     bar_diagram.lang_alter(import_str='exe_times_02_cpp_array_vs_vector_TODD',
    #     diagram_title='C++: picks table: vector vs array')

    return svgset1


class BarsDiagram:
    """
    collection of diagrams
    """
    def __init__(self):
        self.d_d = DataDraw()


    def lang_pair(self, import_str='exe_times_WEIGHTS_TODD_16_17_18_cpp_rust', \
        language_pair='C++ vs Rust -- TODD class problems', \
        pickstable='on'):
        """
        - diagrams for two programming languages and different test cases
        """
        d_d = self.d_d

        chunks = re.split(' ', language_pair)
        lang_str1 = chunks[0]
        lang_str2 = chunks[2]
        print("  lang_str1 =", lang_str1)
        print("  lang_str2 =", lang_str2)


        if pickstable== 'on':
            diagram_title = language_pair + ", picks on"
        else:
            diagram_title = language_pair + ", picks off"

        import_str1 = 'import ' + import_str
        # print("import_str1 =", import_str1)
        import_str2 = "exec(" + '"' + import_str1 + '")'
        # print("import_str2 =", import_str2)

        # target:
        # eval('exec("import exe_times_WEIGHTS_TODD_16_17_18_cpp_rust")')
        eval(import_str2)

        import_str3 = import_str + '.lang1'
        mydata_lang1 = eval(import_str3)

        import_str3 = import_str + '.lang2'
        mydata_lang2 = eval(import_str3)
        # print("   mydata_lang1 =",  mydata_lang1)
        # print("   mydata_lang2 =",  mydata_lang2)
        # print("   len(mydata_lang1) =",  len(mydata_lang1))
        # print("   len(mydata_lang2) =",  len(mydata_lang2))

        d_d.svgbegin(600, 550)
        d_d.settext(ptsize=14, color='#777')
        d_d.setline(color='#aaa', save=True)

        test_cases_lang1 = []
        test_values_lang1 = []
        test_cases_lang2 = []
        test_values_lang2 = []

        # not a number (nan) data points => make a comment label:
        nan_flag_lang1 = False
        test_nan_lang1 = []
        nan_flag_lang2 = False
        test_nan_lang2 = []


        for i, item in enumerate(mydata_lang1):

            d_d_tuple = item
            test_case_str = d_d_tuple[0] + ", " + lang_str1
            test_cases_lang1.append(test_case_str)
            test_values_lang1.append(d_d_tuple[1])

            if math.isnan(d_d_tuple[1]):
                nan_flag_lang1 = True
                test_nan_lang1.append(1)
            else:
                test_nan_lang1.append(0)


            d_d_tuple = mydata_lang2[i]
            test_case_str = d_d_tuple[0] + ", " + lang_str2
            test_cases_lang2.append(test_case_str)
            test_values_lang2.append(d_d_tuple[1])

            if math.isnan(d_d_tuple[1]):
                nan_flag_lang2 = True
                test_nan_lang2.append(1)
            else:
                test_nan_lang2.append(0)


        y_max = max(*test_values_lang1, *test_values_lang2)
        print("  y_max =", y_max)

        test_cases_zipped = sum(zip(test_cases_lang1, test_cases_lang2),())
        print("  test_cases_zipped =", test_cases_zipped)

        d_d.setspace('X', svgrange=(100,450), categorical=test_cases_zipped)
        d_d.setspace('Y', svgrange=(290,500), datarange=(0,y_max))

        d_d.axis('X', loc='bottom-18', axisline=False, stubrotate=50)
        d_d.axis('Y', grid=True)
        d_d.plotlabels(ylabel='execution time [ms]', ylabelpos=-70)

        # draw the column bars:
        for i, item in enumerate(test_cases_lang1):
            d_d.bar(x=item, y=test_values_lang1[i], color='#88AA88', width=16)
            d_d.bar(x=test_cases_lang2[i], y=test_values_lang2[i], \
                    color='#AB89AB', width=16)

        # title:
        d_d.settext(ptsize=20, adjust=(-45,0))
        d_d.plotlabels(titlepos=+20, title= diagram_title)
        d_d.settext(restore=True)

        if nan_flag_lang1 is True or nan_flag_lang2 is True:
            d_d.settext(ptsize=12, color='#99f')
            nan_label = 'test(s) with no valid result\n(timeout, not enough memory):'
            i = 0
            for j in test_nan_lang1:
                if j == 1:
                    nan_label += "\n" + test_cases_lang1[i]
                i += 1
            i = 0
            for j in test_nan_lang2:
                if j == 1:
                    nan_label += "\n" + test_cases_lang2[i]
                i += 1
            d_d.label(10, y_max*1.05, nan_label)  # 10 = test case #10 as x-position

        return d_d.svgresult()


    def lang_alter(self, import_str='exe_times_02_cpp_array_vs_vector', \
        diagram_title='C++: picks table: vector vs array'):
        """
        - diagrams for a set of test cases for two implementations of the same language
        """
        d_d = self.d_d

        chunks = re.split(' ', diagram_title)
        alt_str1 = chunks[3]
        alt_str2 = chunks[5]
        print("  alt_str1 =", alt_str1)
        print("  alt_str2 =", alt_str2)

        import_str1 = 'import ' + import_str
        print("import_str1 =", import_str1)
        import_str2 = "exec(" + '"' + import_str1 + '")'
        print("import_str2 =", import_str2)

        # target:
        # eval('exec("import exe_times_02_cpp_array_vs_vector")')
        eval(import_str2)

        import_str3 = import_str + '.alt1'
        mydata_alt1 = eval(import_str3)

        import_str3 = import_str + '.alt2'
        mydata_alt2 = eval(import_str3)
        # print("   mydata_alt1 =",  mydata_alt1)
        # print("   mydata_alt2 =",  mydata_alt2)
        # print("   len(mydata_alt1) =",  len(mydata_alt1))
        # print("   len(mydata_alt2) =",  len(mydata_alt2))

        d_d.svgbegin(600, 550)
        d_d.settext(ptsize=14, color='#777')
        d_d.setline(color='#aaa', save=True)

        test_cases_alt1 = []
        test_values_alt1 = []
        test_cases_alt2 = []
        test_values_alt2 = []

        # not a number (nan) data points => make a comment label:
        nan_flag_alt1 = False
        test_nan_alt1 = []
        nan_flag_alt2 = False
        test_nan_alt2 = []


        for i, item in enumerate(mydata_alt1):

            d_d_tuple = item
            test_case_str = d_d_tuple[0] + ", " + alt_str1
            test_cases_alt1.append(test_case_str)
            test_values_alt1.append(d_d_tuple[1])

            if math.isnan(d_d_tuple[1]):
                nan_flag_alt1 = True
                test_nan_alt1.append(1)
            else:
                test_nan_alt1.append(0)


            d_d_tuple = mydata_alt2[i]
            test_case_str = d_d_tuple[0] + ", " + alt_str2
            test_cases_alt2.append(test_case_str)
            test_values_alt2.append(d_d_tuple[1])

            if math.isnan(d_d_tuple[1]):
                nan_flag_alt2 = True
                test_nan_alt2.append(1)
            else:
                test_nan_alt2.append(0)


        y_max = max(*test_values_alt1, *test_values_alt2)
        print("  y_max =", y_max)

        test_cases_zipped = sum(zip(test_cases_alt1, test_cases_alt2),())
        print("  test_cases_zipped =", test_cases_zipped)

        d_d.setspace('X', svgrange=(100,450), categorical=test_cases_zipped)
        d_d.setspace('Y', svgrange=(290,500), datarange=(0,y_max))

        d_d.axis('X', loc='bottom-18', axisline=False, stubrotate=50)
        d_d.axis('Y', grid=True)
        d_d.plotlabels(ylabel='execution time [ms]', ylabelpos=-70)

        # draw the column bars:
        for i, item in enumerate(test_cases_alt1):
            d_d.bar(x=item, y=test_values_alt1[i], color='#88AA88', width=16)
            d_d.bar(x=test_cases_alt2[i], y=test_values_alt2[i], \
                    color='#AB89AB', width=16)

        # title:
        d_d.settext(ptsize=20, adjust=(-45,0))
        d_d.plotlabels(titlepos=+20, title= diagram_title)
        d_d.settext(restore=True)

        if nan_flag_alt1 is True or nan_flag_alt2 is True:
            d_d.settext(ptsize=12, color='#99f')
            nan_label = 'test(s) with no valid result\n(timeout, not enough memory):'
            i = 0
            for j in test_nan_alt1:
                if j == 1:
                    nan_label += "\n" + test_cases_alt1[i]
                i += 1
            i = 0
            for j in test_nan_alt2:
                if j == 1:
                    nan_label += "\n" + test_cases_alt2[i]
                i += 1
            d_d.label(4, y_max*1.05, nan_label)  # 4 = test case #4 as x-position

        return d_d.svgresult()


if __name__ == "__main__":
    svgset = run_all()
    print('writing svg to files...')

    for key, value in svgset.items():
        print(f'  {key}.svg ...')
        write_svgfile(value, f'{key}.svg')

    print('Done.')


# end of knapsack_top_down_exe_times_other_cases.py
