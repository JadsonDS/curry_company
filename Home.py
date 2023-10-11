import streamlit as st
from PIL import Image 

st.set_page_config(
    page_title = 'Home',
    page_icon = ':house:')
    

image=Image.open('logo.png')
st.sidebar.image(image, width=300)

st.sidebar.markdown('# JNH Company')
st.sidebar.markdown('## Fastest Delivery in town')
st.sidebar.markdown('''___''')

st.write('# Curry Company Grouwth Dasbord')

st.markdown(
    """
    Growth Dashbord foi construído para acompanhar as métricas de crescimento dos Entregadores, Restaurantes e Empresas.
    ### Como Utilizar esse Grouwth Dashbord?:
    
    - #### Visão Empresa:
        - Visão Geremcial: Métrica gereais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica : Insights de geolocalização.
        
        
    - #### Visão Entregador:
      - Acompanhamento dos indicadores semanais de crescimento.
      
        
    - #### Visão Restaurantes: 
        - Indicadores semanais de crescimento dos restaurantes
        
    #### Ask for Help
    - Time de Data Science no  Discord    
        - @jadson            
""")