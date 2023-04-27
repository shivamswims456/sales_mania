from django.db import models

# Create your models here.





class zi_documents(models.Model):

    name = models.CharField(max_length=30)



class langs(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(45)
    formatted = models.CharField(105)


class custom_fields(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    value = models.CharField(max_length=10024, default=None)
    value_float = models.FloatField(default=None)
    zi_document = models.ForeignKey(zi_documents, on_delete=models.CASCADE)



class chart_of_accounts(models.Model):

    zid = models.PositiveBigIntegerField()
    account = models.CharField(max_length=45)
    parent_account = models.ForeignKey("self", on_delete=models.CASCADE)


class comment_type(models.Model):

    name = models.CharField(max_length=45)




class comments(models.Model):

  zid = models.PositiveBigIntegerField()
  description = models.CharField(105)
  commented_by_id = models.PositiveBigIntegerField() 
  comment_type = models.ForeignKey(comment_type, on_delete=models.CASCADE)
  date_with_time = models.DateTimeField()
  date_description = models.CharField(105)
  operation_type = models.CharField(45)



class country(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=12)
    formatted = models.CharField(max_length=105)


class state(models.Model):

    name = models.CharField(max_length=12)
    formatted = models.CharField(max_length=105)
    parent_country = models.ForeignKey(country, on_delete=models.CASCADE)

class city(models.Model):

    name = models.CharField(max_length=12)
    formatted = models.CharField(max_length=105)
    parent_sate = models.ForeignKey(state, on_delete=models.CASCADE)


class currency(models.Model):

    zid = models.PositiveBigIntegerField()
    currency_code = models.CharField(max_length=12)
    currency_symbol = models.CharField(max_length=12)
    price_precision = models.IntegerField()
    exchange_rate = models.FloatField()


class addresses(models.Model):

    zid = models.PositiveBigIntegerField()
    attention = models.CharField(max_length=105)
    address = models.CharField(max_length=105)
    street2 = models.CharField(max_length=105)
    city = models.ForeignKey(city, on_delete=models.CASCADE)
    state_code = models.ForeignKey(state, on_delete=models.CASCADE)
    country = models.ForeignKey(country, on_delete=models.CASCADE)
    zip = models.CharField(max_length=12)  
    phone = models.CharField(max_length=13)
    


class tags(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=15)
    parent_tag = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)




class base_measuring_units(models.Model):
   
   unit = models.CharField(max_length=15)


class measuring_unit(models.Model):
   
    name = models.CharField(max_length=15)
    base_unit = models.ForeignKey(base_measuring_units,
                                  on_delete=models.SET_NULL,
                                  null=True)
    
    conversion_factor = models.FloatField()
    conversion_precision = models.IntegerField()

    




class dimensions(models.Model):

    zid = models.PositiveBigIntegerField()
    length = models.FloatField()
    width = models.FloatField()
    weight = models.FloatField()
    weight_unit = models.ForeignKey(measuring_unit, on_delete=models.CASCADE)
    demension_unit = models.ForeignKey(measuring_unit, on_delete=models.CASCADE)        




class default_tax_zones(models.Model):

    name = models.CharField(max_length=45)
    #business_gst, personal_gst



class default_tax_types(models.Model):

    zid = models.PositiveBigIntegerField()
    zone = models.ForeignKey(default_tax_zones, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    formatted = models.CharField(max_length=105)
    zi_document = models.ForeignKey(zi_documents, on_delete=models.CASCADE)





class default_taxes(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    formatted = models.CharField(max_length=105)
    value = models.FloatField()
    type = models.ForeignKey(default_tax_types, on_delete=models.CASCADE)
    is_source_deducted = models.BooleanField(default=False) #for TDS





class default_tax_exemption(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    reason = models.CharField(max_length=105)


class default_payment_terms(models.Model):

    label = models.CharField(max_length=45)
    description = models.CharField(max_length=105)


class sales_channels(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    z_document = models.ForeignKey(zi_documents, on_delete=models.CASCADE)


class source(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=105)
    format = models.CharField(max_length=45)


class statues(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(45)
    zi_document = models.ForeignKey(zi_documents, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE)




class balance_types(models.Model):

    name = models.CharField(max_length=45)
    document = models.ForeignKey(zi_documents, on_delete=models.CASCADE)


class balance_store(models.Model):

    zid = models.PositiveBigIntegerField()
    balance_type = models.ForeignKey(balance_types, on_delete=models.CASCADE)
    balance = models.FloatField()
    receiveable = models.FloatField()
    precision = models.IntegerField()
    payable = models.FloatField()
    currency = models.ForeignKey(currency, on_delete=models.CASCADE)
    is_base_currency = models.BooleanField(default=False)



class contact_sub_type(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    format = models.CharField(max_length=105)
    parent = models.ForeignKey(zi_documents, on_delete=models.CASCADE)


class contacts(models.Model):

    zid = models.PositiveBigIntegerField()
    contact_name = models.CharField(105)
    company_name = models.CharField(105)
    first_name = models.CharField(45)
    last_name = models.CharField(45)
    designation = models.CharField(105)
    department = models.CharField(105)
    website = models.URLField()
    is_bcy_only_contact = models.BooleanField()
    is_credit_limit_migration_completed = models.BooleanField()
    lang = models.ForeignKey(langs, on_delete=models.SET_NULL, null=True)
    contact_salutation = models.CharField(max_length=5)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    mobile = models.CharField(max_length=13)
    has_transaction = models.BooleanField()
    contact_type = models.ForeignKey(zi_documents, on_delete=models.CASCADE)
    customer_sub_type = models.ForeignKey(contact_sub_type, on_delete=models.CASCADE)
    owner_id = models.ForeignKey() #tobemade
    source = models.ForeignKey(source, on_delete=models.CASCADE)
    twitter = models.URLField()
    facebook = models.URLField()
    payment_terms = models.ManyToManyField(default_payment_terms)
    credit_limit_exceeded_amount = models.FloatField()
    currency = models.ForeignKey(currency, on_delete=models.CASCADE)
    can_show_customer_ob = models.BooleanField()
    can_show_vendor_ob = models.BooleanField()
    opening_balance = models.ForeignKey(balance_store, on_delete=models.SET_NULL)
    outstanding_ob = models.ForeignKey(balance_store, on_delete=models.SET_NULL)
    unused_credits = models.ForeignKey(balance_store, on_delete=models.SET_NULL)
    unused_retainer_payments = models.ForeignKey(balance_store, on_delete=models.SET_NULL)
    status = models.ForeignKey(statues, on_delete=models.SET_NULL)
    payment_reminder_enabled = models.BooleanField()
    is_sms_enabled = models.BooleanField()
    is_portal_enabled = models.BooleanField()
    is_consent_agreed = models.BooleanField()
    consent_date = models.DateField()
    is_client_review_settings_enabled = models.BooleanField()
    default_tax = models.ForeignKey(default_taxes, on_delete=models.SET_NULL)
    tds_tax_id = models.ForeignKey(default_tax, on_delete=models.SET_NULL)
    place_of_contact = models.ForeignKey(state, on_delete=models.CASCADE)
    gst_no  = models.CharField(max_length=16)
    pan_no = models.CharField(max_length=12)
    trader_name = models.CharField(max_length=45)
    legal_name = models.CharField(max_length=105)
    vat_reg_no = models.CharField(max_length=45)
    tax_treatment = models.ForeignKey(default_tax_zones, on_delete=models.SET_NULL)
    gst_treatment = models.ForeignKey(default_tax_zones, on_delete=models.SET_NULL)
    sales_channel = models.ForeignKey(sales_channels, on_delete=models.SET_NULL)
    portal_receipt_count = models.IntegerField(default=0)
    billing_address = models.ForeignKey(addresses, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(addresses, on_delete=models.SET_NULL)
    created_stamp = models.DateTimeField()
    last_modified_time = models.DateTimeField()
    currency_summary = models.ManyToManyField(balance_store)
    comments = models.ManyToManyField(comments)
    custom_fields = models.ManyToManyField(custom_fields)



class users(models.Model):

    zid = models.PositiveBigIntegerField()
    role_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    email = models.EmailField()
    is_customer_segmented = models.BooleanField()
    is_vendor_segmented = models.BooleanField()
    user_role_formatted = models.CharField(max_length=45)
    user_type_formatted = models.CharField(max_length=45)
    status_id = models.ForeignKey(statues, on_delete=models.CASCADE)
    photo_url = models.URLField()
    is_payroll_admin = models.BooleanField()
    is_employee = models.BooleanField()
    allocated_warehouse_count = models.IntegerField()
    total_warehouse_count = models.IntegerField()
    custom_fields = models.ManyToManyField(custom_fields)



class warehouses(models.Model):

    zid = models.PositiveBigIntegerField()
    warehouse_name  = models.CharField(max_length=105)
    attention = models.CharField(max_length=45)
    address  = models.ForeignKey(addresses, on_delete=models.SET_NULL, null=True)
    email  = models.EmailField()
    is_primary = models.BooleanField()
    status = models.ForeignKey(statues, on_delete=models.CASCADE)
    is_fba_warehouse  = models.BooleanField()
    sales_channels = models.ManyToManyField(sales_channels)
    custom_fields = models.ManyToManyField(custom_fields)



class item_types(models.Model):

    name = models.CharField(max_length=12)


class product_types(models.Model):

    name = models.CharField(max_length=12)


class items(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=105)
    sku = models.CharField(max_length=105)
    brand = models.CharField(max_length=45)
    manufacturer = models.CharField(max_length=45)
    category_id = models.PositiveBigIntegerField() #tobemade
    hsn_or_sac = models.CharField(max_length=45)
    image_name = models.CharField(max_length=45)
    status = models.ForeignKey(statues, on_delete=models.CASCADE)
    source = models.ForeignKey(source, on_delete=models.CASCADE)
    unit = models.ForeignKey(measuring_unit, on_delete=models.SET_NULL, null=True)
    quantity_decimal_place = models.IntegerField()
    description = models.CharField(max_length=105)
    item_tax_preferences = models.ManyToManyField(default_tax_types)
    rate = models.FloatField()
    account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    is_default_tax_applied = models.BooleanField()
    is_taxable = models.BooleanField()
    tax_exemption_id = models.ForeignKey(default_tax_exemption, on_delete=models.SET_NULL, null=True)
    taxability_type = models.CharField(max_length=12)
    purchase_description = models.CharField(max_length=105)
    product_description = models.CharField(max_length=105)
    product_short_description = models.CharField(max_length=45)
    pricebook_rate = models.FloatField()
    pricebook_discount = models.FloatField()
    sales_rate = models.FloatField()
    purchase_rate = models.FloatField()
    purchase_account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    inventory_account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField()
    offline_created_date_with_time = models.DateTimeField()
    last_modified_time = models.DateTimeField()
    item_type = models.ForeignKey(item_types, on_delete=models.SET_NULL, null=True)
    product_type = models.ForeignKey(product_types, on_delete=models.CASCADE)
    is_returnable = models.BooleanField()
    reorder_level = models.FloatField()
    minimum_order_quantity = models.FloatField()
    maximum_order_quantity = models.FloatField()
    initial_stock = models.FloatField()
    initial_stock_rate = models.FloatField()
    total_initial_stock = models.FloatField()
    vendor_id = models.ForeignKey(contacts, on_delete = models.SET_NULL, null=True)
    stock_on_hand = models.FloatField()
    asset_value = models.FloatField()
    available_stock = models.FloatField()
    actual_available_stock
    committed_stock
    actual_committed_stock
    available_for_sale_stock
    actual_available_for_sale_stock
    custom_fields
    image_document_id
    track_serial_number
    track_batch_number
    upc
    ean
    isbn
    part_number
    is_combo_product
    sales_channels
    warehouses
    preferred_vendors
    comments
    package_details
    __item_type
    mapped_items