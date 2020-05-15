
# coding: utf-8

# # Question 1
# 

# ### Use the BeautifulSoup package or any other way you are comfortable with to transform the data in the table on the Wikipedia page into the above pandas dataframe
# 

# ### Importing lib to get data in required format
# 

# In[29]:


from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen as uReq
import requests
import lxml
import pandas as pd
from pandas import DataFrame
import numpy as np


# In[30]:


my_url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'


# In[31]:


r=requests.get(my_url)


# ### Parsing the web html file with BeautifulSoup package
# 
# 

# In[32]:


# Parse the htlm with Soup
page=bsoup(r.text,"html.parser")
page


# ### 'The htlm 'page' indicates that there is a 'table class' - let's find that table
# 

# In[33]:


rtable=page.table
rtable


# In[35]:


results=rtable.find_all('tr')
nrows=len(results)
nrows


# ### Therefore, there are 181 rows of data ( index 0 to 179) the first two being the table header
# 

# In[36]:


results[0:5]


# ### The Header of the DataFrame is the first row of data [index 0]
# 

# In[37]:


header=results[0].text.split()
header


# ### Let's check some rows in order to prepare to build the loop that will extract all cells into a DataFrame. For example, let's examine row 85
# 

# In[38]:


results[85].text


# In[39]:


results[85].text.split('\n')


# In[40]:


results[85].text.split('\n')


# In[41]:


Postcode=results[85].text.split('\n')[1]
Postcode


# In[42]:


Borough=results[85].text.split('\n')[2]
Borough


# In[43]:


Neighborhood=results[85].text.split('\n')[3]
Neighborhood


# ### Iteration loop to extract all cells into a dataframe df
# 

# In[44]:


# iteration loop to harvest all records

records =[]
n=1
while n < nrows :
    Postcode=results[n].text.split('\n')[1]
    Borough=results[n].text.split('\n')[2]
    Neighborhood=results[n].text.split('\n')[3]
    records.append((Postcode, Borough,Neighborhood))
    n=n+1

df=pd.DataFrame(records, columns=['PostalCode', 'Borough', 'Neighbourhood'])
df.head(5)


# In[45]:


df.shape


# ### Let's check the tail of dataframe to assure all data is included as in Wikipedia table
# 

# In[46]:


df.tail()    #  Perfect! all data is included.


# ### Now, let's remove all rows with Borough = 'Not assigned' strings
# 

# In[47]:


# How many rows have Borough equal to 'Not assigned'?
df[df['Borough']=='Not assigned'].count()


# In[48]:


# drops those rows where 'Not assigned' appears in column '[Borough]'
df1=df[~df.Borough.str.contains("Not assigned")]
df1=df1.reset_index(drop=True)


# In[49]:


df1.head(5)


# In[50]:


df1.tail()


# In[51]:


df1.shape


# ### Now, let's replace 'Not assigned' neighborhoods with the name of the Borough
# 

# In[52]:


df1.loc[df1['Neighbourhood'] == 'Not assigned', 'Neighbourhood'] = df1['Borough']


# In[53]:


df1.head()           # Now, there are no rows with 'Not assigned' strings anymore


# In[54]:


df1.shape


# In[55]:


postalcodes = df1['PostalCode'].nunique()
boroughs = df1['Borough'].nunique()
neighbourhoods= df1['Neighbourhood'].nunique()
print('Unique Postalcodes : ' + str(postalcodes))
print('Unique Boroughs  : '+ str(boroughs))
print('Unique Neighbourhoods  :' + str(neighbourhoods))


# In[56]:


#df1.groupby(['PostalCode','Borough','Neighbourhood']).size().reset_index(name='Count').head()


# ### Let's Consolidate the dataframe to each unique PostalCodes and aggregated Neighbourhoods
# 

# In[57]:


# Starting DataFrame df1
df1.head()


# In[58]:


nrows1=len(df1)
nrows1


# ### Let's keep df1 intact and let's work with df2 as precaution
# 

# In[59]:


# DataFrame df2 also has 212 rows or cells
df2=df1
df2.head()


# In[60]:


# I will use two pointers, 'n and m' to sweep through the dataframe. So 'n' will vary from
#  0 to 211, and 'm ' will vary from 1 to 212
nrows2=len(df2)-1
nrows2


# ## Loop Algorithm to extract the consolidate dataframe df2 with unique postalcodes.
# 

# In[61]:


n=0

