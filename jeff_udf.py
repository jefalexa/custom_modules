import pandas as pd
import numpy as np
import datetime as dt
import os, sys
import re
import logging
import ipywidgets as widgets
from ipywidgets import interact, interact_manual, Button, Box, Layout, interactive, fixed, interact_manual
from IPython.display import clear_output

dir_home_options = ["/home/jovyan/work/", "/Users/jefalexa/"]
for dir_home in dir_home_options:
    if bool(re.match(dir_home, os.getcwd())):
        break
    else:
        continue
dir_clipboard = os.path.join(dir_home, "Box Sync/data_repo/interim/clipboard")


def check_match(x, y, Match_Case=True):
    '''Check if variable (x) matches regex pattern (y).  Return True, False or N/A'''
    try:
        if Match_Case:
            pattern = re.compile(y)
        else:
            pattern = re.compile(y, flags=re.IGNORECASE)
        return(bool(re.search(pattern=pattern, string=x)))
    except:
        return("N/A")

		
def usd_to_float(test_string):
    '''Turn a string representing a dollar amount into a float. '''
    pattern = re.compile("(\$)|(USD \$)|(USD)")
    try:
        split = re.split(pattern, test_string)
        return(float(split[-1]))
    except:
        return(0)
        

def get_fy_info(date, calendar_fy, field=''):
    '''Returns the fiscal calendar information for a given date
    INPUTS:  
        date='%Y-%m-%d'
        calendar_fy=DataFrame with Fiscal Information, generaly saved in Interim folder
        field=If a valid field from the DF is listed, return just the value, if not, return the entire DF
    '''
    f1 = calendar_fy['Fiscal Week Start Date'] <= date
    f2 = calendar_fy['Fiscal Week End Date'] >= date
    if field in calendar_fy.columns:
        return(calendar_fy.loc[f1&f2, field].to_list()[0])
    else:
        return(calendar_fy.loc[f1&f2, :])


   
def local_find(working_dir, x=".*"):
    pattern = re.compile(x)
    file_list = []
    try:
        for file in os.listdir(working_dir):
            if re.match(pattern=pattern, string=file):
                file_list.append(file)
        return(file_list)
    except:
        file_list = []
        return(file_list)

def local_find_recent(working_dir, x=".*"):
    pattern = re.compile(x)
    file_list = []
    fts_min = 0
    try:
        for file in os.listdir(working_dir):
            if re.match(pattern=pattern, string=file):
                f2 = os.path.join(working_dir, file)
                fts = os.stat(f2).st_mtime
                fdt = dt.datetime.fromtimestamp(fts)
                if ((fts_min < fts) | (fts_min == 0)):
                    file_list = [file, f2, fdt]
                    fts_min = fts
        return(file_list)
    except:
        print("Error")
        file_list = []
        return(file_list)


def local_find_to_df(working_dir, x=".*"):
    pattern = re.compile(x)
    file_list = []
    try:
        for file in os.listdir(working_dir):
            if re.match(pattern=pattern, string=file):
                f2 = os.path.join(working_dir, file)
                fsize = os.stat(f2).st_size
                fts = os.stat(f2).st_mtime
                fdt = dt.datetime.fromtimestamp(fts)
                #print(file, fsize, fdt)
                file_list.append([file, fsize, fdt])
        return(pd.DataFrame(columns=['Filename', 'Size', 'Modified Time'], data=file_list))
    except:
        print("Error")
        file_list = []
        return(pd.DataFrame(columns=['Filename', 'Size', 'Modified Time'], data=file_list))
 
def local_find_dir(working_dir):
	'''Returns a list of root directories in a given directory'''
	directory_list = []
	for name in os.listdir(working_dir):
		if os.path.isdir(os.path.join(working_dir, name)):
			directory_list.append(os.path.join(working_dir, name))
		return(directory_list)


