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

st.set_page_config(page_title='Visão Restaurantes', page_icon=':fork_and_knife:', layout='wide')

# ==================================================
# Funções
# ==================================================
def avg_std_time_on_traffic(df1):
    """ Está função tem a responsabilidade de Criar a visão empresa. 
        Conteúdo:
        1- O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.
    """    
    df_aux=(df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
               .groupby(['City', 'Road_traffic_density'])
               .agg({'Time_taken(min)':['mean', 'std']}))
    
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    
    fig=px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', 
                    color='std_time', color_continuous_scale='jet', 
                    color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig

def avg_std_time_graph(df1):
    """ Está função tem a responsabilidade de Criar a visão empresa. 
        Conteúdo:
        1- O tempo médio e o desvio padrão de entregas por cidade.
    """    
    df_aux=df1.loc[:, ['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)':['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    
    fig=go.Figure()
    fig.add_trace(go.Bar(name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data',
array=df_aux['std_time'])))
    fig.update_layout(barmode='group')
    
    return fig

def avg_std_time_delivery (df1, festival, op):
    """ Está função cálcula o tempo médio e o desvio padrão do tempo de entrega. 
        Parâmetros:
            Imput:
                - df: Dataframe com dados necessários para o cálculo;
                - op: Tipo de operação que precisa ser calculado.
                    'avg_time': calcula o tempo médio;
                    'std_time': calculao desvio padrão do tempo.
            Output:
                - df: Dataframe com 2 colunas e 1 linha.
    """       
    df_aux=(df1.loc[:, ['Time_taken(min)', 'Festival']]
               .groupby('Festival')
               .agg({'Time_taken(min)':['mean', 'std']}))

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op], 2)
    
    return df_aux 

def distance(df1, fig):
    """ Está função tem a responsabilidade de Criar a visão empresa. 
        Conteúdo:
        1- Quantidade de Entregadores Únicos.
    """    
    if fig == False:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude',
                'Restaurant_latitude', 'Restaurant_longitude']

        df1['distance']= df1.loc[0:, cols].apply(lambda x:
                                  haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                  (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

        avg_distance = np.round(df1['distance'].mean(), 2)

        return avg_distance
    
    else:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude',
                'Restaurant_longitude']
        df1['distance']= df1.loc[:, cols].apply(lambda x: 
            haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                     (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        
        avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
        fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1,
0])])
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
st.markdown('# Marketplace - Visão Restaurantes')

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

City_options=st.sidebar.multiselect(
    '#### Qual a média e desvio padrão de entregas por cidade?',
    ['Metropolitian', 'Semi-Urban', 'Urban'],
    default=['Metropolitian', 'Semi-Urban', 'Urban'])

st.sidebar.markdown('''___''')

tipo_pedidos_options=st.sidebar.multiselect(
    '#### Qual a média e desvio padrão de entregas por tipo de pedido?',
    ['Buffet', 'Drinks', 'Meal', 'Snack'],
    default=['Buffet', 'Drinks', 'Meal', 'Snack'])

st.sidebar.markdown('''___''')
st.sidebar.markdown('### Powered by Comunidade DS')

#Filtro da data
linhas_selecionadas=df1['Order_Date'] < date_slider
df1=df1.loc[linhas_selecionadas, :]

#Filtro de Trânsito
linhas_selecionadas=df1['Road_traffic_density'].isin(traffic_options)
df1=df1.loc[linhas_selecionadas, :]

#Filtro da Média e Desvio Padrão de entregas da Cidade
linhas_selecionadas=df1['City'].isin(City_options)
df1=df1.loc[linhas_selecionadas, :]

#Filtro da Média e Desvio Padrão de entregas por tipo de pedido
linhas_selecionadas=df1['Type_of_order'].isin(tipo_pedidos_options)
df1=df1.loc[linhas_selecionadas, :]

# ==================================================
# Layout no Streamliy
# ==================================================
st.header('Visão Gerencial', divider='gray') 

with st.container():
    st.markdown('### Overall Metrics')
    col1, col2, col3, col4, col5, col6 =st.columns(6, gap='small')

with col1:
    st.markdown('###### Quantidade de Entregadores Únicos') 
    qnt = len(df1.loc[:, 'Delivery_person_ID'].unique())
    col1.metric('', qnt, )

with col2:
    avg_distance = distance(df1, fig=False)   
    st.markdown('###### Distância Média dos Resturantes e Locais de Entrega')
    col2.metric('', avg_distance )
     
with col3:
    df_aux = avg_std_time_delivery (df1, 'Yes', 'avg_time')
    st.markdown('###### Tempo Médio de Entregas durante o Festival')
    col3.metric('', df_aux )
    
with col4:
    df_aux = avg_std_time_delivery (df1, 'Yes', 'std_time')
    st.markdown('###### Desvio Padrão Médio de  Entregas com Festival')
    col4.metric('', df_aux )
    
with col5:
    df_aux = avg_std_time_delivery (df1, 'No', 'avg_time')
    st.markdown('###### Tempo Médio de Entregas Durante o Festival')
    col5.metric('', df_aux )
    
with col6:
    df_aux = avg_std_time_delivery (df1, 'No', 'std_time')
    st.markdown('###### Desvio Padrão Médio de  Entregas sem Festival')
    col6.metric('', df_aux )

    
with st.container():
    st.markdown('''___''')
    st.markdown('### Tempo Médio de Entregas por Cidade')
    col1, col2 =st.columns(2, gap='small')


with col1:
    fig = avg_std_time_graph(df1)
    st.markdown('###### O tempo médio e o desvio padrão de entregas por cidade')
    st.plotly_chart(fig, use_container_width=True, height=500)
    
with col2:
    st.markdown('###### O tempo médio e o desvio padrão de entregas por cidade e tipo de pedido.')  
    cols= ['Time_taken(min)', 'City', 'Type_of_order']
    df_aux=df1.loc[:, cols].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)':['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    st.dataframe(df_aux, use_container_width=True, height=380)            
    
with st.container():
    st.markdown('''___''')
    st.markdown('### Distribuição do Tempo')

col1, col2=st.columns(2, gap='small')    
        
with col1:
    fig = avg_std_time_on_traffic(df1)
    st.markdown('###### O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego')
    st.plotly_chart(fig, use_container_width=True, height=200)    

with col2:
    fig = distance (df1, fig=True)
    st.markdown('###### A distância média dos resturantes e dos locais de entrega')
    st.plotly_chart(fig, use_container_width=True, height=200)

         