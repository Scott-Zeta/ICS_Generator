import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
from datetime import datetime

load_dotenv()
configuration = {
    "api_key": os.getenv("OPENAI_NLP_KEY"),
    "model": os.getenv('OPENAI_MODEL')
}
current_year = datetime.now().year

class NLP_OpenAI_Exception(Exception):
    """Exception for errors encountered with OpenAI service."""
    pass

def nlp_openai(input_text):
  
  if not input_text.strip():
        raise ValueError("There isn't valid text to process.")
      
  try:
    client = OpenAI(api_key = configuration["api_key"])
    response = client.chat.completions.create(
    model=configuration["model"],
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": "You are an assistant tasked with converting event information provided in natural language into a structured JSON format suitable for creating ICS files."},
      {"role": "system", "content": "Output JSON should adhere to this structure: {\"events\": [{\"name\": \"Event name\", \"begin\": \"Start time in ISO format, use local time if timezone not specified\", \"end\": \"Start time in ISO format, use local time if timezone not specified\", \"location\": \"Location or URL if online event\", \"description\": \"Event description\", \"url\": \"Related event URL\", \"organizer\": \"Organizer in required ICS format\", \"category\": \"Event category\", \"RRULE\": \"ICS recurring rule if applicable\"}, ...]}"},
      {"role": "system", "content": "If the date and time provided are unclear, interpret them based on the context or default to British English date format. Leave any unspecified or uncertain information as an empty string in the output."},
      {"role": "system", "content": f"If the year is not clear, use {current_year}."},
      {"role": "system", "content": "Focus solely on information relevant to event creation. Omit any unrelated details."},
      {"role": "system", "content": "If text provided doesn't contain event information, return an JSON object with {\"error\": \"No event information found.\"}"},
      {"role": "user", "content": input_text},
      ]
    )
    event_json = response.choices[0].message.content
    # print(event_json)
    return event_json
  except openai.APIError as e:
    raise NLP_OpenAI_Exception(f"OpenAI API returned an API Error: {e}")
  except openai.APIConnectionError as e:
    raise NLP_OpenAI_Exception(f"Failed to connect to OpenAI API: {e}")
  except openai.RateLimitError as e:
    raise NLP_OpenAI_Exception(f"OpenAI API request exceeded rate limit: {e}")
  except Exception as e:
    raise NLP_OpenAI_Exception(f"An unexpected error occurred: {e}")


# nlp_openai("I have a meeting with John from 2pm to 4pm on 3rd of June at the room 101, Elder Hall, University of Adelaide.")
