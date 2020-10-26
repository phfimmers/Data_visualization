#!/usr/bin/env python
# coding: utf-8

# # __Visualisations from cleaned data:__<br>
# 
#  - Necessary further price cleaning<br>
#  - Divide dataframe into numerical, boolean and categorical variables<br>
#  - Price correlations of categorical variables<br>
#      - Data overview<br>
#      - Data preparation<br>
#      - Visual creation<br>
#  - Price correlations of numerical variables<br>
#      - Data overview<br>
#      - Visual creation<br>
#  - Price correlations of boolean variables<br>
#      - Data overview<br>
#      - Data preparation<br>
#      - Visual creation<br>

# In[132]:


import pandas as pd
import matplotlib
import seaborn as sns
from pandas.api.types import infer_dtype
import numpy as np

get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt


# In[140]:


df = pd.read_csv('../csv_files/cleaned_properties.csv', low_memory = False, index_col = 0)

print(df.info(),'\n')

print('Inferred datatypes:\n',df.apply(infer_dtype),'\n')


# ## __Necessary further price cleaning__

# In[135]:


df['price'] = df['price'].replace(1, np.nan).replace(2, np.nan)
df['price'] = df['price'].apply(lambda x: np.nan if x < 50000 else x)


# In[136]:


df.columns


# ## __Divide dataframe into numerical, boolean and categorical variables__

# In[116]:


df_numerical = df[['price', 'area', 'terrace_area', 'garden_area', 'land_surface', 'land_plot_surface']].copy()
df_boolean = df[['price', 'region', 'open_fire', 'terrace', 'house_is',
         'swimming_pool_has', 'kitchen_has', 'furnished', 'garden']].copy()
df_categorical = df[['price', 'region', 'house_is', 'property_subtype', 'facades_number', 'building_state', 'rooms_number']].copy()


# ## __Price correlations of categorical variables__

# ### Data overview

# In[117]:


print(df_categorical.info(),'\n')

print('Inferred datatypes:\n',df_categorical.apply(infer_dtype),'\n')

uniques = pd.DataFrame()
for col in df_categorical:
    col_uniques = pd.DataFrame({f'{col}_value': df_categorical[f'{col}'].value_counts().index,
                                f'{col}_count': df_categorical[f'{col}'].value_counts().values})
    uniques = pd.concat([uniques, col_uniques], axis = 1)

print('Value counts:')
uniques.head(15)


# ### Data preparation

# In[118]:


# Change subtype to all smallcaps
df_categorical['property_subtype'] = df_categorical['property_subtype'].str.lower()

# Change - to underscore
df_categorical['property_subtype'].replace('-', '_', inplace = True)


# In[119]:


df_categorical['building_state'].replace('TO_BE_DONE_UP', 'TO_RENOVATE', inplace = True)
df_categorical['building_state'].replace('TO_RESTORE', 'TO_RENOVATE', inplace = True)


# ### Visual 1

# In[121]:


g = sns.FacetGrid(df_categorical, col="region",
                  col_order = ['Flanders', 'Wallonia'], height=7)

g.map(sns.barplot, 'property_subtype', 'price', alpha=1,
     order = ['villa', 'apartment_block', 'mansion', 'penthouse',
                     'mixed_use_building', 'duplex', 'ground_floor',
                     'apartment', 'house'], palette="muted", ci = 'sd')

g.set(ylim=(0, 1500000))
g.axes[0,0].set_ylabel('Price (million)', fontsize = 25)
g.axes[0,0].set_xlabel('')
g.axes[0,1].set_xlabel('')
g.axes[0,0].set_title('Flanders', fontsize=25)
g.axes[0,1].set_title('Wallonia', fontsize=25)


g.axes[0,0].tick_params(axis='x', which='major', labelsize = 25)
g.axes[0,1].tick_params(axis='x', which='major', labelsize = 25)
g.axes[0,0].tick_params(axis='y', which='major', labelsize = 25)
plt.setp(g.axes[0,0].xaxis.get_majorticklabels(), rotation=-30, ha="left", rotation_mode="anchor")
plt.setp(g.axes[0,1].xaxis.get_majorticklabels(), rotation=-30, ha="left", rotation_mode="anchor")

plt.savefig("./pictures/property_subtype_cor_by_region.png", transparent=True)

plt.show()


# ### Visual 2

# In[130]:


house_mask = df_categorical.house_is == 1
house_flanders_mask = house_mask & (df_categorical.region == 'Flanders')

fig1, (ax1, ax2) = plt.subplots(1, 2, sharey = True, figsize=(17,8))

sns.barplot(x='facades_number', y='price',
               data=df_categorical[house_flanders_mask], palette="muted",
               ax=ax1, ci = 'sd', order = [1, 2, 3, 4])
sns.barplot(x='rooms_number', y='price',
               data=df_categorical[house_flanders_mask], palette="muted",
               ax=ax2, ci = 'sd', order = [1, 2, 3, 4, 5, 6, 7])

for ax in (ax1, ax2):
    ax.set_ylabel('')
    ax.tick_params(axis='x', which='major', labelsize = 'xx-large')
    ax.tick_params(axis='y', which='major', labelsize = 'xx-large')

ax1.axis([None, None, 0, 1500000])
ax1.set_ylabel('House price (million)', fontsize = '25')

ax2.set_ylabel('', fontsize = 'xx-large')

