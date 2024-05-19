import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key = os.getenv('OPENAI_NLP_KEY'))

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are an assitant help convert the event information included in nature language to JSON output."},
    {"role": "system", "content": "Your output format always follow the following guidelines: {\"events\": [{\"name\":'The name of the event', \"begin\": 'The begin time of the event, always write in ISO time format, if timezone not been specific mentioned, leave it as local time format', \"end\": 'The end time of the event, always write in ISO time format, if timezone not been specific mentioned, leave it as local time format', \"location\": 'The location of the event, put the url if it is an online event', \"description\": The description of the event, \"url\":'the url that relative to the event', \"organizer\": 'Write the organiser as an ics file required format', \"category\": 'The category of the event', \"RRULE\": 'The Recurring event rule, it shall be write in an ics file required format'}, ...more events in the array]}"},
    {"role": "system", "content": "If the date format in nature language provide by user is not clear, determine based on the language or location context. If still can not be determined, use british english date format."},
    {"role": "system", "content": "You shall not provide any information not relative to an event. Anything uncertain or not provided by user, you shall leave it as an empty string in your output."},
    {"role": "user", "content": ""}
  ]
)

print(completion.choices[0].message.content)

