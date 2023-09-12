import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# st.title('MPG')

# df=pd.read_csv('data/mpg.csv')

# ## add a side bar with a checkbox to decide to show dataframe or not
# if st.sidebar.checkbox('Show dataframe'):
#     st.header('dataframe')
#     st.dataframe(df.sample(10))



st.title('Renewable energy plants')

import pandas as pd
data_path = "data/renewable_power_plants_CH.csv"
df = pd.read_csv(data_path)

import json
import random
f = open("data/georef-switzerland-kanton.geojson")
data = json.load(f)

cantons_dict = {
'TG':'Thurgau', 
'GR':'Graubünden', 
'LU':'Luzern', 
'BE':'Bern', 
'VS':'Valais',                
'BL':'Basel-Landschaft', 
'SO':'Solothurn', 
'VD':'Vaud', 
'SH':'Schaffhausen', 
'ZH':'Zürich', 
'AG':'Aargau', 
'UR':'Uri', 
'NE':'Neuchâtel', 
'TI':'Ticino', 
'SG':'St. Gallen', 
'GE':'Genève',
'GL':'Glarus', 
'JU':'Jura', 
'ZG':'Zug', 
'OW':'Obwalden', 
'FR':'Fribourg', 
'SZ':'Schwyz', 
'AR':'Appenzell Ausserrhoden', 
'AI':'Appenzell Innerrhoden', 
'NW':'Nidwalden', 
'BS':'Basel-Stadt'}

df['canton'] = df['canton'].map(cantons_dict)

# if st.sidebar.checkbox('show data'):
#     if st.checkbox('Show Swiss canton list'):
#         st.header('Dictionary')
#         st.dataframe(cantons_dict)



##############2nd part> show the total amount of plants per canton


df_production=df.groupby('canton').sum('production')
#df_production['prod_share']=df_production['production']/sum(df_production['production'])

if st.sidebar.checkbox('Display data inspection options'):
    if st.checkbox('Show Swiss canton list'):
        st.header('Dictionary')
        st.dataframe(cantons_dict)
    if st.checkbox('Show sum of renewable productino per canton'):
        st.header('Sum productino per canton')
        st.dataframe(df_production['production'])


### 1st graphic
st.title("The number of renewable plants per canton")
df_count=df.groupby(['canton'])['canton'].count()
fig = px.choropleth_mapbox(df_count, geojson=data,color=df_count,
            color_continuous_scale="turbo",
            locations=df_count.index, featureidkey="properties.kan_name", center={'lat':46.80111 , 'lon':8.22667},
            mapbox_style="open-street-map", 
            zoom=6.3,
            opacity=0.8,
            width=1000,
            height=800,
            )

fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})
fig

### 2nd graphic
st.title("The share of production per canton")


fig = px.choropleth_mapbox(df_production['production'], 
                           geojson=data, 
                           color=df_production['production'],
            locations=df_production.index, featureidkey="properties.kan_name", center={'lat':46.80111 , 'lon':8.22667},
            mapbox_style="open-street-map", 
            color_continuous_scale="turbo",
            zoom=6.3,
            opacity=0.8,
            width=1000,
            height=800,
            )

fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})
fig

### 3rd graphic
st.title("The production by source")
df_sum=df.groupby(['canton','energy_source_level_3'])['production'].sum().reset_index()
# df_sum.index=df_sum['canton']
# df_sum.drop(columns=['canton'],inplace=True)

select_source = st.radio(
    label='Renewable energy source', options=df_sum['energy_source_level_3'].unique())

fig = px.choropleth_mapbox(df_sum[df_sum['energy_source_level_3']=="select_source"], 
                           geojson=data, 
                           color=df_sum['production'],
            locations=df_sum['canton'], featureidkey="properties.kan_name", center={'lat':46.80111 , 'lon':8.22667},
            mapbox_style="open-street-map", 
            color_continuous_scale="turbo",
            zoom=6.3,
            opacity=0.8,
            width=1000,
            height=800,
            )

fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})
fig



from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

# Sample Choropleth mapbox using Plotly GO
import plotly.graph_objects as go

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df.fips, z=df.unemp,
                                    colorscale="Viridis", zmin=0, zmax=12,
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig