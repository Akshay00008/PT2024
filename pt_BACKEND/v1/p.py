from v1.setups.database.mongo import mongo_crud

dd = mongo_crud(host='40.81.232.147', port=27017, db_name='hi',
                        collection_name='hi', operation='updatemany', query={}, update={
                            "$set": { "ctbArr.4": 23 } 
                        })

# print(sum(dd['entArr']))