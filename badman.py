import pandas as pd
import numpy as np
import streamlit as st

# Data import & columns
df=pd.read_html('https://fbref.com/en/comps/Big5/2020-2021/shooting/players/2020-2021-Big-5-European-Leagues-Stats')[0]
df = df.droplevel(0, axis=1)
df = df[df.Player != 'Player']
df["90s"] = pd.to_numeric(df["90s"])
df["Gls"] = pd.to_numeric(df["Gls"])

cols= ["Player","Squad","90s","Gls","Sh/90","SoT/90"]

df = df[cols]

df1=pd.read_html('https://fbref.com/en/comps/Big5/2020-2021/misc/players/2020-2021-Big-5-European-Leagues-Stats')[0]
df1 = df1.droplevel(0, axis=1)
df1 = df1[df1.Player != 'Player']
df1["90s"] = pd.to_numeric(df1["90s"])
df1["Fls"] = pd.to_numeric(df1["Fls"])

df1["Fls/90"]=df1["Fls"]/df1["90s"]

cols1= ["Player","Squad","90s","CrdY","Fls","Fls/90"]

df1 = df1[cols1]


#positions = list(df['Pos'].drop_duplicates())
teams = list(df['Squad'].drop_duplicates())
#leagues = list(df['Comp'].drop_duplicates())

# App

# Sidebar - title & filters
st.sidebar.markdown('### Data Filters')

#league_choice = st.sidebar.multiselect(
 #   "Leagues:", leagues, default=None)
teams_choice = st.sidebar.multiselect(
    "Filter by Team:", teams, default=None)
#position_choice = st.sidebar.multiselect(
 #   'Choose position:', positions, default=None)
mins_choice = st.sidebar.number_input(
    'Filter by Minimum 90s played:',step=0.5)

#df = df[df['Comp'].isin(league_choice)]
df = df[df['Squad'].isin(teams_choice)]
#df = df[df['Pos'].isin(position_choice)]
df = df[df['90s'] > mins_choice]

df1 = df1[df1['Squad'].isin(teams_choice)]
df1 = df1[df1['90s'] > mins_choice]

# Main
st.title(f"Toolkit Builder")

# Main - dataframes
st.markdown('### Shooting Stats 2020/21')

st.dataframe(df.sort_values(by=['Sh/90'],ascending=False).reset_index(drop=True))

st.markdown('### Tackling Stats 2020/21')

st.dataframe(df1.sort_values(by=['Fls/90'],ascending=False).reset_index(drop=True))
