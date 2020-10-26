from utils import *

float_col = ['house_is', 'price', 'rooms_number', 'area',
           'kitchen_has', 'furnished', 'open_fire', 'terrace', 'terrace_area',
           'garden', 'garden_area', 'land_surface', 'land_plot_surface',
           'facades_number', 'swimming_pool_has']

object_col = ['property_subtype', 'sale', 'building_state']


clean_df = StandardCleaningDataFrame('csv_files/properties.csv', float_col, object_col).df

clean_df.to_csv('csv_files/cleaned_properties.csv')

DataAnalysis(clean_df)


