# CS122 Project: FaultLine: Interactive Earthquake Tracker

## Authors: 
- Matilda Verdejo
- Guadalupe Carrillo Vega
  
## Author Emails: 
- matilda.verdejoaitken@sjsu.edu
- guadalupe.carrillovega@sjsu.edu

## Project Description:
This project is an interactive real-time Earthquake Monitoring tool built with Python. It pulls seismic data from the [USGS Earthquake Hazards API](https://earthquake.usgs.gov/fdsnws/event/1/), a free and publicly available data source maintained by the U.S. Geological Survey. Users can search for earthquakes by location, filter results by magnitude and date range, and view the number of events (seismic activity/earthquakes) in a given time period, stats related to the data (mean/median frequency, etc), and the places/times where they happened. The goal of this project is to make seismic activity data more accessible and interpretable through a user-friendly interface combined with meaningful statistical analysis and visual outputs. Understanding earthquake patterns helps scientists, governments, and everyday people anticipate risk, allocate emergency resources, and build safer infrastructure; a need that is urgent in California, where seismic activity is prevalent. 

## Project Outline/Plan 
### Interface Plan:
- The interface will consist of a GUI built with Python's Tkinter library.
- We intend to include two windows, "Home" which will allow users to request data and select filters, and "Results" which will display the earthquake information.
- The "Home" window's filters will come in the form of buttons for selecting magnitude range, location, date (sliders/dropdowns), and ultimately a button to fetch data, triggering the API request.
- When the user clicks the "fetch data" button, it will prompt the "Results" window to pop up, showing graphs/tables of earthquake events.
- We also added a "clear history" button to reset the program in the home window

### Data Collection and Storage Plan (Partner #1: Guadalupe Carrillo Vega):
- Data will be collected from the USGS Earthquake Hazards API (https://earthquake.usgs.gov/fdsnws/event/1/), which provides free access to global seismic event data with no API key requiered.
- The program will send HTTP GET requests using Python's 'requests' library.
  - Query parameters will include: location, magnitude range, and date range which will be supplied by the user through our interface.
- USGS responses are returned in GeoJSON format and will be parsed using Python's built-in 'json' module to extract relevent fields.
  - Fields include: event time, location name, latitude, longitude, depth, and magnitude.
- Cleaned data will be stored locally in a CSV file using Python's 'csv' module, with each row representing one earthquake event.
- If the user runs a new query, new results will be appended to the existing CSV file with a timestamp column so records from different sessions can be destinguished.     

### Data Analysis and Visualization Plan (Partner #2: Matilda Verdejo):
- Once earthquake data is collected and stored, the program will perform statistical analyses to allow users to understand seismic patterns, using Python's numpy and scipy libraries.
- This includes calculating median, mean, standard deviation of earthquake magnitudes, and frequency trends over user specified time ranges.
- We will use matplotlib for the visualization component to generate two plots, a chart showing earthquake frequency over time, and a histogram showing distribution of magnitude in a given dataset.
- Both plots show up in the same results window, rather than other pop-ups
- we also added a "close" button that closes the results window and redirects users back to the home window.
