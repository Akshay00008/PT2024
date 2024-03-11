from ...utilities.summaryPage import summaryPage
from ...utilities.scenarioPlanner import scenarioPlanner
from ..database.mongo import mongo_crud
from ...utilities.subAssembly import subassembly
from ..database.mysql import read
from ...utilities.subAssemblyHierarchy import createHierarchy
import pandas as pd
import json
from datetime import datetime
import concurrent.futures
import time
import multiprocessing

def func_wrapperProtec(args):
    sublist, df, scenarioAllItem = args
    return dataMaker(df, sublist, 'Protec', df, scenarioAllItem)

def func_wrapperAmery(args):
    sublist, df, scenarioAllItem = args
    return dataMaker(df, sublist, 'Amery', df, scenarioAllItem)

def dataMaker(dfx, parent, location, df2x, scenarioAllItem):
    location = location.capitalize()
    for fgs in parent:
        df = dfx[dfx['parent_item'] == fgs]
        for index, row in df.iterrows():
            if row['dateRange'] == 'All':
                print(row['parent_item'])
                dataCheck = mongo_crud(host='40.81.232.147', port=27017, db_name='pt', collection_name='fgMasterV2_{}'.format(location),
                                operation='findone', query={"FG": row['parent_item']}, update={})
                if dataCheck != None:
                    print("Already Exists, Ignoring Insertion")
                else:
                    # Alternate_item='''SELECT * FROM pt_Protec.Alternates_table'''
                    # alternateData=read(Alternate_item,location)
                    try:
                      scenarioPlannerObj = scenarioPlanner(location, scenarioAllItem, row['parent_item'], [])
                      df2 = scenarioPlannerObj.scenerioplanner()
  
                      finalPushData = {
                          "FG": row['parent_item'],
                          "total_order_quantity": row['total_order_quantity'],
                          "entaglement": row['entaglement'],
                          "ctb": row['ctb'],
                          "deficient": row['deficient'],
                          "potential_ctb": row['potential_ctb'],
                          "data": df2['itemdata'],
                          "ctbArr": df2['ctb'],
                          "entArr": df2['entangled'],
                          "defArr": df2["deficient"],
                          "unresolvedArr": df2['unresolved']
                      }
                      
                      try:
                          finalPushData = json.dumps(finalPushData,default=str)
                          finalPushData = json.loads(finalPushData)
                          res = mongo_crud('', 0, 'pt',
                                      'fgMasterV2_{}'.format(location), 'create', finalPushData)
                          res = mongo_crud('', 0, 'pt',
                                      'fgMasterV2_{}backup'.format(location), 'create', finalPushData)
                      except Exception as e:
                          print("error with finalData",len(df2), e)
                      
                      try:
                          finalPushData = json.dumps(df2['itemMaster'],default=str)
                          finalPushData = json.loads(finalPushData)
                          res = mongo_crud('', 0, 'pt',
                                      'itemMaster_{}'.format(location), 'insertmany', finalPushData)
                          res = mongo_crud('', 0, 'pt',
                                      'itemMaster_{}backup'.format(location), 'insertmany', finalPushData)
                      except Exception as e:
                          print(e)
                    except:
                      print("X")


class ETL:
    def __init__(self, location):
        self.location = location.capitalize()

    @staticmethod
    def date_to_milliseconds(date):
        if date == None:
            return -19800000
        d = datetime.combine(date, datetime.min.time())
        return int(d.timestamp() * 1000)    

    def __enter__(self):
        location = self.location
        mongo_crud('', 0, 'pt',
                   'fgMasterV2_{}'.format(location), 'drop')
        mongo_crud('', 0, 'pt',
                   'summaryMaster_{}'.format(location), 'drop')
        mongo_crud('', 0, 'pt',
                   'itemMaster_{}'.format(location), 'drop')
        mongo_crud('', 0, 'pt',
                   'fgMasterV2_{}backup'.format(location), 'drop')
        mongo_crud('', 0, 'pt',
                   'summaryMaster_{}backup'.format(location), 'drop')
        mongo_crud('', 0, 'pt',
                   'itemMaster_{}backup'.format(location), 'drop')
        
        summaryPageObj = summaryPage(location)
        print("summarypage")
        df = summaryPageObj.summarypage_Api()

        scenario_item = ''' SELECT * FROM Scenario_Page_Useable_new;'''
        scenarioAllItem=read(scenario_item,location)

        # get all distinct FGs
        uniqueFG = df.parent_item.unique()

        print(uniqueFG)

        # create sublist
        sublists = [uniqueFG[x:x+int(len(uniqueFG)/8)] for x in range(0, len(uniqueFG), int(len(uniqueFG)/8))]


        pool = multiprocessing.Pool(processes=8)

        # Map the func_wrapper function to each sublist in the sublists list using the pool.map() method
        arg_list = [(sublist, df, scenarioAllItem) for sublist in sublists]
        if location == 'Amery':
            results = pool.map(func_wrapperAmery, arg_list)
        elif location == 'Protec':
            results = pool.map(func_wrapperProtec, arg_list)

        # Close the pool and join the processes
        pool.close()
        pool.join()

        # Print the results
        print(results)
                    
        df['lastUpdated'] = str(datetime.now()).split('.')[0]
        data = df.to_json(orient='records')
        data = pd.read_json(data)
        records = data.to_dict('records')
        mongo_crud('', 0, 'pt',
                   'summaryMaster_{}'.format(location), 'insertmany', records)

        # subassembly(location)

        return "Service Run Completed For {}".format(location)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("Service Run Completed For {}".format(self.location))