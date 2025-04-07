''' 
    Contains script for Preparing 311 service request data for a Tableau project

    Original data contains ~580,000 observations for 311 service requests made between 1/2020 and 9/2024
    ~20% of the rows were dropped due to missing zipcode information
    
    The latest update for this data occured on April 5, 2025
'''

import pandas as pd

def main():

    # read in unprepared data
    df = pd.read_csv('allservicecalls.csv')

    # select colunms needed for project 
    df = df[['Category',
             'OPENEDDATETIME',
             'Dept', 
             'REASONNAME', 
             'TYPENAME', 
             'OBJECTDESC', 
             'Council District']]

    # Rename columns for ease of access
    df = df.rename(columns = {'Category' : 'catagory',
                              'OPENEDDATETIME' : 'open_date',
                              'Dept' : 'city_dept',
                              'REASONNAME' : 'dept_div', 
                              'TYPENAME' : 'type', 
                              'OBJECTDESC' : 'location', 
                              'Council District' : 'district'})

    # drop rows that contain null values
    df = df.dropna()

    # add zipcode column using last five digits of address
    df['zip_code'] = df.location.apply(lambda x: x[-5:])

    # drop columns with ambiguous zip codes
    df = df.loc[df.zip_code.str.contains(r'\d{5}')]

    # writre prepared data to csv
    df.to_csv('service_calls_prepared.csv', index = False)


if __name__ == "__main__":

    main()