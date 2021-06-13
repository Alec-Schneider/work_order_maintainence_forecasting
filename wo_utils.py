import pandas as pd
from pandas import DataFrame
import numpy as np


def clean_currency(x):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    DF.apply(clean_currency).astype(float)
    """
    if isinstance(x, str):
        return(x.replace('$', '').replace(',', '').replace("(", "").replace(")", ""))
    return(x)



class WorkOrder(DataFrame):

    @property
    def _constructor(self):
        return WorkOrder
        
    

    
    @property
    def currency_cols(self):
        return ["total_cost", "total_charged_amount", "total_labor_cost", "total_services_cost", 
                "total_materials_cost", "total_spot_purchase_cost", "total_miscellaneous_cost"]

    @property
    def timestamp_cols(self):
        return ["date_time_created", "date_time_completed__last"]

    @property
    def drop_cols(self):
        return ["customer_gl_account_code", "work_description", "work_order_address",
            "work_order_address_2", "property_name", "reason_note", "description"]

    @property
    def duration_cols(self):
        return ["created_to_picked_up", "created_to_started"]

    @property
    def category_cols(self):
        return ["wo#", "property_number", "specialty", "portfolio", "priority", "district", 
                "region", "status", "organization", "item_asset_model", "type_category", "type",
                "work_order_city", "work_order_state_prov", "work_order_zip_postal_code", 
                "repair_category", "repair_code", "reason", "specialty_group"]

    
    def clean_currency(self, x):
        """ 
        If the value is a string, then remove currency symbol and delimiters
        otherwise, the value is numeric and can be converted
        DF.apply(clean_currency).astype(float)
        """
        if isinstance(x, str):
            return(x.replace('$', '').replace(',', '').replace("(", "").replace(")", ""))
        return x
    
    
    def _clean_currency_cols(self):
        """
        Convert USD columns into float types
        """
        for col in self.currency_cols:
            self[col] =  self[col].apply(clean_currency).astype(float)


    def clean_durations(self, x):
        hours, minutes, seconds = x.split(":")
        hours = int(hours) * 60 * 60
        minutes = int(minutes) * 60
        seconds = int(seconds)
        return hours + minutes + seconds

    def _clean_duration_cols(self):
        """
        Convert the timestamp duration columns into seconds
        """
        for col in self.duration_cols:
            self[col] = self[col].apply(self.clean_durations)

    def preprocess_raw_df(self):
        """
        Clean the data before passing to a data pipeline
        """
        self.converted_col_names = ['_'.join(col.lower().replace(".", "").replace("/", " ").replace("-", "").split(" ")) 
                      for col in  self.columns.tolist()]
        self.columns = self.converted_col_names

        self.drop(self.drop_cols, axis=1, inplace=True)
        self._clean_currency_cols()
        self._clean_duration_cols()

        for col in self.timestamp_cols:
            self[col] = pd.to_datetime(self[col])

    def get_category_details(self):
        """
        Get the value counts, unique values, and number of unique values in
        the categorical columns of the dataset
        """
        category_details = {}

        for col in self.category_cols:
            print(col, end="\n\n")
            d = {}
            d["value_counts"] = self[col].value_counts().sort_values(ascending=False)
            d["unique_values"] =  self[col].unique()
            d["num_unique"] = len(d["unique_values"])
            category_details[col] = d
        
        return category_details
        




    
