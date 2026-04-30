import csv
import os
from datetime import datetime ,timezone


def save_to_csv(earthquakes, filename = "earthquake_data.csv"):
    """
    Saves or appends a list of earthquake records to a csv file. If the file does not exist it will be created with the appropriate header
    row. If the file already exists new records will be appened without rewriting the header 

    Parameters:
        earthquakes (list of dict): List of earthquake records returned by parse_earthquakes()
        filename (str): Name of the CSV file to save to, defaluts to 'earthquake_data.csv'
    
    Returns:
        None
    """

    if not earthquakes:
        print("No earthquake data to save")
        return
    
    #calculate quesry timestamp
    query_timestamp = datetime.now(tz = timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    #CSV file names
    fieldnames = ["query_timestamp", "time", "location", "latitude", "longitude", "depth_km", "magnitude"]

    #check if file alr exists 
    file_exists = os.path.isfile(filename)

    with open(filename, mode = 'a', newline = '') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)

        #if file does not exist write header
        if not file_exists:
            writer.writeheader()
        
        for earthquake in earthquakes:
            row = {"query_timestamp": query_timestamp}
            row.update(earthquake)
            writer.writerow(row)
        
    print(f"saved {len(earthquakes)} earthquake records to '{filename}'")
