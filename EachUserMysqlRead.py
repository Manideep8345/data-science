import mysql.connector as sql
import pandas as pd
import matplotlib.pyplot as plt
import sys



userName=sys.argv[1]
plotPath=sys.argv[2]

db_connection = sql.connect(database='pb_user_product_task_db', user='root', password='mysql')
db_cursor = db_connection.cursor()
db_cursor.execute('select count(*) from pb_task_pb_user where pb_task_pb_users_id in'
                  '( select distinct(id) FROM pb_task where task_complete_pers<=100)and'
                  ' pb_user_id in(select id from pb_user where first_name="'+userName+'") group by pb_user_id')

db_connection.close()
table_rows = db_cursor.fetchall()
TotalTask = pd.DataFrame(table_rows)
# print TotalTask
db_cursor.execute('select count(*) from pb_task_pb_user where pb_task_pb_users_id in'
                      '( select distinct(id) FROM pb_task where task_complete_pers=100)and '
                      'pb_user_id in(select id from pb_user where first_name="'+userName+'") group by pb_user_id;')
db_connection.close()
table_rows = db_cursor.fetchall()
compleTedTask = pd.DataFrame(table_rows)
# print compleTedTask
db_cursor.execute('select count(*) from pb_task_pb_user where pb_task_pb_users_id in'
                      '( select distinct(id) FROM pb_task where task_complete_pers<100)and '
                      'pb_user_id in(select id from pb_user where first_name="'+userName+'") group by pb_user_id;')
db_connection.close()
table_rows = db_cursor.fetchall()
PendingTask = pd.DataFrame(table_rows)

if(TotalTask.empty):
    sizes = [0,0]
    #fig1, ax1 = plt.subplots()
    plt.title('This User Has No Task')
    plt.pie(sizes)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(plotPath)
    #plt.show()
else:
    # ab=list(compleTedTask[0])
    # ab1=list(PendingTask[0])
    labels1=[]
    # labels1.append(str("Completed"+"("+str(ab[0])+")"))
    # labels1.append(str("Pending"+"("+str(ab1[0])+")"))

    if(compleTedTask.empty):
        complete=0
        labels1.append(str("Completed"+"(0)"))
    else:
        ab=list(compleTedTask[0])
        labels1.append(str("Completed"+"("+str(ab[0])+")"))
        complete=compleTedTask[0]
    if(PendingTask.empty):
        pending=0
        labels1.append(str("Pending"+"(0)"))
    else:
        ab1=list(PendingTask[0])
        labels1.append(str("Pending"+"("+str(ab1[0])+")"))
        pending=PendingTask[0]
    if(TotalTask.empty):
        total=TotalTask[0]
        total=0
    total=TotalTask[0]
    compPer=(complete/total)*100
    pendPer=(pending/total)*100
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Completed', 'Pending'
    # sizes = [15, 30, 45, 10]
    sizes = [compPer,pendPer]
    explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

    #fig1, ax1 = plt.subplots()
    plt.title('Task Reports',y=1.08)
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    shadow=True, startangle=90)
    plt.legend(labels=labels1)
    # ax1.title='Anil'
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #plt.show()
    plt.savefig(plotPath)
