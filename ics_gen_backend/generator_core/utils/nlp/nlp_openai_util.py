import os
from dotenv import load_dotenv
from openai import OpenAI

class NLP_OpenAI_Exception(Exception):
    """Exception for errors encountered with OpenAI NLP service."""
    pass

def nlp_openai(input_text):
  load_dotenv()
  configuration = {"api_key": os.getenv('OPENAI_NLP_KEY'), "model": os.getenv('OPENAI_MODEL')}
  if not all([configuration["api_key"], configuration["model"]]):
    raise NLP_OpenAI_Exception("Missing required OpenAI NLP configuration.")
  
  client = OpenAI(api_key = configuration["api_key"])
  response = client.chat.completions.create(
  model=configuration["model"],
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are an assistant tasked with converting event information provided in natural language into a structured JSON format suitable for creating ICS files."},
    {"role": "system", "content": "Output JSON should adhere to this structure: {\"events\": [{\"name\": \"Event name\", \"begin\": \"Start time in ISO format, use local time if timezone not specified\", \"end\": \"Start time in ISO format, use local time if timezone not specified\", \"location\": \"Location or URL if online event\", \"description\": \"Event description\", \"url\": \"Related event URL\", \"organizer\": \"Organizer in required ICS format\", \"category\": \"Event category\", \"RRULE\": \"ICS recurring rule if applicable\"}, ...]}"},
    {"role": "system", "content": "If the date and time provided are unclear, interpret them based on the context or default to British English date format. Leave any unspecified or uncertain information as an empty string in the output."},
    {"role": "system", "content": "Focus solely on information relevant to event creation. Omit any unrelated details."},
    {"role": "system", "content": "If text provided doesn't contain event information, return an JSON object with {\"error\": \"No event information found.\"}"},
    {"role": "user", "content": input_text},
    ]
  )
  event_json = response.choices[0].message.content
  print(event_json)
  return event_json


nlp_openai("Ellena's Birthday party on 12th December at 7pm at the Roystonpark playground. Meanwhile, John's wedding is on 15th December at 2pm on the same location.")
