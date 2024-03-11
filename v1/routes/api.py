from flask import jsonify, request
from ..setups.database.mongo import mongo_crud
from ..utilities.entangledUpdateV2 import updateAllEntangled
from ..utilities.summaryPageUpdateV2 import summarypageUpdate
from ..utilities.forecastAllPagedData import paged_data, search, plan_code, deficients_item, deficients_plan, manufactured_item, Purchased_order,all,plan_code_M,plan_code_P,deficients_plan_P,deficients_plan_M,deficients_item_P,deficients_item_M
from ..setups.database.mysql import connect_with_sql, read
from ..utilities.arryToJSON import arrToJ
from datetime import datetime
import pandas as pd
import numpy as np
import math

globalUserList = {}
globalItemList = []
previousCTB = {}

def find_indices_of_ones(array):
    return [i for i, value in enumerate(array) if value == 1]

def makeDataReverse(data):
    x = []
    for i in data.keys():
        y = {
            "FG":data[i]["FG"],
            "req_ctb":data[i]["req_ctb"],
            "qpa":data[i]["qpa"],
            "allocated_qty":data[i]["allocated_qty"],
            "ctb_qoh":data[i]["ctb_qoh"],
            "ctb":data[i]["ctb"],
            "potential_ctb":data[i]["potential_ctb"],
        }
        x.append(y)
    return x

def makeData(data,item,fg):
    x = {}
    for i in data:
        x.update({
            "{}_{}_{}".format(fg,item,i):{
                "FG":i["FG"],
                "req_ctb":i["req_ctb"],
                "qpa":i["qpa"],
                "allocated_qty":i["allocated_qty"],
                "ctb_qoh":i["ctb_qoh"],
                "ctb":i["ctb"],
                "potential_ctb":i["potential_ctb"],
            }
        })
    return x

def login():
    username = request.json['username']
    password = request.json['password']
    userData = mongo_crud('','','pt','users','read',{'username': username},{})
    print(userData)
    if len(userData) == 0:
        return {"msg": "User Doesn't Exists", "data": []}
    elif userData[0]['password'] == password:
        data1 = mongo_crud('','','pt','filter','read',{'user': username},{})
        data2 = mongo_crud('','','pt','users','findone',{'username': username},{})
        del data2['_id']
        for x in data1:
            del x['_id']
        return jsonify({"msg": "Logged In Successfully", "data":{"filterData": data1, "userData": data2}})
    else:
        return {"msg": "Wrong Creds Given", "data":[]}


def summaryPageData(location, dateRange):
    location = location.capitalize()
    productCode = request.json['productCode']
    dd = mongo_crud(host='40.81.232.147', port=27017, db_name='pt',
                    collection_name='summaryMaster_{}'.format(location), operation='readV2', query=[{"dateRange": dateRange, "product_code": {"$in": productCode}}, {"_id": 0}], update={})

    return jsonify(dd)


