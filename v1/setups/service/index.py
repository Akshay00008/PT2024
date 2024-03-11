from ...utilities.summaryPage import summaryPage
from ...utilities.scenarioPlanner import scenarioPlanner
from ..database.mongo import mongo_crud
from ...utilities.subAssembly import subassembly
from ..database.mysql import read
import pandas as pd
import json
from datetime import datetime


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
        mongo_crud('40.81.232.147', 27017, 'pt',
                   'fgMasterV2_{}'.format(location), 'drop')
        mongo_crud('40.81.232.147', 27017, 'pt',
                   'summaryMaster_{}'.format(location), 'drop')
        mongo_crud('40.81.232.147', 27017, 'pt',
                   'itemMaster_{}'.format(location), 'drop')
        mongo_crud('40.81.232.147', 27017, 'pt',
                   'subassembly_{}'.format(location), 'drop')
        
        summaryPageObj = summaryPage(location)
        df = summaryPageObj.summarypage_Api()
        scenario_item = ''' SELECT * FROM Scenario_Page_Useable;'''
        scenarioAllItem=read(scenario_item,location)
        itemCheck = []
        for index, row in df.iterrows():
            if row['dateRange'] == 'All':
                print(row['parent_item'])
                dataCheck = mongo_crud(host='40.81.232.147', port=27017, db_name='pt', collection_name='fgMasterV2_{}'.format(location),
                                    operation='findone', query={"FG": row['parent_item']}, update={})
                if dataCheck != None:
                    print("Already Exists, Ignoring Insertion")
                else:
                    scenarioPlannerObj = scenarioPlanner(location, scenarioAllItem, row['parent_item'])
                    df2 = scenarioPlannerObj.scenerioplanner()
                    itemMaster = []
                    finalPushData = {
                        "FG": row['parent_item'],
                        "total_order_quantity": row['total_order_quantity'],
                        "entaglement": row['entaglement'],
                        "ctb": row['ctb'],
                        "deficient": row['deficient'],
                        "potential_ctb": row['potential_ctb'],
                        "data": []
                    }
                    for index2, rows in df2.iterrows():
                        itemdata = {
                            "Parentitem": rows["Parentitem"],
                            "Level": rows["Level"],
                            "item": rows["item"],
                            "QPA": rows["QPA"],
                            "p_m_t": rows["p_m_t"],
                            "Oper_Num": rows["Oper_Num"],
                            "Alt_Group": rows["Alt_Group"],
                            "Alt_Grp_Rnk": rows["Alt_Grp_Rnk"],
                            "Effect_Date": ETL.date_to_milliseconds(rows["Effect_Date"]),
                            "OBS_Date": ETL.date_to_milliseconds(rows["OBS_Date"]),
                            "description": rows["description"],
                            "QOH": rows["QOH"],
                            "inv_ctb": rows["inv_ctb"],
                            "req_ctb": rows["req_ctb"],
                            "deficient_flag": True if rows["deficient_flag"] != 0 else False,
                            "entanglment_flag": True if rows["entanglment_flag"] != 0 else False,
                            "cost_of_part": rows["cost_of_part"],
                            "alternate_flag": True if rows["alternate_flag"] != 0 else False,
                            "altenate_item_allocated_ctb": [],
                            "allocated_item_ctb": 0,
                            "total_alt_item_allocated_ctb": 0,
                            "total_item_alt_item_allocated_ctb": (rows["entanglment_flag"] == False and rows["deficient_flag"] == False) and rows["req_ctb"] or 0,
                            "no_conflict": False,
                            "resolved_flag": False
                        }
                        if rows["item"] not in itemCheck:
                            itemCheck.append(rows["item"])
                            itemMaster.append({
                                "item": rows["item"],
                                "QPA": rows["QPA"],
                                "Alt_Grp_Rnk": rows["Alt_Grp_Rnk"],
                                "QOH": rows["QOH"],
                                "cost_of_part": rows["cost_of_part"],
                                "oldQOH": 0,
                                "newQOH": 0,
                                "deltaQOH": 0,
                                "totalAvailableParts": rows["QOH"]
                            })

                        tojsonData = json.loads(rows['entagled_parents_details'])
                        entData = []
                        for x in tojsonData:
                            entMas = df[df['parent_item'] == x['entagled_parents']]
                            if entMas.empty == True :
                                print("Entanglement Is Empty")
                            else:
                                entData.append({
                                    "FG": x['entagled_parents'],
                                    "req_ctb": x['req_ctb'],
                                    "qpa":x['qpa'],
                                    "allocated_qty": x['allocated_qty'],
                                    "ctb_qoh": x['ctb_qoh'],
                                    "ctb":float(entMas["ctb"].iloc[0]),
                                    "potential_ctb":float(entMas["potential_ctb"].iloc[0])
                                })
                        tojsonData = json.loads(rows['alternate_details'])
                        altData = []
                        for x in tojsonData:
                            altData.append(x['alternate_parents'])
                        itemdata['entagled_parents_details'] = entData
                        itemdata['alternate_details'] = altData
                        finalPushData['data'].append(itemdata)
                    try:
                        res = mongo_crud('40.81.232.147', 27017, 'pt',
                                    'fgMasterV2_{}'.format(location), 'create', finalPushData)
                    except Exception as e:
                        print("error with finalData", finalPushData)
                    
                    try:
                        res = mongo_crud('40.81.232.147', 27017, 'pt',
                                    'itemMaster_{}'.format(location), 'insertmany', itemMaster)
                    except Exception as e:
                        print("error with Item Master", e)

        df['lastUpdated'] = str(datetime.now()).split('.')[0]
        data = df.to_json(orient='records')
        data = pd.read_json(data)
        records = data.to_dict('records')
        mongo_crud('40.81.232.147', 27017, 'pt',
                   'summaryMaster_{}'.format(location), 'insertmany', records)

        subassembly(location)

        return "Service Run Completed For {}".format(location)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("Service Run Completed For {}".format(self.location))