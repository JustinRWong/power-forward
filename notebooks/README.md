## RELEVANT FILE DESCRIPTIONS

### API Data Collection -
This notebook was used to collect data from Google Maps’ API. It contains a function get_nearest_places, which takes in a set of coordinates and returns 
the places of interest nearest to the coordinates, within the specified radius. The output is a json file containing all of the POIs, and relevant data 
about each place.

### GMaps + Mongo Scraper full-address -
This updated version of our Google Maps scraper uploads scraped data to our Mongo database, this time pulling the full address (123 Boulder St, Berkeley CA 90000).
It utilizes selenium and chromedriver to loop through the results of a Google Map's search page, giving us charging station availability rates at the time of pull. 
This data was ultimately used to consider utilization rates in our final model.

### Modeling Timeseries- Utilization Rates -
This notebook contains multiple models analyzing utilization rates as a time series.

### Reading Utilization Rates Combining Collections -
A formalized compilation of our utilization rate data. This notebook pulls from mongoDB, where we have stored the scraped data, and was used to geoencode and 
analyze the scraped data.

### X-matrix-gen -
This notebook is responsible for our x-matrix generation. Given a list of POIs, the x matrix returned features a list of integers representing how many of the 
specified POIs are within the designated radius of a set of coordinates. 