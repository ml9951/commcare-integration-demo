#!/usr/bin/env python

import pandas, pdb, re, requests, os, numpy, glob
from sqlalchemy import create_engine
import getpass

client = requests.session()
engine = create_engine('postgresql://localhost:5432/commcare-demo')
# Uncomment the below line to use SQLite instead...
# engine = create_engine('sqlite:///commcare-demo.db')

# Rename columns to something that is PostgreSQL compliant
def renameCol(col):
    col = col.split('/')[-1]
    return re.sub(' +', '_', col.lower())

if __name__ == '__main__':
    # Get all .xlsx files
    for file in glob.glob('data/*.xlsx'): 
        # Import the file into a Dataframe
        df = pandas.read_excel(file) 
        #Create PostgreSQL compliant names
        df.columns = map(renameCol, df.columns)
        table_name = renameCol(os.path.splitext(os.path.basename(file))[0])
        #Convert `modified_on` from string to datetime object
        df['date_last_modified_on'] = pandas.to_datetime(df['date_last_modified_on'])
        print('Creating %s' % table_name)
        #Write the dataframe to PostgreSQL
        df.to_sql(table_name, engine, if_exists='replace', index=False)
