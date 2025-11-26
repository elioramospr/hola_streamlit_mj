import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px


####################
## ajustar el layout
#################### 

st.set_page_config(layout="wide")


##################
## tamaño del plot
################## 

fig, ax = plt.subplots()


#########
## titulo
######### 

col1, col2, col3 = st.columns([1,3,1])


col1.image("https://github.com/elioramospr/hola_streamlit_mj/blob/main/logouprh.png?raw=true",width=150)
col2.markdown("<p align='center'><h2>Datos de Covid - Variante Omicrón</h2></p>",unsafe_allow_html=True)
col3.image("https://github.com/elioramospr/hola_streamlit_mj/blob/main/covid.png?raw=true",width=150)

st.divider()

#############
## leer datos
############# 

df_covid = pd.read_csv("https://raw.githubusercontent.com/elioramosweb/archivo_datos/main/datos_diarios-2022-03-22_10_20_15.csv",parse_dates=['date'])

######################
## seleccionar columna
###################### 

nombres = list(df_covid.columns)[1:]

columna = st.sidebar.selectbox("Columna de interés:",nombres)


################################
## indicar si se quiere suavizar
################################ 

suavizado = st.sidebar.checkbox("Suavizado")

#####################################
## indicar si se quiere mostrar tabla
##################################### 

tabla = st.sidebar.checkbox("Mostrar datos")

st.sidebar.divider()


# df_covid.plot(x="date",y=columna,ax=ax,
#               xlabel="Fecha",
#               ylabel=columna,
#               title="\n")

fig1 = px.line(df_covid,x="date",y=columna)

fig1.update_layout(
    margin={"r":10,"t":50,"l":10,"b":1},
    title_text="Serie de Tiempo",
    title_x=0.6,
    title_xanchor="center"
)

fig1.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
fig1.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)



##########################
## formato de dos columnas
########################## 

col1,col2 = st.columns(2)


#############################
## si se selecciono suavizado
############################# 

if suavizado:
    ventana = st.sidebar.slider("Ventana de suavizado [días]",1,15,7)
    df_rolling =  df_covid[columna].rolling(ventana,center=True).mean()  
    df_covid[columna+"_rolling"] = df_rolling
    #df_covid.plot(x="date",y=columna+"_rolling",ax=ax)
    fig2 = px.line(df_covid,x="date",y=columna+"_rolling")
    fig2.update_traces(line_color='orange')
    fig1.add_traces(list(fig2.select_traces()))
    st.sidebar.divider()



col1.plotly_chart(fig1)

#col1.pyplot(fig)
     
st.sidebar.markdown("""Aplicación desarrollada por:<br> <i>Elio Ramos <br>
                    Comp3005<br>Universidad de Puerto Rico en Humacao</i>""", 
                    unsafe_allow_html=True)


if col2:
    if tabla:
        df_covid["date"] = df_covid["date"].dt.strftime("%d-%b-%Y")
        df_filtrado = df_covid[["date",columna]]
        col2.space()
        col2.write(df_filtrado)