import pandas as pd

def load_raw_data(file_path, sheet_name):
    #Load and preprocess raw data from an Excel file.
    raw_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Convert data types
    columns_to_string = ['Added Minor', 'Class Level', 'Entry Cohort', 'Enrolled Semester', 'Dept', 'Course Number', 'Course Title']
    raw_data[columns_to_string] = raw_data[columns_to_string].astype("string")

    # Grade conversion
    grade_mapping = {'A': '4.000', 'A-': '3.667', 'B+': '3.333', 'B': '3.000', 'B-': '2.667',
                     'C+': '2.333', 'C': '2.000', 'C-': '1.667', 'D+': '1.333', 'D': '1.000', 
                     'D-': '0.667', 'F': '0.000', 'W': '7'}
    raw_data['Verified Grade'] = raw_data['Verified Grade'].replace(grade_mapping)
    raw_data['Verified Grade'] = pd.to_numeric(raw_data['Verified Grade'], errors='coerce', downcast='float')

    raw_data['Completed Credits'] = pd.to_numeric(raw_data['Completed Credits'], errors='coerce', downcast='float')

    return raw_data


def keep_column(group_data, column_name):
    column_value = group_data[column_name].iloc[0]
    return '' if pd.isna(column_value) else str(column_value)

def calculate_science_gpa(group_data):
    #Calculate the science GPA for a student.
    science_courses = group_data.loc[
        (group_data['Dept'].str.contains('BL|CH', na=False)) & group_data['Verified Grade'].notna()
    ]

    weighted_sum = (science_courses['Verified Grade'] * science_courses['Completed Credits']).sum()
    total_credits = science_courses['Completed Credits'].sum()

    return (weighted_sum / total_credits).round(2) if total_credits != 0 else 0.00


def cohort_check(entry_data):
    #Determine cohort type based on entry data.
    def year(data):
        return '20' + data[:2]

    if 'STR' in entry_data or 'FTR' in entry_data:
        return 'TRANSFER'
    elif 'FN' in entry_data:
        return 'Fall ' + year(entry_data)
    elif 'SN' in entry_data:
        return 'Spring ' + year(entry_data)
    else:
        return entry_data


def has_low_grade(group_data, threshold=2.0):
    #Check if the student has any grades below the threshold.
    return 'yes' if (group_data['Verified Grade'] < threshold).any() else 'no'


def get_classes_below_c(group_data):
    #Get a list of courses where a student scored below a C.
    classes = group_data.loc[(group_data['Verified Grade'] < 2) & (group_data['Completed Credits'] > 0.00), ['Dept', 'Course Number']]
    return ', '.join((classes['Dept'] + classes['Course Number']).tolist()) if not classes.empty else ''


def rcc_check(group_data):
    return 'yes' if (
        ((group_data['Dept'].str.contains('RCC')) & (group_data['Course Number'].str.contains('200')))
        & (group_data['Verified Grade'] >= 2)).any() else 'no'


def science_grade_check_inc_trans(group_data):
    #science grades lower than a c, will include transfer classes
    return 'yes' if ((group_data['Verified Grade'] < 2) 
        & ((group_data['Dept'].str.contains('BL')) | (group_data['Dept'].str.contains('CH')))).any() else 'no'


def science_below_c_list_inc_trans(group_data):
    #list of science classes lower than a c, will include transfer classes and will still have the * so you know it was a transfer
    science_below_c = group_data.loc[((group_data['Verified Grade']) < 2) & (group_data['Dept'].str.contains('BL') | group_data['Dept'].str.contains('CH')) & (group_data['Completed Credits'] > 0.00), ['Dept', 'Course Number']]
    science_below_c = science_below_c['Dept'] + science_below_c['Course Number']
    science_below_c = ', '.join(science_below_c.tolist()) if not science_below_c.empty else ''
    return science_below_c


def science_at_regis_c_or_above(group_data):
    # this one only checks for classes taken at Regis
    # Select specific science courses where the student earned C or above
    science_at_regis_c_or_above = group_data.loc[
    (group_data['Verified Grade'] >= 2) 
    & (
    ((group_data['Dept'].str.contains('CH', na=False)) & 
    (group_data['Course Number'].str.contains('206A|207A', na=False))) 
    | 
    ((group_data['Dept'].str.contains('BL', na=False)) & 
    (group_data['Course Number'].str.contains('254|255|274|275|276|277', na=False)))
    ) 
    & (group_data['Completed Credits'] > 0.00), 
    ['Dept', 'Course Number']
    ]

    # Concatenate 'Dept' and 'Course Number' columns
    science_at_regis_c_or_above = science_at_regis_c_or_above['Dept'] + science_at_regis_c_or_above['Course Number']

    # Convert list to a string with courses separated by ", " or empty string if no courses
    science_at_regis_c_or_above = ', '.join(science_at_regis_c_or_above.tolist()) if not science_at_regis_c_or_above.empty else ''
    
    return science_at_regis_c_or_above

    
def science_6_at_regis_check(group_data):
    science_at_regis_c_or_higher = science_at_regis_c_or_above(group_data)
    return 'yes' if len(science_at_regis_c_or_higher.split(', ')) >= 6 else 'no'


def science_8_at_regis_check(group_data):
    science_at_regis_c_or_higher = science_at_regis_c_or_above(group_data)
    return 'yes' if len(science_at_regis_c_or_higher.split(', ')) >= 8 else 'no'