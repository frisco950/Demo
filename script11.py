from flask import Flask, render_template, request
app=Flask(__name__)
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/',methods=["POST"])
def about():
    if request.method=='POST':
        fecha_conocer=request.form["fecha_conocer"]
        print(fecha_conocer)
    import pandas as pd
    import numpy as np
    #from sklearn import linear_model
    #from sklearn.metrics import mean_squared_error, r2_score
    #from datetime import datetime
    from difflib import get_close_matches
    import folium


    data3=pd.read_csv('Demo/air_quality_Nov2017.csv')

    #data3.head(2)

    data3["O3 Value"]=data3["O3 Value"].fillna(0)
    data3["NO2 Value"]=data3["NO2 Value"].fillna(0)
    data3["PM10 Value"]=data3["PM10 Value"].fillna(0)
    data3["O3 Quality"]=data3["O3 Quality"].fillna('Good')
    data3["NO2 Quality"]=data3["NO2 Quality"].fillna('Good')
    data3["PM10 Quality"]=data3["PM10 Quality"].fillna('Good')
    #data3.head(2)


    #data3.dtypes


    dummy_Air_Q=pd.get_dummies(data3["Air Quality"], prefix="AQ")
    data3=pd.concat([data3, dummy_Air_Q], axis=1)
    #data3.head(2)









    #fecha_conocer=input('¿Para cuando la previsión?(dd/mm/aa hh:mm) : ')

    fecha_buscar=get_close_matches(fecha_conocer,data3['Generated'],3,0.7)

    fecha_buscar[0]

    Data_Fecha= data3[data3['Generated']==fecha_buscar[0]]


    NO2_mu=data3['NO2 Value'].mean()
    PM10_mu=data3['PM10 Value'].mean()
    AQ_mu=data3['AQ_Moderate'].mean().item()

    NO2_sd=data3['NO2 Value'].std()
    PM10_sd=data3['PM10 Value'].std()


    Qi_list=[]
    dF_list=[]
    Lo_list=[]
    La_list=[]

    #fecha_conocer

    #type(fecha_conocer)
    for dF in Data_Fecha['Station']:
        dF_list.append(dF)

        #print(dF)
        Data_S=Data_Fecha[Data_Fecha['Station']==dF]

        Data_N=Data_S['NO2 Value'].item()

        Data_P=Data_S['PM10 Value'].item()
        Data_Lo=Data_S['Longitude'].item()
        Data_La=Data_S['Latitude'].item()
        Lo_list.append(Data_Lo)
        La_list.append(Data_La)

        #PM10_mu= 22.781337#media
        #PM10_sd=8.454874 # Desviación standard
        Z_PM10=np.random.randn(5744) # valores aleatorios con distribución normal
        dataP=PM10_mu+PM10_sd*Z_PM10 # Tipificamos la variable
        #NO2_mu=50.449290
        #NO2_sd=25.645727
        Z_NO2=np.random.randn(5744)
        dataN=NO2_mu+NO2_sd*Z_NO2
        pi_avg=0
        pi_value_list=[]
        n_exp=1000
        y=Data_P
        j=Data_N
        for i in range(n_exp):

            value=0
            x=np.random.choice(dataP).tolist()
            t=np.random.choice(dataN).tolist()
            z= np.sqrt(x*y)
            v= np.sqrt(t*j)
            if z>=36 or v>=92:
                value+=1
            float_value=float(value)
            pi_value=float_value
            pi_value_list.append(pi_value)
            pi_avg+=pi_value

        pi=pi_avg/n_exp


        if pi>=AQ_mu:
            Qi_list.append('Aire de Calidad Moderada')
        else:
            Qi_list.append('Aire de  Calidad Buena')






        #print(fecha_buscar[0],Qi_list)

    #for df in Data_Fecha['Station']:
        #Qi_list.append(Qi)






    ## Añadir un mapa

    lat = list(La_list)
    lon = list(Lo_list)
    est = list(dF_list)
    cal = list(Qi_list)
    def color_producer(calidad):
        if calidad == 'Aire de  Calidad Buena':
            return 'green'
        elif calidad=='Aire de Calidad Moderada':
            return 'orange'
    map = folium.Map(location=[41.3875,2.16835 ], zoom_start=10, tiles="Stamen Terrain")
    fgv = folium.FeatureGroup(name="Calidad del Aire")
    fill_color='Grey'
    for lt, ln, est,cal in zip(lat, lon, est, cal):
        fgv.add_child(folium.CircleMarker(location=[lt, ln], radius = 30, popup=est+" " + cal,
        fill_color = color_producer(cal), fill=True,  color = fill_color, fill_opacity=0.5))

    map.add_child(fgv)


    map.save('Demo/templates/Map1.html')


    return render_template("Map1.html")

if __name__=="__main__":
    app.run(debug=True)
