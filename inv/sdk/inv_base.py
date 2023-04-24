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



class inv_base(get_session):

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
    
    def gen_cahcepath(self):

        """
            Internal function for genrating cahche location for storing  
            large results or memory unsafe results

            returns str(path)
        """

        return os.path.join(self.cache_store, f"{str(uuid.uuid4())}.json")
    
    def select_n(self, _list, sort_func, qty_key, n, reverse = False):

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




