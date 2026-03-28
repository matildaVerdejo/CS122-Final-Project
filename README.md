# CS122 Project: FaultLine: Interactive Earthquake Tracker

## Authors: 
- Matilda Verdejo
- Guadalupe Carrillo Vega
  
## Author Emails: 
- matilda.verdejoaitken@sjsu.edu
- guadalupe.carrillovega@sjsu.edu

## Project Description:
This prject is an interacive real-time Earthquake Monitoring tool Built in Python. It pulls seismic data from the USGS Earthquake Hazards API, a free and publicaly available data source maintained by the U.S Geological Survey. Users can search for recent earthquakes by location, filter results by magnitude and date range, and view a live feed of seismic activity around the world. The goal of this project is to make seismic activity data more accessible and interpretable through a user-freindly interface combined with meaningful statistical analysis and visual outputs. Understanding earthquake patterns helps scientists, governments, and everyday people anticipate risk, allocate emergency resources, and build safer infastrucutre - a need that is urgent in California, where sciesmic activity is a reality. 

## Project Outline/Plan 
### Interface Plan

### Data Collection and Storage Plan (Partner #1: Guadalupe Carrillo Vega)
Data will be collected from the USGS Earthquake Hazards API (https://earthquake.usgs.gov/fdsnws/event/1/), which provides free access to global seismic event data with no API key requiered. The program will send HTTP GET requests using Python's 'requests' library, with query parameters for location, magnitude range, and date range supplied by the user through our interface. USGS responses are returned in GeoJSON format and will be parsed using Python's built-in 'json' module to extract relevent fields including event time, location name, latitude, longitude, depth, and magnitude. The cleaned data will be stored locally in a CSV file using Python's 'csv' module, with each row representing one earthquake event. If the user runes a new query, new results will be appended to the existing CSV file with a timestamp column so records from different sessions can be destinguished.     

### Data Analysis and Visualization Plan (Partner #2: Matilda Verdejo)

