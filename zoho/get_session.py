""" 
File Number = 3334449789804
current_error = 2
"""
import os, dill as pickel
from .login import zoho_login

class get_session(object):


    def __init__(self, login_store, user_id, password,\
                  data_center, org_id, service) -> None:
        

        """ 
            @login_store:str    = path where pickeles should be written
            @user_id:str        = login user id of zoho user
            @password:str       = password of zoho usr
            @data_center:str    = data center in which account is located
            @service:str        = service for which login has to be made
        """
        
        self.login_store = login_store
        self.user_id = user_id
        self.password = password
        self.data_center = data_center
        self.org_id = org_id
        self.session = None
        self.validation_rounds = 0
        self.service = service

        self.__set_session()
        self.__validate_session()


    


    def validate_200(self, response):

        if response.status_code != 200:

            raise Exception("Request invalidated 3334449789804_1")
        
        return response
    
    def to_json(self, response):

        return response.json()
    
    


    def __validate_session(self):

        #fetch orgs for session validation
        try:
            
            self.validate_200(response = self.session.get(f"https://inventory.zoho.in/api/v1/activeorganizations?organization_id={self.org_id}"))

        except Exception:

            if self.validation_rounds > 0:

                raise Exception("Unable to process request 3334449789804_2")
            

            zl = zoho_login(login_store = self.login_store, user_id = self.user_id, password = self.password,\
                            data_center = self.data_center, org_id = self.org_id, service = self.service)
            
                

            zl.login()
            self.__set_session()
            self.validation_rounds += 1
            self.__validate_session()



        
        

    def __set_session(self):

        with open(os.path.join(self.login_store, f"{self.user_id}.pkl"), "rb") as f:

            self.session = pickel.load(f)

