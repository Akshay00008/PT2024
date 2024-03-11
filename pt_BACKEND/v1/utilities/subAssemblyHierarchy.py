from ..setups.database.mysql import read
from ..setups.database.mongo import mongo_crud
import uuid
import random


def generate_uuid():
    return str(uuid.uuid4().fields[-1])[:5]

def createHierarchy(location):

    location = location.capitalize()
    
    data = read("SELECT * FROM Detailed_subassembly;", location)
    
    def doit(FG):
        FG_hi = data[data["Parentitem1"] == FG]
        filtered_df = FG_hi
        jsonStructure = []

        for _, rowss in filtered_df.iterrows():
            if len(jsonStructure) == 0:
                jsonStructure.append({
                    "Level": "L1",
                    "uuid": generate_uuid(),
                    "QOH": 0,
                    "QPA": rowss['Childqty1'],
                    "item": rowss['ChildItem1'],
                    "description": rowss['Childdescription1'],
                    "child_p_m_t": rowss['Childp_m_t1'],
                    "childAltGrp": rowss['ChildAltGrp1'],
                    "childOper": rowss['Childoper1'],
                    "childAltGrpRnk": rowss['ChildAltGrpRnk1'],
                    "child": [{
                        "Level": "L2",
                        "uuid": generate_uuid(),
                        "QOH": 0,
                        "QPA": rowss["Childqty2"],
                        "item": rowss['ChildItem2'],
                        "description": rowss['Childdescription2'],
                        "child_p_m_t": rowss['Childp_m_t2'],
                        "childAltGrp": rowss['ChildAltGrp2'],
                        "childOper": rowss['Childoper2'],
                        "childAltGrpRnk": rowss['ChildAltGrpRnk2'],
                        "child": [{
                            "Level": "L3",
                            "uuid": generate_uuid(),
                            "QOH": 0,
                            "QPA": rowss["Childqty3"],
                            "item": rowss['ChildItem3'],
                            "description": rowss['Childdescription3'],
                            "child_p_m_t": rowss['Childp_m_t3'],
                            "childAltGrp": rowss['ChildAltGrp3'],
                            "childOper": rowss['Childoper3'],
                            "childAltGrpRnk": rowss['ChildAltGrpRnk3'],
                            "child": [{
                                "Level": "L4",
                                "uuid": generate_uuid(),
                                "QOH": 0,
                                "QPA": rowss["Childqty4"],
                                "item": rowss['ChildItem4'],
                                "description": rowss['Childdescription4'],
                                "child_p_m_t": rowss['Childp_m_t4'],
                                "childAltGrp": rowss['ChildAltGrp4'],
                                "childOper": rowss['Childoper4'],
                                "childAltGrpRnk": rowss['ChildAltGrpRnk4'],
                                "child": [{
                                    "Level": "L5",
                                    "uuid": generate_uuid(),
                                    "QOH": 0,
                                    "QPA": rowss["Childqty5"],
                                    "item": rowss['ChildItem5'],
                                    "description": rowss['Childdescription5'],
                                    "child_p_m_t": rowss['Childp_m_t5'],
                                    "childAltGrp": rowss['ChildAltGrp5'],
                                    "childOper": rowss['Childoper5'],
                                    "childAltGrpRnk": rowss['ChildAltGrpRnk5'],
                                    "child": []
                                }] if rowss['ChildItem5'] != None else []
                            }] if rowss['ChildItem4'] != None else []
                        }] if rowss['ChildItem3'] != None else []
                    }] if rowss['ChildItem2'] != None else []
                })
            else:
                l1c = 0
                for x in jsonStructure:
                    if x['item'] == rowss['ChildItem1']:
                        l1c = 1
                        l2c = 0
                        for y in x['child']:
                            if y['item'] == rowss['ChildItem2']:
                                l2c = 1
                                l3c = 0
                                l4c = 0
                                for z in y['child']:
                                    if z['item'] == rowss['ChildItem3']:
                                        l3c = 1
                                        l4c = 0
                                        for a in z['child']:
                                            if a['item'] == rowss['ChildItem4']:
                                                l4c = 1
                                                l5c = 0
                                                for b in a['child']:
                                                    if b['item'] == rowss['ChildItem5']:
                                                        l5c = 1
                                                        pass
                                                if l5c == 0:
                                                    if rowss['ChildItem5'] == None:
                                                        print("None")
                                                    else:
                                                        a['child'].append({
                                                            "Level": "L5",
                                                            "QOH": 0,
                                                            "QPA": rowss["Childqty5"],
                                                            "item": rowss['ChildItem5'],
                                                            "description": rowss['Childdescription5'],
                                                            "child_p_m_t": rowss['Childp_m_t5'],
                                                            "childAltGrp": rowss['ChildAltGrp5'],
                                                            "childOper": rowss['Childoper5'],
                                                            "childAltGrpRnk": rowss['ChildAltGrpRnk5'],
                                                            "child": []
                                                        })
                                    if l4c == 0:
                                        if rowss['ChildItem4'] == None or rowss['ChildItem4'] == 'None':
                                            print("None")
                                        else:
                                            z['child'].append({
                                                "Level": "L4",
                                                "uuid": generate_uuid(),
                                                "QOH": 0,
                                                "QPA": rowss["Childqty4"],
                                                "item": rowss["ChildItem4"],
                                                "description": rowss['Childdescription4'],
                                                "child_p_m_t": rowss['Childp_m_t4'],
                                                "childAltGrp": rowss['ChildAltGrp4'],
                                                "childOper": rowss['Childoper4'],
                                                "childAltGrpRnk": rowss['ChildAltGrpRnk4'],
                                                "child": [{
                                                    "Level": "L5",
                                                    "uuid": generate_uuid(),
                                                    "QOH": 0,
                                                    "QPA": rowss['Childqty5'],
                                                    "item": rowss["ChildItem5"],
                                                    "description": rowss['Childdescription5'],
                                                    "child_p_m_t": rowss['Childp_m_t5'],
                                                    "childAltGrp": rowss['ChildAltGrp5'],
                                                    "childOper": rowss['Childoper5'],
                                                    "childAltGrpRnk": rowss['ChildAltGrpRnk5'],
                                                    "child": []
                                                }] if rowss['ChildItem5'] != None else []
                                            })
                                if l3c == 0:
                                    if rowss['ChildItem3'] == None or rowss['ChildItem3'] == 'None':
                                        print("None")
                                    else:
                                        y['child'].append({
                                            "Level": "L3",
                                            "uuid": generate_uuid(),
                                            "QOH": 0,
                                            "QPA": rowss["Childqty3"],
                                            "item": rowss["ChildItem3"],
                                            "description": rowss['Childdescription3'],
                                            "child_p_m_t": rowss['Childp_m_t3'],
                                            "childAltGrp": rowss['ChildAltGrp3'],
                                            "childOper": rowss['Childoper3'],
                                            "childAltGrpRnk": rowss['ChildAltGrpRnk3'],
                                            "child": [{
                                                "Level": "L4",
                                                "uuid": generate_uuid(),
                                                "QOH": 0,
                                                "QPA": rowss["Childqty4"],
                                                "item": rowss["ChildItem4"],
                                                "description": rowss['Childdescription4'],
                                                "child_p_m_t": rowss['Childp_m_t4'],
                                                "childAltGrp": rowss['ChildAltGrp4'],
                                                "childOper": rowss['Childoper4'],
                                                "childAltGrpRnk": rowss['ChildAltGrpRnk4'],
                                                "child": [{
                                                    "Level": "L5",
                                                    "uuid": generate_uuid(),
                                                    "QOH": 0,
                                                    "QPA": rowss['Childqty5'],
                                                    "item": rowss["ChildItem5"],
                                                    "description": rowss['Childdescription5'],
                                                    "child_p_m_t": rowss['Childp_m_t5'],
                                                    "childAltGrp": rowss['ChildAltGrp5'],
                                                    "childOper": rowss['Childoper5'],
                                                    "childAltGrpRnk": rowss['ChildAltGrpRnk5'],
                                                    "child": []
                                                }] if rowss['ChildItem5'] != None else []
                                            }] if rowss['ChildItem4'] != None else []
                                        })
                        if l2c == 0:
                            if rowss['ChildItem2'] == None or rowss['ChildItem2'] == 'None':
                                print("None")
                            else:
                                x['child'].append({
                                    "Level": "L2",
                                    "uuid": generate_uuid(),
                                    "QOH": 0,
                                    "QPA": rowss["Childqty2"],
                                    "item": rowss["ChildItem2"],
                                    "description": rowss['Childdescription2'],
                                    "child_p_m_t": rowss['Childp_m_t2'],
                                    "childAltGrp": rowss['ChildAltGrp2'],
                                    "childOper": rowss['Childoper2'],
                                    "childAltGrpRnk": rowss['ChildAltGrpRnk2'],
                                    "child": [{
                                        "Level": "L3",
                                        "uuid": generate_uuid(),
                                        "QOH": 0,
                                        "QPA": rowss["Childqty3"],
                                        "item": rowss["ChildItem3"],
                                        "description": rowss['Childdescription3'],
                                        "child_p_m_t": rowss['Childp_m_t3'],
                                        "childAltGrp": rowss['ChildAltGrp3'],
                                        "childOper": rowss['Childoper3'],
                                        "childAltGrpRnk": rowss['ChildAltGrpRnk3'],
                                        "child": [{
                                            "Level": "L4",
                                            "uuid": generate_uuid(),
                                            "QOH": 0,
                                            "QPA": rowss["Childqty4"],
                                            "item": rowss["ChildItem4"],
                                            "description": rowss['Childdescription4'],
                                            "child_p_m_t": rowss['Childp_m_t4'],
                                            "childAltGrp": rowss['ChildAltGrp4'],
                                            "childOper": rowss['Childoper4'],
                                            "childAltGrpRnk": rowss['ChildAltGrpRnk4'],
                                            "child": [{
                                                "Level": "L5",
                                                "uuid": generate_uuid(),
                                                "QOH": 0,
                                                "QPA": rowss['Childqty5'],
                                                "item": rowss["ChildItem5"],
                                                "description": rowss['Childdescription5'],
                                                "child_p_m_t": rowss['Childp_m_t5'],
                                                "childAltGrp": rowss['ChildAltGrp5'],
                                                "childOper": rowss['Childoper5'],
                                                "childAltGrpRnk": rowss['ChildAltGrpRnk5'],
                                                "child": []
                                            }] if rowss['ChildItem5'] != None else []
                                        }] if rowss['ChildItem4'] != None else []
                                    }] if rowss['ChildItem3'] != None else []
                                })
                if l1c == 0:
                    if rowss['ChildItem1'] == None or rowss['ChildItem1'] == 'None':
                        print("None")
                    else:
                        jsonStructure.append({
                            "Level": "L1",
                            "uuid": generate_uuid(),
                            "QOH": 0,
                            "QPA": rowss["Childqty1"],
                            "item": rowss["ChildItem1"],
                            "description": rowss['Childdescription1'],
                            "child_p_m_t": rowss['Childp_m_t1'],
                            "childAltGrp": rowss['ChildAltGrp1'],
                            "childOper": rowss['Childoper1'],
                            "childAltGrpRnk": rowss['ChildAltGrpRnk1'],
                            "child": [{
                                "Level": "L2",
                                "uuid": generate_uuid(),
                                "QOH": 0,
                                "QPA": rowss["Childqty2"],
                                "item": rowss["ChildItem2"],
                                "description": rowss['Childdescription2'],
                                "child_p_m_t": rowss['Childp_m_t2'],
                                "childAltGrp": rowss['ChildAltGrp2'],
                                "childOper": rowss['Childoper2'],
                                "childAltGrpRnk": rowss['ChildAltGrpRnk2'],
                                "child": [{
                                    "Level": "L3",
                                    "uuid": generate_uuid(),
                                    "QOH": 0,
                                    "QPA": rowss["Childqty3"],
                                    "item": rowss["ChildItem3"],
                                    "description": rowss['Childdescription3'],
                                    "child_p_m_t": rowss['Childp_m_t3'],
                                    "childAltGrp": rowss['ChildAltGrp3'],
                                    "childOper": rowss['Childoper3'],
                                    "childAltGrpRnk": rowss['ChildAltGrpRnk3'],
                                    "child": [{
                                        "Level": "L4",
                                        "uuid": generate_uuid(),
                                        "QOH": 0,
                                        "QPA": rowss["Childqty4"],
                                        "item": rowss["ChildItem4"],
                                        "description": rowss['Childdescription4'],
                                        "child_p_m_t": rowss['Childp_m_t4'],
                                        "childAltGrp": rowss['ChildAltGrp4'],
                                        "childOper": rowss['Childoper4'],
                                        "childAltGrpRnk": rowss['ChildAltGrpRnk4'],
                                        "child": [{
                                            "Level": "L5",
                                            "uuid": generate_uuid(),
                                            "QOH": 0,
                                            "QPA": rowss['Childqty5'],
                                            "item": rowss["ChildItem5"],
                                            "description": rowss['Childdescription5'],
                                            "child_p_m_t": rowss['Childp_m_t5'],
                                            "childAltGrp": rowss['ChildAltGrp5'],
                                            "childOper": rowss['Childoper5'],
                                            "childAltGrpRnk": rowss['ChildAltGrpRnk5'],
                                            "child": []
                                        }] if rowss['ChildItem5'] != None else []
                                    }] if rowss['ChildItem4'] != None else []
                                }] if rowss['ChildItem3'] != None else []
                            }] if rowss['ChildItem2'] != None else []
                        })
        return {"Level": "L0", "item": FG, "description": FG['Parentdescription1'].iloc[0], 'uuid': generate_uuid(), "child": jsonStructure}
    
    dx = []
    FGS = data.Parentitem1.unique()
    for x in FGS:
        print(x)
        d = doit(x)
        mongo_crud('', 0, 'pt', 'subassemblyV4_Amery', 'create', d, {})
    return "Created"
    # return
