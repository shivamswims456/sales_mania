"""
    This module is inteded to geenrate analytical reports with zoho inventory
"""
import os, time
from sdk.inv_sdk import inv_sdk
from collections import defaultdict

class ireports(object):


    def __init__(self, login_store, cache_store, user_id, password, data_center, org_id) -> None:
        
        """ 
            @login_store        = path where login sessions are stored
            @cache_store        = path where temp files will be stored
            @login_store:str    = path where pickeles should be written
            @user_id:str        = login user id of zoho user
            @password:str       = password of zoho usr
            @data_center:str    = data center in which account is located
            
        """
        self.isdk = inv_sdk(login_store = login_store,
                            cache_store = cache_store,
                            user_id = user_id,
                            password = password,
                            data_center = data_center,
                            org_id = org_id)
        

    
        
    def valuation_by(self, item_qty, type, opening, warehouse, reverse):

        """ 
            #opening has to be implemented based on warehouse,
            using hack shift methods for bills assumimg that every bill 
            and opening are from same warehouse

            #as we can not get opening stock addition date, all opening shall by default will added to last of fifo records
        """

        valuation_keys = {"bills":{"unit_price":"item_price", "qty":"item_quantity"}}
        
        valuation_chart = defaultdict(int)

        
        
        for item_id, qty in item_qty:

            print(item_id)

            qty = float(qty)

            transactions = []

            if opening:

                item_opening = self.isdk.get_opening(item_id = item_id, warehouse_id = warehouse)

                transactions = [{valuation_keys[type]["unit_price"]:item_opening["initial_stock_rate"],
                                valuation_keys[type]["qty"]:item_opening["initial_stock"]}]


            
            transactions = self.isdk.get_transactions(item_id = item_id,
                                               last_n = qty, type = type,
                                               reverse = reverse)[0] + transactions
                    
            #print(transactions)
            
            #TO-DO: transactions implementations over bill qty check left

            for each in transactions:
                

                unit_price = each[valuation_keys[type]["unit_price"]]
                doc_qty = each[valuation_keys[type]["qty"]]

                if qty <= 0:

                    break

                if qty >= doc_qty:

                    valuation_chart[item_id] += doc_qty * unit_price

                else:

                    valuation_chart[item_id] += qty * unit_price

                
                qty -= doc_qty

            
            time.sleep(1)


        return valuation_chart






""" 


irv = ireports(login_store = os.path.join(os.getcwd(), "pickel"),
               cache_store = os.path.join(os.getcwd(), "cache"),
               user_id = "it.kvtek@outlook.com",
               password = "IT4kvtek",
               data_center = ".in",
               org_id = "60008720898")

print(irv.valuation_by(item_qty = [["536460000007555518", 100]], type = "bills", opening = True, reverse = False, warehouse = "Main Store")) """