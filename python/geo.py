import requests
import pandas as pd
import folium
# Many of the prints & photographs in HAER are tagged with geographic coordinates ('latlong')
# Using the requests package we imported, we can easily 'get' data for an item as JSON and parse it for our latlong:

get_any_item = requests.get("https://www.loc.gov/item/al0006/?fo=json")
#print('latlong: {}'.format(get_any_item.json()['item']['latlong']))
# To retrieve this sort of data point for a set of search results, we'll first use Laura's get_image_urls function.
# This will allow us to store the web address for each item in a list, working through the search page by page.

def get_image_urls(url, items=[]):

    #Retrieves the image_ruls for items that have public URLs available.
    #Skips over items that are for the collection as a whole or web pages about the collection.
    #Handles pagination.

    # request pages of 100 results at a time
    params = {"fo": "json", "c": 100, "at": "results,pagination"}
    call = requests.get(url, params=params)
    data = call.json()
    results = data['results']
    for result in results:
        # don't try to get images from the collection-level result
        if "collection" not in result.get("original_format") and "web page" not in result.get("original_format"):
            # take the last URL listed in the image_url array
            item = result.get("id")
            items.append(item)
    if data["pagination"]["next"] is not None: # make sure we haven't hit the end of the pages
        next_url = data["pagination"]["next"]
        #print("getting next page: {0}".format(next_url))
        get_image_urls(next_url, items)

    return items
url = "https://www.loc.gov/search/?fa=contributor:christianson,+justine&fo=json"
# This is the base URL we will use for the API requests we'll be making as we run the function.
# retrieve all image URLs from the search results and store in a variable called 'image_urls'
image_urls = get_image_urls(url, items=[])

# how many URLs did we get?
len(image_urls)

# to save on a little time, let's see what the last 100 look like
img100 = image_urls[200:300]

len(img100)
#create an empty set to store our latlongs
# storing in a set rather than a list eliminates any potential duplicates
spatial_set = set()

# the parameters we set for our API calls taken the first function
p1 = {"fo" : "json"}

# loop through the item URLs
for img in img100:

    # make HTTP request to loc.gov API for each item
    r = requests.get(img, params=p1)

    # extract only from items with latlong attribute
    try:

        # expose in JSON format
        data = r.json()

        # parse for location
        results = data['item']['latlong']

        # add it to our running set
        spatial_set.add(results)

    # skip anything with missing 'latlong' data
    except:

        # on to the next item until we're through
        pass

# show us the data!
spatial_set

# how many unique data points were we able to gather?
len(spatial_set)
latlong_list = list(spatial_set)
df = pd.DataFrame(latlong_list)
df = df[0].str.split(',', expand=True)
df = df.rename(columns={0: 'latitude', 1: 'longitude'})
df

#df.to_csv('haer_sample.csv')
# convert spreadsheet to pandas dataframe using just the first two columns of the spreadsheet
latlong_df = pd.read_csv('files/haer_sample.csv', usecols=[1,2])
# convert pandas dataframe back to a list for folium
latlong_list = latlong_df.values.tolist()

# picking a spot in the midwest to center our map around
COORD = [35.481918, -97.508469]

# uses lat then lon - the bigger the zoom number, the closer in you get
map_haer = folium.Map(location=COORD, zoom_start=3)

# add a marker to the base leaflet map for every latlong pair in our list
for i in range(len(latlong_list)):
    folium.CircleMarker(latlong_list[i], radius=1, color='#0080bb', fill_color='#0080bb').add_to(map_haer)
# calls the map into display
map_haer
