import pandas as pd


raw_data = pd.read_excel("/Users/jenniferrush/Python/Regis_Nursing_Analysis/data/nursing_data.xlsx", sheet_name="IDS - Regis College - Pre-Nursi")

#print(raw_data.sample(30))
#print(raw_data.dtypes)

overview = raw_data.filter(['Student ID#', 'Cum GPA', 'Entry Cohort'], axis =1).drop_duplicates()
raw_data['Dept'] = raw_data['Dept'].astype("string")
raw_data['Course Number'] = raw_data['Course Number'].astype("string")

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
overview['Entry Cohort'] = overview['Entry Cohort'].astype("string")


#print(overview.sample(50))
#print(overview.dtypes)
#print(overview['Entry Cohort'].value_counts())

raw_data['Verified Grade'] = raw_data['Verified Grade'].replace({'A': 4.000, 'A-': 3.667 ,'B+': 3.333, 'B': 3.000, 'B-': 2.667, 'C+': 2.333, 'C': 2.000, 'C-': 1.667, 'D+': 1.333, 'D': 1.000, 'D-': 0.667, 'F': 0.000, 'W': 1})


#print(raw_data['Verified Grade'].sample(30))
#print(raw_data['Verified Grade'].value_counts())
#print(raw_data.dtypes)

#print(raw_data.query(("Dept == 'CH' & 'Course Number' == ('206A' or '207A')") or ("Dept == 'BL' & 'Course Number' == ('258' or '259' or '274' or '275' or '276' or '277')")).groupby(['Student ID#']).sample(50))
raw_data['Verified Grade'] = pd.to_numeric(raw_data['Verified Grade'], errors = 'coerce', downcast = 'float')

print(raw_data.dtypes)
raw_data.loc[((raw_data['Dept'].str.contains('CH') & (raw_data['Course Number'].str.contains('206A'))) | ((raw_data['Dept'].str.contains('BL')))) & (raw_data['Course Number'].str.contains('254' or '274' or '276')), 'Completed Credits'] = 3.000



#science_data = raw_data.filter(['Student ID#', 'Dept' , 'Course Number', 'Verified Grade', 'Completed Credits'], axis =1)
#print(science_data.head(50))

#raw_data['Weighted Grade'] = raw_data['Verified Grade'] * raw_data['Completed Credits']
#print(raw_data[['Student ID#','Weighted Grade','Verified Grade','Completed Credits']].head(50))
#print(raw_data[((raw_data['Dept'].str.contains('CH')) & (raw_data['Course Number'].str.contains('206A' or '207A'))) | ((raw_data['Dept'].str.contains('BL') & (raw_data['Course Number'].str.contains('258' or '259' or '274' or '275' or '276' or '277'))))].groupby(['Student ID#']).agg({'Weighted Grade': 'mean'}))
#print(raw_data[((raw_data['Dept'].str.contains('CH')) & (raw_data['Course Number'].str.contains('206A' or '207A'))) | ((raw_data['Dept'].str.contains('BL') & (raw_data['Course Number'].str.contains('258' or '259' or '274' or '275' or '276' or '277'))))].head(50))
