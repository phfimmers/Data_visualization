from pandas.api.types import infer_dtype
import pandas as pd
import numpy as np
import sys

##-----------------------------Data Analysis---------------------
class DataAnalysis:
	def __init__(self, df):
		self.df = df
		self.exit = True
		self.choices = {
		"1": self.df.info,
		"2": self.dtypes_control,   
		"3": self.percent_nan_value,
		"4": self.unique_values_per_column,
		"5": self.quit
		}

	def display(self):
		print("""
			Analysis:
			1. General information about data
			2. Check if there are columns with mixed data types 
			3. Display the percent of NaNs per column
			4. Unique values per column
			5. Quit
			""")
		while self.exit == True: 
			choice = input('please enter the number of your request: ')
			action = self.choices.get(choice, "Your choice is not a valid choice")
			action()

	def dtypes_control(self):
		# Check if there are columns with mixed data types ==> NO
		print("\nCheck if there are columns with mixed data types ==> NO")
		print("there are no columns with 'mixed' part of the inferred datatype")


		# print data type of each column to check if there are
		# any mixed ones, turns out that there are none
		def is_mixed(col):
		    return infer_dtype(col)

		print(self.df.apply(is_mixed))

		# ==> there are no columns with 'mixed' part of the inferred datatype

	def percent_nan_value(self):
		# Display the percent of NaNs per column
		print('\nDisplay the percent of NaNs per column')

		# display the percent of NaNs per column
		percent_missing = self.df.isnull().sum() * 100 / len(self.df)
		missing_value_df = pd.DataFrame({'%_missing': percent_missing})
		missing_value_df = missing_value_df.sort_values('%_missing', ascending = False)
		print(missing_value_df)

	def unique_values_per_column(self):
		# Print unique values per column
		print('\nPrint unique values per column')
		uniques = pd.DataFrame()
		for col in self.df:
		    col_uniques = pd.DataFrame({f'{col}_value': self.df[f'{col}'].value_counts().index,
		                                f'{col}_count': self.df[f'{col}'].value_counts().values})
		    uniques = pd.concat([uniques, col_uniques], axis = 1)

		col_name = input('please write your column name to analysis: ')
		col_name1 = col_name + '_value'
		col_name2 = col_name + '_count'
		print(uniques.loc[0:10, [col_name1, col_name2]])

	def quit(self):
	    print("Thank you for using our analysis.")
	    self.exit = False
	    return self.exit
