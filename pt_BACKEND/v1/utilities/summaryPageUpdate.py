import math

def summarypageUpdate(mongo, parent, location, summaryPageDataUpdate, allFGs):
    xyz = 0
    for p in allFGs:

        print(p,"FG")
    
        dd = mongo(host='40.81.232.147', port=27017, db_name='pt',
                        collection_name='fgMasterV2_{}'.format(location), operation='findone', query={"FG": p}, update={})
        
        itemMasterData = mongo(host='40.81.232.147', port=27017, db_name='pt',
                        collection_name='itemMaster_{}'.format(location), operation='read', query={}, update={})

        countForEnt = 0
        countForDef = 0
        total_item_alt_item_allocated_item_ctb = []
        potentialCtb = []
        
        for i in dd['data'].keys():
            if dd['data'][i]["entanglment_flag"] == True and dd['data'][i]["resolved_flag"] == False:
                countForEnt += 1
            if dd['data'][i]["deficient_flag"] == True and dd['data'][i]["resolved_flag"] == False:
                countForDef += 1
            if dd['data'][i]['entanglment_flag'] == True or dd['data'][i]["deficient_flag"] == True:
                if int(dd['data'][i]['allocated_item_ctb']) >= 0:
                    total_item_alt_item_allocated_item_ctb.append(int(dd['data'][i]['allocated_item_ctb']))
            try:
                itemMasterD = [x for x in itemMasterData if x['item'] == dd['data'][i]['item']]
                x = math.floor(int(itemMasterD[0]['totalAvailableParts'])/int(dd['data'][i]['QPA']))
            except:
                x = 9000000
            potentialCtb.append(x)

        update_operations = {
            "$set": {
                "entaglement": countForEnt,
                "deficient": countForDef,
                "ctb": min(total_item_alt_item_allocated_item_ctb),
                "lastUpdated": summaryPageDataUpdate['lastUpdated']
            }
        }

        print(update_operations, p, total_item_alt_item_allocated_item_ctb, "ARRR")

        if p == parent:
            xyz = min(total_item_alt_item_allocated_item_ctb)

        dd = mongo('', 0, db_name='pt',
                        collection_name='summaryMaster_{}'.format(location), operation='updatemany', query={"parent_item": p}, update=update_operations)
        
        dd = mongo('', 0, db_name='pt',
                        collection_name='fgMasterV2_{}'.format(location), operation='updatemany', query={"FG": parent}, update=update_operations)
        
    return {
        parent: xyz
    }