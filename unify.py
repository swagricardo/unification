# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 00:24:29 2022

@author: PuraLumbreMusic
"""

from oauth2client.service_account import ServiceAccountCredentials
import gspread

import pandas as pd 

scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name("swagchat-1643821248945-96b4bfd45712.json", scopes) #access the json key you downloaded earlier 
client = gspread.authorize(credentials)



def project_snapshot():
    """
    Fontana Case Note - San Bernardino Intake
    """
    intakes = client.open('Fontana Case Note')
    intake_responses = intakes.get_worksheet_by_id(1638025085) 
    service_logs = client.open('San Bernardino County Client Intake Form')
    form_responses = service_logs.get_worksheet_by_id(1135909388)
    return intake_responses, form_responses


  
intake_responses, form_responses_1 = project_snapshot()
form_responses_1_df = pd.DataFrame(form_responses_1.get_all_records())

intake_responses_df = pd.DataFrame(intake_responses.get_all_records())
#jan_df['Gender_Freq'] = jan_df.groupby('Gender:')['SocialSecurityNumber:'].transform('count')
 

 

form_responses_1_df['Names'] =  form_responses_1_df['Client First Name'].str.rstrip() + ' ' + form_responses_1_df['Client Last Name'].str.rstrip()
intake_responses_df['Names'] =  intake_responses_df['First Name'].str.rstrip() + ' ' + intake_responses_df['Last Name'].str.rstrip()


outer = pd.merge(form_responses_1_df, intake_responses_df,how="outer", on=["Names"])

#outer.to_csv('SB_client_ledger_bnl_names2.csv', index=False)

#bnl_reference_df['Names'] = bnl_reference_df['Names'].str.rstrip()
#bnl_reference_df['Names'] = bnl_reference_df['Names'].str.lstrip()
#bnl_reference_df['Names'] = bnl_reference_df['Names'].str.title()

#gunshy = pd.merge(bnl_reference_df, outer, how="outer", on=['Names'])
outer['Date'] = pd.to_datetime(outer["Date"], errors = 'coerce')
#outer = outer[(outer['Date'] > '1/1/2021') & (outer['Date'] < '8/31/2022')]
outer.to_csv('fontana_all.csv')


df2 = pd.read_csv('fontana_all.csv')

uniform_intake = df2.filter(['Names', 'Date', 'Assessment Date','Are you on parole?', 'If you receive income, how many dollars a month?',\
                             'Age', 'Age Demographic', 'Date of Birth', 'Length of Homelessness (Calculated)','Substance Abuse',\
                                 'Developmental Disability','Physical Disability','Disabling Condition?',\
                                     'Are you a veteran?', 'Do you have any children under 18?', \
                                         'If applicable, with whom do the children live with?'])
    
outer = uniform_intake[(uniform_intake['Date'] > '2022-10-01') & (uniform_intake['Date'] < '2022-10-31')]



como = outer.filter(['Names', 'Are you on parole?', 'If you receive income, how many dollars a month?',\
                             'Age', 'Age Demographic', 'Date of Birth', 'Length of Homelessness (Calculated)', 'Substance Abuse' ,\
                                 'Developmental Disability','Physical Disability','Disabling Condition?',\
                                     'Are you a veteran?', 'Do you have any children under 18?', \
                                         'If applicable, with whom do the children live with?'])
como= como.drop_duplicates() 

como.to_csv('sb_como_oct12.csv')


uniform_intake.groupby(['Date','Names']).size().reset_index().rename(columns={0:'count'})

uniform_intake.to_csv('candidates_october.csv')

outer.to_csv('october_only.csv')
