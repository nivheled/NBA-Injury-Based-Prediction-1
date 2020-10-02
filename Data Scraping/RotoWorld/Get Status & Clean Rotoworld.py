"""
Please note that the code below was written in Spyder environment.
Due to this, you will encounter the symbols #%%, which indicates on a new cell of code that can be exectued independently.  
"""

#%% import all packages
import pandas as pd
import numpy as np
from datetime import datetime
#%%

#%% read the scraped data
roto_world = pd.read_csv("C:/Student/NBA Project/rotoworld_injuries_not_clean.csv",encoding='latin1')

#%%

#%% function that find the n'th location of char in a string
def find_nth(word, char, n):
    start = word.find(char)
    while start >= 0 and n > 1:
        start = word.find(char, start+len(char))
        n -= 1
    return start

#%%

#%%
#split date & time to different cols

def split_dt(df):
    df.insert(0,"Game Date",np.nan)
    df.insert(1,"Game Time",np.nan)
    df['Game Date'] = df['date_time'].apply(lambda x: x[:find_nth(x,",",2)])
    df['Game Time'] = df['date_time'].apply(lambda x: x[find_nth(x,",",2)+2:])
    return df

#change date format to: YYYY-MM-DD

def switch_date_format(df):
    df['Game Date'] = df['Game Date'].apply(lambda x: datetime.strptime(x,'%b %d, %Y'))
    df['Game Date'] = df['Game Date'].dt.date
    return df

#change time format to: HH:MM:SS

def switch_time_format(df):
    df['Game Time'] = df['Game Time'].apply(lambda x: x.replace("ET",""))
    df['Game Time'] = df['Game Time'].apply(lambda x: x[:-1])
    df['Game Time'] = df['Game Time'].apply(lambda x: datetime.strptime(x, '%I:%M %p')).dt.time
    return df

#split columns of player position and his team to 2 different columns

def split_pos_team(df):
    df.insert(3,"Team",np.nan)
    df.insert(4,"Position",np.nan)
    df['position_and_team'] = df['position_and_team'].apply(lambda x: x.strip())
    df["Team"] = df["position_and_team"].apply(lambda x: x[x.find(",")+1:])
    df["Position"] = df["position_and_team"].apply(lambda x: x[:x.find(",")])
    df["Team"] = df["Team"].apply(lambda x: x.strip())
    df["Position"] = df["Position"].apply(lambda x: x.strip())
    return df

#remove unwanted columns

def remove_old_cols(df):
    del df['position_and_team']
    del df['date_time']
    return df




#%%


#%% dictionary for all options of player's status
roto_dic = {"ruled out":"out",
"night off to rest":"out",
"getting the day off":"out",
"sitting out":"out",
"out again":"out",
"will rest":"out",
"expected to sit out":"doubtful",
"sit out":"out",
" resting":"out",
"out with thigh contusion":"out",
"sits out":"out",
"will not play":"out",
"won't play":"out",
"still out":"out",
"does not play":"out",
"doesn't play":"out",
"placed in concussion protocol":"out",
" out":"out",
"likely to sit":"doubtful",
"unlikely to play":"doubtful",
" doubtful":"doubtful",
" questionable":"questionable",
"plans to play":"probable",
"not expected to play":"doubtful",
"expected to play":"probable",
"likely back":"probable",
" probable":"probable",
"will play":"available",
"will start":"available",
"schedule to play":"available",
"available to play":"available",
"not on the injury report":"available",
"off injury report":"available",
" active ":"available",
"starting on":"available",
"to play":"available",
"to start":"available",
"not on injury report":"available",
"off the injury report":"available",
" starting":"available",
"will be good to go":"available",
"not playing ":"out",
" playing ":"available",
"is available":"available",
" available":"available",
"good to go": "available",
"game-time call":"game time desicion",
"game-time decision":"game time desicion",            
" GTD":"game time desicion",
"game-time":"game time desicion",
"uncertain":"questionable",  
"will not start":"out",
"not traveling":"out",
}
#%%

def create_status_col(df):    
    df.insert(5,"Current Status",np.nan)
    return df

#get status by the dic we created

def get_status_from_dic(str1, dic): 
    for status in dic.keys():
        if status in str1:
            return dic[status]
    return str1
    
#insert status we found

def insert_status(df): 
    df['Current Status'] = df['social_headline'].apply(lambda x: get_status_from_dic(x, roto_dic))
    return df

#make 1 col of Date&Time

def combine_dt(df): 
    df.insert(0,"Game DT",np.nan)
    df["Game DT"] = df.apply(lambda r : pd.datetime.combine(r['Game Date'],r['Game Time']),1)
    return df

#change col names according to the official injury report

def adj_col_names(df): 
    df = df.rename({'Game DT':'Report DT','Game Date':'Report Date','Game Time':'Report Time','player': 'Player Name', 'title': 'Title','summary':'Summary','source':'Source'}, axis='columns')
    return df

#execute all the functions

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

#%%

#%% main - run all and export to csv
roto_world = organize_roto(roto_world)
os.chdir('C:/Student/NBA Project')
roto_world.to_csv("Roto_World - Clean Report.csv", index=False)
#%%