def interactive_file_saveloc(dir_list, search_pattern):
    output_file = ""
    def test01(dir_input=dir_list, search_pattern=fixed(search_pattern)):
        file_df = local_find_to_df(dir_input, search_pattern).sort_values(by='Modified Time', ascending=False)
        file_list = file_df['Filename'].tolist()
        file_list.insert(0, "")
        interact(test02, file_picker="{}".format(dt.datetime.strftime(dt.datetime.now(), '%m%d%Y_%H%M')), dir_input=fixed(dir_input), file_df=fixed(file_df))
    def test02(file_picker, dir_input, file_df):
        global interactive_file_saveloc_output
        interactive_file_saveloc_output = [file_picker, os.path.join(dir_input, file_picker), dir_input]
        if len(file_picker) > 0:
            print(output_file)
            return(file_df.loc[file_df['Filename'].apply(lambda x: check_match(x, file_picker)) == True ]     )
        else:
            return(file_df)    
    interact(test01, dir_input=dir_list, search_pattern=fixed(search_pattern))
 


def interactive_table_frame(df):
    col_list = df.select_dtypes('object').columns
    val_list = df.select_dtypes('float').columns
    def itf01(Filter1_Name, Filter2_Name, col_list, val_list):
        l1 = df[Filter1_Name].sort_values().unique().tolist()
        l1.insert(0, 'ANY')
        l1.insert(1, '')
        l2 = df[Filter2_Name].sort_values().unique().tolist()
        l2.insert(0, 'ANY')
        interact(test02, Filter1_Value='ANY', Filter2_Value='ANY', SortBy=df.columns, Ascending=[True, False], Clipboard=[False, True], Filter1_Name=fixed(Filter1_Name), Filter2_Name=fixed(Filter2_Name))
    def test02(Filter1_Value, Filter2_Value, SortBy, Ascending, Clipboard, Filter1_Name, Filter2_Name):
        try: 
            if Filter1_Value == 'ANY':
                pdata1 = df
            else:
                #pattern = re.compile(r"{}".format(Filter1_Value))
                pdata1 = df.loc[df[Filter1_Name].apply(lambda x: check_match(x, Filter1_Value)) == True]

            if Filter2_Value == 'ANY':
                pdata2 = pdata1
            else:
                #pattern = re.compile(r"{}".format(Filter2_Value))
                pdata2 = pdata1.loc[pdata1[Filter2_Name].apply(lambda x: check_match(x, Filter2_Value)) == True]

            pdata3 = pdata2.sort_values(SortBy, ascending=Ascending)
            if Clipboard:
            	pdata3.to_clipboard(index=False)
            global interactive_table_frame_output
            interactive_table_frame_output = pdata3
            return(pdata3)
        except:
            print("Make a selection")
    interact(itf01, Filter1_Name=col_list, Filter2_Name=col_list, col_list=fixed(col_list), val_list=fixed(val_list))
                   

def interactive_tabs(df):
    global tab_contents
    global tab
    #tab_contents = df.columns.sort_values()
    tab_contents = df.columns
    children = []
    for name in tab_contents:
        try:
            l1 = df[name].dropna().sort_values().unique().tolist()
            l1.insert(0, '')
            if df[name].dtype == (float or int):
                f1 = widgets.HBox([widgets.Label(name), widgets.FloatRangeSlider(value=[df[name].min(), df[name].max()], min=df[name].min(), max=df[name].max(), step=1, disabled=False, continuous_update=False, orientation='horizontal', readout=True, readout_format='.0f', ) ])
            else:
                if len(l1) <= 20:
                    f1 = widgets.HBox([widgets.Label(name), widgets.SelectMultiple(options=l1, disabled=False) ])
                else:
                    #f1 = widgets.Text(value='.*',placeholder='.*',description='Filter:  ',disabled=False) 
                    f1 = widgets.HBox([widgets.Label(name), widgets.Text(value='.*',placeholder='.*',disabled=False) ])

            children.append(f1)
        except:
            print("Error on {}".format(name))
    tab = widgets.Tab()
    tab.children = children
    for i in range(len(children)):
        tab.set_title(i, tab_contents[i])
    return(tab)

