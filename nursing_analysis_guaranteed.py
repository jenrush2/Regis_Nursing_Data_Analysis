import pandas as pd
from data_processing import load_raw_data, calculate_science_gpa, cohort_check, has_low_grade, get_classes_below_c

#example layout, not yet final or applicable to actual guaranteed admission requriements -- just trying to see how things would look with this method

# Load and preprocess data
file_path = "/Users/jenniferrush/Python/Regis_Nursing_Analysis/data/nursing_data.xlsx"
sheet_name = "IDS - Regis College - Pre-Nursi"
raw_data = load_raw_data(file_path, sheet_name)

# Group by student
grouped_data = raw_data.groupby('Student ID#')
result = []

for student_id, group_data in grouped_data:
    entry_cohort = cohort_check(group_data['Entry Cohort'].iloc[0])
    gpa = group_data['Cum GPA'].iloc[0]
    science_gpa = calculate_science_gpa(group_data)
    any_low_grade = has_low_grade(group_data)
    classes_below_c = get_classes_below_c(group_data)

    result.append({
        'Student ID#': student_id,
        'Entry Cohort': entry_cohort,
        'Cumulative GPA': gpa,
        'Science GPA': science_gpa,
        'Any Grade Lower Than C': any_low_grade,
        'Classes Lower Than C': classes_below_c
    })

# Convert to DataFrame and save to Excel
nursing_final = pd.DataFrame(result)
nursing_final.to_excel('nursing_report1.xlsx', index=False, engine='openpyxl')


#still need highlighting code below