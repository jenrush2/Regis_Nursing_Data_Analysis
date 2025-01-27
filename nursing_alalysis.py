import pandas as pd


raw_data = pd.read_excel("/Users/jenniferrush/Python/Regis_Nursing_Analysis/data/nursing_data.xlsx", sheet_name="IDS - Regis College - Pre-Nursi")

#print(raw_data.sample(30))
#print(raw_data.dtypes)

overview = raw_data.filter(['Student ID#', 'Cum GPA', 'Entry Cohort'], axis =1).drop_duplicates()

#print(overview.sample(20))
#print(overview.dtypes)



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

overview['Entry Cohort'] = overview['Entry Cohort'].apply(cohort_check)

print(overview.sample(50))
