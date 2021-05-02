from engine.utils import flatten_json
import googlemaps
import time
import pandas as pd

def get_nearest_places(lat, long, GOOGLE_API_KEY, log=False, type_param = None, radius=500, keyw = None):
    '''
    Gets the nearest places given a coordinate location using the Google Places API.

    Inputs:
    @param lat: latitude coordinate (of charging station, real or potential)
    @param long: longitude coordinate (of charging station, real or potential)
    @param GOOGLE_API_KEY: required Google api key. See https://developers.google.com/maps/documentation/javascript/get-api-key

    Below are parameters for google places api: https://developers.google.com/maps/documentation/places/web-service/search
    @type_param: type of place. See supported types at https://developers.google.com/maps/documentation/places/web-service/supported_types
    @param radius: Defines the distance (in meters) within which to return place results. The maximum allowed radius is 50 000 meters

    Outputs:
    - list of POIs within radius surrounding the given coordinates
    '''
    # Define our Client
    gmaps = googlemaps.Client(key = GOOGLE_API_KEY)

    constructing_places_result = []
    page_token = ''
    location = str(lat) + ',' + str(long)
    n = 3
    uncommon = set(['school','gym','synagogue','church','library','pharmacy','supermarket','park','stadium','clothing_store','museum'])

    if type_param in uncommon or type_param is None:
      n = 1
    for i in range(n): ## get up to 60 places
        if log:
            print("Processing" , i)
        places_berk_result = []
        ## do not include the page token on the first call, since it doesn't exist yet
        ## rankby parameter
        if i==0:
            ## rank by distance if default radius
            if radius != 4000:
                places_result = gmaps.places_nearby(location = location, radius = radius, keyword = keyw, open_now = False, type = type_param)
            else:
                places_result = gmaps.places_nearby(location = location, keyword = keyw,  open_now = False, type = type_param, rank_by='distance')
        else:
            ## rank by distance if default radius
            if radius != 4000:
                places_result = gmaps.places_nearby(location = location,  radius = radius, keyword = keyw, open_now = False, type = type_param, page_token=page_token)
            else:
                places_result = gmaps.places_nearby(location = location,  keyword = keyw, open_now = False,  type = type_param, rank_by='distance', page_token=page_token)

        if log:
            print('\tResults returned the following keys')
            [print("\t> {k}".format(k=k)) for k in places_result.keys()]

        ## indicate if the page token was passed back from google maps response
        if 'next_page_token' in places_result.keys():
            page_token=places_result['next_page_token']
        else:
            if log:
                print('No page token received')

        ## add it to the list off results from previous googlee places api calls
        constructing_places_result.extend(places_result['results'])
        time.sleep(2)

    if log:
        print("Total Results returned: {n}".format(n=len(constructing_places_result)))
    return constructing_places_result


def maps_api_to_df(lat, long, api, type_p, radius):

  places_json_result = get_nearest_places(lat, long, api, type_param = type_p, radius = radius)
  flattened_places_json = [flatten_json(place) for place in places_json_result]
  flattened_places_df = pd.DataFrame(flattened_places_json)

  return flattened_places_df

def X_matrix(lat, lon, api_key, types, radius):
  '''
  inputs:

  lat: latitude of interest
  lon: longitude of interest
  api_key: google maps API key
  types: List of all the types that we are interested in for our model. Ordering of list is very important and determines what each POI will be classified as
  radius: radius from lat/lon coordinates

  output:

  array of len(types) where each index corrensponds to the # of POIs that fall under that category within the given radius of the lat/lon coordinate

  EXAMPLE:

  input

  types: ['restaurant', 'bar', 'grocery', 'gym]

  output:

  [4, 2, 5, 2]

  corresponding to 4 restuarants, 2 bars, 5 grocery stores, and 2 gyms within radius distance from lat/long coordinate

  NOTE:
  We calll the function maps_api_to_df which takes in lat lon api key t and radius and returns a df with this information.
  This function is limited to 60 results per API call. There are some categories that probably have more thatn 60 results in a certain radius
  '''

  print('MAKING X MATRIX')
  # set of all  POI ids that have already come up in a search
  results_set = set()

  # the return value of the function (a list)
  r_val = []

  for t in types:
    types_count = 0
    df = maps_api_to_df(lat, lon, api_key, t, radius)
    if len(df)>0:

      ids = list(df['place_id'])
      for id in ids:
        if id not in results_set:
          types_count+=1
          results_set.add(id)
        # if id not in full_ids:
        #   full_ids.add(id)
          # z = df[df['place_id']==id][['geometry_location_lat','geometry_location_lng','name','icon']]
          # final_df.append(list(z.iloc[0])+[t])
    r_val += [types_count]
    print(t)


  return r_val

def find_surrounding_places(lat, long):
    '''
    Wrapper to generate the X matrix that finds the surrounding places of different points of Interests

    Returns a dictionary that maps the types to the number of types that surround the lat, long input
    '''
    types = ['lodging', 'supermarket', 'pharmacy', 'park', 'restaurant',
       'clothing_store', 'store', 'school', 'gym', 'library',
       'local_government_office', 'doctor', 'stadium', 'museum', 'church',
       'synagogue']
    GOOGLE_API_KEY = 'AIzaSyCOfMy3PtzA64w_cU4YEtAxPa_gXCSnt_k'#os.environ.get('GOOGLE_API_KEY')
    x_vector = X_matrix(lat, long, GOOGLE_API_KEY, types, 500)
    returned_dict = {}
    for t, v in zip(types, x_vector):
        returned_dict[t] = v
    return returned_dict