# def senarioPlannerData(location,pageNumber):
def senarioPlannerData(location):
    # start = 0 if int(pageNumber) == 1 else (int(pageNumber)*10) - 9
    # stop = int(pageNumber) * 10
    location = location.capitalize()
    Parentitem = request.json["Parentitem"]
    entFlag = request.json['entFlag']
    defFlag = request.json['defFlag']
    resFlag = request.json['resFlag']
    plannerCode = request.json['plannerCode']
    filterFlag = request.json['filterFlag']
    
    dd = mongo_crud(host='40.81.232.147', port=27017, db_name='pt',
                    collection_name='fgMasterV2_{}'.format(location), operation='findone', query={"FG": Parentitem}, update={})
    dd2 = mongo_crud(host='40.81.232.147', port=27017, db_name='pt',
                     collection_name='itemMaster_{}'.format(location), operation='read', query={}, update={})
    if dd != None:
        parts = []
        for i in dd['data'].keys():
            # print(i)
            if Parentitem in i:
                # print(i)
                # print(dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Plan_Code"])
                # if(dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["index"] >= start and dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["index"] <= stop):
                if dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Plan_Code"] in plannerCode:
                    print("in planner code")
                    if filterFlag == True:
                        if dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["deficient_flag"] == defFlag and dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["entanglment_flag"] == entFlag and dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["resolved_flag"] == resFlag:
                            itemQOH = [item for item in dd2 if item["item"] == dd['data']
                                    ['{}_{}'.format(Parentitem, i.split('_')[1])]["item"]]
                            parts.append({
                                "Parentitem": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Parentitem"],
                                "Level": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Level"],
                                "item": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["item"],
                                "index": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["index"],
                                "QPA": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["QPA"],
                                "p_m_t": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["p_m_t"],
                                "Oper_Num": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Oper_Num"],
                                "Alt_Group": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Alt_Group"],
                                "Alt_Grp_Rnk": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Alt_Grp_Rnk"],
                                "description": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["description"],
                                "resolved_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["resolved_flag"],
                                "QOH": itemQOH[0]['QOH'],
                                "totalAvailableParts": itemQOH[0]['totalAvailableParts'],
                                "inv_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["allocated_item_ctb"],
                                "req_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["req_ctb"],
                                "deficient_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["deficient_flag"],
                                "entanglment_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["entanglment_flag"],
                                "Plan_Code": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Plan_Code"],
                                "alternate_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["alternate_flag"],
                                "parent_ctb": int(dd["ctb"]) < 0 and 0 or int(dd["ctb"]),
                                "parent_potential_ctb": int(dd["potential_ctb"]) < 0 and 0 or int(dd["potential_ctb"]),
                                "allocated_item_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["allocated_item_ctb"],
                                "total_alt_item_allocated_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["total_alt_item_allocated_ctb"],
                                "total_item_alt_item_allocated_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["total_item_alt_item_allocated_ctb"]
                            })
                    elif filterFlag == False:
                        if dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["deficient_flag"] == True or dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["entanglment_flag"] == True:
                            itemQOH = [item for item in dd2 if item["item"] == dd['data']
                                    ['{}_{}'.format(Parentitem, i.split('_')[1])]["item"]]
                            parts.append({
                                "Parentitem": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Parentitem"],
                                "Level": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Level"],
                                "item": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["item"],
                                "index": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["index"],
                                "QPA": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["QPA"],
                                "p_m_t": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["p_m_t"],
                                "Oper_Num": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Oper_Num"],
                                "Alt_Group": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Alt_Group"],
                                "Alt_Grp_Rnk": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Alt_Grp_Rnk"],
                                "description": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["description"],
                                "resolved_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["resolved_flag"],
                                "QOH": itemQOH[0]['QOH'],
                                "totalAvailableParts": itemQOH[0]['totalAvailableParts'],
                                "inv_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["allocated_item_ctb"],
                                "req_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["req_ctb"],
                                "deficient_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["deficient_flag"],
                                "entanglment_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["entanglment_flag"],
                                "Plan_Code": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Plan_Code"],
                                "alternate_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["alternate_flag"],
                                "parent_ctb": int(dd["ctb"]) < 0 and 0 or int(dd["ctb"]),
                                "parent_potential_ctb": int(dd["potential_ctb"]) < 0 and 0 or int(dd["potential_ctb"]),
                                "allocated_item_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["allocated_item_ctb"],
                                "total_alt_item_allocated_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["total_alt_item_allocated_ctb"],
                                "total_item_alt_item_allocated_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["total_item_alt_item_allocated_ctb"]
                            })
                    else:
                        print("Not Deficient and Not Entangled")
                # else:
                #     print("Not in paginated range")
        return jsonify(parts)
    return []


