
# coding: utf-8

# # Segmenting and Clustering Neighborhoods in Toronto

# ## Problem 1

# In[30]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[31]:


List_url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
source = requests.get(List_url).text


# In[32]:


soup = BeautifulSoup(source, 'xml')


# In[33]:


table=soup.find('table')


# In[34]:


column_names=['Postalcode','Borough','Neighbourhood']
df = pd.DataFrame(columns=column_names)


# In[35]:


for tr_cell in table.find_all('tr'):
    row_data=[]
    for td_cell in tr_cell.find_all('td'):
        row_data.append(td_cell.text.strip())
    if len(row_data)==3:
        df.loc[len(df)] = row_data


# In[36]:


df.head()


# In[37]:


df=df[df['Borough']!='Not assigned']


# In[39]:


df[df['Neighbourhood']=='Not assigned']==df['Borough']
df.head()


# In[40]:


temp_df=df.groupby('Postalcode')['Neighbourhood'].apply(lambda x: "%s" % ', '.join(x))
temp_df=temp_df.reset_index(drop=False)
temp_df.rename(columns={'Neighbourhood':'Neighbourhood_joined'},inplace=True)


# In[41]:


df_merge = pd.merge(df, temp_df, on='Postalcode')


# In[42]:


df_merge.drop(['Neighbourhood'],axis=1,inplace=True)


# In[43]:


df_merge.drop_duplicates(inplace=True)


# In[44]:


df_merge.rename(columns={'Neighbourhood_joined':'Neighbourhood'},inplace=True)
df_merge.head()


# In[45]:


df_merge.shape


# # Problem 2

# In[46]:


def get_geocode(postal_code):
    # initialize your variable to None
    lat_lng_coords = None
    while(lat_lng_coords is None):
        g = geocoder.google('{}, Toronto, Ontario'.format(postal_code))
        lat_lng_coords = g.latlng
    latitude = lat_lng_coords[0]
    longitude = lat_lng_coords[1]
    return latitude,longitude


# In[47]:


geo_df=pd.read_csv('http://cocl.us/Geospatial_data')


# In[48]:


geo_df.head()


# In[49]:


geo_df.rename(columns={'Postal Code':'Postalcode'},inplace=True)
geo_merged = pd.merge(geo_df, df_merge, on='Postalcode')


# In[50]:


geo_data=geo_merged[['Postalcode','Borough','Neighbourhood','Latitude','Longitude']]


# In[51]:


geo_data.head()


# In[52]:


toronto_data=geo_data[geo_data['Borough'].str.contains("Toronto")]
toronto_data.head()


# # PROBLEM - 3

# ## The notebook from here includes clustering and plotting of the neighborhoods.

# In[92]:


CLIENT_ID =  'BIV2M0K4TULSISCMODQ2QKB000FOV5K3NKDL4V01J42R4KDZ' # your Foursquare ID
CLIENT_SECRET = 'EFBKBJO5JWEV2LAQ4RUJW5ZOEYAS2NUSW3Z2EUFMMWIAZFSX' # your Foursquare Secret
VERSION = '20180604'


# In[93]:


def getNearbyVenues(names, latitudes, longitudes):
    radius=500
    LIMIT=100
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


# In[91]:



toronto_venues  = getNearbyVenues(neighborhood=toronto_data['Neighborhood'],
                                   latitudes=toronto_data['Latitude'],
                                   longitudes=toronto_data['Longitude']
                                  )