def interactive_tabs_display(df1):
    index_num = 0
    total_len = len(df1)
    for index_num in range(0, len(tab_contents)):
        tname = tab_contents[index_num]
        tval = tab.children[index_num].children[1].value
        if tval:
            vt = type(tval)
            if vt == type(tuple()):
                if df1[tname].dtype == (float or int):
                    if ((tab.children[index_num].children[1].min == tval[0]) & (tab.children[index_num].children[1].max == tval[1])):
                        continue
                    else:
                        f1 = df1[tname] >= tval[0]
                        f2 = df1[tname] <= tval[1]
                        df1 = df1.loc[f1&f2, :]
                        print("____________\n{} Min: {} - Max: {}".format(tname, tval[0], tval[1]))
                        print("Matched {} entries".format(len(df1)))
                else:
                    if tval == ('',):
                        continue
                    else:
                        f1 = df1[tname].isin(tval)
                        df1 = df1.loc[f1, :]
                    print("____________\n{} {}".format(tname, tval))
                    print("Matched {} entries".format(len(df1)))
            else:
                if tval == '.*':
                    continue
                else:
                    Match_Case = True
                    df1 = df1.loc[df1[tname].apply(lambda x: check_match(x, tval, Match_Case)) == True]
                    print("____________\n{}: '{}' Matched:\n".format(tname, tval), df1[tname].value_counts())
    
    print("____________\n", "Matched {} of {} entries".format(len(df1), total_len))
    return(df1)


def to_myclip(df):
    date_str = dt.datetime.strftime(dt.datetime.now(), '%m-%d-%y_%H%M%S')
    file_name = "clipboard_{}.csv".format(date_str)
    file = os.path.join(dir_clipboard, file_name)
    df.to_csv(file)
    print("Saved:  {}".format(file))


def read_myclip():
	file = local_find_recent(dir_clipboard, x=".*.csv")[1]
	df = pd.read_csv(file, index_col=0)
	return(df)
	
	
class file_picker():
    '''
    Create a file_picker object mypicker01, then call mypicker01.interactive_file_picker(dir_list=['./', '../'], search_pattern=".*") to pick files from a set of directories.  
    Then reference file name, full file path and the directory as mypicker01.file_name, mypicker01.file_path, mypicker01.file_dir.  Or all three as mypicker01.interactive_file_picker_output
    '''
    def __init__(self, dir_list=['./', '../'], search_pattern=".*"):
        self.file = ""
        self.interactive_file_picker_output = []
        self.file_name = ""
        self.file_path = ""
        self.file_dir = ""
        self.dir_list = []
        self.search_pattern = ""
        self.dir_list = dir_list
        self.search_pattern = search_pattern
    def select(self):
        dir_list = self.dir_list
        search_pattern = self.search_pattern
        def ifp_sub01(dir_input, search_pattern):
            file_list = self.__local_find_to_df(dir_input, search_pattern).sort_values(by='Modified Time', ascending=False)['Filename'].tolist()
            file_list.insert(0, "")
            interact(ifp_sub02, dir_input=fixed(dir_input), file_picker=file_list, search_pattern=fixed(search_pattern))
        def ifp_sub02(dir_input, file_picker, search_pattern):
            self.file = os.path.join(dir_input, file_picker)
            if len(file_picker) > 0:
                file_path = os.path.join(dir_input, self.file)
                if os.path.isdir(file_path):
                    print("'{}' added to directory list.  Reload select function.".format(file_path))
                    self.dir_list.append(file_path)
                else:
                    self.interactive_file_picker_output = [file_picker, self.file, dir_input]
                    self.file_name, self.file_path, self.file_dir = [file_picker, self.file, dir_input]
                    print("  File:  {}\n  Path:  {}\n  Size: {}\n  Modified: {}".format(file_picker, self.file, os.stat(self.file).st_size, dt.datetime.strftime(dt.datetime.fromtimestamp(os.stat(self.file).st_mtime), '%m-%d-%y %H:%M')))
            else:
                return(self.__local_find_to_df(dir_input, search_pattern).sort_values(by='Modified Time', ascending=False))
        interact(ifp_sub01, dir_input=dir_list, search_pattern=fixed(search_pattern))

    def __local_find_to_df(self, working_dir, x=".*"):
        pattern = re.compile(x)
        file_list = []
        try:
            for file in os.listdir(working_dir):
                if re.match(pattern=pattern, string=file):
                    f2 = os.path.join(working_dir, file)
                    fsize = os.stat(f2).st_size
                    fts = os.stat(f2).st_mtime
                    fdt = dt.datetime.fromtimestamp(fts)
                    #print(file, fsize, fdt)
                    file_list.append([file, fsize, fdt])
            return(pd.DataFrame(columns=['Filename', 'Size', 'Modified Time'], data=file_list))
        except:
            print("Error")
            file_list = []
            return(pd.DataFrame(columns=['Filename', 'Size', 'Modified Time'], data=file_list))