def alternateEntangled(location, user):
    print("alternate entangled")
    location = location.capitalize()
    FG, item = request.json['FG'], request.json['item']

    if item in globalItemList and globalUserList[item] != user:
        return {"alternate_details": [], "entagled_parents_details": [], "data": [], "msg": "{} is already making some changes in {}".format(globalUserList[item], item)}
    else:
        globalUserList.update({item: user})
        globalItemList.append(item)

    dd = mongo_crud(host='40.81.232.147', port=27017, db_name='pt',
                    collection_name='fgMasterV2_{}'.format(location), operation='findone', query={"FG": FG, "data.{}_{}.item".format(FG, item): item}, update={})
    print(dd,"DATA")

    parts = ''

    # indexesEnt = dd['entArr']
    # indexesDef = dd['defArr']

    finalData = []
    
    if dd != None:
        entPartsFinal = []
        entParts = dd['data']['{}_{}'.format(
            FG, item)]['entagled_parents_details']
        print(len(entParts.keys()),"KEYS LENGHT")
        for entitems in entParts.keys():
            # entmongo = mongo_crud(host='40.81.232.147', port=27017, db_name='pt', collection_name='summaryMaster_{}'.format(
            #     location), operation='read', query={"parent_item": entitems.split('_')[2]}, update={})
            # if (len(entmongo) > 0):
            # try:
            #     print(entParts[entitems]["req_ctb"].dtype,"search NAN")
            #     print(entParts[entitems]["req_ctb"],"search NAN2")
            # except:
            #     pass
            entPartsFinal.append({
                "FG": entParts[entitems]['FG'],
                "req_ctb": entParts[entitems]["req_ctb"] if entParts[entitems]["req_ctb"] is not np.nan or math.isnan(entParts[entitems]["req_ctb"]) == True else 0,
                "qpa": entParts[entitems]['qpa'],
                "allocated_qty": entParts[entitems]['allocated_qty'],
                "ctb_qoh": entParts[entitems]['ctb_qoh'],
                "ctb": entParts[entitems]['ctb'],
                "potential_ctb": entParts[entitems]['potential_ctb']
            })
            print(entPartsFinal,"ENt FINAL")
        altParts = dd['data']['{}_{}'.format(FG, item)]['alternate_details']

        parts = {
            "entagled_parents_details": entPartsFinal,
            "alternate_details": altParts
        }

        finalData = parts

    return jsonify(finalData)


