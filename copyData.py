#==============================================================================
# This python script mimics the Data folder system (Raw_Data, Analysis, etc.) and
# copies the scans specified in ScanList.txt into a single Raw_Data folder so
# that a single analysis program can be run on all the relevant raw data files at
# once. 
# 
# This script needs to be placed in a project subfolder. 
# 
# Example original Data folder structure:
#   U:\DOCUMENTS\Data\Analysis\87Sr\2017.09.11_87Sr_n76_Rydberg_Spectroscopy
#   U:\DOCUMENTS\Raw_Data\87Sr\2017.09.11
# 
# Example Project subfolder of where this script should be placed:
#   U:\DOCUMENTS\Projects\Test_Project
#
# NOTES:
#   2017.09.14 - Using ScanList.txt instead of ProjectFiles.txt as list of scans to search for. 
#   2017.09.11 - Improved comments. Now sorting by date and timestamp. (WIP = work in progress)
#==============================================================================

import os
import datetime
import pandas as pd
import glob
import shutil

dateWithPeriods = datetime.datetime.today().strftime('%Y.%m.%d')
dateWithoutPeriods = datetime.datetime.today().strftime('%Y%m%d')

CWD = os.getcwd()
DIR_PROJ = os.path.dirname(CWD)
ROOT = os.path.dirname(DIR_PROJ)
DIR_ORIG = os.path.join(ROOT, 'Data')
DIR_ORIG_RAW_DATA = os.path.join(DIR_ORIG, 'Raw_Data')

# Directory for where to copy the relevant Raw_Data.
DIR_PROJ_RAW_DATA = os.path.join(CWD, 'Raw_Data')

# Directory for project analysis folder.
DIR_PROJ_ANALYSIS = os.path.join(CWD, 'Analysis')

#==============================================================================
# User options
#==============================================================================
# (WIP - 2017.09.11) If no analysis folder name is specified, use dateWithPeriods as analysis folder name. 
analysisName = ''
if not analysisName:
    analysisName = dateWithPeriods

#==============================================================================
# Reading in the scans to search for listed in ScanList.txt and sort by date and timestamp. 
#==============================================================================
scanFileList = pd.read_csv('ScanList.txt', sep = '\t', 
                              header = 0,
                              comment = '%')

scanFileList = scanFileList.sort_values(by = ['Date', 'Timestamp'], ascending = [True, True])

#==============================================================================
# Get the isotopes used in scans and create isotope project subfolders in Raw_Data and Analysis
#==============================================================================
for i in range(0, len(scanFileList.Isotope.unique())):
    isotope = scanFileList.Isotope.unique()[i]
    
    TEMP_PROJ_RAW_DATA = os.path.join(DIR_PROJ_RAW_DATA, isotope, dateWithPeriods)
    TEMP_PROJ_ANALYSIS = os.path.join(DIR_PROJ_ANALYSIS, isotope, dateWithPeriods)
    
    if not os.path.exists(TEMP_PROJ_RAW_DATA):
        os.makedirs(TEMP_PROJ_RAW_DATA)
        
    # Analysis folder name is the date for now...
    if not os.path.exists(TEMP_PROJ_ANALYSIS):
        os.makedirs(TEMP_PROJ_ANALYSIS)

#==============================================================================
# Loop through each scan listed in ScanList.txt and copy from relevant line from original master batch file into project master batch file
#==============================================================================
new_master_batch_atom = ''
new_master_batch_bg = ''
new_master_batch_counts = ''

for i in range(0, len(scanFileList.Isotope.unique())):
    isotope = scanFileList.Isotope.unique()[i]
    
    # Idea to imrpove - loop throuch the isotopes separately...
    for index, row in scanFileList[scanFileList.Isotope == isotope].iterrows():
        PATH_ORIG_SCAN = os.path.join(DIR_ORIG_RAW_DATA, isotope, row['Date'])
        PATH_PROJ_SCAN = os.path.join(DIR_PROJ_RAW_DATA, isotope, dateWithPeriods)
        
        # Path to original master batch file
        orig_master_batch_atom = os.path.join(PATH_ORIG_SCAN, 'Files_' + row['Date'].replace('.','') + '.txt')
        orig_master_batch_bg = os.path.join(PATH_ORIG_SCAN, 'Files_' + row['Date'].replace('.','') + '_Bg.txt')
        orig_master_batch_counts = os.path.join(PATH_ORIG_SCAN, 'Files_' + row['Date'].replace('.','') + '_Counts.txt')
            
        # Path to project master batch file
        proj_master_batch_atom = os.path.join(PATH_PROJ_SCAN, 'Files_' + dateWithoutPeriods + '.txt')
        proj_master_batch_bg = os.path.join(PATH_PROJ_SCAN, 'Files_' + dateWithoutPeriods + '_Bg.txt')
        proj_master_batch_counts = os.path.join(PATH_PROJ_SCAN, 'Files_' + dateWithoutPeriods + '_Counts.txt')
        
        # Open the original master batch file and look for row with matching scan name. If present, copy line to project master batch file. 
        with open(orig_master_batch_atom) as orig_f:
            for line in orig_f:
                if row['Scan'] in line:
                    new_master_batch_atom = new_master_batch_atom + line
         
        # Open the original master batch file (background)  and look for row with matching scan name. If present, copy line to project master batch file (background). 
        with open(orig_master_batch_bg) as orig_f:
            for line in orig_f:
                if row['Scan'] in line:
                    new_master_batch_bg = new_master_batch_bg + line
     
        # Open the original master batch file (counts)  and look for row with matching scan name. If present, copy line to project master batch file (counts). 
        with open(orig_master_batch_counts) as orig_f:
            for line in orig_f:
                if row['Scan'] in line:
                    new_master_batch_counts = new_master_batch_counts + line
    
        # Copy all raw data files associated with the scan name (using *-wildcard to identify related files). 
        for file in glob.glob(os.path.join(PATH_ORIG_SCAN, row['Scan'] + '*')):
            print(file)
            shutil.copy(file, PATH_PROJ_SCAN)
    
    # Once it's looped through the master, background, and counts batch files, write to a new master batch file for each isotope.
    text_file = open(proj_master_batch_atom, 'w')
    text_file.write(new_master_batch_atom)
    text_file.close()
    
    text_file = open(proj_master_batch_bg, 'w')
    text_file.write(new_master_batch_bg)
    text_file.close()
    
    text_file = open(proj_master_batch_counts, 'w')
    text_file.write(new_master_batch_counts)
    text_file.close()
