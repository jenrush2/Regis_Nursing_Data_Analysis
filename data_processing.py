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
    #Check if the student has any grades below the a C.
    return 'yes' if (group_data['Verified Grade'] < threshold).any() else 'no'


def get_classes_below_c(group_data):
    #Get a list of courses where a student scored below a C.
    classes = group_data.loc[(group_data['Verified Grade'] < 2) & (group_data['Completed Credits'] > 0.00), ['Dept', 'Course Number']]
    return ', '.join((classes['Dept'] + classes['Course Number']).tolist()) if not classes.empty else ''


def rcc_check(group_data):
    return 'yes' if (
        ((group_data['Dept'].str.contains('RCC')) & (group_data['Course Number'].str.contains('200')))
        & (group_data['Verified Grade'] >= 2)).any() else 'no'


def science_grade_check(group_data):
    #science grades lower than a c, will not include transfer classes because all transfer classes are above a C and have no Verified Grade
    return 'yes' if ((group_data['Verified Grade'] < 2) 
        & ((group_data['Dept'].str.contains('BL')) | (group_data['Dept'].str.contains('CH')))).any() else 'no'


def science_below_c_list(group_data):
    #list of science classes lower than a c, will not include transfer classes because all transfer classes are above a C and have no Verified Grade
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

def science_inc_trans_c_or_above(group_data):
    # Select specific science courses where the student earned C or above
    #Filter Regis courses with Verified Grade >= 2
    regis_courses = group_data.loc[
        (group_data['Verified Grade'] >= 2)  # Only check Verified Grade for Regis courses
        & (
            # Regular courses
            ((group_data['Dept'].str.contains('CH', na=False)) & 
             (group_data['Course Number'].str.contains('206A|207A', na=False))) 
            | 
            ((group_data['Dept'].str.contains('BL', na=False)) & 
             (group_data['Course Number'].str.contains('254|255|274|275|276|277', na=False)))
        ) 
        & (group_data['Completed Credits'] > 0.00),  # Ensure completed credits > 0
        ['Dept', 'Course Number']
    ]
    
    regis_courses = regis_courses['Dept'] + regis_courses['Course Number']

    #Transfer courses (Dept contains both dept and course number for transfer courses)
    transfer_courses = group_data.loc[
        group_data['Dept'].str.contains(r'CH\*206A|CH\*207A|BL\*254|BL\*255|BL\*274|BL\*275|BL\*276|BL\*277', na=False)
        & (group_data['Completed Credits'] > 0.00),  # Ensure completed credits > 0 for transfer courses
        ['Dept']
    ]

    # Remove * from transfer courses
    transfer_courses['Dept'] = transfer_courses['Dept'].str.replace(r'\*', '', regex=True)

    #get the list of courses for transfer (so transfer_courses is no longer a dataframe)
    transfer_courses = transfer_courses['Dept']

    all_courses = pd.concat([regis_courses, transfer_courses])

    # Convert list to a string with courses separated by ", " or empty string if no courses
    course_list = ', '.join(all_courses.tolist()) if not all_courses.empty else ''
    
    return course_list


    
def science_6_at_regis_check(group_data):
    science_at_regis_c_or_higher = science_at_regis_c_or_above(group_data)
    return 'yes' if len(science_at_regis_c_or_higher.split(', ')) >= 6 else 'no'


def science_8_at_regis_check(group_data):
    science_at_regis_c_or_higher = science_at_regis_c_or_above(group_data)
    return 'yes' if len(science_at_regis_c_or_higher.split(', ')) >= 8 else 'no'


def science_6_inc_trans_check(group_data):
    science_inc_trans_c_or_higher = science_inc_trans_c_or_above(group_data)
    return 'yes' if len(science_inc_trans_c_or_higher.split(', ')) >= 6 else 'no'

def science_8_inc_trans_check(group_data):
    science_inc_trans_c_or_higher = science_inc_trans_c_or_above(group_data)
    return 'yes' if len(science_inc_trans_c_or_higher.split(', ')) >= 8 else 'no'


# List of required science courses, does not include transfer classes
all_science_classes_list_regis = ['CH206A', 'CH207A', 'BL254', 'BL255', 'BL274', 'BL275', 'BL276', 'BL277']
transfer_science_classes = ['CH*206A', 'CH*207A', 'BL*254', 'BL*255', 'BL*274', 'BL*275', 'BL*276', 'BL*277']

def science_at_regis_remaining(group_data):
    # Convert completed courses into a set
    completed_science_courses_at_regis = science_at_regis_c_or_above(group_data)
    completed_science_courses_at_regis = set(completed_science_courses_at_regis.split(', ')) if completed_science_courses_at_regis else set()

    # Find missing courses, lists transfer classes as missing
    science_at_regis_remaining = list(set(all_science_classes_list_regis) - completed_science_courses_at_regis)
    science_at_regis_remaining = ', '.join(science_at_regis_remaining) if science_at_regis_remaining else ''
    return science_at_regis_remaining


def science_inc_trans_remaining(group_data):
    # Convert completed courses into a set
    completed_science_courses = science_inc_trans_c_or_above(group_data)
    completed_science_courses = set(completed_science_courses.split(', ')) if completed_science_courses else set()

    # Find missing courses, lists transfer classes as missing
    science_remaining = list(set(all_science_classes_list_regis) - completed_science_courses)
    science_remaining = ', '.join(science_remaining) if science_remaining else ''
    return science_remaining

def list_of_science_transfer_classes(group_data):
    check = r'CH\*206A|CH\*207A|BL\*254|BL\*255|BL\*274|BL\*275|BL\*276|BL\*277'
    science_non_regis = group_data.loc[
        group_data['Dept'].str.contains(check, na=False), 'Dept'
    ].dropna()

    return ', '.join(science_non_regis) if not science_non_regis.empty else ''


def list_of_withdrawn_classes(group_data):
    withdrawn = group_data.loc[group_data['Verified Grade'] == 7, ['Dept', 'Course Number']].dropna()
    withdrawn = withdrawn['Dept'] + withdrawn['Course Number']
    withdrawn = ', '.join(withdrawn.tolist()) if not withdrawn.empty else ''
    return withdrawn


def registered_for_remaining_check(group_data):
    #registered for remaining science courses?
    #check for courses from the science_remaining list AND empty verfied grade column
    registered_science_classes = group_data.loc[
        (group_data['Verified Grade'].isnull())
        & (
        ((group_data['Dept'].str.contains('CH', na=False)) & 
         (group_data['Course Number'].str.contains('206A|207A', na=False))) 
        | 
        ((group_data['Dept'].str.contains('BL', na=False)) & 
         (group_data['Course Number'].str.contains('254|255|274|275|276|277', na=False)))
        )
        ]
    
    registered_science_classes = registered_science_classes['Dept'] + registered_science_classes['Course Number']
    registered_science_classes = ', '.join(registered_science_classes.tolist()) if not registered_science_classes.empty else ''
    
    #run list of science classes remaining (counts transfer classes as ok)
    science_at_regis_remaining = science_inc_trans_remaining(group_data)
    
    #make sure both string lists are converted to sets
    registered_science_set = set(registered_science_classes.split(', ')) if registered_science_classes else set()
    science_at_regis_remaining = set(science_at_regis_remaining.split(', ')) if science_at_regis_remaining else set()
    
    if not science_at_regis_remaining:
        registered = ''
    else: 
        registered = 'yes' if registered_science_set == science_at_regis_remaining else 'no'
        
    return registered