def updateDocuments(location, user):
    location = location.capitalize()
    item_QOH, FG_item = request.json['item_QOH'], request.json['FG_item']
    item = item_QOH["item"]
    QOH = item_QOH["QOH"]
    oldQOH = item_QOH["oldQOH"]
    newQOH = item_QOH["newQOH"]
    deltaQOH = item_QOH["deltaQOH"]
    index = FG_item['index']

    summaryPageDataUpdate = request.json['summary']

    if globalUserList[item] == user:
        print("Same User")
    else:
        return {"type": "error", "msg": "{} is already making some changes in {}".format(globalUserList[item], item)}

    update_operations = {
        "$set": {
            "QOH": QOH,
            "oldQOH": oldQOH,
            "newQOH": newQOH,
            "deltaQOH": deltaQOH
        }
    }

    mongo_crud(host='40.81.232.147', port=27017, db_name='pt',
                    collection_name='itemMaster_{}'.format(location), operation='updatemany', query={"item": item}, update=update_operations)

    x = {
        "Alt_Group": FG_item["Alt_Group"],
        "Alt_Grp_Rnk": FG_item["Alt_Grp_Rnk"],
        "Level": FG_item["Level"],
        "Oper_Num": FG_item["Oper_Num"],
        "Parentitem": FG_item["Parentitem"],
        "QOH": FG_item["QOH"],
        "QPA": FG_item["QPA"],
        "allocated_item_ctb": FG_item["allocated_item_ctb"],
        "alternate_flag": FG_item["alternate_flag"],
        "deficient_flag": FG_item["deficient_flag"],
        "description": FG_item["description"],
        "entanglment_flag": FG_item["entanglment_flag"],
        "resolved_flag": FG_item["resolved_flag"],
        "inv_ctb": FG_item["inv_ctb"],
        "item": FG_item["item"],
        "index": FG_item["index"],
        "p_m_t": FG_item["p_m_t"],
        "parent_ctb": FG_item["parent_ctb"],
        "parent_potential_ctb": FG_item["parent_potential_ctb"],
        "req_ctb": FG_item["req_ctb"],
        "total_alt_item_allocated_ctb": FG_item["total_alt_item_allocated_ctb"],
        "total_item_alt_item_allocated_ctb": FG_item["total_item_alt_item_allocated_ctb"],
        "alternate_details": FG_item["alternate_details"],
        "entagled_parents_details": makeData(FG_item["entagled_parents_details"],FG_item["item"],FG_item["Parentitem"])
    }

    update_operations = {
        "$set": {
            "ctbArr.{}".format(index): int(FG_item["allocated_item_ctb"]),
            "defArr.{}".format(index): 0 if FG_item["resolved_flag"] == True else 1,
            "entArr.{}".format(index): 0 if FG_item["resolved_flag"] == True else 1,
            "data.{}_{}".format(FG_item["Parentitem"], FG_item["item"]): x
        }
    }

    mongo_crud(host='40.81.232.147', port=27017, db_name='pt',
                    collection_name='fgMasterV2_{}'.format(location), operation='updatemany', query={"FG": FG_item['Parentitem']}, update=update_operations)

    # print(len(FG_item['entagled_parents_details']))
    # print(FG_item['entagled_parents_details'])
    if len(FG_item['entagled_parents_details']) > 0:
        summaryFGParam = updateAllEntangled(FG_item["entagled_parents_details"],
                        mongo_crud, FG_item['Parentitem'], item, FG_item, location)
    else:
        summaryFGParam = [FG_item['Parentitem']]

    calculatedPreviousCtb = summarypageUpdate(
        mongo_crud, FG_item['Parentitem'], location, summaryPageDataUpdate, summaryFGParam)

    previousCTB.update({"{}".format(FG_item['Parentitem']):calculatedPreviousCtb})

    try:
        while True:
            globalItemList.remove(item)
    except ValueError:
        pass

    del globalUserList[item]
    
    return {"type": "success", "msg": "updated"}


def forecastAll(location, page_number, page_size,):
    location = location.capitalize()
    productCode = request.json['productCode']
    planner_code = request.json.get('planner_code')
    def_flag = request.json.get('def_flag')
    PO_code=request.json.get('PO_code')
    Make_code=request.json.get('Make_code')
    
    if PO_code == 'P' and len(planner_code)==0:
        df = Purchased_order(location, page_number, page_size,PO_code)
        
    if Make_code == 'M' and len(planner_code)==0:
        df = manufactured_item(location, page_number, page_size,Make_code)
        
    if Make_code == 'M' and PO_code == 'P' :
        df = all(location, page_number, page_size,PO_code,Make_code)
    
    if def_flag == 1 and len(planner_code)==0:
        val='deficient'
        df = deficients_item(location,page_number,page_size,val)
        
        
    if def_flag == 1 and len(planner_code)==0 and PO_code=='P':
        val='deficient'
        df = deficients_item_P(location,page_number, page_size,val,PO_code)
        
    if def_flag == 1 and len(planner_code)==0 and Make_code=='M' :
        val='deficient'
        df = deficients_item_M(location,page_number, page_size,val,Make_code)
    
   
        
    if def_flag == 1 and len(planner_code)>0 and PO_code =='P':
        val='deficient'
        df=deficients_plan_P(location,page_number, page_size,val,planner_code,PO_code)
        
    if def_flag == 1 and len(planner_code)>0 and Make_code =='M':
        val='deficient'
        df=deficients_plan_M(location,page_number, page_size,val,planner_code,Make_code)
        
        
    if def_flag == 1 and len(planner_code)>0:
        val='deficient'
        df=deficients_plan(location,page_number, page_size,val,planner_code)
        
        
    if len(planner_code) > 0 and def_flag==0 :
        df = plan_code(location, page_number, page_size, planner_code)
        
    elif def_flag == 0 and len(planner_code)==0 and Make_code!='M' and PO_code!='P':
        df = paged_data(location, page_number, page_size, productCode)
    
    if len(planner_code) > 0 and def_flag==0 and PO_code =='P':
        df = plan_code_P(location, page_number, page_size, planner_code,PO_code)
        
    if len(planner_code) > 0 and def_flag==0 and Make_code =='M':
        df = plan_code_M(location, page_number, page_size, planner_code,Make_code)
    return df 

