import mysql.connector
from datetime import datetime

def connect_to_database():
    return mysql.connector.connect(user= 'root', password= 'newjeans', host= 'localhost', database= 'sys')

###
### TABLE = node_ifo
###
def systemOn_node_info() : #추가
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f"SELECT * FROM sys.node_info where time = (SELECT max(time) from sys.node_info)"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    return results


def node_info_apply_weight(list_weight) : #성공 
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f'''INSERT INTO node_info (node1_6, node2_7, node3_8, node5_6, node6_1, node6_5, 
    node6_7, node6_11, node7_2, node7_6, node7_8, node7_12, 
    node8_3, node8_7, node8_9, node8_13, node9_8, node10_11, 
    node11_6, node11_10, node11_12, node11_16, node12_7, node12_11, 
    node12_13, node12_17, node13_8, node13_12, node13_14, node13_18, 
    node14_13, node15_16, node16_11, node16_15, node16_17, node16_21, 
    node17_12, node17_16, node17_18, node17_22, node18_13, node18_17, 
    node18_19, node18_23, node19_18, node21_16, node22_19, node23_18)
    VALUES ('{list_weight[0]}', '{list_weight[1]}', '{list_weight[2]}', '{list_weight[3]}', '{list_weight[4]}', '{list_weight[5]}',
    '{list_weight[6]}', '{list_weight[7]}', '{list_weight[8]}', '{list_weight[9]}', '{list_weight[10]}', '{list_weight[11]}',
    '{list_weight[12]}', '{list_weight[13]}', '{list_weight[14]}', '{list_weight[15]}', '{list_weight[16]}', '{list_weight[17]}',
    '{list_weight[18]}', '{list_weight[19]}', '{list_weight[20]}', '{list_weight[21]}', '{list_weight[22]}', '{list_weight[23]}',
    '{list_weight[24]}', '{list_weight[25]}', '{list_weight[26]}', '{list_weight[27]}', '{list_weight[28]}', '{list_weight[29]}',
    '{list_weight[30]}', '{list_weight[31]}', '{list_weight[32]}', '{list_weight[33]}', '{list_weight[34]}', '{list_weight[35]}',
    '{list_weight[36]}', '{list_weight[37]}', '{list_weight[38]}', '{list_weight[39]}', '{list_weight[40]}', '{list_weight[41]}',
    '{list_weight[42]}', '{list_weight[43]}', '{list_weight[44]}', '{list_weight[45]}', '{list_weight[46]}', '{list_weight[47]}')
    '''
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


###
### TABLE = m_info
###
# 모빌리티 정보 가지고 오기 
def m_info() : #성공 
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = 'SELECT * FROM m_info'
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    return results

# 임무를 할당받은 모빌리티 상태 변경 및 시작점, 도착점 변경 
def m_info_assignment(M_name, departure, destination) : #성공 작동 중 : work 미작동 중 : idle 고장 : not 
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f"UPDATE m_info SET departure = '{departure}', destination = '{destination}', M_status = 'work' WHERE (`M_name` = '{M_name}')"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

# 임무를 완료하였을 때
def m_info_finish(M_name) : #성공
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f"UPDATE m_info SET departure = NULL, M_status = 'idle' WHERE (`M_name` = '{M_name}')"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()
    
# 임무 중 고장났을 때


###
### TABLE = path
###
def path_info(M_name):
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f"SELECT path FROM path where M_name = '{M_name}'"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
        # Check if any results are returned
    if results:
        # Modify the result format
        modified_results = [(result[0],) for result in results]
        return modified_results[0][0].split(' ')
    else:
        return results[0][0].split(' ')

def on_path(M_name, path) : #성공
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f"UPDATE path SET path = '{path}' WHERE M_name = '{M_name}'"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

    
#임무를 끝낸 시호를 받으면 테이블에서 정보를 삭제 
def del_path(M_name) : #성공
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f"UPDATE path SET path = NULL WHERE M_name = '{M_name}'"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

###
### TABLE = action
###
def action_info(M_name):
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f"SELECT action FROM action where M_name = '{M_name}'"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Check if any results are returned
    if results:
        # Modify the result format
        modified_results = [(result[0],) for result in results]
        return modified_results[0][0].split(' ')
    else:
        return results[0][0].split(' ')

def on_action(M_name, action) : #성공
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f"UPDATE action SET action = '{action}' WHERE M_name = '{M_name}'"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def del_action(M_name) : #성공
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f"UPDATE action SET action = NULL WHERE M_name = '{M_name}'"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

###
### TABLE = comeinout
###
def on_comeinout(M_name, comeout, comein) : #성공
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f"UPDATE comeinout SET comeOut = '{comeout}', comeIn = '{comein}' WHERE M_name = '{M_name}'"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def del_comeinout(M_name) : #성공
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = f"DELETE FROM comeinout WHERE M_name = '{M_name}'"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()




