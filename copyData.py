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

#Directory for where to copy the relevant Raw_Data.
DIR_PROJ_RAW_DATA = os.path.join(CWD, 'Raw_Data')

#Directory for project analysis folder.
DIR_PROJ_ANALYSIS = os.path.join(CWD, 'Analysis')

#Read in the list of scans to search for
projectFileList = pd.read_csv('ProjectFiles.txt', sep = '\t', header = None,
                              names = ['Date', 'Isotope', 'Scan'],
                              comment = '%')

#Get the isotopes used in scans and create isotope project subfolders in Raw_Data and Analysis
for i in range(0, len(projectFileList.Isotope.unique())):
    isotope = projectFileList.Isotope.unique()[i]
    
    TEMP_PROJ_RAW_DATA = os.path.join(DIR_PROJ_RAW_DATA, isotope, dateWithPeriods)
    TEMP_PROJ_ANALYSIS = os.path.join(DIR_PROJ_ANALYSIS, isotope, dateWithPeriods)
    
    if not os.path.exists(TEMP_PROJ_RAW_DATA):
        os.makedirs(TEMP_PROJ_RAW_DATA)
        
    #Analysis folder name is the date for now...
    if not os.path.exists(TEMP_PROJ_ANALYSIS):
        os.makedirs(TEMP_PROJ_ANALYSIS)
        
    #create the master batch files
    proj_master_batch_atom = os.path.join(TEMP_PROJ_RAW_DATA, 'Files_' + dateWithoutPeriods + '.txt')
    proj_master_batch_bg = os.path.join(TEMP_PROJ_RAW_DATA, 'Files_' + dateWithoutPeriods + '_Bg.txt')
    proj_master_batch_counts = os.path.join(TEMP_PROJ_RAW_DATA, 'Files_' + dateWithoutPeriods + '_Counts.txt')
    
    try:
        f = open(proj_master_batch_atom, 'r')
        f.close()
    except:
        f = open(proj_master_batch_atom, 'w+')
        f.close()
    
    try:
        f = open(proj_master_batch_bg,'r')
        f.close()
    except:
        f = open(proj_master_batch_bg,'w+')
        f.close()
        
    try:
        f = open(proj_master_batch_counts,'r')
        f.close()	
    except:
        f = open(proj_master_batch_counts,'w+')
        f.close()

#Loop through each scan listed in ProjectFiles and copy from relevant master batch file into project master batch file
for index, row in projectFileList.sort_values(['Date'], ascending = [True]).iterrows():
    PATH_ORIG_SCAN = os.path.join(DIR_ORIG_RAW_DATA, row['Isotope'], row['Date'])
    PATH_PROJ_SCAN = os.path.join(DIR_PROJ_RAW_DATA, row['Isotope'], dateWithPeriods)
    
    #Path to original master batch file
    orig_master_batch_atom = os.path.join(PATH_ORIG_SCAN, 'Files_' + row['Date'].replace('.','') + '.txt')
    orig_master_batch_bg = os.path.join(PATH_ORIG_SCAN, 'Files_' + row['Date'].replace('.','') + '_Bg.txt')
    orig_master_batch_counts = os.path.join(PATH_ORIG_SCAN, 'Files_' + row['Date'].replace('.','') + '_Counts.txt')
    
    #Path to project master batch file
    proj_master_batch_atom = os.path.join(PATH_PROJ_SCAN, 'Files_' + dateWithoutPeriods + '.txt')
    proj_master_batch_bg = os.path.join(PATH_PROJ_SCAN, 'Files_' + dateWithoutPeriods + '_Bg.txt')
    proj_master_batch_counts = os.path.join(PATH_PROJ_SCAN, 'Files_' + dateWithoutPeriods + '_Counts.txt')
    
    with open(orig_master_batch_atom) as orig_f:
        for line in orig_f:
            if row['Scan'] in line:
                with open(proj_master_batch_atom, 'a') as proj_f:
                    proj_f.write(line)
 
    with open(orig_master_batch_bg) as orig_f:
        for line in orig_f:
            if row['Scan'] in line:
                with open(proj_master_batch_bg, 'a') as proj_f:
                    proj_f.write(line)
 
    with open(orig_master_batch_counts) as orig_f:
        for line in orig_f:
            if row['Scan'] in line:
                with open(proj_master_batch_counts, 'a') as proj_f:
                    proj_f.write(line)

    for file in glob.glob(os.path.join(PATH_ORIG_SCAN, row['Scan'] + '*')):
        print(file)
        shutil.copy(file, PATH_PROJ_SCAN)