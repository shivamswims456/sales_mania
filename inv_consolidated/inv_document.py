from sales_mania.zoho.get_session import get_session
from collections import defaultdict
import os, copy, datetime, json
import urllib.parse

class inv_document( get_session ):

    def __init__(self, login_store, cache_store, user_id, password, data_center, org_id) -> None:
        self.service = 'inventory'
        super().__init__(login_store, user_id, password, data_center, org_id, service = self.service)



    def __add_path(self, path_addon):

        path_addon = ""

        if len(path_addon) > 0:

            path_addon = f"/{'/'.join(path_addon)}"

        return path_addon
    

    def __get_params(self, document, attribute, extra_params = {}):

        document_map = {
                        "items":{
                                "item_count":{'page': '1', 'per_page': '200', 'filter_by': 'Status.All',
                                 'sort_column': 'created_time', 'response_option': '2'},
                                
                                "item_page":{'filter_by': 'Status.All', 'sort_column': 'created_time',
                                 'sort_order': 'A', 'usestate': 'true'},

                                 "item_details":{}
                                },
                        "report_activity":{
                                "report_activity":{"sort_column":"date", "sort_order":"D", "response_option":"1"}
                                }
                        }
        

        
        #treateing base cofig as immute to preserve config for future use
        temp = copy.deepcopy(document_map[document][attribute])
        temp.update(extra_params)

        temp = {param: json.dumps(value) if type(value) in [dict, list] else value  for param, value in temp.items()}
        return urllib.parse.urlencode(temp, quote_via=urllib.parse.quote)
    
    
    def __get_base_uri(self, document, path_addon = []):

        api_names = {"items":"items",
                     "report_activity":"reports/activitylogs"}

        path_addon = self.__add_path(path_addon = path_addon)

        print(document)

        return f"https://inventory.zoho{self.data_center}/api/v1/{api_names[document]}{path_addon}?organization_id={self.org_id}&"
    

    def __find_chained(self, response, chain_list):
        
        final_response = None

        for each in chain_list:

            if final_response == None:

                final_response = response[each]

            else:

                final_response = final_response[each]


        return final_response

    def __fetch_result(self, document, attribute, path_addon = [], extra_params = {}):

        keys = {"item_count":
                    {"status":"message", "data":["page_context", "total"], "success":"success"},
                "item_page":
                    {"status":"message", "data":["items"], "success":"success"},
                "item_details":
                    {"status":"message", "data":["items"], "success":"success"},
                "report_activity":
                    {"status":"message", "data":["activitylogs"], "success":"success"}
                }
        

        url = f"{self.__get_base_uri(document=document, path_addon=path_addon)}{self.__get_params(document=document, attribute = attribute, extra_params = extra_params)}"
        
        zoho_resp = self.session.get(url) 
        
        response = self.to_json(
            response = self.validate_200(
                response = zoho_resp
            )
        )


        status = response[keys[attribute]["status"]]

        if status == keys[attribute]["success"]:
            

            return self.__find_chained(response = response, chain_list = keys[attribute]["data"]) 
        
        else:

            raise Exception(f"Can not collect documet {document} with attribute {attribute} failed with {status}")
        

    def __document_check(self, relations, document, segment = None):

        
        
        if relations.get(document) is False:

            raise Exception(f"Document {document} not avaialble")
        
        if segment != None and segment not in relations.get(document)[1]:

            raise Exception(f"Segment {segment} of {document} not possible")

        
        return True



    def get_document_page_n(self, document, segment, round, extra_params = {}, path_addon = []):

        """
            if directly accessing this function, its user reponsiblilty to 
            catch out of range page exception 
            {"document":["attribute_query_name", None/[Allowed segments], ]}
        """
        
        page_relation = {"items":["item_page", None],
                         "report_activity":["report_activity", None]}

        self.__document_check(relations = page_relation, document = document)

        __extra_params = {
                            "page":round, "per_page":segment
                         }
        
        extra_params.update(__extra_params)

        return self.__fetch_result(document = document,
                                   attribute = page_relation[document][0],
                                   extra_params = extra_params,
                                   path_addon = path_addon)
    

    def get_document_page_range(self, document, segment, start_page, end_page, extra_params):

        results = []

        for round in range(start_page, end_page + 1):

            results.append(self.get_document_page_n(document = document, segment = segment,
                                     round = round, extra_params = extra_params))

        return results


    def get_document_detail(self, document, document_id):

        details_relations = {"items":["item_details", None, [document_id, "inventorysummary"]]}

        return self.__fetch_result(document=document, attribute=details_relations[document][0],
                            path_addon=details_relations[document][2], extra_params={})
        


    def get_documents_details(self, documents, document_ids, sort_document = False):

        document_store = defaultdict(list)

        for stick0 in documents if sort_document else document_ids:

            for stick in document_ids if sort_document else documents:

                document_id = stick if sort_document else stick0
                document = stick0 if sort_document else stick

                documet_detail = self.get_document_detail(document = document,
                                                          document_id = document_id)

                document_store[stick0].append(documet_detail)


        return document_store
    

    def get_report_activity(self, round, start_date = None, end_date = None,
                            static_range = None, document_filters = [],
                            additional_filters = [], columns = []):
        

        allowed_statics = ["today","week","month","quarter","year",
         "day_1","week_1","month_1","quarter_1","year_1"]
        
        documents_possible = ["bill","vendor_payment","invoice","customer_payment",
                              "item","purchaseorder","salesorder","package","shipment_order",
                              "purchase_receive","stripe","users","contact","vendor",
                              "vat_return","bill_of_entry","shipping_bill"] 
        

        if len(columns) == 0:

            columns = [{"field":"date","group":"report"},
                       {"field":"transaction_type","group":"report"},
                       {"field":"description","group":"report"}]

        
        
        if static_range not in allowed_statics:

            raise Exception(f"static_range {static_range} not allowed for this report")




        
        if start_date != None:
        
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        
        if end_date != None:
            
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")


        
        error_documents = set(document_filters) - set(documents_possible)
        
        if len(error_documents) != 0:

            raise Exception(f"Filter for {error_documents} are not possible, posssible filters are {documents_possible}")
        

        select_rule = [{"index":1,
                        "field":"transaction_type",
                        "value":document_filters,
                        "comparator":"in",
                        "group":"report"}]
                                 
        
         
        

        columns = [{"field":"date","group":"report"},
                   {"field":"transaction_type","group":"report"},
                   {"field":"description","group":"report"}]


        return self.get_report(document = "report_activity", round = round,
                               static_range = static_range,
                               end_date = end_date, start_date = start_date,
                               select_rule = select_rule, select_columns = columns,
                               additional_filters = additional_filters)
        

        


        



            

    def get_report(self, document, round, static_range = None,
                   start_date = None, end_date = None,
                   select_rule = [], select_columns = [],
                   additional_filters = [], extra_params = {}):
        
        static_range_map = {"today":"CreatedDate.Today",
                            "week":"CreatedDate.ThisWeek",
                            "month":"CreatedDate.ThisMonth",
                            "quarter":"CreatedDate.ThisQuarter",
                            "year":"CreatedDate.ThisYear",
                            "day_1":"CreatedDate.PreviousDay",
                            "week_1":"CreatedDate.PreviousWeek",
                            "month_1":"CreatedDate.PreviousMonth",
                            "quarter_1":"CreatedDate.PreviousQuarter",
                            "year_1":"CreatedDate.PreviousQuarter",
                            "range":"CreatedDate.CustomDate"}
        
        
        if all(each == None for each in [start_date, end_date, static_range]):
            
            raise Exception("Please provide start_date and end_date or static_range")

        if None not in [start_date, end_date] and start_date > end_date:

            raise Exception("start_date can not be earlier than end_date")
        

        

        if static_range == "range":

            extra_params.update({"from_date": start_date.strftime("%Y-%m-%d"),
                                 "to_date":end_date.strftime("%Y-%m-%d")})
        
        
        for index, rule in enumerate(additional_filters):
            
            rule.update({"index": index + len(select_rule)})

            select_rule.append(rule)


        criteria_string = f"{' AND '.join([str(each) for each in range(1, len(select_rule) + 1)])}"

        __for_urlencode = {"select_columns": select_columns, "filter_by":static_range_map[static_range]}

        if len(select_rule) > 0:

            __for_urlencode.update({"rule":{"columns":select_rule, "criteria_string":criteria_string}})


        __for_urlencode.update(extra_params)
        extra_params = __for_urlencode

        
        return self.get_document_page_n(document=document, segment=200, round=round, extra_params=extra_params)




    def get_document_count(self, document):

        count_relation = {"items":["item_count", None]}

        self.__document_check(relations = count_relation, document = document)

        return self.__fetch_result(document = document,
                                    attribute = count_relation[document][0],
                                    extra_params = {}, segment = None, )



        

document = inv_document(login_store = os.path.join(os.getcwd(), "sales_mania", "pickel"), cache_store = os.path.join(os.getcwd(), "sales_mania", "cache"),  user_id = "it.kvtek@outlook.com", password = "IT4kvtek",\
                  data_center = ".in", org_id = "60008720898")

#print(document.get_document_count("items"))
#print(document.get_document_page_n(document = "items", segment=10, round=1))
#print(document.get_document_detail(document = "items", document_id = "536460000007476086"))
print(document.get_report_activity(round=1, start_date=None, end_date=None, static_range="year",
                                  document_filters=["bill"], additional_filters=[], columns=[]))