def fg_item(location):
    location = location.capitalize()
    item = request.json['item']
    
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.Parent_fg where item = '{}' ;".format(item)
        
    
    else :
        
        query = "SELECT * FROM pt_Amery.Parent_fg where item = '{}' ;".format(item)
        
    
    df = pd.read_sql(query, con=connect_with_sql(location))
    json_data = df.to_json(orient='records')

    return json_data
    

def forecastSearch(location, searchVal):
    location = location.capitalize()
    df = search(searchVal, location)
    return df

def forecastplanner_code(location, page_number, page_size):
    location = location.capitalize()
    planner_code = request.json.get('planner_code')
    df = plan_code(location, page_number, page_size, planner_code)
    return df

def deficient(location,page_number, page_size, val):
    location = location.capitalize()
    df = deficients_item(location, page_number, page_size,val)
    return df



def forecastSearch(location, searchVal):
    location = location.capitalize()
    df = search(searchVal, location)
    return df


def subassemblyInitial(location, parent, child):
    location = location.capitalize()

    allFGs = request.json['productCode']

    accessFGs = mongo_crud('',0,'test','summaryMaster_{}'.format(location), 'read',  { "product_code": { "$in": allFGs }}, {})

    productCodeArr = []
    for x in accessFGs:
        productCodeArr.append(x['parent_item']) if x['parent_item'] not in productCodeArr else print("non duplicate")

    # return ""

    res = []

    
    data = read("SELECT Parentitem, QPA FROM pt_{}.flatbom_data where Item = '{}';".format(location,child), location)
    return data.reset_index().to_json(orient='records')


def subassemblyFinal(location, parent, child):
    location = location.capitalize()
    prentNew = parent
    data = mongo_crud(host='40.81.232.147', port=27017, db_name='pt',
                      collection_name='subassemblyV4_{}'.format(location), operation='read', query={"item": parent}, update={})

    resp = {}

    if len(data) > 0:
        del data[0]['_id']
        resp = {
            "data": data[0] if len(data) > 0 else [],
            "itemQOH": mongo_crud('',0,'pt', 'itemMaster_{}'.format(location),'findone',{"item": child})['QOH']
        }
    
    return resp


def saveSnap(location, user):
    print(previousCTB)
    print(request.json['FGs'],"DATA")
    if len(request.json['FGs']) == 0:
        print(request.json['FGs'],"DATA PRINT")
        return "Check With Allocation If Lock Button Is Pressed"
    try:
        location = location.capitalize()
        FGs = request.json['FGs']
        for fg in FGs:
            existing_snap_data = mongo_crud('40.81.232.147', 27017, 'pt', 'snap_{}'.format(location), 'read', {'FG': fg}, {})
            print(existing_snap_data)
            if existing_snap_data:
                mongo_crud('40.81.232.147', 27017, 'pt', 'snap_{}'.format(location), 'delete', {'FG': fg}, {})
            
            summaryData = mongo_crud(host='40.81.232.147', port=27017, db_name='pt',
                            collection_name='summaryMaster_{}'.format(location), operation='findone', query={"parent_item": fg}, update={})
            combinationData = mongo_crud(host='40.81.232.147', port=27017, db_name='pt',
                            collection_name='fgMasterV2_{}'.format(location), operation='findone', query={"FG": fg}, update={})
            
            del summaryData['_id']
            del combinationData['_id']
            snapData = {
                "parent_item" : summaryData['parent_item'],
                "deficient" : summaryData['deficient'],
                "potential_ctb" : summaryData['potential_ctb'],
                "entaglement" : summaryData['entaglement'],
                "total_order_quantity" : summaryData['total_order_quantity'],
                "ctb" : summaryData['ctb'],
                "Quantity_yet_to_make": summaryData['Quantity_yet_to_make'],
                "description" : summaryData['description'],
                "product_code" : summaryData['product_code'],
                "dateRange" : summaryData['dateRange'],
                "lastUpdated" : summaryData['lastUpdated'],
                "scenarioPage": combinationData,
                "user": user,
                "timestamp": str(datetime.now()),
                "FG": fg,
                "previousCTB": previousCTB.get(fg,0)
            }

            mongo_crud('40.81.232.147',27017,'pt','snap_{}'.format(location),'create',snapData)

        return "Scenario Saved"
    except Exception as e:
        print(e,"EXCEPTION")
        return "Check With Allocation If Lock Button Is Pressed, EXCEPTION {}".format(str(previousCTB))


