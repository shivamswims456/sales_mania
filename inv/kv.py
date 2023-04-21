import os
from ireports import ireports


irv = ireports(login_store = os.path.join(os.getcwd(), "pickel"),
               cache_store = os.path.join(os.getcwd(), "cache"),
               user_id = "it.kvtek@outlook.com",
               password = "IT4kvtek",
               data_center = ".in",
               org_id = "60008720898")

""" item_qty = [["536460000007476086",	9],
            ["536460000015459322",	31],
            ["536460000011084352",	45],
            ["536460000011093685",	14],
            ["536460000011095759",	93],
            ["536460000011092648",	32],
            ["536460000018385606",	2],
            ["536460000019764308",	1],
            ["536460000018603392",	2],
            ["536460000018373774",	37]]




data = irv.valuation_by(item_qty = item_qty, type = "bills", opening = True, reverse = False, warehouse = "Main Store")
 """
import csv



with open("inv.csv", "r") as f:

    l = list(csv.reader(f))
    n = 100

    t = [l[i:i + n] for i in range(0, len(l), n)]

    for index, chunk in enumerate([l[i:i + n] for i in range(0, len(l), n)]):

        data = irv.valuation_by(item_qty = chunk, type = "bills", opening = True, reverse = False, warehouse = "Main Store")

        
        with open(f"data_{index}.csv", "w+", newline='') as fp:

            writer = csv.writer(fp)

            for item_id, value in data.items():

                writer.writerow([item_id, value])

