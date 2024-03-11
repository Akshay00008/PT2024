from flask import request
from ..setups.service.index_v2 import ETL
import concurrent.futures
import time
import multiprocessing

def process_db(db_name):
        t = time.time()
        with ETL(db_name) as obj:
            print("Execution Is In Progress For = {}".format(db_name))
        print("{} took total {}".format(db_name, time.time() - t))

def gatherData():
    dbList = request.json['location']
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        future_to_db = {executor.submit(process_db, db): db for db in dbList}
        for future in concurrent.futures.as_completed(future_to_db):
            db_name = future_to_db[future]
            #try:
            result = future.result()
            #except Exception as exc:
             #   print('%r generated an exception: %s' % (db_name, exc))
    return "Exection For {} Is In Progress".format(', '.join(dbList))