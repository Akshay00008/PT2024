import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote as urlquote
import warnings
warnings.filterwarnings("ignore")
# sql parameters
sql_username="root"
sql_password="Dev123456"
sql_ip="10.1.200.123"
sql_port="3307"

def connect_with_sql(db):
    try:
        connect_query = "mysql+pymysql://"+sql_username+":%s"%urlquote(sql_password)+"@"+sql_ip+":"+sql_port+"/"+'pt_'+db
        engine = create_engine(connect_query)
        # print(engine)
        return  engine
    except:
        raise"Failed to connect"

def read(query,db):
    return pd.read_sql(query, con=connect_with_sql(db))

def write(query):
    with connect_with_sql().connect() as con:
        con.execute(query)
    return "done"