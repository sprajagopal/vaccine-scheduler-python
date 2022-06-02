import sys
sys.path.append('src/main/scheduler')
from db.ConnectionManager import ConnectionManager
import pymssql
from model.Vaccine import Vaccine

v = Vaccine("test", 10)
v.get()
print(v)

c = CareGiver

# cm = ConnectionManager()
# conn = cm.create_connection()
# cursor = conn.cursor()
# 
# try:
#     cursor.execute(get_all_vaccines)
#     for row in cursor:
#         print(f"name: {str(row['Name'])}, available_doses: {str([row['Doses']])}")
# except pymssql.Error:
#     print('Error occured when getting details from Vaccines')


