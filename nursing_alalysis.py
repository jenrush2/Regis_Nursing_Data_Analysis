import pandas as pd


raw_data = pd.read_excel("/Users/jenniferrush/Python/Regis_Nursing_Analysis/data/nursing_data.xlsx", sheet_name="IDS - Regis College - Pre-Nursi")
raw_data['Dept'] = raw_data['Dept'].astype("string")
raw_data['Course Number'] = raw_data['Course Number'].astype("string")
#print(raw_data.sample(30))
#print(raw_data.dtypes)

def process_data(grouped_data):

    #create new df that each function will add a column to -- keep colums that are already good to use
    final_df = grouped_data.filter(['Cum GPA'], axis =1)
    
    #Letter Grade to Numerical in the input data so that it can be used in all functions below
    grouped_data['Verified Grade'] = grouped_data['Verified Grade'].replace({'A': '4.000', 'A-': '3.667' ,'B+': '3.333', 'B': '3.000', 'B-': '2.667', 'C+': '2.333', 'C': '2.000', 'C-': '1.667', 'D+': '1.333', 'D': '1.000', 'D-': '0.667', 'F': '0.000', 'W': '1'})
    grouped_data['Verified Grade'] = pd.to_numeric(grouped_data['Verified Grade'], errors = 'coerce', downcast = 'float')
    

    #create cohort check
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

    #Apply cohort check
    final_df['Entry Cohort']=grouped_data['Entry Cohort'].apply(cohort_check)

    #Science sort
    def science_sort(data):
        
        #getting rid of extra rows we don't need for science GPA
        data.dropna(subset=['Dept'], inplace=True)
        data.dropna(subset=['Verified Grade'], inplace=True)
        data=data[data['Dept'].isin(['CH', 'BL'])]
        
        #If student earned an F, the credits are listed as 0. Replace credits as 3 for the course and 1 for the lab.
        data.loc[
            (
                (data['Dept'].str.contains('CH')) & 
                (data['Course Number'].str.contains('206A'))
            ) | 
            (
                (data['Dept'].str.contains('BL')) & 
                (data['Course Number'].str.contains('254|274|276')) 
            ), 
            'Completed Credits'
        ] = 3.000

        data.loc[
            (
                (data['Dept'].str.contains('CH')) & 
                (data['Course Number'].str.contains('207A'))
            ) | 
            (
                (data['Dept'].str.contains('BL')) & 
                (data['Course Number'].str.contains('255|275|277')) 
            ), 
            'Completed Credits'
        ] = 1.000

        #calculate science gpa
        result = (data['Verified Grade'] * data['Completed Credits'])/(data['Completed Credits'].sum)
        
        return result


    #Apply Science sort
    #final_df['Science GPA']=grouped_data.apply(science_sort)

    return final_df



result = raw_data.groupby('Student ID#').apply(process_data)
print('Head 50')
print(result.head(50))
print('Sample 50')
print(result.sample(50))

#Everything below was for development in chunks

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
overview['Entry Cohort'] = overview['Entry Cohort'].astype("string")


#print(overview.sample(50))
#print(overview.dtypes)
#print(overview['Entry Cohort'].value_counts())

raw_data['Verified Grade'] = raw_data['Verified Grade'].replace({'A': 4.000, 'A-': 3.667 ,'B+': 3.333, 'B': 3.000, 'B-': 2.667, 'C+': 2.333, 'C': 2.000, 'C-': 1.667, 'D+': 1.333, 'D': 1.000, 'D-': 0.667, 'F': 0.000, 'W': 1})


#print(raw_data['Verified Grade'].sample(30))
#print(raw_data['Verified Grade'].value_counts())
#print(raw_data.dtypes)

raw_data['Verified Grade'] = pd.to_numeric(raw_data['Verified Grade'], errors = 'coerce', downcast = 'float')

#print(raw_data.dtypes)


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


science_data = raw_data.filter(['Student ID#', 'Dept' , 'Course Number', 'Verified Grade', 'Completed Credits'], axis =1)
#print(science_data[1608:1612])

#getting rid of extra rows we don't need for science GPA
science_data.dropna(subset=['Dept'], inplace=True)
science_data.dropna(subset=['Verified Grade'], inplace=True)
science_data=science_data[science_data['Dept'].isin(['CH', 'BL'])]

science_data['Grade Credits'] = science_data['Verified Grade'] * science_data['Completed Credits']

grouped_sum = science_data.groupby('Student ID#')['Completed Credits'].sum()
science_data['Science GPA'] = grouped_sum



#print(science_data.head(50))
