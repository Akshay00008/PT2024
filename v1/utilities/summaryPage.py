import pandas as pd
import time
from datetime import timedelta
from datetime import date
import numpy as np
from math import floor
from ..setups.database.mysql import connect_with_sql

class summaryPage():
    def __init__(self, location):
        self.location = location

    def summaryPageDbSync(self):
        '''
            read important data req for calculation 
        '''
        query_item = '''select item, QOH from item_master;'''
        query_coitem = '''select * from coitem_master;'''
        query_flatbom = '''select * from flatbom_data;'''
        # reading all data requrired for summary page logic
        df_item = pd.read_sql(query_item, connect_with_sql(self.location))
        df_coitem = pd.read_sql(query_coitem,  connect_with_sql(self.location))
        
        df_coitem['due_date'] = pd.to_datetime(df_coitem['due_date']).dt.date
        df_flatbom = pd.read_sql(query_flatbom,connect_with_sql(self.location))
        # rename items to parentitem 
        df_coitem.rename(columns={"item":"Parentitem"}, inplace= True)
        df_flatbom.rename(columns={"Item":"item"}, inplace= True)
        # merge qty ordered in df in order to
    # Select the required columns and filter the parent items at level 0
        df_unique_parentitem = df_flatbom.loc[df_flatbom["Level"] == '0', "Parentitem"]

        # Merge with df_coitem and group by parent item
        df_with_req_ctb =pd.merge(df_unique_parentitem,df_coitem, on="Parentitem")

        # Create a new column 'dateRange' with value 'All'
        #df_with_req_ctb["dateRange"] = "All"


        # Define the date and time delta for future orders
        
        time_delta = [15, 30, 60, 90]
        df_with_req_ctb_new=pd.DataFrame(columns=df_with_req_ctb.columns)
        # Loop through the time delta and create the new dataframes with their respective dateRange value
        for delta in time_delta:
            date_date = date.today()
            date_date=date_date + timedelta(days=delta)
            date_date=np.datetime64(date_date)
            df_temp = df_with_req_ctb.loc[df_with_req_ctb['due_date'] < date_date]
            df_temp = df_temp.groupby("Parentitem", as_index=False)["qty_ordered"].sum()
            df_temp["dateRange"] = delta
            df_with_req_ctb_new = pd.concat([df_with_req_ctb_new, df_temp], ignore_index=True)



        df_with_req_ctb = df_with_req_ctb.groupby('Parentitem',as_index=False)['qty_ordered'].sum() 
        df_with_req_ctb['dateRange']='All'

        # print(df_with_req_ctb)


        df_with_req_ctb_new=pd.concat([df_with_req_ctb_new, df_with_req_ctb], ignore_index=True)
        # Merge with df_item and df_flatbom and create df_flatbom_with_inv_ctb
        df_flatbom_with_inv_ctb = pd.merge(df_flatbom, df_item, on=["item"], how="left")
        df_flatbom_with_inv_ctb["inv_ctb"] = df_flatbom_with_inv_ctb["QOH"] / df_flatbom_with_inv_ctb["QPA"]

        '''
            total order quantity calcultaion
        '''
        df_coitem_qty_sum = df_coitem.groupby("Parentitem",as_index=False)["qty_ordered"].sum()
        # dataframe with qty ordered
        '''
            Code to calculate deficient items
        '''
        df_flatbom_with_req_qty = pd.merge(df_flatbom_with_inv_ctb, df_with_req_ctb,how="left",on="Parentitem")
        df_flatbom_with_req_qty["deficient_flag"] = df_flatbom_with_req_qty["inv_ctb"] < df_flatbom_with_req_qty["qty_ordered"]
        df_flatbom_with_req_qty.drop_duplicates(subset=['item'],keep='first',inplace=True)
        df_flatbom_with_req_qty["Level"]=df_flatbom_with_req_qty["Level"].astype(int)
        df_deficient_count = df_flatbom_with_req_qty.loc[(df_flatbom_with_req_qty["Level"]>0 )]
        df_deficient_count=df_flatbom_with_req_qty.loc[~df_flatbom_with_req_qty["Level"].isin([0])].groupby("Parentitem", as_index=False)["deficient_flag"].sum()
        df_deficient_count.rename(columns={"deficient_flag":"deficient_count"}, inplace=True)

        # print(df_flatbom_with_req_qty_deficient_count)
        '''
            Code to calculate potential CTB considering Alternates
        '''
        final_df = pd.merge(df_flatbom_with_req_qty, df_deficient_count, how="left", on="Parentitem")
        final_df['shifted_Alt_Grp_Rnk'] = final_df['Alt_Grp_Rnk'].shift(1)
        # Calculate the difference between the original and shifted Alt_Grp_Rnk
        final_df['diff'] = final_df['Alt_Grp_Rnk'] - final_df['shifted_Alt_Grp_Rnk']
        # Check if the difference is equal to 1
        final_df['is_consecutive'] = np.where(final_df['diff'] == 1, True, False)
        final_df['Ref_item'] = final_df['item'].where(~final_df['is_consecutive']).ffill()
        check_df = final_df.groupby(["Parentitem","Ref_item"],as_index=False)["inv_ctb"].sum()
        check_df.rename(columns={"inv_ctb":"potential_ctb_with_alt"}, inplace=True)
        #print("this is check df")
    # print(check_df)
        check_df["potential_ctb_with_alt"] = np.where(check_df["potential_ctb_with_alt"]<0,0,check_df["potential_ctb_with_alt"])
        check_df2 = check_df.groupby(["Parentitem"],as_index=False)["potential_ctb_with_alt"].min()
        final_df = pd.merge(final_df,check_df2,how="left",on="Parentitem")
        
        '''
            entanglment code
        '''
        # print(final_df.dtypes)
        final_df_no_alternate = final_df[(final_df["Alt_Grp_Rnk"]==0)& (final_df["Level"]!='0')]#taking Alt_GRp_rnk > 0 is considered to be a alternate for sone item
        final_df_no_alternate["qpa_mult_qtyOrdered"] = final_df_no_alternate["QPA"] * final_df_no_alternate["qty_ordered"]
        # check_df_3 = final_df_no_alternate.groupby(["item"],as_index=False)["qpa_mult_qtyOrdered"].sum()
        check_df_3 = final_df_no_alternate.groupby(["item"],as_index=False).agg({"qpa_mult_qtyOrdered":"sum","QOH":"mean"})
        check_df_3["entangled_flag"] = np.where(check_df_3["qpa_mult_qtyOrdered"] > check_df_3["QOH"], True, False)
        #check_df_3.to_csv("entangled2.csv")
        final_df_entangled = pd.merge(final_df,check_df_3[["item","entangled_flag"]], on="item", how="left")
        #final_df_entangled.to_csv("entangled2.csv")
        final_df_entangled["Level"]=final_df_entangled["Level"].astype(int)
        final_df_entangled["entangled_flag"].fillna(False, inplace=True)
        final_df_last = final_df_entangled.copy()
        final_df_entangled = final_df_entangled.loc[(final_df_entangled["Level"]>0)]

        final_df_entangled=final_df_entangled.loc[~final_df_entangled["Level"].isin(['0'])].groupby("Parentitem", as_index=False)["entangled_flag"].sum().rename(columns={'entangled_flag':"entangled_count"})
        #final_df_entangled.to_csv('entnagledtrue.csv')
        final_df_entangled = final_df_entangled[['Parentitem','entangled_count']]
        final_df_last = pd.merge(final_df_last, final_df_entangled, on="Parentitem", how="left")
        '''
            CTB calculation
        '''
        final_df_last["ctb"] = np.where(final_df_last["deficient_flag"] == True, final_df_last["qty_ordered"] - final_df_last["inv_ctb"], final_df_last["inv_ctb"])
        final_df_last["ctb"] = np.where(final_df_last["entangled_flag"] == True, 0, final_df_last["inv_ctb"])
        
        '''
        Storing the result in the Mysql table to use it in Scenario Planner
        '''
        
        final_df_last['ctb'] = final_df_last['ctb'].replace([np.inf, -np.inf], np.nan).fillna(0).astype(int)
        final_df_last['ctb'] = final_df_last['ctb'].apply(lambda x: 0 if x < 0 else x)

        final_df_last['inv_ctb'] = final_df_last['ctb'].replace([np.inf, -np.inf], np.nan).fillna(0).astype(int)
        final_df_last['inv_ctb'] = final_df_last['ctb'].apply(lambda x: 0 if x < 0 else x)

        final_df_last.to_sql("Scenario_Page_Useable", connect_with_sql(self.location), if_exists="replace"  ,index=True)


        date_range_df = final_df_last[["Parentitem","dateRange"]]
        #print(final_df_last)
        #print(date_range_df)
        
        '''
            final df with only columns that are required
        '''
    
        final_df_last = final_df_last.groupby(["Parentitem"], as_index=False).agg({"deficient_count":"min", "potential_ctb_with_alt":"min", "entangled_count":"min","qty_ordered":"min","ctb":"min"})
        final_df_last = pd.merge(final_df_last, date_range_df, on="Parentitem", how="left")

        df_with_req_ctb_new.drop(['qty_ordered','due_date'],axis=1,inplace=True)


        final_df_last=pd.merge(final_df_last,df_with_req_ctb_new,on=['Parentitem'],how='inner')
        final_df_last.drop(['dateRange_x'],axis=1,inplace=True)

        final_df_last['potential_ctb_with_alt']=final_df_last['potential_ctb_with_alt'].apply(np.floor)
        final_df_last['ctb']=final_df_last['ctb'].apply(np.floor)
        final_df_last=final_df_last.fillna(0)


        #final_df_last.to_csv('summary.csv')
        final_df_last['plus']=final_df_last['Parentitem']+'-'+ final_df_last['dateRange_y'].astype(str)
        final_df_last.drop_duplicates(subset=['plus'],keep='first',inplace=True)

        final_df_last.rename(columns={"Parentitem":"parent_item","qty_ordered":"total_order_quantity","entangled_count":"entaglement","deficient_count":"deficient","potential_ctb_with_alt":"potential_ctb","dateRange_y":"dateRange"}, inplace= True)
        # final_df_last['deficient']=final_df_last['deficient']-1
        # final_df_last['deficient'][final_df_last['deficient'] < 0] = 0
    
        final_df_last.to_sql("summary_page", connect_with_sql(self.location) ,if_exists="replace",index=False)


        #print(final_df_last)

        end= time.time()
        print("The time taken for the summary page is \n")

    def summarypage_Api(self):
        try:
            query = '''select * from summary_page_current_dummy;'''
            df = pd.read_sql(query, connect_with_sql(self.location))
            return df 
        except Exception as e: 
            raise e