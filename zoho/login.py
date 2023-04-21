""" 
    Intended for logging in zoho account via session
    for now user acceptence has not been tested, please provide
    validated id, password

    File Number = 3334449789803
    current_error = 1
"""

import requests, time, json, dill as pickel, os


class zoho_login(object):

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
        self.service = service
        self.session = requests.Session()


    def __validate_200(self, request):

        print(request)

        if request.status_code != 200:

            raise Exception("Unknown status code 3334449789803_1")
        

        return request
    

    def __pwd_uri(self, user):

        pwd_url = {"inventory":f'https://accounts.zoho{self.data_center}/signin/v2/primary/{user["lookup"]["identifier"]}/password?digest={user["lookup"]["digest"]}&cli_time={int(time.time())}&servicename=ZohoInventory&serviceurl=https%3A%2F%2Finventory.zoho{self.org_id}%2Fapp%2F{self.org_id}&signupurl=https%3A%2F%2Fwww.zoho{self.data_center}%2Finventory%2Fsignup'}
    

        return pwd_url[self.service]
    

    def __service_uri(self):

        base_connect = {"inventory":[f"https://inventory.zoho{self.data_center}",
                                      f"https://accounts.zoho{self.data_center}/signin?servicename=ZohoInventory&signupurl=https://www.zoho{self.data_center}/inventory/signup&serviceurl=https%3A%2F%2Finventory.zoho{self.data_center}%2Fapp%2F{self.org_id}",
                                      f"mode=primary&cli_time={int(time.time())}&servicename=ZohoInventory&serviceurl=https%3A%2F%2Finventory.zoho{self.data_center}%2Fapp%2F{self.org_id}&signupurl=https%3A%2F%2Fwww.zoho{self.org_id}%2Finventory%2Fsignup",
                                      "ZohoInventory"]}
        


        

        return base_connect[self.service]
    

    def __make_header_user(self, cookie_jar):

        headers = {'inventory':{'Accept': '*/*',
        'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'accounts.zoho.in',
        'Origin': f'https://accounts.zoho{self.data_center}',
        'Referer': f'https://accounts.zoho{self.data_center}/signin?servicename=ZohoInventory&signupurl=https://www.zoho{self.data_center}/inventory/signup&serviceurl=https%3A%2F%2Finventory.zoho{self.data_center}%2Fapp%2F{self.org_id}',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
        'X-ZCSRF-TOKEN': f'iamcsrcoo={cookie_jar["iamcsr"]}'}}


        self.session.headers = headers[self.service]



    def __make_header_nrm(self):

        headers = {'inventory':{'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'max-age=0',
                        'Connection': 'keep-alive',
                        'Host': f'inventory.zoho{self.data_center}',
                        'Referer': f'https://accounts.zoho{self.data_center}/',
                        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'}}
        
        self.session.headers = headers[self.service]






    def __login_ritual(self):

        connection_uri, account_uri, login_mode, service_name = self.__service_uri()
        
        self.__validate_200( request = self.session.get(connection_uri) )
        
        account = self.__validate_200( request = self.session.get(account_uri) )

        self.__make_header_user(cookie_jar = account.cookies.get_dict())

        user_request = self.session.post(f"https://accounts.zoho{self.data_center}/signin/v2/lookup/{self.user_id}", data=login_mode)

        #TO_DO  user_accept_check
        
        z_user = user_request.json()

        pwd = json.dumps({'passwordauth':{'password':self.password}})

        self.__validate_200(self.session.post(self.__pwd_uri(user = z_user), data = pwd))

        self.__make_header_nrm()


    def __write_login(self):

        with open(os.path.join(self.login_store, f"{self.user_id}.pkl"), "wb+") as f:

            pickel.dump(self.session, f)

    
    def login(self):

        self.__login_ritual()
        self.__write_login()


        
""" 

zl = zoho_login(login_store = os.path.join(os.getcwd(), "pickel"), user_id = "it.kvtek@outlook.com", password = "IT4kvtek",\
                  data_center = ".in", org_id = "60008720898", service = "inventory")

zl.login()
 """
    


    

        