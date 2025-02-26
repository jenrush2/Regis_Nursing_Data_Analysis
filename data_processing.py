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



