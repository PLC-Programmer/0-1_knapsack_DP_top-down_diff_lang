# knapsack_top_down_in_diff_languages_exe_times.py
"""
Diagram the execution times of the dynamic programming top-down (recursive)
algorithm for different test cases and coded in different programming languages
using the DataDraw Python library
"""
#
# Robert Sackmann, 2023-09-20a
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
# code analysis: 8.39/10 (20.9.2023, Spyder)
#
#
# to do:
#  -
#  -


import math
import re
import string
from datadraw import DataDraw, write_svgfile


def run_all():
    """ run diagrams and return the result svg objects in a dict """
    bar_diagram = BarsDiagram()
    svgset1 = {}

    # using method for an individual language:
    # svgset1['python']  = bar_diagram.lang(import_str='exe_times_01_python', \
    #                                       exclude='03_WEIGHTS100_Xu_Xu_et_al.in')
    # svgset1['cpp']  = bar_diagram.lang(import_str='exe_times_02_cpp', \
    #                                    exclude='03_WEIGHTS100_Xu_Xu_et_al.in')
    # svgset1['cs']  = bar_diagram.lang(import_str='exe_times_03_cs', \
    #                                   exclude='03_WEIGHTS100_Xu_Xu_et_al.in')
    # svgset1['rust']  = bar_diagram.lang(import_str='exe_times_04_rust', \
    #                                   exclude='03_WEIGHTS100_Xu_Xu_et_al.in')

    # using method for a group of languages for both: picks on + off:
    # svgset1['lang1_WEIGHTS100_Xu_Xu'] = \
    #    bar_diagram.lang_grp(import_str='exe_times_WEIGHTS100_Xu_Xu_lang1', exclude='none')

    # filtering out Python, then call:
    # svgset1['lang1_WEIGHTS_TODD_18'] = \
    #   bar_diagram.lang_grp(import_str='exe_times_WEIGHTS_TODD_18_lang1', exclude='Python')
    # svgset1['lang1_WEIGHTS24_Kreher_Stinson'] = \
    #   bar_diagram.lang_grp(import_str='exe_times_WEIGHTS24_Kreher_Stinson_lang1', exclude='Python')

    # C++: effect of different g++ optimization options:
    svgset1['cpp_gpp_WEIGHTS100_Xu_Xu'] = \
        bar_diagram.cpp_gpp(import_str='exe_times_02_cpp_gpp_options_WEIGHTS100_Xu_Xu')

    return svgset1


