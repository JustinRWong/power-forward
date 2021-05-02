# Power Forward

[![Build Status](https://www.travis-ci.com/JustinRWong/power-forward.svg?token=PypfBCP6DVTswgKuxbJa&branch=main)](https://www.travis-ci.com/JustinRWong/power-forward)

## Team 19 for Data X

## Description
This repository contains the code contents for Power Forward, the ML-enabled brainchild of UC Berkeley data scientists who obsess over where and why Electric Vehicle Charging Stations succeed or fail.

America’s EV Charging Stations have a problem: they aren’t where drivers need them to be. The root of that problem is imperfect planning information.

Power Forward is here to provide a solution by suggesting the best locations for new EV charging infrastructure in cities around the country. We use machine learning to predict where in a city a new charging station would get the most use, based on a technical and holistic analysis rooted in social, environmental, and data sciences. Power Forward delivers its ML powered platform via an interactive map, where users can use the pin drop feature or view heat maps to better understand and predict charging station use and placement. 

One of the biggest issues within the electric vehicle industry right now is the lack of charging stations near an EV driver’s work. “If there were a charging station near your job and you could leave home and work with 80 miles of range every day, there’d be a lot more EV drivers”. What Power Forward is doing will ensure that EV drivers have conveniently placed charging stations around the city, to not only satisfy current users but also attract those who haven’t switched over to an electric vehicle yet. 

A report from the Harris polling firm has found that 49% of their responders haven’t made the switch yet due to “low availability of charging stations” so the potential market is still vast if stations are placed conveniently.

By utilizing and tuning an ensemble of Machine Learning models, this group of data scientists developed a model that will use regional data to provide the most optimal suggestions for the placement of new EV charging stations. The model is driven by key data points around points of interest in the area, which could range from restaurants to office spaces, and utilization rates of existing chargers. Such data systematically finds the best location to install a new charging station for a given area, considering nearby points of interest to engage the EV owner while charging their vehicle. Another key functionality of the product is its ability to predict a utilization rate for any given location, just at the drop of a pin.

### Technical Approach
It all starts with our “POI-based” approach; We use the quantity of Points of Interest (like stores, restaurants, parks, and stadiums) within 500 meters of a location as its defining features. Ultimately, if 2 locations have very similar surrounding POIs, we expect them to have very similar utilization rates.

We had to gather all of our data ourselves. For utilization rates, that meant each member of our team has been webscraping the utilization rate and addresses of chargers from Google Maps nonstop for the past 4 weeks. To gather our POI data, we accessed the Google Places API.

Once we had sufficient data, we built multiple ML models (Neural Nets, Random Forests, Decision Trees, Linear Regression, K-Nearest Neighbors).

Using that model, we predict the utilization rate of a charger at a given location and send that (prediction, Lat, Long) pairing to  our arcGIS Map UI.


About Us: Power Forward is a team of data scientists and engineers passionate about EVs and energy efficiency. The members, Casey McGonigle, Ivy Bragin, Justin Wong, Mickey Piekarski, Sammy Sheldon, and Seth Bloomer, have the technical capability and ambitious drive to optimize the EV charging industry. This project is an affiliate of the UC Berkeley Data-X course and the Sutardja Center for Entrepreneurship and Technology.


### Contributors
Casey McGonigle, Ivy Bragin, Mickey Piekarski, Justin Wong,  Sammy Sheldon, Seth Bloomer

## Starting the Virtual Environment

Follow this as a reference: https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/


To get started with running the venv for Power Forward, run the following command:
```
virtualenv power-forward-app-env
source power-forward-app-env/bin/activate
pip install -r requirements.txt
chmod +x start_local.sh
./start_local.sh
```


## Starting the app

### Locally
```
source power-forward-app-env/bin/activate

ls
Procfile		__pycache__		power-forward-app-env	src			static
README.md		app.py			requirements.txt	start_local.sh		templates

pip install requirements.txt

./start_local.sh
```



### App structure
`server`
Deployed to google cloud engine.


`static`
Deployed to firebase hosting.

### Live (Production)
[Visit our app!](powerforward.tech)


### Analytics
We have analytics such that when any page is loaded, we get ip address, the url visited, and device information sent to our discord channel. This is done in the `src/gateway.py: analytics(req)`

## References
- https://medium.com/innovation-incubator/flask-before-and-after-request-decorators-e639b06c2128
- https://stackoverflow.com/questions/9878020/how-do-i-get-the-user-agent-with-flask
- https://stackoverflow.com/questions/3759981/get-ip-address-of-visitors-using-flask-for-python
- https://medium.com/firebase-developers/hosting-flask-servers-on-firebase-from-scratch-c97cfb204579
- https://cloud.google.com/sdk/gcloud/reference/beta/run/deploy#--platform
