## RELEVANT FILE DESCRIPTIONS

### API Data Collection
This notebook was used to collect data from Google Maps’ API. It contains a function get_nearest_places, which takes in a set of coordinates and returns 
the places of interest nearest to the coordinates, within the specified radius. The output is a json file containing all of the POIs, and relevant data 
about each place.

### GMaps + Mongo Scraper full-address
This updated version of our Google Maps scraper uploads scraped data to our Mongo database, this time pulling the full address (123 Boulder St, Berkeley CA 90000).
It utilizes selenium and chromedriver to loop through the results of a Google Map's search page, giving us charging station availability rates at the time of pull. 
This data was ultimately used to consider utilization rates in our final model.

### Modeling Timeseries-Utilization Rates
 A formalized compilation of our utilization rate data. This notebook pulls from different collections in our mongoDB database, where we stored the scraped data. Additionally, data transformations were made such that addresses, time of measurement, and geocoding columns were created. There was an uneven distribution of measurements for the charging stations and chargers representing the same location had multiple addresses. This notebook deals with this address mapping issue. Data was grouped at different granularities to prepare data for time series data. 

### X-matrix-gen
This notebook is responsible for our x-matrix generation. Given a list of POIs and a set of (lat, long) coordinates, the x matrix returned features a list of integers representing how many of the 
specified POIs are within the designated radius of a set of coordinates. 

### Data Engineering
For the POI model approach, we needed a single utilization for a unique charging station address, which would reflect how good of a location the charging station is based on surrounding points of interests. This required having geoencoded addresses(lat and long) and ensuring that the selected stations has sufficient measurements. We defined sufficient measurements as stations where we had measurements from 12 unique hours of the day. Additionally, the surrounding points of interest must map to the address. This data engineering hell aggregates all the measurements to come up with a single utilization rate for a single station, combines the charging station to the geoencoded data, and combines the geoencoded data with the results from generating the points of interest X matrix. 
