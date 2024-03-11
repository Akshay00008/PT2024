import multiprocessing

def updateAllEntangled_inner(i, item, fg, location, mongo_crud):
    # print(i, item, fg, location)
    update_operations = {
        "$set": {
            "data.{}_{}.allocated_item_ctb".format(i['FG'], item): i["ctb_qoh"],
            "data.{}_{}.total_item_alt_item_allocated_ctb".format(i['FG'], item): i["ctb_qoh"],
            "data.{}_{}.entagled_parents_details.{}_{}_{}.FG".format(i['FG'], item, i['FG'], item, fg): i["FG"],
            "data.{}_{}.entagled_parents_details.{}_{}_{}.req_ctb".format(i['FG'], item, i['FG'], item, fg): i["req_ctb"],
            "data.{}_{}.entagled_parents_details.{}_{}_{}.qpa".format(i['FG'], item, i['FG'], item, fg): i["qpa"],
            "data.{}_{}.entagled_parents_details.{}_{}_{}.allocated_qty".format(i['FG'], item, i['FG'], item, fg): i["allocated_qty"],
            "data.{}_{}.entagled_parents_details.{}_{}_{}.ctb_qoh".format(i['FG'], item, i['FG'], item, fg): i["ctb_qoh"],
            "data.{}_{}.entagled_parents_details.{}_{}_{}.ctb".format(i['FG'], item, i['FG'], item, fg): i["ctb"],
            "data.{}_{}.entagled_parents_details.{}_{}_{}.potential_ctb".format(i['FG'], item, i['FG'], item, fg): i["potential_ctb"]
        }
    }

    print(update_operations)

    mongo_crud('', 0, db_name='pt', collection_name='fgMasterV2_{}'.format(location), operation='updatemany', query={"FG": i['FG']}, update=update_operations)

    return i['FG']

def updateAllEntangled(entArray, mongo_crud, parent, item, fg, location):
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)

    fg = fg['Parentitem']
    allEntFGs = []

    for fgs in entArray:
        allEntFGs.append(fgs['FG'])

    results = []

    for i in entArray:
        result = pool.apply_async(updateAllEntangled_inner, (i, item, fg, location, mongo_crud))
        results.append(result)

    pool.close()
    pool.join()

    updatedEntFGs = [result.get() for result in results]

    return allEntFGs
