
import cx_Oracle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import chart_studio.dashboard_objs as dashboard
import os
import chart_studio
import chart_studio.plotly as py
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


try: 


    chart_studio.tools.set_credentials_file(username='wktorion', api_key='k9dClZ8sAkmvkkNXZJMk')
    def fileId_from_url(url):
        """Return fileId from a url."""
        raw_fileId = re.findall("~[A-z.]+/[0-9]+", url)[0][1: ]
        return raw_fileId.replace('/', ':')
  
    con = cx_Oracle.connect('viktor/Password@localhost') 
      
    cursor = con.cursor() 

    cursor.execute("""SELECT incedents.CITY,incedents.severity, Count(*) as NumberOfHardIncedents
                        from INCEDENTS 
                        group by (incedents.CITY,incedents.severity)
                        having incedents.severity > 2
                        ORDER BY incedents.CITY""") 
    
    BarQuery = {'X':[],'Y':[]}
    for result in cursor:
        BarQuery['X'].append(str(result[0])+':'+str(result[1]))
        BarQuery['Y'].append(result[2])

    cursor.execute("""SELECT incedents.CITY, ROUND(Count(*)/(select count(ID) from incedents),2) as PrecentOfAll
                    from INCEDENTS 
                    group by (incedents.CITY)""")

    PieQuery = {'Lables':[],'Values':[]}
    for result in cursor:
        PieQuery['Lables'].append(str(result[0]))
        PieQuery['Values'].append(result[1])


    cursor.execute("""SELECT to_char(STARTTIME, 'DD.MM.YYYY') as IncedentsDate,count(*) as Incedents
                    from INCEDENTS
                    GROUP BY (to_char(STARTTIME, 'DD.MM.YYYY'))
                    ORDER BY (to_Date(IncedentsDate))""")

    ScatterResult = {'X':[],'Y':[]}
    for result in cursor:
        ScatterResult['X'].append(result[0])
        ScatterResult['Y'].append(result[1])

    x = []
    for i in range(len(ScatterResult['X'])):
        x.append(i+1)


    x = np.array(x).reshape((-1, 1))
    y = np.array(ScatterResult['Y'])
    
        
        
    # При тестуванні градус 3 дав найбільшу точність *shrug*
    x_ = PolynomialFeatures(degree=3, include_bias=False).fit_transform(x)
    model = LinearRegression().fit(x_, y)
    r_sq = model.score(x_, y)
        
    print('coefficient of determination:', r_sq)
    ScatterResult['Y'] = model.predict(x_)


    fig = go.Figure(
    data=[go.Bar(y=BarQuery['Y'],x=BarQuery['X'])],
    layout_title_text="Вивести кількість аварій кожної тяжкості, де тяжкість більше 2 у кожномі місті"
    )
    BarQuery = py.plot(fig)
    fig = go.Figure(
    data=[go.Pie(labels=PieQuery['Lables'], values=PieQuery['Values'])],
    layout_title_text="Вивести відсоток аварій для кожного міста, відносно загальної кількості"
    )
    PieQuery = py.plot(fig)
    fig = go.Figure(
    data=[go.Scatter(x=ScatterResult['X'], y=ScatterResult['Y'])],
    layout_title_text="Динаміка кількості аварій по датам"
    )
    ScatterQuery = py.plot(fig)




    """--------CREATE DASHBOARD------------------ """
    
 
    my_dboard = dashboard.Dashboard()

    BarQueryId = fileId_from_url(BarQuery)
    PieQueryId = fileId_from_url(PieQuery)
    ScatterQueryId = fileId_from_url(ScatterQuery)
     
    box_1 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': BarQueryId,
        'title': 'Кількість аварій кожної тяжкості, де тяжкість більше 2 у кожномі місті'
    }
     
    box_2 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': PieQueryId,
        'title': 'відсоток аварій для кожного міста'
    }
     
    box_3 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': ScatterQueryId,
        'title': 'Динаміка кількості аварій по датам'
    }
     
     
    my_dboard.insert(box_1)
    my_dboard.insert(box_2, 'below', 1)
    my_dboard.insert(box_3, 'left', 2)
 
 
 
    py.dashboard_ops.upload(my_dboard, 'Лабораторна 2')










except Exception as e: 
    print("There is a problem with Oracle", e) 
  
finally: 
    if cursor: 
        cursor.close() 
    if con: 
        con.close()