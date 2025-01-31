import pandas as pd


raw_data = pd.read_excel("/Users/jenniferrush/Python/Regis_Nursing_Analysis/data/nursing_data.xlsx", sheet_name="IDS - Regis College - Pre-Nursi")

#Change all of the data types so they are strings or floats instead of objects
raw_data[['Added Minor', 'Class Level', 'Entry Cohort', 'Enrolled Semester','Dept', 'Course Number', 'Course Title']] = raw_data[['Added Minor', 'Class Level', 'Entry Cohort', 'Enrolled Semester','Dept', 'Course Number', 'Course Title']].astype("string")
raw_data['Verified Grade'] = raw_data['Verified Grade'].replace({'A': '4.000', 'A-': '3.667' ,'B+': '3.333', 'B': '3.000', 'B-': '2.667', 'C+': '2.333', 'C': '2.000', 'C-': '1.667', 'D+': '1.333', 'D': '1.000', 'D-': '0.667', 'F': '0.000', 'W': '1'})
raw_data['Verified Grade'] = pd.to_numeric(raw_data['Verified Grade'], errors = 'coerce', downcast = 'float')

#If a student earned an F, their credits are listed as 0. 
#Take science classes we care about and changes credits to 3 for course and 1 for lab
raw_data.loc[
    (
        (raw_data['Dept'].str.contains('CH')) & 
        (raw_data['Course Number'].str.contains('206A'))
    ) | 
    (
        (raw_data['Dept'].str.contains('BL')) & 
        (raw_data['Course Number'].str.contains('254|274|276')) 
    ), 
    'Completed Credits'
] = 3.000

raw_data.loc[
    (
        (raw_data['Dept'].str.contains('CH')) & 
        (raw_data['Course Number'].str.contains('207A'))
    ) | 
    (
        (raw_data['Dept'].str.contains('BL')) & 
        (raw_data['Course Number'].str.contains('255|275|277')) 
    ), 
    'Completed Credits'
] = 1.000

#Group by Student ID#
grouped_data = raw_data.groupby('Student ID#')



#Check stuff
print(raw_data.sample(50))
print(raw_data.dtypes)
print(raw_data[1608:1612])
