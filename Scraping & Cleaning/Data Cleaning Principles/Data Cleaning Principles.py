#!/usr/bin/env python
# coding: utf-8

# # Tidying messy datasets
# 1. Column headers are values, not variable names.
# 2. Multiple variables are stored in one column.
# 3. Variables are stored in both rows and columns.
# 4. Multiple types of observational units are stored in the same table.
# 5. A single observational unit is stored in multiple tables.
# 

# # 1st principle: 
# 
# # Avoid having column headers with values, they must have variable names.

# In[13]:


import pandas as pd


# In[14]:


# intialise data of lists. 
data = {'Profession':['Chemist', 'Biologist', 'Software_Engineer', 'Sailor'], 
        '<$10k':[20, 23, 19, 18],
        '<$20k':[45, 334, 19, 18],
        '<$30k':[64, 23241, 19, 18],      
        '<$40k':[124, 23241, 19, 73],
        '<$50k':[23, 234, 58, 18],
        '<$60k':[124, 65, 19, 18],      
        '<$70k':[520, 568, 865, 18],
        '<$80k':[769, 800, 87, 536]
       } 
  
# Create DataFrame 
df = pd.DataFrame(data) 
  
# Print the output. 
df


# In[15]:


#if we want to decrease the dataframe width and extend its length we need to use the melt function
df_long = pd.melt(df, id_vars = 'Profession')


# In[16]:


df_long.head()


# In[17]:


#now each column is a variable and each row is now ab observation
df_long = pd.melt(df, id_vars = 'Profession', var_name = 'Income', value_name = 'Count')
df_long.head()


# # 2nd principle: 
# 
# # Avoid storing multiple variables in one column

# In[18]:


# intialise data of lists. 
data = {'Years_of_experience':[1,2,3,4], 
        'Salary_Chemist':['50k', '60k', '70k', '80k'],

        'Salary_Biologist':['50k', '60k', '70k', '80k'],


     'Taxes_Chemist':['5k', '5k', '6k', '7k'],
           'Taxes_Biologist':['4k', '5k', '6k', '7k'],

       } 
  
# Create DataFrame 
df1 = pd.DataFrame(data) 
  
# Print the output. 
df1


# In[19]:


df1.shape


# In[20]:


#In this case we are really want to modify this dataset in the following way:
# column called Years_of_experience leave as it is
# create a column for the profession
#create a column for the Salary_before_taxes
#create a column for the Salary_after_taxes
# create a column for the actual salary count


# In[21]:


df1_long = pd.melt(df1, id_vars = 'Years_of_experience')
df1_long.head()


# In[22]:


variable_split = df1_long['variable'].str.split('_')


# In[23]:


variable_split


# In[24]:


df1_long['Type'] =  variable_split.str[0]
df1_long['Profession'] =  variable_split.str[1]


# In[25]:


df1_long.head()


# In[26]:


#Or we can do it in one go just adding expand
df1_long[['Type_', 'Profession_']] = df1_long['variable'].str.split('_', expand = True)


# In[27]:


df1_long.head()


# # 3rd principle: 
# 
# # Avoid variables to be stored in both rows and columns.

# In[28]:


# intialise data of lists. 
data = {
        'Year':[2020,2020,2018,2018], 
        
        'Factor':['maxSalary', 'minSalary', 'maxSalary', 'minSalary'],

        'Obervation_1':[100, 120, 130, 130],
          'Obervation_2':[45, 56, 65, 44],
          'Obervation_3':[88, 90, 65, 76],
          'Obervation_4':[88, 120, 130, 60],
          'Obervation_5':[80, 95, 65, 88],
          'Obervation_6':[100, 120, 55, 66]


       } 
  
# Create DataFrame 
df2 = pd.DataFrame(data) 
  
# Print the output. 
df2


# In[29]:


#Here we have a row data that are duplicated like tmax, tmin 

#In the tidy df we would prefer to have the following columns:
"""
1. Year
2. Factor
3. Observarion
4. Amount

"""


# In[30]:


# the opposit of melt is the pivot, we do not want the column Factor anymore, 
# instead we want to have the tmin and tmax column
df2_long = pd.melt(df2, id_vars = ['Year', 'Factor'], var_name = 'Observation', value_name = 'Amount')
df2_long


# In[31]:


df2_long_tidy = df2_long.pivot_table(
index = ['Year', 'Observation'],
columns = 'Factor',
values = 'Amount'
)


# In[32]:


df2_long_tidy


# In[33]:


df2_long_tidy.reset_index()


# # 4th principle: 
# 
# # Avoid storing multiple types of observational units in the same table

# In[34]:


# make a dataset storage and preson friendly
# intialise data of lists. 
data = {'Profession':['Chemist', 'Chemist', 'Software_Engineer', 'Sailor'], 
        '<$10k':[20, 20, 19, 18],
        '<$30k':[21, 21, 19, 18],      
        '<$40k':[23, 23, 19, 73],
        '<$50k':[455, 455, 58, 18],
        '<$60k':[124, 124, 19, 18],      
        '<$70k':[520, 520, 865, 18],

       } 
  
# Create DataFrame 
df3 = pd.DataFrame(data) 
  
# Print the output. 
df3


# In[35]:


df3.duplicated()


# In[36]:


#Tidy data is better for the storage


# In[37]:


df3.drop_duplicates(keep = 'last', inplace = True)


# In[38]:


df3.head()


# # 5th principle: 
# 
# # Avoid storing a single observational unit in multiple tables.

# In[39]:


df_long.head(8)


# In[40]:


#I will break this dataframe into two dataframes
df_long_1 = df_long.iloc[0:4]


# In[41]:


df_long_1


# In[42]:


df_long_2 = df_long.iloc[4:8]


# In[43]:


df_long_2


# In[44]:


#Here we can merge two datasets based on their key which is the column profession which is unique for the each dataframe


# In[45]:


df_long_merged = df_long_1.append(df_long_2)
df_long_merged


# # Conclusion: 
# 
# Your data cleaning plan should be based on the 5 above mentioned principles
