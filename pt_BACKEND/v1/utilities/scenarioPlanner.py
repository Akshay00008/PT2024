import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote as urlquote
import warnings
import numpy as np
import time
import json

class scenarioPlanner():
    def __init__(self, location, scenarioData, parentItem, alternateData):
        self.location = location
        self.scenarioData = scenarioData
        self.parentItem = parentItem
        self.df_item = alternateData

    def scenerioplanner(self):
        final_df_last = self.scenarioData
        df_work_with = final_df_last[(final_df_last["Parentitem"] == self.parentItem)]
        df_work_with["entagled_parents_details"] = "[]"
        df_work_with["cost_of_part"] = 10 #need to change it with the actual cost
        df_work_with["alternate_details"] = "[]"
        df_work_with["alternate_flag"] = False

        itemSet = {}

        itemMaster = []

        count=0

        ctb = []
        entangled = []
        unresolved = []
        deficient = []

        for l in df_work_with["item"]:
            json_list_entangled = {}
            temp_test = final_df_last[final_df_last["item"] == l]
            temp_test2 = df_work_with[df_work_with["item"] == l]
            temp_test2 = temp_test2[temp_test2["Parentitem"] == self.parentItem]
            ddx = {
                "Parentitem":temp_test2.iloc[0]['Parentitem'],
                "Level":0,
                "index": count,
                "item":temp_test2.iloc[0]['item'],
                "QPA":temp_test2.iloc[0]['QPA'],
                "p_m_t":temp_test2.iloc[0]['p_m_t'],
                "Oper_Num":0,
                "Alt_Group":0,
                "Alt_Grp_Rnk":0,
                "description":temp_test2.iloc[0]['description'],
                "QOH":temp_test2.iloc[0]['QOH'],
                "Plan_Code":temp_test2.iloc[0]['plan_code'],
                "inv_ctb":temp_test2.iloc[0]['inv_ctb'],
                "req_ctb":temp_test2.iloc[0]['qty_ordered_new'],
                "deficient_flag": True if temp_test2.iloc[0]['deficient_flag'] == 1 else False,
                "entanglment_flag":True if temp_test2.iloc[0]['entangled_flag'] == 1 else False,
                "alternate_flag":False,
                "altenate_item_allocated_ctb":[],
                "allocated_item_ctb":0,
                "total_alt_item_allocated_ctb":0,
                "total_item_alt_item_allocated_ctb":(temp_test2.iloc[0]["entangled_flag"] == False and temp_test2.iloc[0]["deficient_flag"] == False) and temp_test2.iloc[0]["qty_ordered"] or 0,
                "no_conflict":False,
                "resolved_flag":False,
                "entagled_parents_details":{},
                "alternate_details":[]      
            }
            # ctb.append(0)
            entangled.append(1 if temp_test2.iloc[0]['entangled_flag'] == 1 else 0)
            deficient.append(1 if temp_test2.iloc[0]['deficient_flag'] == 1 else 0)
            if temp_test2.iloc[0]['entangled_flag'] == 0 and temp_test2.iloc[0]['deficient_flag'] == 0:
                ctb.append(9999999)
            else:
                ctb.append(0)

            unresolved.append(0)

            itemMaster.append({
                "item": temp_test2.iloc[0]['item'],
                "QPA": temp_test2.iloc[0]['QPA'],
                "Alt_Grp_Rnk": temp_test2.iloc[0]['Alt_Grp_Rnk'],
                "QOH": temp_test2.iloc[0]['QOH'],
                "cost_of_part":10,
                "oldQOH":0,
                "Plan_Code":temp_test2.iloc[0]['plan_code'],
                "newQOH":0,
                "deltaQOH":0,
                "totalAvailableParts":temp_test2.iloc[0]['QOH']
            })
            if len(temp_test) > 1:
                for index, row in temp_test.iterrows():
                    entangled_dict = {}
                    entangled_dict["FG"] = row["Parentitem"]
                    entangled_dict["req_ctb"] = row["qty_ordered_new"]
                    entangled_dict["qpa"] = row["QPA"]
                    entangled_dict["allocated_qty"] = 0
                    entangled_dict["ctb_qoh"] = 0
                    entangled_dict["ctb"] = temp_test[temp_test['Parentitem'] == row["Parentitem"]]['ctb'].iloc[0]
                    entangled_dict["potential_ctb"]=temp_test[temp_test['Parentitem'] == row["Parentitem"]]['potential_ctb_with_alt'].iloc[0]
                    json_list_entangled.update({"{}_{}_{}".format(temp_test2.iloc[0]['Parentitem'],temp_test2.iloc[0]['item'],row["Parentitem"]):entangled_dict})
            else:
                pass

            count=count+1

            ddx['entagled_parents_details'].update(json_list_entangled)
            itemSet.update({"{}_{}".format(temp_test2.iloc[0]['Parentitem'],temp_test2.iloc[0]['item']):ddx})
        
        return {"itemdata": itemSet, "itemMaster":itemMaster, "ctb": ctb, "entangled": entangled, "deficient": deficient, "unresolved": unresolved}

    @staticmethod
    def alternates(self):

        Parentitem, df_item = self.parentItem, self.df_item
        parents_Df=df_item.loc[df_item['Parentitem'].isin([Parentitem])]
        levels=parents_Df['Level'].unique()

        for level in levels :

            level_df=parents_Df.loc[parents_Df['Level'].isin([level])]
            if (level_df['Alt_Grp_Rnk'] > 0).any():

                rows_with_condition_true = level_df[level_df['Alt_Grp_Rnk'] > 0]

                filtered_df = level_df[(level_df['Oper_Num'].isin(rows_with_condition_true['Oper_Num'])) & 
                        (level_df['Alt_Group'].isin(rows_with_condition_true['Alt_Group']))]
                filtered_df['new'] = False
                filtered_df.loc[filtered_df['Alt_Grp_Rnk'] == 0, 'alternate_flag'] = True
                filtered_df["Alt_Grp_Rnk"]=filtered_df["Alt_Grp_Rnk"].astype(int)
                for l in filtered_df["Item"][filtered_df["alternate_flag"] == True]:
                    json_list_Alternates=[]
                    temp_test = filtered_df[filtered_df["Alt_Grp_Rnk"] > 0]
                    for index, row in temp_test.iterrows():
                        alternate_dict = {}
                        alternate_dict["Alternate_item"] = row["Item"]
                        alternate_dict["Alt_Grp_Rnk"] = row["Alt_Grp_Rnk"]
                        alternate_dict["qpa"] = row["QPA"]
                        json_list_Alternates.append(alternate_dict)

                    filtered_df.loc[(filtered_df["Item"] == l), "alternate_item_details"]= json.dumps(json_list_Alternates, separators=(',', ':'))
                    filtered_df=filtered_df.loc[filtered_df['alternate_flag']==True]
            else :
                print("No alternates")
        return filtered_df