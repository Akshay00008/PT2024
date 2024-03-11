import concurrent.futures
import multiprocessing
import math
from pymongo import UpdateOne, UpdateMany

def summarypageUpdate_inner(mongo, parent, location, summaryPageDataUpdate, fg_chunk):
    result = {}
    xyz = 0
    update_operations = []
    update_operationsFG = []
    for p in fg_chunk:    
        dd = mongo(host='40.81.232.147', port=27017, db_name='pt',
                        collection_name='fgMasterV2_{}'.format(location), operation='findone', query={"FG": p}, update={})
        
        try:
            # print(p,"FFFFFFFF")
        # print(dd['ctbArr'],"CTB")
            # print("ERRRRRRRR")
            try:
                total_item_alt_item_allocated_item_ctb = min(dd['ctbArr'])
            except:
                total_item_alt_item_allocated_item_ctb = 0
            # print("ERRRRRRRR2")
            countForEnt = sum(dd['entArr'])
            # print("ERRRRRRRR3")
            countForDef = sum(dd['defArr'])

            update_operationsFG.append(UpdateOne({"FG": parent},{
                "$set": {
                    "entaglement": countForEnt,
                    "deficient": countForDef,
                    "ctb": total_item_alt_item_allocated_item_ctb,
                    "lastUpdated": summaryPageDataUpdate['lastUpdated']
                }
            }))
            update_operations.append(UpdateMany({"parent_item": p},{
                "$set": {
                    "entaglement": countForEnt,
                    "deficient": countForDef,
                    "ctb": total_item_alt_item_allocated_item_ctb,
                    "lastUpdated": summaryPageDataUpdate['lastUpdated']
                }
            }))
            
            if p == parent:
                xyz = total_item_alt_item_allocated_item_ctb

            result[parent] = xyz
        except:
            print("================================={}=================================".format(p))


    if(len(update_operations) > 0 and len(update_operationsFG) >0):
        dd = mongo('', 0, db_name='pt',collection_name='summaryMaster_{}'.format(location), operation='bulkWrite', query={}, update=update_operations)
        dd = mongo('', 0, db_name='pt',collection_name='fgMasterV2_{}'.format(location), operation='bulkWrite', query={}, update=update_operationsFG)
    return result

def summarypageUpdate(mongo, parent, location, summaryPageDataUpdate, allFGs):
    num_cores = multiprocessing.cpu_count()
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=num_cores)
    future_results = []
    fg_chunks = [allFGs[i::num_cores] for i in range(num_cores)]

    for fg_chunk in fg_chunks:
        future = executor.submit(summarypageUpdate_inner, mongo, parent, location, summaryPageDataUpdate, fg_chunk)
        future_results.append(future)

    # Wait for the results to complete
    concurrent.futures.wait(future_results)

    results = {}
    for future in future_results:
        result = future.result()
        results.update(result)

    return results[parent]