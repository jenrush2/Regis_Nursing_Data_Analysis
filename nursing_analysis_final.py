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

#Check stuff
# print(raw_data.sample(50))
# print(raw_data.dtypes)
# has a student that earned an F in science course to confirm credit change
# print(raw_data[1608:1612])

#Group by Student ID#
grouped_data = raw_data.groupby('Student ID#')

result = []

#Iterate through each group
for student_id, group_data in grouped_data:
    #calculations to create each variable
    
    #entry cohort
    def cohort_check(entry_data):

        def year(data):
            two_digit_year = data[0:2]
            year = '20' + two_digit_year
            return year

        if 'STR' in entry_data or 'FTR' in entry_data:
            return 'TRANSFER'
        elif 'FN' in entry_data:
            year = year(entry_data)
            return 'Fall ' + year
        elif 'SN' in entry_data:
            year = year(entry_data)
            return 'Spring ' + year
        else:
            return entry_data

    entry_cohort = group_data['Entry Cohort'].apply(cohort_check)

    #science gpa
    science_gpa = 'not calculated yet'
    #admission check
    admission_check = 'ncy'
    #rcc check
    rcc_check = 'ncy'
    #any grades lower than a c and which ones
    all_grade_check = 'ncy'
    #science grades lower than a c and which ones
    science_grade_check = 'ncy'
    #minor
    minor = 'ncy'
    #completed all 8 science courses? missing which?
    science_8_check = 'ncy'
    #withdrawn from any classes? which?
    withdrawn = 'ncy'
    #registered for remaining science courses?
    registered = 'ncy'

    #result as key and value pairs
    result.append(
        {'Student ID#': student_id, 
         'Entry Cohort': entry_cohort, 
         'Science GPA': science_gpa, 
         'Guaranteed Admission': admission_check, 
         'RCC 200': rcc_check, 
         'Any Grade Lower Than C': all_grade_check, 
         'Science Grade Lower Than C': science_grade_check, 
         'Minor': minor, 
         'Science Classes Completed': science_8_check, 
         'Withdrawn': withdrawn, 
         'Registered for Remaining': registered}
         )

#result to a new dataframe
nursing_final = pd.DataFrame(result)


print(nursing_final.head(50))
print(nursing_final.sample(50))

#when you're done, drop ID numbers
#nursing_final.to_excel('nursing_analysis_final.xlsx', index=False)

