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

#positions = list(df['Pos'].drop_duplicates())
teams = list(df['Squad'].drop_duplicates())
#leagues = list(df['Comp'].drop_duplicates())

# App

# Sidebar - title & filters
st.sidebar.markdown('### Data Filters')


teams_choice = st.sidebar.multiselect(
    "Teams:", teams, default=None)

mins_choice = st.sidebar.number_input(
    '90s played:',step=0.5)


df = df[df['Squad'].isin(teams_choice)]
df = df[df['90s'] > mins_choice]

# Main
st.title(f"Toolkit Builder")

# Main - dataframes
st.markdown('### Player Dataframe')

st.dataframe(df.sort_values(by=['Sh/90'],ascending=False).reset_index(drop=True))
