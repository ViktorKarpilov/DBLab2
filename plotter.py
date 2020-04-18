
import cx_Oracle
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try: 
  
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








    fig = make_subplots(rows=3, cols=1,specs=[[{"type": "xy"}],[{"type": "domain"}],[{"type": "xy"}]])

    fig.add_trace(
    go.Bar(y=BarQuery['Y'],x=BarQuery['X']),
    row=1, col=1)

    fig.add_trace(
    go.Pie(labels=PieQuery['Lables'], values=PieQuery['Values']),
    row=2, col=1)

    fig.add_trace(
    go.Scatter(x=ScatterResult['X'], y=ScatterResult['Y']),
    row=3, col=1)
    
    print(ScatterResult)
    fig.show()







except cx_Oracle.DatabaseError as e: 
    print("There is a problem with Oracle", e) 
  
finally: 
    if cursor: 
        cursor.close() 
    if con: 
        con.close()