while n < nrows2 :
    post1=df2.iloc[n,0]
    #post1
    m=n+1
    post2=df2.iloc[m,0]
    #post2
    neigh1=df2.iloc[n,2]
    neigh2=df2.iloc[m,2]
    if post1==post2:
        df2.Neighbourhood[n,2] = neigh1=neigh1+','+neigh2
        #df2 = df2[df2.Neighbourhood != 'neigh2']
        df2=df2.drop(df2.index[m])
        nrows2=nrows2-1
        df2 = df2.reset_index(drop=True)
    else:
        n=n+1


#df2 = df2.reset_index(drop=True)
# print(post1, post2, 'Nigh1 is...'+ neigh1,',,,,,,,','Nigh2 is...' + neigh2, n,m)
df2.index


# In[62]:


df2.head()


# In[63]:


df2.index


# In[64]:


df2.head(15)


# In[65]:


df2.tail()


# In[66]:


df2.shape


# ### Dataframe has 180 rows and 3 columns 

# # PART - 2

# Now, let's get the Latitude and Longitude coordenates for every PostalCode and add those columns to the dataframe
# 

# In[68]:


# Read the cvs file and convert it to a dataframe
#df_pcodes=pd.read_csv('Toronto_Geospatial_Coordinates.csv')
#df_pcodes.columns = ['PostalCode','Latitude','Longitude']
#df_pcodes.head()

# Read the cvs file and convert it to a dataframe

url='http://cocl.us/Geospatial_data'
df_pcodes=pd.read_csv(url)
df_pcodes.head()


# ### Need to rename the column "Postal Code" to "PostalCode" in order to do a proper merger
# 

# In[69]:


df_pcodes.columns = ['PostalCode', 'Latitude', 'Longitude']
df_pcodes.head()


# ### Now, let's sort our db2 dataframe by PostalCode, then we merge it with the df_pcodes created from the cvs file, based on common column of PostalCodes
# 

# In[70]:


df2s=df2.sort_values('PostalCode')


# ### dataframe 'neighborhoods' contains the latitude and longitude needed to start mapping.
# 

# ### dataframe 'neighborhoods' contains the latitude and longitude needed to start mapping.
# Table is sorted by PostalCode
# 

# In[71]:


neighborhoods=pd.merge(df2s,df_pcodes, how='right', on = 'PostalCode')
neighborhoods.head(15)


# In[72]:


neighborhoods.shape


# ## End of part - 2

# # PART - 3:

# ### Explore and cluster the neighborhoods in Toronto
# 

# In[76]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

#!conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans


import folium # map rendering library

print('Libraries imported.')


# ### I will focus on a subset of all the Borough that contain the word "Toronto".
# 

# In[78]:


toronto_data= neighborhoods[neighborhoods['Borough'].str.contains('Toronto', na = False)].reset_index(drop=True)
toronto_data.head()


# In[75]:


toronto_data.shape


# In[79]:


latitude = 43.6532
longitude= -79.3832


# ### Let's create a map of Toronto with Boroughs that cointain the word Toronto
# 

# In[80]:


# create map of TORONTO using latitude and longitude values above:
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=11)

# add markers to map
for lat, lng, label in zip(toronto_data['Latitude'], toronto_data['Longitude'], toronto_data['Neighbourhood']):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# ### Next, we are going to start utilizing the Foursquare API to explore the neighborhoods and segment them.
# 

# ### Let's create a function to repeat the same process to all the neighborhoods in Manhattan Lab example¶
# 

# In[81]:


LIMIT = 100 # limit of number of venues returned by Foursquare API
radius = 500 # define radius


# In[82]:


def getNearbyVenues(names, latitudes, longitudes, radius=500):
    
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
        print(name)
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        # make the GET request
        results = requests.get(url).json()["response"]['groups'][0]['items']
        
        # return only relevant information for each nearby venue
        venues_list.append([(
            name, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighborhood', 
                  'Neighborhood Latitude', 
                  'Neighborhood Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)


# ### Now write the code to run the above function on each neighborhood and create a new dataframe called toronto_venues.
# 

# In[88]:


CLIENT_ID = BIV2M0K4TULSISCMODQ2QKB000FOV5K3NKDL4V01J42R4KDZ
CLIENT_SECRET = 


EFBKBJO5JWEV2LAQ4RUJW5ZOEYAS2NUSW3Z2EUFMMWIAZFSX

VERSION = '20180605'

print("Your Credentials:")
print('CLIENT_ID: ' + BIV2M0K4TULSISCMODQ2QKB000FOV5K3NKDL4V01J42R4KDZ)
print('CLIENT_SECRET:' + EFBKBJO5JWEV2LAQ4RUJW5ZOEYAS2NUSW3Z2EUFMMWIAZFSX)



