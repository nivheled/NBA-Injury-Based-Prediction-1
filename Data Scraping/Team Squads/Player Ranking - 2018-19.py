#%% import required packages
import pandas as pd
from urllib.request import Request
from urllib.request import urlopen
import numpy as np
from bs4 import BeautifulSoup

#%%


#%%
#use beautiful soup on ranking of 2018-2019 NBA players from nbamath.com

players_ranking_url = "https://nbamath.com/crystalbasketball-ranking-all-nba-players-for-2018-19/"
r = Request(players_ranking_url, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(r)
soup = BeautifulSoup(html, 'lxml')

#%%

#%% 

"""
In the website - each string conatins the name of the player, his team and
his ranking. The following functions extracts each element by 2018-2019 pattern.
"""

def get_player_name(player):
    start = player.find(" ") +1
    end = player.find(",")
    name = player[start:end]
    return name

def get_player_team(player):
    start = player.find(",") + 2
    end = player.find(":")
    team = player[start:end]
    return team

def get_player_ranking(player):
    end = player.rfind("(") - 1
    sub_str_player = player[:end]
    start = sub_str_player.rfind(" ") + 1
    rank = player[start:end]
    return float(rank)
    

#%%

#%%

#group by: Team
#in each team, sort by: Rank
#add column 'Value_to_Team' - inside ranking for each team

def sort_df_by_rank(df):
    df = df.sort_values(by=['Team','Ranking'], ascending = False)
    df['Value_to_Team'] = df.groupby('Team')['Ranking'].cumcount().apply(lambda x: x+1)
    return df

#drop unwanted rows (not players, random strings)

def drop_irrelevant(df):    
    df.drop(df.loc[df['Team']=="ow-End Starters"].index, inplace=True)
    df.drop(df.loc[df['Team']=="nd-of-Bench Pieces"].index, inplace=True)
    return df

#iterate through all players, add problematic lines and execute all 

def append_all_players(df):
    i = 0
    for player in soup.find_all('p'):
        i = i+1
        if (i<5 or i>538):
            continue
        else:
            player = str(player.text)
            name = get_player_name(player)
            team = get_player_team(player)
            ranking = get_player_ranking(player)
            ls = [name, team, ranking,np.nan]
            df.loc[i-5] = ls
    df.loc[i-8] = ["LeBron James", "Los Angeles Lakers", float(11.89), np.nan]
    df = drop_irrelevant(df)
    df.loc[df.Name == "Justise Winslow", 'Team'] = "Miami Heat"
    df = sort_df_by_rank(df)
    return df
#%%
"""
Create the data frame, exectue the functions and export to PDF
"""


players_ranking_2018_2019 = pd.DataFrame(columns =['Name', 'Team', 'Ranking','Value_to_Team'])
players_ranking_2018_2019 = append_all_players(players_ranking_2018_2019)
players_ranking_2018_2019.to_csv("Players Ranking - 2018-19.csv", index=False)
#%%