def saveFilter(location, user):
    filter_data = {
        "createdAt": str(datetime.now()),
        "productCode": request.json['productCode'],
        "days": request.json['days'],
        "user": user,
        "filterName": request.json['filterName'],
        "modifiedAt": str(datetime.now()),
        "location": location.capitalize()
    }

    existing_filter_data = mongo_crud('40.81.232.147', 27017, 'pt', 'filter', 'read', {
                                      'user': user, 'filterName': request.json['filterName'], 'location': location.capitalize()})
    if len(existing_filter_data) != 0:
        mongo_crud('40.81.232.147', 27017, 'pt', 'filter', 'updatemany', {'user': user, 'filterName': request.json['filterName']}, {'$set': {
                   "productCode": request.json['productCode'], "days": request.json['days'],'location': location.capitalize(), "user": user, "filterName": request.json['filterName'], "modifiedAt": str(datetime.now())}})
    else:
        mongo_crud('40.81.232.147', 27017, 'pt',
                   'filter', 'create', filter_data)
    return "Filter Saved"


def getFilter(location, user):
    data = mongo_crud('', '', 'pt', 'filter', 'read', {'user': user,'location': location.capitalize()}, {})
    for x in data:
        del x['_id']
    return jsonify(data)


def getProductCode(location):
    location = location.capitalize()
    data = mongo_crud('', '', 'pt', 'summaryMaster_{}'.format(
        location), 'read', {}, {})
    productCodeArr = []
    for x in data:
        productCodeArr.append(
            x['product_code']) if x['product_code'] not in productCodeArr else print("non duplicate")
    return jsonify(sorted(productCodeArr))

def getSnapFG(location, user):
    location = location.capitalize()
    data = mongo_crud('','','pt','snap_{}'.format(location),'readV2',[{},{"_id":0,"scenarioPage":0}],{})
    return jsonify(data)

