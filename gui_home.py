import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from data_access import fetch_earthquakes, parse_earthquakes
from data_organization import save_to_csv, clear_csv
from gui_result import ResultsWindow

COUNTRY_COORDINATES = {
    "Chile": (-35.6751, -71.5430),
    "China": (35.8617, 104.1954),
    "Greece": (39.0742, 21.8243),
    "India": (20.5937, 78.9629),
    "Indonesia": (-0.7893, 113.9213),
    "Italy": (41.8719, 12.5674),
    "Japan": (36.2048, 138.2529),
    "Mexico": (23.6345, -102.5528),
    "Nepal": (28.3949, 84.1240),
    "New Zealand": (-40.9006, 174.8860),
    "Peru": (-9.1900, -75.0152),
    "Philippines": (12.8797, 121.7740),
    "Turkey": (38.9637, 35.2433),
    "USA": (37.0902, -95.7129),
}

DEFAULT_RADIUS_KM = 2000

class HomeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("FaultLine: Earthquake Tracker")
        self.root.resizable(False, False)


        #Title label
        self.title_label = tk.Label(
            root,
            text = 'FaultLine: Interactive Earthquake Tracker',
            font = ('Helvetica', 16, 'bold')
        )
        self.title_label.grid(row = 0, column = 0, columnspan = 2, pady = (20, 15))

        #Location
        self.location_label = tk.Label(
            root,
            text = 'Location:',
            font = ('Helvetica', 11)
        )
        self.location_label.grid(row = 1, column = 0, sticky = 'e', padx=(20, 10), pady = 8)
        self.selected_country = tk.StringVar()
        #Defaults to USA as country  
        self.selected_country.set('USA')

        #Location selection
        self.location_dropdown = ttk.OptionMenu(
            root,
            self.selected_country,
            'USA',
            *COUNTRY_COORDINATES.keys()
        )
        self.location_dropdown.config(width = 18)
        self.location_dropdown.grid(row = 1, column = 1, sticky= 'w', padx= (0, 20), pady= 8)

        #start date label
        self.start_date_label = tk.Label(
            root,
            text='Start Date:',
            font=('Helvetica', 11)
        )
        self.start_date_label.grid(row=2, column=0, sticky='e', padx=(20, 10), pady=8)

        #start date entry
        self.start_date_entry = DateEntry(
            root,
            width=18,
            background= 'darkblue',
            foreground= 'white',
            borderwidth= 2,
            date_pattern= 'yyyy-mm-dd',
            selectmode = 'day'
        )
        self.start_date_entry.grid(row=2, column=1, sticky= 'w', padx=(0, 20), pady=8)

        #end date label
        self.end_date_label = tk.Label(
            root,
            text= 'End Date:',
            font=('Helvetica', 11)
        )
        self.end_date_label.grid(row=3, column=0, sticky='e', padx=(20, 10), pady=8)
 
        #end date entry
        self.end_date_entry = DateEntry(
            root,
            width = 18,
            background = 'darkblue',
            foreground = 'white',
            borderwidth = 2,
            date_pattern = 'yyyy-mm-dd',
            selectmode = 'day'
        )
        self.end_date_entry.grid(row=3, column=1, sticky='w', padx=(0, 20), pady=8)

        #magnitude label
        self.magnitude_label = tk.Label(
            root,
            text= 'Min Magnitude:',
            font= ('Helvetica', 11)
        )
        self.magnitude_label.grid(row=4, column=0, sticky= 'e', padx=(20, 10), pady=8)
 
        self.magnitude_frame = tk.Frame(root)
        self.magnitude_frame.grid(row=4, column=1, sticky= 'w', padx=(0, 20), pady=8)
 
        self.magnitude_var = tk.DoubleVar()
        
        # Default minimum magnitude
        self.magnitude_var.set(4.0)  
 
        #magnitude slider 
        self.magnitude_slider = tk.Scale(
            self.magnitude_frame,
            from_ = 0.0,
            to = 9.0,
            resolution = 0.5,
            orient = "horizontal",
            variable = self.magnitude_var,
            length = 160,
        )
        self.magnitude_slider.pack(side = "left")
 
        self.magnitude_value_label = tk.Label(
            self.magnitude_frame,
            textvariable = self.magnitude_var,
            font = ('Helvetica', 11)
        )
        self.magnitude_value_label.pack(side = 'left', padx=(8, 0))

        #fetch data button
        self.fetch_button = tk.Button(
             root,
             text = 'Fetch Data',
             font = ('Helvetica', 12, 'bold'),
             bg = 'pink',
             fg = 'black',
             padx = 20,
             pady = 8,
             command = self.fetch_data
        )
        self.fetch_button.grid(row=5, column=0, columnspan=2, pady=(15, 25))


        #to center clear history 
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row = 6, column= 0, columnspan= 2, pady = (0,25))
        
        #Clear history, contents of csv button
        self.clear_button = tk.Button(
            self.button_frame,
            text = 'Clear History',
            font = ('Helvetica', 11),
            bg = 'pink',
            fg = 'black',
            padx=20,
            pady= 8,
            command = self.clear_history
        )
        self.clear_button.pack(side= 'left', padx = (0,10))

        
    def fetch_data(self):
        """
        Uses user inputs to call fetch_earthquakes() and parse_earthquakes() from data access
        saves results using save_to_csv() from data_orgnaization, will trigger the Results windo to open
        """

        #get user inputs
        country = self.selected_country.get()
        start_date = self.start_date_entry.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date_entry.get_date().strftime("%Y-%m-%d")
        min_magnitude = self.magnitude_var.get()

        #ensure correct date range
        if start_date > end_date:
            messagebox.showerror("Invalid Date Range", "Start date must be before end date")
            return
        
        # Get coordinates for selected country
        latitude, longitude = COUNTRY_COORDINATES[country]

        # Fetch and parse data
        raw_data = fetch_earthquakes(
            start_date = start_date,
            end_date = end_date,
            min_magnitude = min_magnitude,
            latitude =latitude,
            longitude = longitude,
            max_radius_km = DEFAULT_RADIUS_KM
        )

        earthquakes = parse_earthquakes(raw_data)

        #if no earthquakes exist message will be shown
        if not earthquakes:
            messagebox.showinfo("No Results" , "No earthquakes found for the selected filters")
            return 
        
        #save results to CSV
        save_to_csv(earthquakes)

        # open results window
        ResultsWindow(self.root, earthquakes)

    def clear_history(self):
        """
        clears earthquake_data.csv file
        """

        confirm = messagebox.askyesno('Clear History', 'Are you sure you want to delete all saved earthquake data?')

        if confirm:
            clear_csv()
            messagebox.showinfo('Cleared', 'Earthquake history has been cleared.')
