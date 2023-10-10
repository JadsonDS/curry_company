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

st.set_page_config(page_title='Visão Entregadores', page_icon=':articulated_lorry:', layout='wide')

# ==================================================
# Funções
# ==================================================
def avaliacao(df1):
    """ Está função tem a responsabilidade de Criar a visão entregadores em forma de Tabelas. 
        Conteúdo:
        1- Avaliação Média e Desvio Padrão por Trânsito.
        """   
    df_avaliacao= (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                      .groupby('Road_traffic_density',)
                      .agg({'Delivery_person_Ratings':['mean', 'std']}))

    df_avaliacao.columns = ['delivery_mean', 'delivery_std']
    df_avaliacao.reset_index()
    st.dataframe(df_avaliacao)
    
    return st.dataframe

def avaliacao1(df1):
    """ Está função tem a responsabilidade de Criar a visão entregadores em forma de Tabelas. 
        Conteúdo:
        1- Avaliação Média e Desvio Padrão por Trânsito.
        """   
    df_avaliacao1= (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                       .groupby('Weatherconditions')
                       .agg({'Delivery_person_Ratings':['mean', 'std']}))

    df_avaliacao1.columns = ['delivery_mean', 'delivery_std']

    df_avaliacao1.reset_index()
    st.dataframe(df_avaliacao1)
    
    return st.dataframe


def top_deliveres(df1, top_asc): 
    """ Está função tem a responsabilidade de Criar a visão entregadores em forma de Tabelas. 
        Conteúdo:
        1- Top Entregadores mais rápidos;
        2- Top Entregadores mais Lentos.
    """    
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
              .groupby(['City','Delivery_person_ID']).max()
              .sort_values(['City', 'Time_taken(min)'],ascending=top_asc)
              .reset_index())

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03, ]).reset_index(drop=True)
    
    return df3
       
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
df = pd.read_csv('dataset/train.csv')

# ==================================================
# Limpando os dados
# ==================================================
df1 = clean_code(df)

# ==================================================
# Barra Lateral
# ==================================================
st.markdown('# Marketplace - Visão Entregador')

image=Image.open('logo.png')
st.sidebar.image(image, width=340)

st.sidebar.markdown('# JNH Company')
st.sidebar.markdown('## Fastest Delivery in town')
st.sidebar.markdown('''___''')

st.sidebar.markdown('## Selecione uma data limite')

date_slider=st.sidebar.slider(
    'Até qual valor',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')

st.sidebar.markdown('''___''')

Weatherconditions_options=st.sidebar.multiselect(
    '#### Quais as condições do Clima?',
    ['conditions Cloudy','conditions Fog', 'conditions Sandstorms', 'conditions stormy', 'conditions Sunny', 'conditions Windy'],
    default=['conditions Cloudy','conditions Fog', 'conditions Sandstorms', 'conditions stormy', 'conditions Sunny', 'conditions Windy'])

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

#Filtro de Clima
linhas_selecionadas=df1['Weatherconditions'].isin(Weatherconditions_options)
df1=df1.loc[linhas_selecionadas, :]

# ==================================================
# Layout no Streamliy
# ==================================================
st.header('Visão Gerencial', divider='gray')

with st.container():
    st.markdown('### Overall Metrics')
    col1, col2, col3, col4 =st.columns(4)

with col1:
    st.markdown('##### Maior de Idade')
    maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
    col1.metric('', maior_idade)
            
with col2:
    st.markdown('##### Menor de Idade')
    menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
    col2.metric('', menor_idade)
                
with col3:
    st.markdown('##### Melhor Condição')
    melhor_condicao = df1.loc[:, "Vehicle_condition"].min()
    col3.metric('', melhor_condicao)
            
with col4:
    st.markdown('##### Pior Condição')
    pior_condicao = df1.loc[:, "Vehicle_condition"].max()
    col4.metric('', pior_condicao)
        
with st.container():
    st.markdown('''___''')
    st.markdown('### Avaliações')

col1, col2 =st.columns(2)

with col1:
    st.markdown('###### Avaliação Média por Entregador')  
    cols= ['Delivery_person_ID', 'Delivery_person_Ratings']
    df_aux = df1.loc[:, cols].groupby(['Delivery_person_ID']).mean().reset_index()
                
    st.dataframe(df_aux, use_container_width=True, height=449)

with col2:
    st.markdown('###### Avaliação Média e Desvio Padrão por Trânsito')
    df_avaliacao = avaliacao(df1)    
    
        
    st.markdown('###### Avaliação Média e Desvio Padrão por Clima')
    df_avaliacao1 = avaliacao1(df1)    
    
with st.container():
    st.markdown('''___''')
    st.markdown('### Velocidade de Entrega')
    
col1, col2 =st.columns(2)

with col1:    
    df3 = top_deliveres(df1, top_asc=True)
    st.markdown('###### Top Entregadores mais Rápidos')
    st.dataframe(df3, use_container_width=True, height=500)

with col2:
    df3 = top_deliveres(df1, top_asc=False)
    st.markdown('###### Top Entregadores mais Lentos')
    st.dataframe(df3,use_container_width=True, height=500) 
        