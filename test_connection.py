import sys
sys.path.append('src/main/scheduler')
from db.ConnectionManager import ConnectionManager
import pymssql
from model.Vaccine import get_all_available_vaccines

print(get_all_available_vaccines())

