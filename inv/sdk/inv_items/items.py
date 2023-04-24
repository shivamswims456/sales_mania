"""
    inteded for scrapping data from item page and item details

    file_number:3334449789806
    last_error:5

"""
import os, json, time
from inv.sdk.inv_base import inv_base

class inv_items(inv_base):

    def __init__(self, login_store, cache_store, user_id, password, data_center, org_id) -> None:
        super().__init__(login_store, cache_store, user_id, password, data_center, org_id)


    def get_transactions_bills(self, item_id, last_n, reverse = False):

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

            raise Exception("Unable to fetch reords 3334449789806_5")
        _error:5

        return transactions

    def get_transaction_to(self, item_id, last_n, reverse = False):
        pass    

    
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
            
            raise Exception("Invalid count 3334449789806_2")
        _error:5


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

                raise Exception("Unable to fetch item 3334449789806_3")

            
            time.sleep(self.FETCH_BUFFER)


        #writing results 


        store_path = self.gen_cahcepath()
        
        with open(store_path, "w+") as f:

            write_items = item_collection[:count]

            json.dump(write_items, f, indent=4)
            

        return store_path

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

            raise Exception("Unable to fetch item 3334449789806_1")
        _error:5
        return item
    
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




isdk = inv_items(login_store = os.path.join(os.getcwd(), "pickel"), cache_store = os.path.join(os.getcwd(), "cache"),  user_id = "it.kvtek@outlook.com", password = "IT4kvtek",\
                  data_center = ".in", org_id = "60008720898")




#print(isdk.get_rotations(fetch_count=48, segment=25, start=48))
#print(isdk.get_opening(item_id = "536460000011084352", warehouse_id="536460000000014524"))
#isdk.get_items(start=0, segment=10, count=33)
##print(isdk.get_transactions(item_id = "536460000011084352", last_n=100, type = "bills", reverse=True))
