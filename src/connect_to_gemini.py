# Python program to connect to google gemini model
# Requirements
# python 3.x
# pip install google-generativeai
import google.generativeai as genai
import os

# Replace with your own API key
# Get the google API key: https://aistudio.google.com/app/apikey
# Create a new system environmental variable with name GOOGLE-API-KEY-VID and value paste the google API key
google_api_key = os.getenv('GOOGLE-API-KEY-VID')
genai.configure(api_key=google_api_key)
# Initialize connection to Gemini
model=genai.GenerativeModel("gemini-pro")

response = model.generate_content("List top 3 cricket matches india played and won from 2020 to 2023, against whom?")

print(response.text)