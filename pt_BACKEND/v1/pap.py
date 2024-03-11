from flask import Flask,  jsonify, request
from flask_cors import CORS
from internal.summarypage import summarypage_Api
from internal.scenario_manager import scenerioplanner
from internal.qoh_utility import getQOH, updateQOH
from internal.connection_mongo import mongo_crud
import pandas as pd
import json
from datetime import datetime
from internal.updateEngtangled import updateAllEntangled, updateAllEntangledBulk
from internal.forecasting import forecasting_page_based, forecasting_page_basedV2, forecasting_page_search, forecasting_page_searchV2
from internal.database_mysql import read
from internal.summarypageUpdate import summarypageUpdate
import time 

df = summarypage_Api()

uniqueFG = df.parent_item.unique()

sublists = [uniqueFG[x:x+int(len(uniqueFG)/8)] for x in range(0, len(uniqueFG), int(len(uniqueFG)/8))]

def pp(dfx, parent, location, df2x):
    location = location.capitalize()
    for fgs in parent:
        df = dfx[dfx['parent_item'] == fgs]
        for index, row in df.iterrows():
            if row['dateRange'] == 'All':
                print(row['parent_item'])
                dataCheck = mongo_crud(host='40.81.232.147', port=27017, db_name='test', collection_name='fgMasterV2_{}'.format(location),
                                    operation='findone', query={"FG": row['parent_item']}, update={})
                if dataCheck != None:
                    print("Already Exists, Ignoring Insertion")
                else:
                    inX = time.time()
                    df2 = scenerioplanner(row['parent_item'])
                    print("time taken for loading df2 ", time.time() - inX)
                    i = 0
                    itemMaster = []
                    finalPushData = {
                        "FG": row['parent_item'],
                        "total_order_quantity": row['total_order_quantity'],
                        "entaglement":row['entaglement'],
                        "ctb": row['ctb'],
                        "deficient": row['deficient'],
                        "potential_ctb": row['potential_ctb'],
                        "data": []   # FG_Item (concat)
                    }
                    itemsCheck = []
                    for index2, rows in df2.iterrows():
                        print("rows")
                        if rows["item"] not in itemsCheck:
                            itemdata = {
                                "Parentitem": rows["Parentitem"],
                                "Level": 0,
                                "item": rows["item"],
                                "QPA": rows["QPA"],
                                "p_m_t": rows["p_m_t"],
                                "Oper_Num": 0,
                                "Alt_Group": 0,
                                "Alt_Grp_Rnk": 0,
                                "Effect_Date": 0,
                                "OBS_Date": 0,
                                "description": rows["description"],
                                "QOH": rows["QOH"],
                                "inv_ctb": rows["inv_ctb"],
                                "req_ctb": rows["req_ctb"],
                                "deficient_flag": True if rows["deficient_flag"] != 0 else False,
                                "entanglment_flag": True if rows["entanglment_flag"] != 0 else False,
                                "cost_of_part": rows["cost_of_part"],
                                "alternate_flag": True if rows["alternate_flag"] != 0 else False,
                                "altenate_item_allocated_ctb": [],
                                "allocated_item_ctb":0,
                                "total_alt_item_allocated_ctb":0,
                                "total_item_alt_item_allocated_ctb": (rows["entanglment_flag"] == False and rows["deficient_flag"] == False) and rows["req_ctb"] or 0, 
                                "no_conflict": False,
                                "resolved_flag": False,
				"entangled_parent_details": json.loads(rows['entagled_parents_details']),
				"alternate_details":[]
                            }
                            itemMaster.append({
                                "item": rows["item"],
                                "QPA": rows["QPA"],
                                "Alt_Grp_Rnk": 0,
                                "QOH": rows["QOH"],
                                "cost_of_part": rows["cost_of_part"],
                                "oldQOH":0,
                                "newQOH":0,
                                "deltaQOH":0,
                                "totalAvailableParts":rows["QOH"]
                            })

                            finalPushData['data'].append(itemdata)
                    try:
                        res = mongo_crud('40.81.232.147', 27017, 'test',
                                    'fgMasterV2_{}'.format(location), 'create', finalPushData)
                        res = mongo_crud('40.81.232.147', 27017, 'test',
                                    'fgMasterV2_{}backup'.format(location), 'create', finalPushData)
                    except Exception as e:
                        print("error with finalData", finalPushData)
                    print("time taken for fg master ", time.time() - inX)
                    try:
                        res = mongo_crud('40.81.232.147', 27017, 'test',
                                    'itemMaster_{}'.format(location), 'insertmany', itemMaster)
                        res = mongo_crud('40.81.232.147', 27017, 'test',
                                    'itemMaster_{}backup'.format(location), 'insertmany', itemMaster)
                    except Exception as e:
                        print("error with Item Master", itemMaster)
                    print("time taken for item master ", time.time() - inX)

import concurrent.futures
import time
import multiprocessing

# Split the list into 8 sublists
# sublists = [my_list[x:x+int(len(my_list)/8)] for x in range(0, len(my_list), int(len(my_list)/8))]

# Define a function to pass to the multiprocessing.Pool.map() method
def func_wrapper(sublist):
    return pp(df, sublist, 'protec', df)

# Create a multiprocessing pool with 8 processes
pool = multiprocessing.Pool(processes=8)

# Map the func_wrapper function to each sublist in the sublists list using the pool.map() method
results = pool.map(func_wrapper, sublists)

# Close the pool and join the processes
pool.close()
pool.join()

# Print the results
print(results)
