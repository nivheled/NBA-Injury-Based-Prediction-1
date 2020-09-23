#%% import all packages
import requests
import urllib
import urllib.request
!pip install pandas
import pandas as pd
!pip install PyPDF2
import PyPDF2
!pip install camelot
import camelot
!pip install os
import os
!pip install re
import re
!pip install numpy
import numpy as np
import datetime
from datetime import datetime
from datetime import timedelta
import os


#%%

#%%
roto_world = pd.read_csv("C:/Student/NBA Project/rotoworld_injuries_not_clean.csv",encoding='latin1')

#%%

#%%
def find_nth(word, char, n):
    start = word.find(char)
    while start >= 0 and n > 1:
        start = word.find(char, start+len(char))
        n -= 1
    return start

#%%

#%%
def split_dt(df):
    df.insert(0,"Game Date",np.nan)
    df.insert(1,"Game Time",np.nan)
    df['Game Date'] = df['date_time'].apply(lambda x: x[:find_nth(x,",",2)])
    df['Game Time'] = df['date_time'].apply(lambda x: x[find_nth(x,",",2)+2:])
    return df

def switch_date_format(df):
    df['Game Date'] = df['Game Date'].apply(lambda x: datetime.strptime(x,'%b %d, %Y'))
    df['Game Date'] = df['Game Date'].dt.date
    return df

def switch_time_format(df):
    df['Game Time'] = df['Game Time'].apply(lambda x: x.replace("ET",""))
    df['Game Time'] = df['Game Time'].apply(lambda x: x[:-1])
    df['Game Time'] = df['Game Time'].apply(lambda x: datetime.strptime(x, '%I:%M %p')).dt.time
    return df

def split_pos_team(df):
    df.insert(3,"Team",np.nan)
    df.insert(4,"Position",np.nan)
    df['position_and_team'] = df['position_and_team'].apply(lambda x: x.strip())
    df["Team"] = df["position_and_team"].apply(lambda x: x[x.find(",")+1:])
    df["Position"] = df["position_and_team"].apply(lambda x: x[:x.find(",")])
    df["Team"] = df["Team"].apply(lambda x: x.strip())
    df["Position"] = df["Position"].apply(lambda x: x.strip())
    return df

def remove_old_cols(df):
    del df['position_and_team']
    del df['date_time']
    return df




#%%


#%%
roto_dic = {"ruled out":"out",
"night off to rest":"out",
"getting the day off":"out",
"sitting out":"out",
"out again":"out",
"will rest":"out",
"sit out":"out",
" resting":"out",
"out with thigh contusion":"out",
"sits out":"out",
"will not play":"out",
"won't play":"out",
"still out":"out",
"does not play":"out",
"placed in concussion protocol":"out",
" out":"out",
"likely to sit":"doubtful",
"unlikely to play":"doubtful",
" doubtful":"doubtful",
" questionable":"questionable",
"plans to play":"probable",
"expected to play":"probable",
"likely back":"probable",
" probable":"probable",
"will play":"available",
"will start":"available",
"schedule to play":"available",
"available to play":"available",
"not on injury report":"available",
"not on injury report":"available",
" active ":"available",
"starting on":"available",
"to play":"available",
"to start":"available",
"not on injury report":"available",
"off the injury report":"available",
" starting ":"available",
"will be good to go":"available",
" playing ":"available",
" available ":"available",
"good to go": "available",
"game-time call":"game time desicion",
" GTD":"game time desicion",
}

#%%
def create_status_col(df):    
    df.insert(5,"Current Status",np.nan)
    return df

def get_status_from_dic(str1, dic): # get status by the dic we created
    for status in dic.keys():
        if status in str1:
            return dic[status]
    return str1
    

def insert_status(df): # insert status we found
    df['Current Status'] = df['social_headline'].apply(lambda x: get_status_from_dic(x, roto_dic))
    return df

def combine_dt(df): # make 1 col of DF
    df.insert(0,"Game DT",np.nan)
    df["Game DT"] = df.apply(lambda r : pd.datetime.combine(r['Game Date'],r['Game Time']),1)
    return df

def adj_col_names(df): #change col names according to injury report
    df = df.rename({'Game DT':'Report DT','Game Date':'Report Date','Game Time':'Report Time','player': 'Player Name', 'title': 'Title','summary':'Summary','source':'Source'}, axis='columns')
    return df

def organize_roto(df):
    df = split_dt(df)
    df = switch_date_format(df)
    df = switch_time_format(df)
    df = split_pos_team(df)
    df = remove_old_cols(df)
    df = create_status_col(df)
    df = insert_status(df)
    df = combine_dt(df)
    df = adj_col_names(df)
    return df


roto_world = organize_roto(roto_world)
os.chdir('C:/Student/NBA Project')
roto_world.to_csv("Roto_World - Clean Report.csv", index=False)

#%%