class interactive_tabs():
    def __init__(self, df):
        self.tab_contents = []
        self.tab = widgets.Tab()
        self.df = df
        self.cols = df.columns

    def select_columns(self):
        f1 = widgets.HBox([widgets.Label("Columns"), widgets.SelectMultiple(options=self.df.columns, value=tuple(self.df.columns), disabled=False) ])
        
        def handle_col_change(change):
            self.cols = list(f1.children[1].value)
            
        button = widgets.Button(description="Apply")
        output = widgets.Output()
        with output:
            display(self.select())
        
        def on_button_clicked(b):
            with output:
                self.cols = list(f1.children[1].value)
                clear_output(wait=True)
                display(self.select())
        f1.children[1].observe(on_button_clicked, names='value')
        
        display(f1, output)

    def select(self):
        self.tab_contents = self.cols
        children = []
        for name in self.tab_contents:
            try:
                l1 = self.df[name].dropna().sort_values().unique().tolist()
                l1.insert(0, '')
                if self.df[name].dtype == (float or int):
                    f1 = widgets.HBox([widgets.Label(name), widgets.FloatRangeSlider(value=[self.df[name].min(), self.df[name].max()], min=self.df[name].min(), max=self.df[name].max(), step=1, disabled=False, continuous_update=False, orientation='horizontal', readout=True, readout_format='.0f', ) ])
                else:
                    if len(l1) <= 30:
                        f1 = widgets.HBox([widgets.Label(name), widgets.SelectMultiple(options=l1, disabled=False) ])
                    else:
                        f1 = widgets.HBox([widgets.Label(name), widgets.Text(value='.*',placeholder='.*',disabled=False) ])
                children.append(f1)
            except:
                print("Error on {}".format(name))
        self.tab.children = children
        for i in range(len(children)):
            self.tab.set_title(i, self.tab_contents[i])
        display(self.tab)

    def display(self):
        index_num = 0
        df1 = self.df[self.cols]
        total_len = len(df1)
        for index_num in range(0, len(self.tab_contents)):
            tname = self.tab_contents[index_num]
            tval = self.tab.children[index_num].children[1].value
            if tval:
                vt = type(tval)
                if vt == type(tuple()):
                    if df1[tname].dtype == (float or int):
                        if ((self.tab.children[index_num].children[1].min == tval[0]) & (self.tab.children[index_num].children[1].max == tval[1])):
                            df1 = df1
                        else:
                            f1 = df1[tname] >= tval[0]
                            f2 = df1[tname] <= tval[1]
                            df1 = df1.loc[f1&f2, :]
                            print("____________\n{} Min: {} - Max: {}".format(tname, tval[0], tval[1]))
                            print("Matched {} entries".format(len(df1)))
                    else:
                        if tval == ('',):
                            continue
                        else:
                            f1 = df1[tname].isin(tval)
                            df1 = df1.loc[f1, :]
                        print("____________\n{} {}".format(tname, tval))
                        print("Matched {} entries".format(len(df1)))
                else:
                    if tval == '.*':
                        df1 = df1
                    else:
                        Match_Case = True
                        df1 = df1.loc[df1[tname].apply(lambda x: check_match(x, tval, Match_Case)) == True]
                        print("____________\n{}: '{}' Matched:\n".format(tname, tval), df1[tname].value_counts())

        print("____________\n", "Matched {} of {} entries".format(len(df1), total_len))
        return(df1)
