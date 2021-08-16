import pandas as pd
import numpy as np
import streamlit as st

# Data import & columns
af=pd.read_html('https://fbref.com/en/comps/Big5/2020-2021/stats/players/2020-2021-Big-5-European-Leagues-Stats')[0]
af = af.droplevel(0, axis=1)
af = af[af.Player != 'Player']
af["MP"] = pd.to_numeric(af["MP"])

af["Player+Team"]=af["Player"]+" "+af["Squad"]

af=af[["Player+Team","MP"]]


df=pd.read_html('https://fbref.com/en/comps/Big5/2020-2021/shooting/players/2020-2021-Big-5-European-Leagues-Stats')[0]
df = df.droplevel(0, axis=1)
df = df[df.Player != 'Player']
df["90s"] = pd.to_numeric(df["90s"])
df["Gls"] = pd.to_numeric(df["Gls"])

df["Player+Team"]=df["Player"]+" "+df["Squad"]

dfatt=df.join(af.set_index('Player+Team'), on='Player+Team')

df1=pd.read_html('https://fbref.com/en/comps/Big5/2020-2021/misc/players/2020-2021-Big-5-European-Leagues-Stats')[0]
df1 = df1.droplevel(0, axis=1)
df1 = df1[df1.Player != 'Player']
df1["90s"] = pd.to_numeric(df1["90s"])
df1["Fls"] = pd.to_numeric(df1["Fls"])

df1["Fls/90"]=df1["Fls"]/df1["90s"]
df1["Player+Team"]=df1["Player"]+" "+df1["Squad"]

cols1= ["Player+Team","Comp","CrdY","Fls","Fls/90"] #,"Squad","90s"

df1 = df1[cols1]

df2=pd.read_html('https://fbref.com/en/comps/Big5/2020-2021/defense/players/2020-2021-Big-5-European-Leagues-Stats')[0]
df2 = df2.droplevel(0, axis=1)
df2 = df2[df2.Player != 'Player']

df2.columns.values[14] = "TEST"

df2["90s"] = pd.to_numeric(df2["90s"])
df2["Tkl"] = pd.to_numeric(df2["Tkl"])

df2["Tkl/90"]=df2["Tkl"]/df2["90s"]
df2["Player+Team"]=df2["Player"]+" "+df2["Squad"]

cols2= ["Player+Team","Player","Squad","90s","Tkl","Tkl/90"] #

df2 = df2[cols2]

dfdef=df1.join(df2.set_index('Player+Team'), on='Player+Team')
dfdef=dfdef.join(af.set_index('Player+Team'), on='Player+Team')

# App

# Sidebar - title & filters
st.sidebar.markdown('### Data Filters')

leagues = list(df['Comp'].drop_duplicates())
league_choice = st.sidebar.selectbox(
    "Filter by league:", leagues, index=1)

dfatt=dfatt.loc[(dfatt['Comp'] == league_choice)]
dfdef=dfdef.loc[(dfdef['Comp'] == league_choice)]


teams = list(dfatt['Squad'].drop_duplicates())
teams=sorted(teams)
teams_choice = st.sidebar.multiselect(
    "Filter by Team:", teams, default=None)

dfatt = dfatt[dfatt['Squad'].isin(teams_choice)]
dfdef = dfdef[dfdef['Squad'].isin(teams_choice)]

mins_choice = st.sidebar.number_input(
    'Filter by Minimum 90s played:',step=0.5)
dfatt = dfatt[dfatt['90s'] > mins_choice]
dfdef = dfdef[dfdef['90s'] > mins_choice]


dfdef=dfdef[["Player","Squad","MP","90s","CrdY","Fls","Fls/90","Tkl","Tkl/90"]]
dfatt=dfatt[["Player","Squad","MP","90s","Gls","Sh/90","SoT/90"]]

# Main
st.title(f"Toolkit Builder")

# Main - dataframes
st.markdown('### Shooting Stats 2020/21')

st.dataframe(dfatt.sort_values(by=['Sh/90'],ascending=False).reset_index(drop=True))

st.markdown('### Tackling Stats 2020/21')

st.dataframe(dfdef.sort_values(by=['Fls/90'],ascending=False).reset_index(drop=True))
