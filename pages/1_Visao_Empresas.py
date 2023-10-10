# ==================================================
# Bibliotecas Necessárias
# ==================================================
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import folium 
import numpy as np
import datetime
from PIL import Image 
from datetime import datetime
from streamlit_folium import folium_static
from haversine import haversine

#-------------------------------------Início das Funções-----------------------------------

st.set_page_config(page_title='Visão Empresas', page_icon=':bar_chart:', layout='wide')

# ==================================================
# Funções
# ==================================================
def Country_maps(df1): 
    """ Está função tem a responsabilidade de Criar a visão empresa com os gráfico. 
        Conteúdo:
        1- A localização central de cada cidade por tipo de tráfego.
    """    
    cols=['City','Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude' ]
    df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).median().reset_index()

    map = folium.Map()

    for index, location_info in df_aux.iterrows():    
       folium.Marker([location_info['Delivery_location_latitude'],
                      location_info['Delivery_location_longitude' ]],
                      popup=location_info[['City', 'Road_traffic_density']]).add_to( map )
            
    folium_static(map, width=850, height=250)
   
def Order_Share_by_Week(df1):    
    """ Está função tem a responsabilidade de Criar a visão empresa com os gráfico. 
        Conteúdo:
        1- A quantidade de pedidos por entregador por semana.
    """    
    df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
    df_aux02 = (df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                   .groupby(['week_of_year'])
                   .nunique()
                   .reset_index())
    
    df_aux = pd.merge(df_aux01, df_aux02, how='inner')

    df_aux['order_by_deliver'] = df_aux ['ID'] / df_aux ['Delivery_person_ID']

    fig=px.line(df_aux, x='week_of_year', y='order_by_deliver' )
    
    return fig
        
def Order_by_Week(df1):
    """ Está função tem a responsabilidade de Criar a visão empresa com os gráfico. 
        Conteúdo:
        1- A quantidade de pedidos por semana.
    """
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    fig=px.line(df_aux, x='week_of_year', y= 'ID')
        
    return fig

def Traffic_Order_City(df1):
    """ Está função tem a responsabilidade de Criar a visão empresa com os gráfico. 
        Conteúdo:
        1- Comparação do volume de pedidos por cidade e tipo de tráfego.
    """
    df_aux = (df1.loc[:, ['ID', 'City','Road_traffic_density']]
                 .groupby(['City', 'Road_traffic_density'])
                 .count()
                 .reset_index())

    fig=px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color= 'City' )
    
    return fig

def Traffic_Order_Share(df1):
    """ Está função tem a responsabilidade de Criar a visão empresa com os gráfico. 
        Conteúdo:
        1- Distribuição dos pedidos por tipo de tráfego.
    """            
    df_aux = (df1.loc[:, ['ID', 'Road_traffic_density']]
                 .groupby(['Road_traffic_density'])
                 .count()
                 .reset_index())
    
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum() 
    fig=px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
    
    return fig

def Order_metric(df1):
    """ Está função tem a responsabilidade de Criar a visão empresa com os gráfico. 
        Conteúdo:
        1- Quantidade de pedidos por dia.
    """            
    cols = ['ID', 'Order_Date']        
    df_aux = df1.loc[:, cols].groupby(['Order_Date']).count().reset_index()        
    fig=px.bar(df_aux, x='Order_Date', y= 'ID')
    
    return fig
        
