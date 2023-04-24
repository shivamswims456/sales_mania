"""
    Inteded for scrapping data from invoice page and invoice details

    file_number:3334449789807
    last_error:1

"""

from inv.sdk.inv_base import inv_base

class inv_invoices(inv_base):

    def __init__(self, login_store, cache_store, user_id, password, data_center, org_id) -> None:
        super().__init__(login_store, cache_store, user_id, password, data_center, org_id)

    
    def get_invoice_count(self):

        "https://inventory.zoho.in/api/v1/invoices?page=1&per_page=25&filter_by=Status.All&sort_column=created_time&sort_order=D&response_option=2&organization_id=60008720898"


    def get_invoices(self, start, segment, count):


        valid_segment = (10, 25, 50, 100, 200)

        if

        invoice_page_request_url = f"https://inventory.zoho{self.data_center}/api/v1/invoices?page=1&per_page=25&filter_by=Status.All&sort_column=created_time&sort_order=D&usestate=true&organization_id={self.org_id}"