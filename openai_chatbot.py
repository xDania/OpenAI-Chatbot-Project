# -*- coding: utf-8 -*-
"""OpenAI_chatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RfYNhIIPE2p5TavRDs0hZdGqJJZ7G1Kk

# 1. What is API? How to make an API call?
- In order to work with APIs in Python, we need tools that will make those requests.
- Next, we need to make a ‘GET’ request, we’ll use the requests.get() function, which requires one argument — the URL we want to make the request to.
"""

import requests

url_test = "https://numbersapi.p.rapidapi.com/6/21/date"
response = requests.get(url_test)

"""### Check the API status code

Status codes are returned with every request that is made to a web server. Status codes indicate information about what happened with a request. Here are some codes that are relevant to GET requests:

200: Everything went okay, and the result has been returned (if any).\
301: The server is redirecting you to a different endpoint. This can happen when a company switches domain names, or an endpoint name is changed.\
400: The server thinks you made a bad request. This can happen when you don’t send along the right data, among other things.\
401: The server thinks you’re not authenticated. Many APIs require login ccredentials, so this happens when you don’t send the right credentials to access an API.\
403: The resource you’re trying to access is forbidden: you don’t have the right perlessons to see it.\
404: The resource you tried to access wasn’t found on the server.\
503: The server is not ready to handle the request.\
"""

print(response)

print(response.status_code)

# Now, let's test a success API endpoint
# Get a list of universities in a specified country.

url = 'http://universities.hipolabs.com/search?country=United+States'

response = requests.get(url)

print(response.status_code)

"""# 2. Next, read from the retrieved data
## We use the `response.json()` method to store the response data in a dictionary object
- note that this only works because the result is written in JSON format – an error would have been raised otherwise.   
- [Read Here](https://requests.readthedocs.io/en/latest/user/quickstart/) for more HTTPs methods
"""

response_json = response.json()
print(response_json)

for i in response_json:
    print(i, "\n")

"""### A complete code for make API call"""

import json

class MakeApiCall:

    def get_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            print("sucessfully fetched the data")
            self.formatted_print(response.json())
        else:
            print(
                f"Hello {parameters['username']}, there's a {response.status_code} error with your request")

    def get_user_data(self, api, parameters):
        response = requests.get(f"{api}", params=parameters)
        if response.status_code == 200:
            print("sucessfully fetched the data with parameters provided")
            self.formatted_print(response.json())
        else:
            print(
                f"Hello {parameters['username']}, there's a {response.status_code} error with your request")

    def formatted_print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def __init__(self, api):
        # self.get_data(api)

        parameters = {
            "username": "Sally"
        }
        self.get_user_data(api, parameters)

url_test = "https://numbersapi.p.rapidapi.com/6/21/date"
if __name__ == "__main__":
    api_call = MakeApiCall(url_test)

"""## Read the json data in dataframe"""

import pandas as pd

df = pd.json_normalize(response_json)
df

"""## Working with a more complex nested json data"""

json_url = "https://itunes.apple.com/gb/rss/customerreviews/id=1500780518/sortBy=mostRecent/json"
r = requests.get(json_url)

# Conversion from JSON to Python:
# data = r.json()
# OR
data = json.loads(r.text)
print(type(data))

# `json.dumps()` encodes any python object into json formatted string
# Conversion from Python to JSON:
new_json =  json.dumps(data)

# The output will be of a JSON string type.
print(type(new_json))

new_json

print(json.dumps(data, sort_keys=True, indent=5))

# Save data to a json file locally
with open("json_data.json", "w") as file:
    json.dump(data, file)

# Read json file in python from local path
with open("json_data.json", "r") as file:
    data_file = json.load(file)

    print(data_file)

"""### Cleaning this json data"""

entries = data["feed"]["entry"]
entries[0]

entries[0].keys()

entries[0]['author']

author_uri_list = []
author_name_list = []

for item in entries:
    author_uri_list.append(list(item.get('author')['uri'].values())[0])
    author_name_list.append(list(item.get('author')['name'].values())[0])

