import pandas as pd
import numpy as np
import re


class StandardCleaningDataFrame:
    def __init__(self, csv_file, float_col, object_col):
        # import csv file as a dataframe
        self.df = pd.read_csv(csv_file, low_memory=False)
        self.float_col = float_col
        self.object_col = object_col
        self.df = self.data_type_cleaning(self.float_col, self.object_col)
        self.df = self.column_cleaning()
        self.df = self.general_cleaning()

    def general_cleaning(self):
        # Remove leading and trailing spaces from column names
        self.df.columns = [x.strip(' ') for x in self.df.columns.values]
        # Remove leading and trailing spaces of every element
        # remove leading and trailing spaces and newline characters from values if they are a string
        self.df = self.df.applymap(lambda x: x.strip() if type(x)==str else x)
        # General Cleaning
        # Put 'unknown' in place of NaN for everything else than int64 and float64 columns
        ## Please run this after converting numerical columns like price and facades from string to integer.  
        # Even a value of NaN might help predict the price, so to avoid the correlation algorithm skipping it?, and because NaN is not allowed, we replace it.
        # replace all None to np.nan
        self.df.fillna(value=np.nan, inplace=True)
        # replace all 'None'/'none' strings with uknown
        self.df.replace({'none':np.nan,'None': np.nan,"True": True,"TRUE": True,"Yes": True,"False": False,"FALSE": False,"No": False,"NaN": np.nan,
                        "":np.nan,'Not specified': np.nan,'Unknown': np.nan,'unknown':np.nan}, inplace=True)
        for col in self.df:
            try:
                self.df[col] = self.df[col].astype('float64')
                # replace zero to np.nan
                if col in ['price', 'area', 'terrace_area', 'garden_area', 'land_surface', 'land_plot_surface']:
                    self.df[col] = self.df[col].replace(0, np.nan)
                    self.df[col] = self.df[col].replace(1, np.nan)
                if col in ['kitchen_has', 'furnished', 'open_fire', 'terrace', 'garden', 'swimming_pool_has']:
                    self.df[col] = self.df[col].apply(lambda x:1 if x>1 else x)
            except:
                self.df[col] = self.df[col].astype('object')
        self.df.drop_duplicates(ignore_index = True, inplace = True)
        return self.df

    def column_cleaning(self):

        self.df.dropna(subset=['price'], inplace=True)
        # drop columns 
        self.df.drop(['source', 'hyperlink', 'postcode'], axis = 1, inplace = True)


        self.df['locality'] = self.df['locality'].astype('object')
        
        self.df['locality'] = self.df['locality'].replace("[^0-9]", np.nan, regex=True)
        
        def get_region(locality):
            if locality != np.nan:
                if float(locality) >= 1000 and float(locality) <=1299:
                    return 'Brussels'
                elif float(locality) >= 1300 and float(locality) <=1499:
                    return 'Wallonia'
                elif float(locality) >= 4000 and float(locality) <=7999:
                    return 'Wallonia'
                else:
                    return 'Flanders'

        self.df['region'] = self.df['locality'].apply(get_region)
        
        self.df.building_state = self.df.building_state.replace(r'\d\.?\d?', np.nan, regex=True)
        self.df.building_state = self.df['building_state'].replace({
            'Good':"GOOD",
            'As new':"AS_NEW",
            'To renovate':"TO_RENOVATE",
            'To restore':"TO_RESTORE",
            '':np.nan,
            'To be done up':"TO_BE_DONE_UP",
            "Just renovated":"JUST_RENOVATED",
            'Not specified':np.nan
        })
        
        def building_st(building):
            building_list = ['AS_NEW', 'GOOD', 'TO_BE_DONE_UP', 'TO_RENOVATE', 'JUST_RENOVATED', 'TO_RESTORE']
            if building not in building_list:
                building = np.nan

        #self.df['building_state'] = self.df['building_state'].apply(building_st)

        self.df.property_subtype = self.df['property_subtype'].replace({'house': "HOUSE",
                                                                        'House': "HOUSE",
                                                                        'apartment': "APARTMENT",
                                                                        'Apartment':"APARTMENT",
                                                                        'APARTEMENT':"APARTMENT",
                                                                        '': "unknown",
                                                                        'villa': "VILLA",
                                                                        'Villa': "VILLA",
                                                                        "duplex":"DUPLEX",
                                                                        "Huis":"HOUSE",
                                                                        "Maison":"HOUSE",
                                                                        'penthouse':'PENTHOUSE',
                                                                        'flat-studio':'FLAT_STUDIO',
                                                                        'ground-floor':'GROUND_FLOOR',
                                                                        'loft':'LOFT',
                                                                        'castle':'CASTLE',
                                                                        'unkonwn':'unknown',
                                                                        'mansion':'MANSION',
                                                                        'bungalow':'BUNGALOW' 
                                                                    })

        def sale_func(row):
            sale_list = ['residential_sale', 'first_session_with_reserve_price', 
                            'Public Sale', 'annuity_monthly_amount', 'Notary Sale',
                            'last_session_reached_price_min_overbid', 'final_public_sale',
                            'annuity_lump_sum']
            if row['sale'] in sale_list:
                return row['sale']
            else:
                return np.nan
                
        self.df['sale'] = self.df.apply(sale_func, axis=1)

        def house_or_apartment(row):
            house_sub_type = ['HOUSE','VILLA','EXCEPTIONAL_PROPERTY', 'MANSION', 'House', 'TOWN_HOUSE'
                             , 'COUNTRY-COTTAGE' ]

            app_sub_type = ['APARTMENT', 'MIXED_USE_BUILDING','DUPLEX','PENTHOUSE',
                   'APARTMENT_BLOCK','GROUND_FLOOR', 'ground-floor', 'Loft/Attic', 'APARTMENT_GROUP',
                   'flat-studio']

            if row['property_subtype'] in house_sub_type:
                return True
            elif row['property_subtype'] in app_sub_type:
                return False
            else:
                return np.NaN

        self.df.house_is = self.df.apply(house_or_apartment, axis=1)

        return self.df


    def data_type_cleaning(self, float_col, object_col):

        for col in self.float_col:
            self.df[col] = self.df[col].replace("[^0-9.-]", "", regex=True)

        for col in self.object_col:
            self.df[col] = self.df[col].replace("[0-9.-]", "", regex=True)

        return self.df



