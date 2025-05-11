import mysql.connector
import sys
try:
    global con
    con=mysql.connector.connect(host='localhost',
                            user='root',
                            password='',
                            database='sales_management_db')
except:
    print('>>>>>>>>>>>',sys.exc_info()[0],'>>>>>>>>>>>')

def run_query(query='select * from users',data_to_insert=None, update_to_db=False, reterival_id=None,
              reterver_table_name='users'):
    table = con.cursor()
    result_set = None
    updated_user_details = None
    print(data_to_insert)
    if data_to_insert != None:    
        table.execute(query,data_to_insert)
        con.commit()
    elif update_to_db:
        table.execute(query)
        con.commit()
        if reterival_id:
            table.execute(f'select * from {reterver_table_name} where id={reterival_id}')
            updated_user_details = table.fetchall()
        return updated_user_details
    else:
        table.execute(query)
        result_set = table.fetchall()
    return result_set

