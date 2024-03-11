import pandas as pd
from ..setups.database.mongo import mongo_crud
from ..setups.database.mysql import connect_with_sql
import json

def subassembly(db):
    data = pd.read_sql('select * from subassembly;', con=connect_with_sql(db))
    data.columns = data.columns.str.lower()
    data = data.rename(columns={
        'item5': 'Item5', 
        'item4': 'Item4', 
        'item3': 'Item3', 
        'item2': 'Item2', 
        'item1': 'Item1', 
        'childitem5':'ChildItem5', 'childitem4':'ChildItem4', 'childitem3':'ChildItem3', 'childitem2':'ChildItem2', 'childitem1':'ChildItem1','qpa':'QPA','qoh':'QOH', 'parent': 'Parentitem1'})
    # print(data.columns)
    # return
    data = data.to_json(orient='records')
    dd = mongo_crud('40.81.232.147', 27017, 'pt',
                             'subassembly_{}'.format(db), 'insertmany', json.loads(data))
    return "done"