import pandas as pd
import numpy as np
import datetime as dt
import os, sys
import re
import logging
from ipywidgets import interact, interactive, fixed, interact_manual


def check_match(x, y):
	try:
		pattern = re.compile(y)
		return(bool(re.match(pattern=pattern, string=x)))
	except:
		return("N/A")
		
def usd_to_float(test_string):
    pattern = re.compile("(\$)|(USD \$)|(USD)")
    try:
        split = re.split(pattern, test_string)
        return(float(split[-1]))
    except:
        return(0)
   
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
 
 
def interactive_file_picker(dir_list, search_pattern):
    file = ""
    def ifp_sub01(dir_input, search_pattern):
        file_list = local_find_to_df(dir_input, search_pattern).sort_values(by='Modified Time', ascending=False)['Filename'].tolist()
        file_list.insert(0, "")
        interact(ifp_sub02, dir_input=fixed(dir_input), file_picker=file_list, search_pattern=fixed(search_pattern))
    def ifp_sub02(dir_input, file_picker, search_pattern):
        file = os.path.join(dir_input, file_picker)
        if len(file_picker) > 0:
        	global interactive_file_picker_output
        	interactive_file_picker_output = [file_picker, file, dir_input]
        	print("  File:  {}\n  Path:  {}\n  Size: {}\n  Modified: {}".format(file_picker, file, os.stat(file).st_size, dt.datetime.strftime(dt.datetime.fromtimestamp(os.stat(file).st_mtime), '%m-%d-%y %H:%M')))
        else:
            return(local_find_to_df(dir_input, search_pattern).sort_values(by='Modified Time', ascending=False))
    interact(ifp_sub01, dir_input=dir_list, search_pattern=fixed(search_pattern))


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
                   

