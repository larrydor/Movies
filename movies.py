from pprint import pprint
import requests
import os
import json
import http.client
from dotenv.main import load_dotenv
load_dotenv()
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "OOPS, please create an environment variable called 'SENDGRID_API_KEY'")
MY_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL_ADDRESS", "OOPS, please create an environment variable called 'SENDER_EMAIL_ADDRESS'")
SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID", default="OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
API_KEY = os.getenv("RAPID_API_KEY")

print("-------------------------")
x = input("Film Title you seek to research: ")
print("Title selected: ", x)
print("Let me look that up for you...")

conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

conn.request("GET", "/auto-complete?q=", headers=headers)

res = conn.getresponse()
data = res.read()

#print(data.decode("utf-8"))

url = "https://imdb8.p.rapidapi.com/auto-complete"


querystring = {"q":x}

headers = {
    'x-rapidapi-key': API_KEY,
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








print("Would you like an emailed copy of this research?")
user_email_address = input("Please input your email address, or 'N' to opt-out: ")

EMAIL_ADDRESS = user_email_address

if user_email_address.upper() in ["N", "NO", "N/A"]:
    print("You've elected to not receive an emailed copy.")
    print("Thank You!")
elif "@" not in user_email_address:
    print("You have entered an invalid email address.")
else:
    print(f"Sending copy to {EMAIL_ADDRESS}.")

    email_products = []
    for items in range(len(selected_ids)):
        if not selected_ids[items].isnumeric():
            email_product = selected_ids[items]
            email_product["name"] = items["name"]
            email_product["price"] = to_usd(items["price"])
            email_products.append(email_product)
        #source: https://stackoverflow.com/questions/10631473/str-object-does-not-support-item-assignment-in-python

    receipt = {
        "subtotal_price_usd": to_usd(total_purchase),
        "tax_price_usd": to_usd(tax_total),
        "total_price_usd": to_usd(total_total),
        "human_friendly_timestamp": now,
        "products": email_products
    }
    
    client = SendGridAPIClient(SENDGRID_API_KEY)

    message = Mail(from_email=MY_EMAIL_ADDRESS, to_emails=user_email_address)
    message.template_id = SENDGRID_TEMPLATE_ID
    message.dynamic_template_data = receipt
    response = client.send(message)

    if str(response.status_code) == "202":
        print("Email sent successfully!")
    else:
        print("Oh, something went wrong with sending the email.")
        print(response.status_code)
        print(response.body)

    print("Thank You!")
