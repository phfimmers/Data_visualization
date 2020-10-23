import pandas as pd
import numpy as np
import re

df = pd.read_csv('../csv_files/properties.csv', low_memory=False)

# Remove leading and trailing spaces from column names
df.columns = [x.strip(' ') for x in df.columns.values]

# Remove leading and trailing spaces of every element
# remove leading and trailing spaces and newline characters from values if they are a string
df = df.applymap(lambda x: x.strip() if type(x)==str else x)

# We start to correct columns
## 1. PostCode
df['postcode'] = df['postcode'].astype('Int64')

## 2. Price
# Converting price
def grabs_strips(x):
    if type(x) == str:
        # return x.str.extract('(\d*\.?\d*)', expand=False).astype(float)
        return re.match(r'(\d*(,\d{3})*\.?\d*)', x).group()
    return x

df['price'] = df['price'].apply(grabs_strips)

# Conversion into float
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# drop rows which is nan in the price 
df.dropna(subset=['price'], inplace=True)

## 3.house_is
# fonction to Update the most relevant value of proprety_subtype
def updates_house_is(row):
    
    house_sub_type = ['HOUSE','house','VILLA','EXCEPTIONAL_PROPERTY', 'MANSION', 'villa', 'House', 'TOWN_HOUSE'
                      , 'Villa', 'COUNTRY-COTTAGE' ]
    
    app_sub_type = ['APARTEMENT', 'APARTEMENT','apartment','MIXED_USE_BUILDING','Apartment','DUPLEX','PENTHOUSE',
                   'APARTMENT_BLOCK','GROUND_FLOOR', 'duplex', 'ground-floor', 'Loft/Attic', 'APARTMENT_GROUP'
                    , 'Penthouse', 'penthouse', 'flat-studio', 'APARTMENT', 'apartement', 'Apartement']
    
    if row['property_subtype'] in house_sub_type:
        return True
    elif row['property_subtype'] in app_sub_type:
        return False
    return np.nan

# Storing in house_is prop of the df
df['house_is'] = df.apply(updates_house_is, axis=1)
df.house_is = df.house_is.astype('float64')

## 4.Sale
df.sale = df['sale'].replace({
    'Wohnung': "Unknown",
    'Appartement': "Unknown",
    'Apartamento': "Unknown",
    '': "Unknown",
    'None': "Unknown",
    "unknown":"Unknown",
    "Maison":"Unknown",
    "Huis":"Unknown",
    "House":"Unknown"
})

df.sale = df['sale'].fillna('Unknown')

## 5.property_subtype
df.property_subtype = df['property_subtype'].replace({
    'house': "HOUSE",
    'House': "HOUSE",
    'apartment': "APARTMENT",
    '': "Unknown",
    'villa': "VILLA",
    "duplex":"DUPLEX",
    "Huis":"HOUSE",
    "Maison":"HOUSE",
    'penthouse':'PENTHOUSE',
    'flat-studio':'FLAT_STUDIO',
    'ground-floor':'GROUND_FLOOR'
})
df.property_subtype = df['property_subtype'].fillna('Unknown')

## 9.properties.room_number
# replace None to np.nan
df.rooms_number.fillna(value=np.nan, inplace=True)

# replace 'None' to np.nan
df.rooms_number = df.rooms_number.apply(lambda x : np.nan if x=='None' else x)

# change data type of rooms_number from object to float64
df.rooms_number = df.rooms_number.astype('float64')

## 10.properties.area
# remove string character from value of area
df.area = df.area.replace("[^0-9.-]", "", regex=True)

# replace 'm2' from value of area
df.area = df.area.replace('', np.nan)

# replace None to np.nan
df.area.fillna(value=np.nan, inplace=True)

# replace 'None' to np.nan
df.area = df.area.apply(lambda x : np.nan if x=='None' else x)

# change data type from object to float64
df.area = df.area.astype('float64')

# replace zero in value of area
df.area = df.area.replace(0, np.nan)

## 11.kitchen_has
# change data type from object to float64
df.kitchen_has = df.kitchen_has.astype('float64')

## 12.furnished
# change data type from object to float64
df.furnished = df.furnished.astype('float64')

## 13.open_fire
# change data type from object to float64
df.open_fire = df.open_fire.astype('float64')

## 14.terrace
# change numerical data to np.nan
df.terrace = df.terrace.replace(r'\d\.?\d?', True, regex=True)

# replace string False to False
df.terrace = df.terrace.replace('False', False)

# replace string False to False
df.terrace = df.terrace.replace('TRUE', True)

# replace string False to False
df.terrace = df.terrace.replace('True', True)

# change data type from object to bool
df.terrace = df.terrace.astype('float64')

## 15.terrace_area
# replace 'None' to np.nan
df.terrace_area = df.terrace_area.apply(lambda x : np.nan if x=='None' else x)

df.terrace_area = df.terrace_area.replace(True, np.nan)
df.terrace_area = df.terrace_area.replace('TRUE', np.nan)

# change data type from object to float64
df.terrace_area = df.terrace_area.astype('float64')

# replace zero in value of area
df.terrace_area = df.terrace_area.replace(0, np.nan)

# replace '1' in value of area
df.terrace_area = df.terrace_area.replace(1, np.nan)

## 16.Garden
# replace string False to False
df.garden = df.garden.replace('False', False)

# replace string False to False
df.garden = df.garden.replace('True', True)

# change data type from object to bool
df.garden = df.garden.astype('float64')

df.garden = df.garden.apply(lambda x:1 if x>1 else x)

## 17.Garden Area
# replace None to np.nan
df.garden_area.fillna(value=np.NaN, inplace=True)

# replace 'None' to np.nan
df.garden_area = df.garden_area.apply(lambda x : np.nan if x=='None' else x)

