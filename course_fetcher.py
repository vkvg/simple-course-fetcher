""" 

Very simple and elementary script/module used for fetching data on courses
using the "urllib.request" and "json" modules.

Can currently only be used  on the University of Helsinki API,
e.g. "https://studies.cs.helsinki.fi/stats/api/courses"
If you use some other JSON, it will just be converted to a file by default.

However, more universities' APIs can be quite easily implemented.

TODO:
- add ability to fetch single course using URL with course id
- add more detailed statistics to courses using single-course data
- add better functionality different APIs (e.g. different unis)
- implement better method for identifying URL

"""

import urllib.request
import json
from datetime import datetime

def __save_to_file(json_data: list):
    # Use datetime module to get basic timestamp on file
    time_string = datetime.strftime(datetime.now(), "%H-%M-%S")

    # Declaring filename
    filename = f"course_fetcher_{time_string}.json"

    # Create file with variable "filename" as filename
    with open(filename, "w") as output_file:
        # "Dump" JSON data to file
        json.dump(json_data, output_file)

        # Reassure workings
        print(f"\nData saved to {filename}")

def __handle_url(url: str):
    # Error handling
    if type(url) != str:
        raise TypeError(f"URL form incorrect\nShould be <class \'str\'>, now {type(url)}")

    # Fetch raw data using urlopen, creates HTTPResponse object
    try:
        raw_data = urllib.request.urlopen(url)
    except Exception:
        raise ConnectionError("Could not fetch data from URL, check URL")
    
    # Use .read() method to process string data to JSON
    try:
        processed_data = raw_data.read()
    except Exception:
        raise ValueError("Error reading data, check URL")
    
    # Use .loads() method to convert JSON to dictionary array
    try:
        json_data = json.loads(processed_data)
        return json_data
    except Exception:
        raise ValueError("Error converting data to JSON, check type of data at URL")

# Fetch single course
def fetch_single_course(url: str): raise NotImplementedError

# Main functionality
def fetch_courses(url: str, save_to_file: bool=False, only_enabled: bool=False):
    json_data = __handle_url(url)
    
    # Check if API is "helsinki.fi"
    if "helsinki.fi" in url:
        # Error handling
        try:
            enabled_courses = [course for course in json_data if course["enabled"]]
            print(f"\nFetched {len(json_data)} courses in total, of which {len(enabled_courses)} are enabled")
            
            # Use for-loop to iterate through json_data and print results
            for course in json_data:
                print("\nCourse name: {fullName:>50}\nTerm: {term:>52} {year}\nURL: {url:>58}".format(**course))
                if not only_enabled:
                    if course["enabled"]:
                        enabled_output = "Enabled"
                    else:
                        enabled_output = "Not enabled"
                    print(f"Enabled: {enabled_output:>54}")
        
        # Abort printing if correct data not found for some reason
        except Exception:
            print(f"Error with default string formatting for \"helsinki.fi\" URL:\n\"{url}\",\nsaving data to file")
    
    # If data not from University of Helsinki API
    else:
        print(f"String formatting not available for API \"{url}\"")
    
    # Save data to file if enabled in function parameters
    if save_to_file == True:
        __save_to_file(json_data)

# For testing purposes
""" 
if __name__ == "__main__":
    fetch_courses("https://studies.cs.helsinki.fi/stats-mock/api/courses/", True)
 """