class BarsDiagram:
    """
    collection of diagrams
    """
    def __init__(self):
        self.d_d = DataDraw()


    def lang(self, import_str='exe_times_01_python', exclude='none'):
        """
        - diagrams for one programming language and different test cases
        - picks on + picks off in one diagram
        """
        d_d = self.d_d

        chunks = re.split('_', import_str)
        lang_str = chunks[3]
        lang_str1 = string.capwords(lang_str)
        if lang_str1 == 'Cpp':
            lang_str1 = 'C++'
        elif lang_str1 == 'Cs':
            lang_str1 = 'C#'
        # print("lang_str1 =", lang_str1)

        diagram_title = lang_str1


        import_str1 = 'import ' + import_str
        # print("import_str1 =", import_str1)
        import_str2 = "exec(" + '"' + import_str1 + '")'
        # print("import_str2 =", import_str2)

        # target:
        # eval('exec("import exe_times_01_python")')
        eval(import_str2)

        import_str3 = import_str + '.picks_on'
        mydata_picks_on = eval(import_str3)

        import_str3 = import_str + '.picks_off'
        mydata_picks_off = eval(import_str3)
        # print("   mydata_picks_on =",  mydata_picks_on)
        # print("   mydata_picks_off =",  mydata_picks_off)
        # print("   len(mydata_picks_on) =",  len(mydata_picks_on))

        d_d.svgbegin(600, 550)
        d_d.settext(ptsize=14, color='#777')
        d_d.setline(color='#aaa', save=True)

        test_cases_picks_on = []
        test_cases_picks_off = []
        test_values_picks_on = []
        test_values_picks_off = []

        # not a number (nan) data points => make a comment label:
        nan_flag_picks_on = False
        test_nan_picks_on = []
        nan_flag_picks_off = False
        test_nan_picks_off = []
        # print("  test_nan_picks_on =", test_nan_picks_on)
        # print("  test_nan_picks_off =",  test_nan_picks_off)
        # print("  len(test_nan_picks_off) =",  len(test_nan_picks_off))


        for i, item in enumerate(mydata_picks_on):

            d_d_tuple = item
            if d_d_tuple[0] != exclude:
                test_case_str = d_d_tuple[0] + ', picks on'
                test_cases_picks_on.append(test_case_str)
                test_values_picks_on.append(d_d_tuple[1])

                if math.isnan(d_d_tuple[1]):
                    nan_flag_picks_on = True
                    test_nan_picks_on.append(1)
                else:
                    test_nan_picks_on.append(0)


            d_d_tuple = mydata_picks_off[i]
            if d_d_tuple[0] != exclude:
                test_case_str = d_d_tuple[0] + ', picks off'
                test_cases_picks_off.append(test_case_str)
                test_values_picks_off.append(d_d_tuple[1])

                if math.isnan(d_d_tuple[1]):
                    nan_flag_picks_off = True
                    test_nan_picks_off.append(1)
                else:
                    test_nan_picks_off.append(0)


        y_max = max(*test_values_picks_on, *test_values_picks_off)
        # print("  y_max =", y_max)

        # mix picks on and picks off cases for same test case:
        # print("  test_cases, picks on =",  test_cases_picks_on)
        # print("  test_cases, picks off =",  test_cases_picks_off)

        # test_cases_picks_on = []
        # test_cases_picks_off = []
        test_cases_zipped = sum(zip(test_cases_picks_on, test_cases_picks_off),())
        # print("\n  test_cases_zipped =", test_cases_zipped)

        d_d.setspace('X', svgrange=(100,450), categorical=test_cases_zipped)
        d_d.setspace('Y', svgrange=(290,500), datarange=(0,y_max))

        d_d.axis('X', loc='bottom-18', axisline=False, stubrotate=50)
        d_d.axis('Y', grid=True)
        d_d.plotlabels(ylabel='execution time [ms]', ylabelpos=-70)

        # draw the column bars:
        for i, item in enumerate(test_cases_picks_on):
            d_d.bar(x=item, y=test_values_picks_on[i], color='#88AA88', width=16)
            d_d.bar(x=test_cases_picks_off[i], y=test_values_picks_off[i], \
                    color='#AB89AB', width=16)

        # title:
        d_d.settext(ptsize=20, adjust=(-45,0))
        d_d.plotlabels(titlepos=+20, title= diagram_title)
        d_d.settext(restore=True)

        if nan_flag_picks_on is True or nan_flag_picks_off is True:
            d_d.settext(ptsize=12, color='#99f')
            nan_label = 'test(s) with no valid result\n(timeout, not enough memory):'
            i = 0
            for j in test_nan_picks_on:
                if j == 1:
                    nan_label += "\n" + test_cases_picks_on[i]
                i += 1
            i = 0
            for j in test_nan_picks_off:
                if j == 1:
                    nan_label += "\n" + test_cases_picks_off[i]
                i += 1
            d_d.label(10, y_max*1.05, nan_label)  # 10 = test case #10 as x-position

        return d_d.svgresult()



    def lang_grp(self, import_str='exe_times_WEIGHTS100_Xu_Xu_lang1', exclude = 'none'):
        """
        - diagrams for different programming languages and one test case
          - this is for test case 03_WEIGHTS100_Xu_Xu_et_al.in
        - picks on + picks off in one diagram
        """
        d_d = self.d_d

        if import_str == 'exe_times_WEIGHTS100_Xu_Xu_lang1':
            diagram_title = 'Test case: 03_WEIGHTS100_Xu_Xu_et_al.in'

        elif import_str == 'exe_times_WEIGHTS_TODD_18_lang1':
            diagram_title = 'Test case: 05_WEIGHTS_TODD_18.in'

        elif import_str == 'exe_times_WEIGHTS24_Kreher_Stinson_lang1':
            diagram_title = '''Test case: 02_WEIGHTS24_Kreher-Stinson.in'''

        else:
            diagram_title = 'Test case: ???'

        # targets:
        # eval('exec("import exe_times_WEIGHTS100_Xu_Xu_lang1.py")')
        #
        # exe_times_WEIGHTS100_Xu_Xu_lang1.picks_on
        # exe_times_WEIGHTS100_Xu_Xu_lang1.picks_ff

        import_str1 = 'import ' + import_str
        # print("import_str1 =", import_str1)
        import_str2 = "exec(" + '"' + import_str1 + '")'
        # print("import_str2 =", import_str2)
        eval(import_str2)

        import_str3 = import_str + '.picks_on'
        mydata_picks_on = eval(import_str3)

        import_str3 = import_str + '.picks_off'
        mydata_picks_off = eval(import_str3)
        # print("   mydata_picks_on =",  mydata_picks_on)
        # print("   mydata_picks_off =",  mydata_picks_off)
        # print("   len(mydata_picks_on) =",  len(mydata_picks_on))

        d_d.svgbegin(600, 550)
        d_d.settext(ptsize=14, color='#777')
        d_d.setline(color='#aaa', save=True)

        test_cases_picks_on = []
        test_cases_picks_off = []
        test_values_picks_on = []
        test_values_picks_off = []

        # not a number (nan) data points => make a comment label:
        nan_flag_picks_on = False
        test_nan_picks_on = [0 for i in mydata_picks_on]
        nan_flag_picks_off = False
        test_nan_picks_off = [0 for i in mydata_picks_off]


        for i, item in enumerate(mydata_picks_on):

            d_d_tuple = item
            if d_d_tuple[0].lower != exclude.lower:
                test_case_str = d_d_tuple[0] + ', picks on'
                test_cases_picks_on.append(test_case_str)
                test_values_picks_on.append(d_d_tuple[1])
                if math.isnan(d_d_tuple[1]):
                    nan_flag_picks_on = True
                    test_nan_picks_on[i] = 1

            d_d_tuple = mydata_picks_off[i]
            if d_d_tuple[0].lower != exclude.lower:
                test_case_str = d_d_tuple[0] + ', picks off'
                test_cases_picks_off.append(test_case_str)
                test_values_picks_off.append(d_d_tuple[1])
                if math.isnan(d_d_tuple[1]):
                    nan_flag_picks_off = True
                    test_nan_picks_off[i] = 1


        y_max = max(*test_values_picks_on, *test_values_picks_off)
        print("  y_max =", y_max)

        # mix picks on and picks off cases for same language:
        print("  test_cases, picks on =",  test_cases_picks_on)
        print("  test_cases, picks off =",  test_cases_picks_off)

        # test_cases_picks_on = []
        # test_cases_picks_off = []
        test_cases_zipped = sum(zip(test_cases_picks_on, test_cases_picks_off),())
        # print("\n  test_cases_zipped =", test_cases_zipped)

        d_d.setspace('X', svgrange=(100,500), categorical=test_cases_zipped)
        d_d.setspace('Y', svgrange=(240,500), datarange=(0,y_max))

        d_d.axis('X', loc='bottom-18', axisline=False, stubrotate=50)
        d_d.axis('Y', grid=True)
        d_d.plotlabels(ylabel='execution time [ms]', ylabelpos=-70)

        # draw the column bars:
        for i, item in enumerate(test_cases_picks_on):
            d_d.bar(x=item, y=test_values_picks_on[i], color='#88AA88', width=18)
            d_d.bar(x=test_cases_picks_off[i], y=test_values_picks_off[i], \
                    color='#AB89AB', width=18)

        # title:
        d_d.settext(ptsize=20, adjust=(-45,0))
        d_d.plotlabels(titlepos=+20, title= diagram_title)
        d_d.settext(restore=True)

        if nan_flag_picks_on is True or nan_flag_picks_off is True:
            d_d.settext(ptsize=14, color='#99f')
            nan_label = 'test(s) with no valid result\n(timeout, not enough memory):'
            i = 0
            for j in test_nan_picks_on:
                if j == 1:
                    nan_label += "\n  " + test_cases_picks_on[i]
                i += 1
            i = 0
            for j in test_nan_picks_off:
                if j == 1:
                    nan_label += "\n  " + test_cases_picks_off[i]
                i += 1
            d_d.label(4, y_max*0.97, nan_label)  # 4 = test case #4 as x-position

        return d_d.svgresult()



    def cpp_gpp(self, import_str='exe_times_02_cpp_gpp_options_WEIGHTS100_Xu_Xu'):
        """
        - diagram for C++: effect of different g++ optimization options
        (- picks on diagram)
        """
        d_d = self.d_d

        diagram_title = 'C++: g++ optimization options, test case: 03_WEIGHTS100_Xu_Xu_et_al.in'

        import_str1 = 'import ' + import_str
        # print("import_str1 =", import_str1)
        import_str2 = "exec(" + '"' + import_str1 + '")'
        # print("import_str2 =", import_str2)

        # target:
        # eval('exec("import exe_times_02_cpp_gpp_options_WEIGHTS100_Xu_Xu")')
        eval(import_str2)

        import_str3 = import_str + '.picks_on'
        mydata_picks_on = eval(import_str3)
        print("   mydata_picks_on =",  mydata_picks_on)
        print("   len(mydata_picks_on) =",  len(mydata_picks_on))

        d_d.svgbegin(600, 550)
        d_d.settext(ptsize=14, color='#777')
        d_d.setline(color='#aaa', save=True)

        test_cases_picks_on = []
        test_values_picks_on = []


        for i, item in enumerate(mydata_picks_on):
            d_d_tuple = item
            test_case_str = d_d_tuple[0] + ', picks on'
            test_cases_picks_on.append(test_case_str)
            test_values_picks_on.append(d_d_tuple[1])


        y_max = max(*test_values_picks_on)
        print("  y_max =", y_max)

        d_d.setspace('X', svgrange=(100,450), categorical=test_cases_picks_on)
        d_d.setspace('Y', svgrange=(290,500), datarange=(0,y_max))

        d_d.axis('X', loc='bottom-18', axisline=False, stubrotate=50)
        d_d.axis('Y', grid=True)
        d_d.plotlabels(ylabel='execution time [ms]', ylabelpos=-70)

        # draw the column bars:
        for i, item in enumerate(test_cases_picks_on):
            d_d.bar(x=item, y=test_values_picks_on[i], color='#88AA88', width=16)

        # title:
        d_d.settext(ptsize=20, adjust=(-45,0))
        d_d.plotlabels(titlepos=+20, title= diagram_title)
        d_d.settext(restore=True)

        return d_d.svgresult()



if __name__ == "__main__":
    svgset = run_all()
    print('writing svg to files...')

    for key, value in svgset.items():
        print(f'  {key}.svg ...')
        write_svgfile(value, f'{key}.svg')

    print('Done.')


# end of knapsack_top_down_in_diff_languages_exe_times.py
