"""
    
    intended for serving as base scrapper for inventory,
    will take login from pickeled session or zoho/login.py

    file_number:3334449789805
    current_error:4

"""

import os, dill as pickel
import sys, time, uuid, json
from datetime import datetime
sys.path.append( str(os.path.join(os.getcwd())))

from zoho.get_session import get_session



class inv_sdk(get_session):

    def __init__(self, login_store, cache_store, user_id, password,\
                  data_center, org_id) -> None:
        

        """ 
            @login_store:str    = path where pickeles should be written
            @cache_store:str    = path where caches are to be stored
            @user_id:str        = login user id of zoho user
            @password:str       = password of zoho usr
            @data_center:str    = data center in which account is located
            @org_id:str         = zoho assigned org id
        """

        self.login_store = login_store
        self.cache_store = cache_store
        self.user_id = user_id
        self.password = password
        self.data_center = data_center
        self.org_id = org_id
        self.session = None
        self.validation_rounds = 0
        self.service = 'inventory'
        self.FETCH_BUFFER = 1

        get_session.__init__(self, login_store = self.login_store,
                                   user_id = self.user_id,
                                   password = self.password,
                                   data_center = self.data_center,
                                   org_id = self.org_id,
                                   service = self.service)
    
    def __gen_cahcepath(self):

        """
            Internal function for genrating cahche location for storing  
            large results or memory unsafe results

            returns str(path)
        """

        return os.path.join(self.cache_store, f"{str(uuid.uuid4())}.json")
    
    def __select_n(self, _list, sort_func, qty_key, n, reverse = False):

        """
            Api pagination helper

            @_list:list         = list of dicts which are to be shorted
            @sort_func:lambda   = function which will dictate sort conditions
            @qty_key:str        = key of list[dict] which yields qty in doc
            @n:float            = number till which document has to be fetched
            @reverse:bool       = True:decending/False:ascending             

            returns   lsit(dict(documents), float(unacc_qty))
        """

        sorted_data = sorted(_list, key = sort_func, reverse = reverse)


        counted_data = []
        qty_unacc = 0
        summed_qty = sum([each[qty_key] for each in _list])
        
        if n > summed_qty:

            qty_unacc = summed_qty - n


        for each in sorted_data:

            counted_data.append(each)
            
            n -= each[qty_key]

            if n <= 0:
                
                break
        
            

        return [counted_data, qty_unacc]
        
    def __get_transactions_bills(self, item_id, last_n, reverse = False):

        """
            internal method for parsing bills filtered on basis of items
            default size of fetch is 200

            @item_id:str     = item_id for which bills have to fetched
            @last_n:float    = qty till which bill has to fetched
            @reverse:bool    = False:descending/True:ascending

            returns list(dict(bills))
        """

        transactions = None


        transaction_bill_request_url = f"https://inventory.zoho{self.data_center}/api/v1/items/transactions/bills?page=1&per_page=200&sort_order=D&sort_column=date&item_id={item_id}&organization_id={self.org_id}"


        transactions_bill = self.to_json(
                        response = self.validate_200( response = self.session.get( transaction_bill_request_url )) 
        )

        #print(transactions_bill)


        if transactions_bill["message"] == "success":

            transactions = self.__select_n(_list = transactions_bill["bills"],
                                           sort_func = lambda bill: datetime.strptime( bill["date"], "%Y-%m-%d"),
                                            qty_key = "item_quantity", n = last_n, reverse = reverse)
            

            
            


        else:

            raise Exception("Unable to fetch reords 3334449789805_5")
        

        return transactions

    def __get_transaction_to(self, item_id, last_n, reverse = False):
        pass

    def get_transactions(self, item_id, last_n, type, reverse):

        """
            Wrapper around internal fetch document methods

            @item_id:str    = item_id for which documents have to fetched
            @last_n:float   = qty till which document has to fetched
            @type:str       = type of document to be fetched
                              ["bills"]
            @reverse:bool   = True:Descending/False:Ascending


            returns list(dict(documents))     
        """

        #not confirmed about paginations in the sidebar
        #implementing for first 200

        transaction_map = {"bills":self.__get_transactions_bills}

        return transaction_map[type](item_id = item_id, last_n = last_n, reverse = reverse)

    def get_item(self, item_id):

        """
            Function for fetching single detailed item

            @item:str   = item_id for which details has to fetched

            returns dict(item) 
        """

        
        #https://inventory.zoho.in/api/v1/items/536460000007285789?organization_id=60008720898

        item = False

        item_request_url = f"https://inventory.zoho{self.data_center}/api/v1/items/{item_id}?organization_id={self.org_id}"

        item_data = self.to_json(
                                    response = self.validate_200(response = self.session.get(item_request_url))
                                )
        
        if item_data["message"] == "success":

            item = {item_id:item_data["item"]}

        else:

            raise Exception("Unable to fetch item 3334449789805_1")
        
        return item
    
    def item_count(self):

        """
            method for finding total items in account

            returns int(item_count) 
        """
        
        item_count_request_url = f"https://inventory.zoho{self.data_center}/api/v1/items?page=1&per_page=200&filter_by=Status.All&sort_column=created_time&sort_order=A&response_option=2&organization_id={self.org_id}"

        item_response = self.to_json(
                        response = self.validate_200(response = self.session.get(item_count_request_url))
                    )
        
        return item_response["page_context"]["total"]

    def get_rotations(self, fetch_count, segment, start, total_count):

        """
            method for determining number of api rotations needed to fetch n documents
            

            @fetch_count:int = number of documents to be fetched
            @segment:int     = segment in which rotations are to be made
            @start:int       = document start point
        
            returns [int(start_page), int(end_page)] 
        """

        #determing start

        if start <= segment:

            start_page = 1

        else:
            
            start_page = int(start/segment) + 1


        #determining end

        if fetch_count <= segment:

            end_index = 1

        else:

            end_count = (start + fetch_count)/segment
            end_round = round(end_count)
            end_index = end_round + 1 if end_count > end_round else end_round

        
        #since range works till [index} so

        end_page = end_index + 1


         


        return start_page, end_page

    def get_items(self, start, segment, count):


        """
            method for fetching list of items in pages 
            @start:int      = start point
            @segment:int    = segment in which rotations have to be made
            @count:int      = number of items to be fetched 

            returns path_file_cahce:str
        """


        valid_segments = (10, 25, 50, 100, 200)
        item_collection = []

        #validateing segment

        if segment not in valid_segments:
            
            raise Exception("Invalid count 3334449789805_2")
        


        #determining start-end page
        item_count = self.item_count()
        start_page, end_page = self.get_rotations(fetch_count = count, segment = segment,\
                           start = start, total_count = item_count)
        
        
        
        

        for round in range(start_page, end_page):
            
            #page request cycle

            item_page_request_url = f"https://inventory.zoho{self.data_center}/api/v1/items?page={round}&per_page={segment}&filter_by=Status.All&sort_column=created_time&sort_order=A&usestate=true&organization_id={self.org_id}"
            items_response = self.to_json(
                response=self.validate_200( response = self.session.get(item_page_request_url) )
            )
            
            if items_response["message"] == "success":

                item_collection += items_response["items"]
                
            else:

                raise Exception("Unable to fetch item 3334449789805_3")

            
            time.sleep(self.FETCH_BUFFER)


        #writing results 


        store_path = self.__gen_cahcepath()
        
        with open(store_path, "w+") as f:

            write_items = item_collection[:count]

            json.dump(write_items, f, indent=4)
            

        return store_path

    def get_opening(self, item_id, warehouse_id = None):

        """
            child function to get item, get opening/s of warehouse
            item_id:str = item_id of the item
            warehouse:str = name of the warehouse

            
            returns dict(item's_warehouse_details)
        """

        warehouse_details = self.get_item(item_id)[item_id]["warehouses"]

        if warehouse_id != None:

            for _warehouse in warehouse_details:

                #print(_warehouse)

                if  _warehouse["warehouse_id"] == warehouse_id:

                    warehouse_details = _warehouse
                    break

                

        return warehouse_details



isdk = inv_sdk(login_store = os.path.join(os.getcwd(), "pickel"), cache_store = os.path.join(os.getcwd(), "cache"),  user_id = "it.kvtek@outlook.com", password = "IT4kvtek",\
                  data_center = ".in", org_id = "60008720898")




#print(isdk.get_rotations(fetch_count=48, segment=25, start=48))
#print(isdk.get_opening(item_id = "536460000011084352", warehouse_id="536460000000014524"))
#isdk.get_items(start=0, segment=10, count=33)
##print(isdk.get_transactions(item_id = "536460000011084352", last_n=100, type = "bills", reverse=True))