def getSnapScenario(location, user, fg):
    location = location.capitalize()
    data = mongo_crud('','','pt','snap_{}'.format(location),'readV2',[{"FG": fg},{"_id":0,"summaryPage":0,"parent_item" : 0, "deficient" : 0, "potential_ctb" : 0, "entaglement" : 0, "total_order_quantity" : 0, "ctb" : 0, "description" : 0, "product_code" : 0, "dateRange" : 0, "plus" : 0, "lastUpdated" : 0}],{})
    parts = []
    Parentitem = data[0]["scenarioPage"]['FG']
    dd = data[0]["scenarioPage"]
    for i in dd['data'].keys():
        print(i)
        if Parentitem in i:
            print(i)
            # if(dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["index"] >= start and dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["index"] <= stop):
            if dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["deficient_flag"] == True or dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["entanglment_flag"] == True:
                parts.append({
                    "Parentitem": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Parentitem"],
                    "Level": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Level"],
                    "item": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["item"],
                    "index": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["index"],
                    "QPA": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["QPA"],
                    "p_m_t": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["p_m_t"],
                    "Oper_Num": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Oper_Num"],
                    "Alt_Group": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Alt_Group"],
                    "Alt_Grp_Rnk": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["Alt_Grp_Rnk"],
                    "description": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["description"],
                    "resolved_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["resolved_flag"],
                    "QOH": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["QOH"],
                    "totalAvailableParts": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["total_alt_item_allocated_ctb"],
                    "inv_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["allocated_item_ctb"],
                    "req_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["req_ctb"],
                    "deficient_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["deficient_flag"],
                    "entanglment_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["entanglment_flag"],
                    "alternate_flag": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["alternate_flag"],
                    "parent_ctb": int(dd["ctb"]) < 0 and 0 or int(dd["ctb"]),
                    "parent_potential_ctb": int(dd["potential_ctb"]) < 0 and 0 or int(dd["potential_ctb"]),
                    "allocated_item_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["allocated_item_ctb"],
                    "total_alt_item_allocated_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["total_alt_item_allocated_ctb"],
                    "total_item_alt_item_allocated_ctb": dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["total_item_alt_item_allocated_ctb"],
                    "entagled_parents_details": makeDataReverse(dd['data']['{}_{}'.format(Parentitem, i.split('_')[1])]["entagled_parents_details"])
                })
            else:
                print("Not Deficient and Not Entangled")
            # else:
            #     print("Not in paginated range")
    return jsonify(parts)
    # return jsonify()

def addUser():
    data = request.json
    checkUser = mongo_crud('host', 'port', 'pt', 'users', 'read', query={'username': data['username']})
    if checkUser:
        return "User Already Exists"
    else:
        mongo_crud('host', 'port', 'pt', 'users', 'create', {
            'username': data['username'],
            'password': data['password'],
            'location': data['location'],
            'access': data['access']
        })
        return "User Created Successfully"

def update():
    data = request.json
    mongo_crud('host', 'port', 'pt', 'users', 'update', {'username': data['username']}, update={
            'password': data['password'],
            'location': data['location'],
            'access': data['access']
    })
    return "User Updated Successfully"

def delete():
    data = request.json
    mongo_crud('host', 'port', 'pt', 'users', 'delete', {'username': data['username']}, update={})
    return "User Deleted Successfully"

def getUsers():
    data = mongo_crud('host', 'port', 'pt', 'users', 'readV2',[{},{"_id":0}],{})
    return data

def plannercode(location):
    location=location.capitalize()
    data = mongo_crud('', '', 'pt', 'itemMaster_{}'.format(
        location), 'read', {}, {})
    planCodeArr = []
    for x in data:
        print(x)
        planCodeArr.append(
            x['Plan_Code']) if x['Plan_Code'] not in planCodeArr else print("non duplicate")
    return jsonify(sorted(planCodeArr))

def export_forecasting(location):
    location=location.capitalize()
    state=request.json.get('state')
    print(state)
    net_balance = 1 if state.get('Net_Balance') else 0
    qoh = 1 if state.get('QOH') else 0
    co = 1 if state.get('CO') else 0
    demand = 1 if state.get('DEMAND') else 0
    make = 1 if state.get('MAKE') else 0
    po = 1 if state.get('PO') else 0
    
    refs = []

    # Check each variable and add its reference to refs if the variable's value is 1
    if net_balance == 1:
        refs.append('Net_Balance')
    if qoh == 1:
        refs.append('QOH')
    if co == 1:
        refs.append('CO')
    if demand == 1:
        refs.append('DEMAND')
    if make == 1:
        refs.append('MAKE')
    if po == 1:
        refs.append('PO')
    
    # refs = refs.strip("[]") 
    refs_str = ", ".join(["'{}'".format(ref) for ref in refs])
    query = "SELECT * FROM pt_{}.forecast_new where Reference IN ({}) ;".format(location,refs_str)
    
    
    df = pd.read_sql(query, con=connect_with_sql(location))
    print(df)
    json_data = df.to_json(orient='records')

    return json_data