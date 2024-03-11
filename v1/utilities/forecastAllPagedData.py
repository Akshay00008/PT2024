from ..setups.database.mysql import connect_with_sql, read
import pandas as pd
import json


# Function to fetch data from SQL (adapt this part for your SQL database)
def fetch_data_from_sql(location, limit,page_number):
    # Assuming you have a way to fetch data from SQL
    # Example: replace this with SQL query and connection code
    # connection = your_db_connection()
    print(f"Location: {location}")
    print(f"Limit: {limit}")
    print(f"Page Number: {page_number}")
    offset = limit * (page_number - 1)
    print(f"OFFSET: {offset}")
    query = "SELECT * FROM pt_{}.forecast_new LIMIT {} OFFSET {};".format(location, limit, limit * (page_number - 1))
    data_1 = read(query, location)
    print(data_1)
    data = pd.DataFrame(data_1)
    return data

def paginate_data(data, page_number, items_per_page):
        # print("this is it")
        # print(page_number)
        # print("data-1")
        # print(data)
        start_row = (page_number - 1) * items_per_page
        end_row = start_row + items_per_page
        return data.iloc[start_row:end_row]

def paged_data(location, page_number, page_size, productCode):
    # Check if page_number is less than 1, set it to 1
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new LIMIT {};".format(limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new LIMIT {};".format(limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data


def search(search_val, location):
    query = "SELECT * FROM pt_{}.forecast_new where item = '{}';".format(location,search_val)
    df = pd.read_sql(query, con=connect_with_sql(location))
    json_data = df.to_json(orient='records')

    return json_data

def plan_code(location, page_number, page_size, planner_code):
    # query= "SELECT * FROM pt_{}.forecast_new WHERE planner_code IN ('{}');;".format(location,planner_code)
    # query = "SELECT * FROM pt_{}.forecast_new WHERE planner_code IN ('{}');".format(location, "','".join(planner_code))
    
    # Check if page_number is less than 1, set it to 1
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new WHERE plan_code IN ('{}') LIMIT {};".format("','".join(planner_code),limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new WHERE plan_code IN ('{}') LIMIT {};".format("','".join(planner_code),limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data


def deficients_item(location,page_number, page_size,val):
    # query = "SELECT * FROM pt_{}.forecast_new where Category = '{}';".format(location,val)
    # df = pd.read_sql(query, con=connect_with_sql(location))
    
    # Check if page_number is less than 1, set it to 1
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new where Category = '{}' LIMIT {};".format(val,limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new where Category = '{}' LIMIT {};".format(val,limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data
    

def deficients_plan(location,page_number, page_size,val,planner_code):
    # query = "SELECT * FROM pt_{}.forecast_new where Category = '{}';".format(location,val)
    # df = pd.read_sql(query, con=connect_with_sql(location))
    
    # Check if page_number is less than 1, set it to 1
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    planner_code=tuple(planner_code)
    

    if len(planner_code) == 1:
        planner_code=(planner_code[0])
        planner_code = "(" + repr(planner_code) + ")"

   
    
#     api_result = planner_code

# # Removing square brackets
#     planner_code = api_result.strip("[]")  

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new where Category = '{}' and plan_code IN {} LIMIT {};".format(val,planner_code,limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new where Category = '{}' and plan_code IN {} LIMIT {};".format(val,planner_code,limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data
    

def Purchased_order(location, page_number, page_size,PO_code) :
    
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    
    
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new where p_m_t_code = '{}' LIMIT {};".format(PO_code, limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new where p_m_t_code = '{}' LIMIT {};".format(PO_code,  limit*page_number)
        print(query)


    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data

def manufactured_item(location, page_number, page_size,Make_code) :
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new where p_m_t_code = '{}' LIMIT {};".format(Make_code,limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new where p_m_t_code = '{}' LIMIT {};".format(Make_code, limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data
    
    
def all(location, page_number, page_size,Make_code,PO_code):
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new  LIMIT {};".format(  limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new  LIMIT {};".format( limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data
    
    

def plan_code_M(location, page_number, page_size, planner_code,Make_code):
    # query= "SELECT * FROM pt_{}.forecast_new WHERE planner_code IN ('{}');;".format(location,planner_code)
    # query = "SELECT * FROM pt_{}.forecast_new WHERE planner_code IN ('{}');".format(location, "','".join(planner_code))
    
    # Check if page_number is less than 1, set it to 1
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new WHERE plan_code IN ('{}') and p_m_t_code = '{}' LIMIT {};".format("','".join(planner_code),Make_code,limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new WHERE plan_code IN ('{}') and p_m_t_code = '{}' LIMIT {};".format("','".join(planner_code),Make_code,limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data

def plan_code_P(location, page_number, page_size, planner_code,PO_code):
    # query= "SELECT * FROM pt_{}.forecast_new WHERE planner_code IN ('{}');;".format(location,planner_code)
    # query = "SELECT * FROM pt_{}.forecast_new WHERE planner_code IN ('{}');".format(location, "','".join(planner_code))
    
    # Check if page_number is less than 1, set it to 1
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new WHERE plan_code IN ('{}') and p_m_t_code = '{}' LIMIT {};".format("','".join(planner_code),PO_code,limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new WHERE plan_code IN ('{}') and p_m_t_code = '{}' LIMIT {};".format("','".join(planner_code),PO_code,limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data

def deficients_plan_M(location,page_number, page_size,val,planner_code,Make_code):
    # query = "SELECT * FROM pt_{}.forecast_new where Category = '{}';".format(location,val)
    # df = pd.read_sql(query, con=connect_with_sql(location))
    
    # Check if page_number is less than 1, set it to 1
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    planner_code=tuple(planner_code)
    

    if len(planner_code) == 1:
        planner_code=(planner_code[0])
        planner_code = "(" + repr(planner_code) + ")"

   
    
#     api_result = planner_code

# # Removing square brackets
#     planner_code = api_result.strip("[]")  

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new where Category = '{}' and plan_code IN {} and p_m_t_code = '{}' LIMIT {};".format(val,planner_code,Make_code,limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new where Category = '{}' and plan_code IN {} and p_m_t_code = '{}' LIMIT {};".format(val,planner_code,Make_code,limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data
def deficients_plan_P(location,page_number, page_size,val,planner_code,PO_code):
    # query = "SELECT * FROM pt_{}.forecast_new where Category = '{}';".format(location,val)
    # df = pd.read_sql(query, con=connect_with_sql(location))
    
    # Check if page_number is less than 1, set it to 1
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    planner_code=tuple(planner_code)
    

    if len(planner_code) == 1:
        planner_code=(planner_code[0])
        planner_code = "(" + repr(planner_code) + ")"

   
    
#     api_result = planner_code

# # Removing square brackets
#     planner_code = api_result.strip("[]")  

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new where Category = '{}' and plan_code IN {} and p_m_t_code = '{}' LIMIT {};".format(val,planner_code,PO_code,limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new where Category = '{}' and plan_code IN {} and p_m_t_code = '{}' LIMIT {};".format(val,planner_code,PO_code,limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data

def deficients_item_P(location,page_number, page_size,val,PO_code):
    # query = "SELECT * FROM pt_{}.forecast_new where Category = '{}';".format(location,val)
    # df = pd.read_sql(query, con=connect_with_sql(location))
    
    # Check if page_number is less than 1, set it to 1
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page


    

    # if len(planner_code) == 1:
    #     planner_code=(planner_code[0])
    #     planner_code = "(" + repr(planner_code) + ")"

   
    
#     api_result = planner_code

# # Removing square brackets
#     planner_code = api_result.strip("[]")  

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new where Category = '{}'  and p_m_t_code = '{}' LIMIT {};".format(val,PO_code,limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new where Category = '{}'  and p_m_t_code = '{}' LIMIT {};".format(val,PO_code,limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data

def deficients_item_M(location,page_number, page_size,val,Make_code):
    # query = "SELECT * FROM pt_{}.forecast_new where Category = '{}';".format(location,val)
    # df = pd.read_sql(query, con=connect_with_sql(location))
    
    # Check if page_number is less than 1, set it to 1
    if page_number < 1:
        page_number = 1

    # Items per page
    items_per_page = 6 * page_size
    limit=items_per_page

    
    

    # if len(planner_code) == 1:
    #     planner_code=(planner_code[0])
    #     planner_code = "(" + repr(planner_code) + ")"

   
    
#     api_result = planner_code

# # Removing square brackets
#     planner_code = api_result.strip("[]")  

    # Function to paginate the data
    
    # print(page_number)
    # print(location)
    # print(items_per_page)
    # Fetch data from SQL based on page number
    if location == 'Protec' :
        query = "SELECT * FROM pt_Protec.forecast_new where Category = '{}' and  p_m_t_code = '{}' LIMIT {};".format(val,Make_code,limit*page_number)
        print(query)
    
    else :
        
        query = "SELECT * FROM pt_Amery.forecast_new where Category = '{}'  and p_m_t_code = '{}' LIMIT {};".format(val,Make_code,limit*page_number)
        print(query)

    data_1 = read(query, location)
    # data_2 = fetch_data_from_sql(location, items_per_page, page_number)
    print(data_1)
    
    start_row = (page_number - 1) * items_per_page
    end_row = start_row + items_per_page
    page_data= data_1.iloc[start_row:end_row]
    
    print("page data")
    print(page_data)

    # Check if there is data for the given page number
   

    # Process the data for the current page
    # page_data = paginate_data(data_1, page_number, items_per_page)

    if page_data.empty:
        print("NO  p Data")
        return json.dumps([])  # No data for this page

    # Convert the page data to JSON
    json_data = page_data.to_json(orient='records')

    return json_data