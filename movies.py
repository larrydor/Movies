from pprint import pprint
import requests
import os
import json
import http.client
from dotenv.main import load_dotenv
load_dotenv()
API = os.getenv("RAPID_API")

print("-------------------------")
x = input("Film Title you seek to research: ")
print("Title selected: ", x)
print("Let me look that up for you...")

conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")

headers = {
    'x-rapidapi-key': API,
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

conn.request("GET", "/auto-complete?q=", headers=headers)

res = conn.getresponse()
data = res.read()

#print(data.decode("utf-8"))

url = "https://imdb8.p.rapidapi.com/auto-complete"


querystring = {"q":x}

headers = {
    'x-rapidapi-key': API,
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
parsed_response = json.loads(response.text)
#print(type(parsed_response))
#print(parsed_response.keys())
#print(parsed_response)
#pprint(response.text)

film_name = [movies["l"] for movies in parsed_response["d"]]
#print(film_name)
film_year = [movies["y"] for movies in parsed_response["d"]]
#print(film_year)
#print(film_name, film_year)

# Function to convert
# source: https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 

print(listToString(film_name))
print(film_name, film_year)
