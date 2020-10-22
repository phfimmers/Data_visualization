##-----------------------------Data Analysis---------------------
# Check if there are columns with mixed data types ==> NO
print("Check if there are columns with mixed data types ==> NO")
print("there are no columns with 'mixed' part of the inferred datatype")

from pandas.api.types import infer_dtype
# print data type of each column to check if there are
# any mixed ones, turns out that there are none
def is_mixed(col):
    return infer_dtype(col)

print(df.apply(is_mixed))

# ==> there are no columns with 'mixed' part of the inferred datatype


# Display the percent of NaNs per column
print(Display the percent of NaNs per column)

# display the percent of NaNs per column
percent_missing = df.isnull().sum() * 100 / len(df)
missing_value_df = pd.DataFrame({'%_missing': percent_missing})
missing_value_df = missing_value_df.sort_values('%_missing', ascending = False)
print(missing_value_df)

df.info()

# Print unique values per column
print('Print unique values per column')
uniques = pd.DataFrame()
for col in df:
    col_uniques = pd.DataFrame({f'{col}_value': df[f'{col}'].value_counts().index,
                                f'{col}_count': df[f'{col}'].value_counts().values})
    uniques = pd.concat([uniques, col_uniques], axis = 1)

print(uniques.head(15))