ax1.set_xlabel('Facades', fontsize = '25')
ax2.set_xlabel('Rooms', fontsize = '25')
ax1.tick_params(axis='both', which='major', labelsize = 25)
ax2.tick_params(axis='both', which='major', labelsize = 25)

fig1.suptitle('Average price & standard deviation', fontsize=35)
     
plt.tight_layout()

plt.savefig("./pictures/facades_rooms_cor_house_flanders.png", transparent=True)

plt.show()


# ## __Price correlations of numerical variables__

# ### Data overview

# In[123]:


print(df_numerical.info(),'\n')

print('Inferred datatypes:\n',df_numerical.apply(infer_dtype),'\n')

uniques = pd.DataFrame()
for col in df_numerical:
    col_uniques = pd.DataFrame({f'{col}_value': df_numerical[f'{col}'].value_counts().index,
                                f'{col}_count': df_numerical[f'{col}'].value_counts().values})
    uniques = pd.concat([uniques, col_uniques], axis = 1)

print('Value counts:')
uniques.head(15)


# ### Data preparation

# In[124]:


# replace 0 or 1 m² with np.nan
df_numerical = df_numerical.applymap(lambda x: np.nan if x == 0 or x == 1 else x)


# ### Visual 3

# In[125]:


labels = ['price', 'area m²', 'terrace m²', 'garden m²', 'land m²', 'land_plot m²']
corr = df_numerical.corr()
 
# Heatmap
fig, ax = plt.subplots(figsize=(15,12))
ax = sns.color_palette("crest", as_cmap=True)
ax = sns.heatmap(corr, xticklabels = labels, yticklabels = labels, cmap = 'crest')
#ax.tick_params(axis='both', which='major', labelsize = 'xx-large')
ax.figure.axes[-2].set_xticklabels(labels, rotation = 45, fontsize = 25)
ax.figure.axes[-2].set_yticklabels(labels, rotation = 45, fontsize = 25)
ax.figure.axes[-1].set_yticklabels(ax.figure.axes[-1].get_yticklabels(), fontsize = 25)

fig.suptitle('m² correlations with price', fontsize=35)

plt.savefig("./pictures/area_cor.png", transparent=True)


# ## __Price correlations of boolean variables__

# ### Data overview

# In[126]:


print(df_boolean.info(),'\n')

print('Inferred datatypes:\n',df_boolean.apply(infer_dtype),'\n')

uniques = pd.DataFrame()
for col in df_boolean:
    col_uniques = pd.DataFrame({f'{col}_value': df_boolean[f'{col}'].value_counts().index,
                                f'{col}_count': df_boolean[f'{col}'].value_counts().values})
    uniques = pd.concat([uniques, col_uniques], axis = 1)

print('Value counts:')
uniques.head(15)


# ### Data preparation

# In[127]:


# change garden values >1 to Yes
df_boolean['garden'].apply(lambda x: 1 if x > 1 else x)

## Make contents a display friendly Has/Has not
# change 0.0 to Has not, 1.0 to Has and unknown to NaN
df_boolean_without_price = df_boolean.iloc[:,1:]
df_boolean_without_price = df_boolean_without_price.replace({'unknown': np.nan, 0: 'Has not', 1: 'Has', 'False': 'Has not', 'True': 'Has'})
df_boolean = pd.concat([df_boolean['price'], df_boolean_without_price], axis = 1)


# ## Melt the dataframe

# In[128]:


# For joint house/apartment display
df_boolean_melted = df_boolean.melt(id_vars = ['price'],
                                    value_vars = ['open_fire', 'terrace',
                                                  'house_is', 'swimming_pool_has',
                                                  'kitchen_has', 'furnished', 'garden'])
df_boolean_melted.head()

# For separate house/apartment/region display
df_boolean_melted_typed = df_boolean.melt(id_vars = ['price', 'house_is', 'region'],
                                          value_vars = ['open_fire', 'terrace',
                                                        'swimming_pool_has', 'kitchen_has',
                                                        'furnished', 'garden'])
df_boolean_melted_typed.head()
df_boolean_melted_house = df_boolean_melted_typed[df_boolean_melted_typed['house_is']
                                                 == 'Has']
df_boolean_melted_apartment = df_boolean_melted_typed[df_boolean_melted_typed['house_is']
                                                 == 'Has not']


# ## Find which columns correlates most with price

# In[131]:


house_mask = df_boolean_melted_typed.house_is == 'Has'
house_flanders_mask = house_mask & (df_boolean_melted_typed.region == 'Flanders')

fig, ax = plt.subplots(figsize=(22,5))

ax = sns.violinplot(x="variable", y="price", hue="value",
                    data=df_boolean_melted_typed[house_flanders_mask], palette="muted",
                   inner = 'box', scale = 'count', hue_order = ['Has not', 'Has'], split = True)

ax.set_ylabel('price (million)', fontsize = 25)
ax.set_xlabel('')
ax.tick_params(axis='both', which='major', labelsize = 25)
ax.axis([None, None, 0, 1500000])
ax.grid(axis = 'y')
ax.legend(loc = 'upper right', fontsize = 25)

plt.setp(ax.xaxis.get_majorticklabels(), rotation=-10, ha="left", rotation_mode="anchor")

fig.suptitle('Price distribution', fontsize=35)

plt.savefig('./pictures/boolean_cor_house_flanders.png', transparent=True)
plt.show()


# In[ ]:




