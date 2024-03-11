def arrToJ(arr,fg,item):
    arrSet = {}
    for i in arr:
        arrSet.update({
            "{}_{}_{}".format(fg,item,i['FG']):{
                "FG": i["FG"],
                "allocated_qty": i["allocated_qty"],
                "ctb": i["ctb"],
                "ctb_qoh": i["ctb_qoh"],
                "potential_ctb": i["potential_ctb"],
                "qpa": i["qpa"],
                "req_ctb": i["req_ctb"]
            }
        })
    return arrSet