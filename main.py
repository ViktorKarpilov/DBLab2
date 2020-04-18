# importing module 
import cx_Oracle  
  
  
# Create a table in Oracle database 
try: 
  
    con = cx_Oracle.connect('viktor/Password@localhost') 
      
    # Now execute the sqlquery 
    cursor = con.cursor() 


    print("First query")
    # Creating a table srollno heading which is number 
    cursor.execute("""SELECT incedents.CITY,incedents.severity, Count(*) as NumberOfHardIncedents
                        from INCEDENTS 
                        group by (incedents.CITY,incedents.severity)
                        having incedents.severity > 2""") 

    for result in cursor:
        print(result)
                      
    print("Successful\n")
    print("Second query")
    cursor.execute("""SELECT incedents.CITY, ROUND(Count(*)/(select count(ID) from incedents),2)*100||'%' as PrecentOfAll
                    from INCEDENTS 
                    group by (incedents.CITY)""")
    for result in cursor:
        print(result)
    print("Successful\n")
    print("Third query")
    cursor.execute("""SELECT to_char(STARTTIME, 'DD.MM.YYYY') as IncedentsDate,count(*) as Incedents
                    from INCEDENTS
                    GROUP BY (to_char(STARTTIME, 'DD.MM.YYYY'))
                    ORDER BY (to_char(STARTTIME, 'DD.MM.YYYY'))""")

    for result in cursor:
        print(result)
    print("Successful\n")




      
except cx_Oracle.DatabaseError as e: 
    print("There is a problem with Oracle", e) 
  
# by writing finally if any error occurs 
# then also we can close the all database operation 
finally: 
    if cursor: 
        cursor.close() 
    if con: 
        con.close() 