import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key = os.getenv('OPENAI_NLP_KEY'))

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are an assistant tasked with converting event information provided in natural language into a structured JSON format suitable for creating ICS files."},
    {"role": "system", "content": "Output JSON should adhere to this structure: {\"events\": [{\"name\": \"Event name\", \"begin\": \"Start time in ISO format, use local time if timezone not specified\", \"end\": \"Start time in ISO format, use local time if timezone not specified\", \"location\": \"Location or URL if online event\", \"description\": \"Event description\", \"url\": \"Related event URL\", \"organizer\": \"Organizer in required ICS format\", \"category\": \"Event category\", \"RRULE\": \"ICS recurring rule if applicable\"}, ...]}"},
    {"role": "system", "content": "If the date and time provided are unclear, interpret them based on the context or default to British English date format. Leave any unspecified or uncertain information as an empty string in the output."},
    {"role": "system", "content": "Focus solely on information relevant to event creation. Omit any unrelated details."},
    {"role": "system", "content": "If text provided doesn't contain event information, return an JSON object with {\"error\": \"No event information found.\"}"},
    {"role": "user", "content": "There is a team meeting every Tuesday at 3 PM starting from June 5, 2024, at our main office in London. The meeting will cover project updates and is expected to end by 4 PM."},
  ]
)

print(response.choices[0].message.content)