# change data type of rooms_number from object to float64
df.garden_area = df.garden_area.astype('float64')

# replace zero in value of area
df.garden_area = df.garden_area.replace(0, np.nan)

# replace '1' in value of area
df.garden_area = df.garden_area.replace(1, np.nan)

## 18.land_surface
# replace None to np.nan
df.land_surface.fillna(value=np.NaN, inplace=True)

# replace np.nan TO 0
df.land_surface = df.land_surface.replace(np.nan, 0)

# replace None to np.nan
df.land_surface.fillna(value=np.nan, inplace=True)

# replace 'None' to np.nan
df.land_surface = df.land_surface.apply(lambda x : np.nan if x=='None' else x)

# change data type of rooms_number from object to float64
df.land_surface = df.land_surface.astype('float64')

# replace zero in value of area
df.land_surface = df.land_surface.replace(0, np.nan)

# replace '1' in value of area
df.land_surface = df.land_surface.replace(1, np.nan)

## 19.land_plot_surface
# replace 'yes' from value to 0
df.land_plot_surface = df.land_plot_surface.replace("[^0-9.-]", "", regex=True)

# replace 'm2' from value of area
df.land_plot_surface = df.land_plot_surface.replace('', np.nan)

# replace None to np.nan
df.land_plot_surface.fillna(value=np.nan, inplace=True)

# replace 'None' to np.nan
df.land_plot_surface = df.land_plot_surface.apply(lambda x : np.nan if x=='None' else x)

# change data type of rooms_number from object to float64
df.land_plot_surface = df.land_plot_surface.astype('float64')

## 20.facades_number
# replace 'None' to np.nan
df.facades_number = df.facades_number.apply(lambda x : np.nan if x=='None' else x)

# change data type of facades_number from object to float64
df.facades_number = df.facades_number.astype('float64')

## 21.swimming_pool_has
#change numerical data to np.nan
df.swimming_pool_has = df.swimming_pool_has.replace(r'\d\.?\d?', np.nan, regex=True)

# replace string 'False' to False
df.swimming_pool_has = df.swimming_pool_has.replace('False', False)

# replace string 'FALSE' to False
df.swimming_pool_has = df.swimming_pool_has.replace('FALSE', False)

# replace string 'True' to True
df.swimming_pool_has = df.swimming_pool_has.replace('True', True)

# replace string 'TRUE' to True
df.swimming_pool_has = df.swimming_pool_has.replace('TRUE', True)

# change data type from object to bool
df.swimming_pool_has = df.swimming_pool_has.astype('float64')

## 22.building_state
# change numerical data to np.nan
df.building_state = df.building_state.replace(r'\d\.?\d?', np.nan, regex=True)
df.building_state = df.building_state.apply(lambda x : np.nan if x=='None' else x)
df.building_state = df['building_state'].replace({
    'Good':"GOOD",
    'As new':"AS_NEW",
    'To renovate':"TO_RENOVATE",
    'To restore':"TO_RESTORE",
    '':np.nan,
    'To be done up':"TO_BE_DONE_UP",
    "Just renovated":"JUST_RENOVATED",
    'Not specified':np.nan
})


# General Cleaning
# Put 'unknown' in place of NaN for everything else than int64 and float64 columns
## Please run this after converting numerical columns like price and facades from string to integer.  
# Even a value of NaN might help predict the price, so to avoid the correlation algorithm skipping it?, and because NaN is not allowed, we replace it.
# replace all NaNs in strings with 'unknown'
df_nanfilled = df.select_dtypes(exclude=['int64','float64']).replace(np.nan, 'unknown')
df.update(df_nanfilled)
print(df.info())

# replace all 'None'/'none' strings with uknown
df_nonefilled = df.select_dtypes(exclude=['int64','float64']).replace('none', 'unknown')
df.update(df_nonefilled)
df_nonefilled = df.select_dtypes(exclude=['int64','float64']).replace('None', 'unknown')
df.update(df_nonefilled)


## 6.locality and postcode
### Drop postcode column, because postcode is more completely available in 'locality'
### first we fix 'locality' column to carry just postcode or 'unknown' (stripping sporadic address parts)
df.drop('postcode', axis = 1, inplace = True)

# write a function that returns the cleaned postcode from elements
# containing the address
def clean_locality(locality): 
    # Search for the presence of a 4 digit number (starts with 1-9)
    if re.search('[1-9]\d{3}', locality):
        # get the number
        return re.findall("[1-9]\d{3}", locality)[0]
    else: 
        # if no postcode is inside insert 'unknown' 
        return 'unknown'
          
# Updated locality column
df['locality'] = df['locality'].apply(clean_locality)

## 7.Create a region column
def get_region(locality):
    if locality == 'unknown':
        return 'unknown'
    else:
        if not re.search('[1-9]\d{3}', locality):
            print('Please run this on already cleaned locality column')
            return 'unknown'
        elif int(locality) >= 1000 and int(locality) <=1299:
            return 'Brussels'
        elif int(locality) >= 1300 and int(locality) <=1499:
            return 'Wallonia'
        elif int(locality) >= 4000 and int(locality) <=7999:
            return 'Wallonia'
        else:
            return 'Flanders'
        
df['region'] = df['locality'].apply(get_region)


# Remove duplicates
### should execute after fixing columns
### should execute after removing non-property detail or incomplete columns: source and hyperlink
# drop columns 
df.drop(['source', 'hyperlink'], axis = 1, inplace = True)

# drop 100% duplicate rows
lenght_before = len(df)
df.drop_duplicates(ignore_index = True, inplace = True)
dropped = len(df) - lenght_before
print(f'Dropped: {dropped}')

