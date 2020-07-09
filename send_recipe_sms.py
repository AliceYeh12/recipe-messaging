import requests 
from twilio.rest import Client

# Spoonacular API
ingredient_list = input("Enter a list of ingredients that you have (comma separated): ")
num_recipes = int(input("Enter the number of recipes you want to receive: "))
phone_num = input("Enter your phone number (format is +10000000000): ")

# API endpoint
URL = "https://api.spoonacular.com/recipes/findByIngredients?apiKey=8c041850bfb64656b32ec72ba28edcc6"
  
# Defining the parameters
PARAMS = {"ingredients": ingredient_list, "number": num_recipes, "limitLicense": True, "ranking": 1, "ignorePantry": True} 
  
# Sending GET request and saving the data
r = requests.get(url = URL, params = PARAMS) 
  
# Extracting data in JSON format 
data = r.json() 

# print(data)

recipes = {}
for recipe in data:
    usedIngredients = []
    missedIngredients = []
    allIngredients = []

    for used in recipe["usedIngredients"]:
        usedIngredients.append(used["original"])
    for missed in recipe["missedIngredients"]:
        missedIngredients.append(missed["original"])
    
    allIngredients.append(usedIngredients)
    allIngredients.append(missedIngredients)

    recipes[recipe["title"]] = allIngredients

recipe_str = ""
for dish, ingredients in recipes.items():
    recipe_str += dish + ": "
    recipe_str += f"Ingredients you already have: {ingredients[0]} \nIngredients you need: {ingredients[1]}\n"

print(recipe_str)

# Twilio Messaging
account_sid = "" # Enter Account SID.
auth_token = "" # Enter auth token.
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body=recipe_str,
         from_="", # Enter Twilio phone number.
         to=phone_num
     )

print(message.sid)