def clean_code(df1):
    
    """ Está função tem a responsabilidade de limpar o dataframe. 
    
        Tipos de Limpesa:
        1- Remoção dos dados NaN;
        2- Mudança do tipo da coluna de dados;
        3- Remoção dos espaços das variáveis de texto;
        4- Formatção da coluna de dados;
        4- Limpeza da coluna de tempo(remoção do texto da variável numérica).
        
        Imput: Dataframe.
        Output: Dataframe.   
    """
        
    # 1 Convertendo as colunas de texto para número
    linhas_selecionadas= (df1 ["Delivery_person_Age"] !="NaN ")
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1 ["Road_traffic_density"] != "NaN ")
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1 ["City"] != "NaN ")
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1 ["Festival"] != "NaN ")
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1 ["Delivery_person_Ratings"] != "NaN ")
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1 ["multiple_deliveries"] != "NaN ")
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # 2 convertendo a coluna ratings de texto para número decimal (float)
    df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype(float)

    # 3 convertendo a coluna order_date de texto para data
    df1["Order_Date"] = pd.to_datetime (df1["Order_Date"], format= "%d-%m-%Y" ) 
    df1["week_of_year"] = df1["Order_Date"].dt.strftime("%U")

    # 4 convertendo de texto para número inteito (int)
    df1["multiple_deliveries"] = df1["multiple_deliveries"].astype(int)
    df1["Delivery_person_Age"] =df1["Delivery_person_Age"].astype(int)

    # 5 removendo os espaços dento de strig/texto/object  fazendo de uma forma mas rápida
    df1.loc[:, "ID"] =  df.loc[:, "ID"].str.strip()
    df1.loc[:, "Road_traffic_density"] =  df.loc[:, "Road_traffic_density"].str.strip()
    df1.loc[:, "Type_of_order"] =  df.loc[:, "Type_of_order"].str.strip()
    df1.loc[:, "Type_of_vehicle"] =  df.loc[:, "Type_of_vehicle"].str.strip()
    df1.loc[:, "City"] =  df.loc[:, "City"].str.strip()
    df1.loc[:, "Festival"] =  df.loc[:, "Festival"].str.strip()

    # 6 limpando a coluna de time taken
    df1["Time_taken(min)"]= df1["Time_taken(min)"].apply(lambda x: x.split("(min) ")[1])
    df1["Time_taken(min)"]= df1["Time_taken(min)"].astype(int)
    
    return df1

#---------------------------Início da Estrutura lógica do código----------------------------

# ==================================================
# Import dataset
# ==================================================
df = pd.read_csv('dataset/train.csv' )

# ==================================================
# Limpando os dados
# ==================================================
df1 = clean_code(df)


# ==================================================
# Barra Lateral
# ==================================================
st.markdown('# Marketplace - Visão Empresas')

#image_path='/home/jadson/Documentos/Repos/logo.png'
image=Image.open('logo.png')
st.sidebar.image(image, width=340)

st.sidebar.markdown('# JNH Company')
st.sidebar.markdown('## Fastest Delivery in town')
st.sidebar.markdown('''___''')

st.sidebar.markdown('## Selecione uma data limite')

date_slider=st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')

st.sidebar.markdown('''___''')

traffic_options=st.sidebar.multiselect(
    '#### Quais as condições do trânsito?',
    ['Low','Medium', 'High', 'Jam'],
    default=['Low','Medium', 'High', 'Jam'])

st.sidebar.markdown('''___''')
st.sidebar.markdown('### Powered by Comunidade DS')

#Filtro da data
linhas_selecionadas=df1['Order_Date'] < date_slider
df1=df1.loc[linhas_selecionadas, :]

#Filtro de Trânsito
linhas_selecionadas=df1['Road_traffic_density'].isin(traffic_options)
df1=df1.loc[linhas_selecionadas, :]


# ==================================================
# Layout no Streamliy
# ==================================================
tab1, tab2, tab3=st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica', ] )

with tab1:
    with st.container():
        fig= Order_metric(df1)
        st.markdown('## Orders by Day')
        st.plotly_chart(fig, use_container_width=True)        
        
    with st.container():   
        st.markdown('''___''')  
        col1, col2=st.columns(2)
        
        with col1:
            fig = Traffic_Order_Share(df1)
            st.markdown('## Traffic Order Share')
            st.plotly_chart(fig, use_container_width=True)  
              
    with col2:
            fig = Traffic_Order_City(df1)
            st.markdown('## Traffic Order City')
            st.plotly_chart(fig, use_container_width=True)
 
with tab2:
    with st.container():
        fig = Order_by_Week(df1)
        st.markdown('### Order by Week') 
        st.plotly_chart(fig, use_container_width=True)
   
    with st.container():
        st.markdown('''___''')
        fig = Order_Share_by_Week(df1)
        st.markdown('### Order Share by Week')
        st.plotly_chart(fig, use_container_width=True)
        
with tab3:
    st.markdown('### Country Maps')
    Country_maps(df1)
    