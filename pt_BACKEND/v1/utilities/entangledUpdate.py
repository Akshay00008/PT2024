from pymongo import UpdateOne
import concurrent.futures
import multiprocessing
def updateAllEntangled_inner(mongo_crud,item,location, allEntFGs, entArray, total_item_alt_item_allocated_ctb, allocated_item_ctb):
    # allEntFGs = []

    # for fgs in entArray:
    #     allEntFGs.append(fgs['FG'])

    # # fg = fg['Parentitem']
    c=0
    update_s = []
    # print(allEntFGs,"ALL ENTS")
    for x in allEntFGs:
        # print(x)
        update_operations = {
            "$set": {
                "data.{}_{}.allocated_item_ctb".format(x,item): allocated_item_ctb,
                "data.{}_{}.total_item_alt_item_allocated_ctb".format(x,item): total_item_alt_item_allocated_ctb,
                "data.{}_{}.entagled_parents_details".format(x, item): entArray
            }
        }

            # update_s.append(i['FG'])

        print(update_operations, "update operations")

        xx = mongo_crud('', 0, db_name='pt',
                        collection_name='fgMasterV2_{}'.format(location), operation='updatemany', query={"FG": x}, update=update_operations)
        
        # print(update_s)
    return "allEntFGs"

def updateAllEntangled(entArray, mongo_crud, parent, item, fg, location):
    num_cores = multiprocessing.cpu_count()
    # print(num_cores)
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=num_cores)
    future_results = []
    total_item_alt_item_allocated_ctb = fg["total_item_alt_item_allocated_ctb"]
    allocated_item_ctb = fg["allocated_item_ctb"]
    # print(fg,"hherer", fg['Parentitem'])
    fg = fg['Parentitem']
    allEntFGs = []

    for fgs in list(entArray.keys()):
        allEntFGs.append(fgs.split('_')[2])

    # results = []
    fg_chunks = [allEntFGs[i::num_cores] for i in range(num_cores)]

    for fg_chunk in fg_chunks:
        future = executor.submit(updateAllEntangled_inner, mongo_crud, item, location, fg_chunk, entArray, total_item_alt_item_allocated_ctb, allocated_item_ctb)
        future_results.append(future)

    # for i in entArray:
    #     result = pool.apply_async(updateAllEntangled_inner, (i, item, fg, location, mongo_crud))
    #     results.append(result)

    # pool.close()
    # pool.join()


    # Wait for the results to complete
    concurrent.futures.wait(future_results)

    # results = {}
    # print(future_results)
    # for future in future_results:
    #     result = future.result()
    #     results.update(result)

    # Process the results as desired

    return allEntFGs