author_uri_dict = {'author_uri' : author_uri_list }
author_name_dict = {'author_name' : author_name_list }

print(author_uri_dict, author_name_dict)

"""## Tips:
You can use `?` or `help()` to get help in python
"""

?

help('math')

"""### Install OpenAI packages and upgrade to the most up-to-date one"""

!pip3 install openai
!pip3 install --upgrade openai

!pip3 show openai | grep Version

"""### Make sure you've generate an API KEY. If not, use this [LINK](https://platform.openai.com/playground)"""

# Initialize the OpenAI client with your API key
import os
from openai import OpenAI

API_KEY = "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"

client = OpenAI(api_key = API_KEY)

"""# 1. Code Interpreter
Code Interpreter allows the Assistants API to write and run Python code in a sandboxed execution environment. This tool can process files with diverse data and formatting, and generate files with data and images of graphs. Code Interpreter allows your Assistant to run code iteratively to solve challenging code and math problems. When your Assistant writes code that fails to run, it can iterate on this code by attempting to run different code until the code execution succeeds.

## Step 1: Create OpenAI Assistant
"""

assistant = client.beta.assistants.create(
    name = "Math Tutor",
    instructions = "You are a personal math tutor. Answer questions briefly, in a sentence or less.",
    tools = [{"type": "code_interpreter"}],
    model = "gpt-3.5-turbo-1106"
)

"""## Step 2: Create a Thread"""

thread = client.beta.threads.create()
print(thread)

"""## Step 3: Add a Message to a Thread"""

message = client.beta.threads.messages.create(
  thread_id = thread.id,
  role = "user",
  content = "Mary, Peter, and Lucy were picking chestnuts. Mary picked twice as much chestnuts than Peter. Lucy picked 2 kg more than Peter. Together the three of them picked 26 kg of chestnuts. How many kilograms did each of them pick?"
  # "Solve this problem: 3x + 11 = 14 ."
  # "What is the result of 78 / 60 ? "
)

print(message)

"""## Step 4: Run the Assistant"""

run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id
)

"""## Step 5: Display the Assistant's Response"""

run = client.beta.threads.runs.retrieve(
    thread_id = thread.id,
    run_id = run.id
)

messages = client.beta.threads.messages.list(
    thread_id = thread.id
)

## reversed -- get the most old messages first
for message in reversed(messages.data):
    print(message.role + ": " + message.content[0].text.value)

"""# 2. Knowledge Retrieval
Retrieval augments the Assistant with knowledge from outside its model, such as proprietary product information or documents provided by your users. Once a file is uploaded and passed to the Assistant, OpenAI will automatically chunk your documents, index and store the embeddings, and implement vector search to retrieve relevant content to answer user queries.

## Upload Files to OpenAI
"""

file = client.files.create(
    file = open("avalon.txt", "rb"),
    purpose = "assistants"
)

print(file)

"""## Delete a file

```
file_deletion_status = client.beta.assistants.files.delete(
  assistant_id=assistant.id,
  file_id=file.id
)

```

## Create the Assistant
"""

assistant = client.beta.assistants.create(
    name = "Avalon Rules",
    instructions = "Teach people how to play Avalon.",
    tools = [{"type": "retrieval"}],
    model = "gpt-3.5-turbo-1106",
    file_ids = [file.id]
)

"""## Create a thread"""

thread = client.beta.threads.create()
print(thread)

"""## Create a message"""

message = client.beta.threads.messages.create(
  thread_id = thread.id,
  role = "user",
  content = "How many teams in the Avalon?"
  # "What does Merlin do?"
)

print(message)

"""## Run the assistant"""

run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id
)

"""## Display the Assistant's Response"""

run = client.beta.threads.runs.retrieve(
    thread_id = thread.id,
    run_id = run.id
)

messages = client.beta.threads.messages.list(
    thread_id = thread.id
)

## reversed -- get the most old messages first
for message in reversed(messages.data):
    print(message.role + ": " + message.content[0].text.value)