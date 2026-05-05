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

### Installation instructions: 
- Ensure to have the required libraries installed. You can find all the libraries used in the program on the requirements.txt file.
- You can run the program from the terminal or from an IDE like Vscode. If you wish to run the program form the terminal run the command _python main.py_. Similiarily, if running from an IDE run the program from main.py file.

### Updates (Whats Next for FaultLine)
- Fixing buggy features
  - On the home page, the calendar pop up when selecting a date doesn't work very well if you're using macOS, so we need to fix that in future implmentations
  - On the home page, the calendar pop when selecting a date does work if you're using Windows, but you can only really select the day (clicking month/year is buggy)
  - We ran into some issues with the color scheme we orginally had when we tested the program using macOS. It appears that if a user is on dark/light mode, some buttons/features may be less visible. While it works fine when using Windows, we'd like to fix this so that all users see the same GUI
  - On the results page, the events list at the bottom of the window isn't very visible when using Windows (it doesn't let users scroll down the page), but this does work if you're using macOS

- Future implementations
  - we would like add more features so that the user can interact with the data more in the results page (such as being able to click on the graphs to see specific information, adding a map component to get a visual idea of where events took place)
  - we would also like to improve the look of the UI, maybe making a logo and pick a color scheme that goes well with our focus (earth, nature, mathematics, etc)
