import streamlit as st
from dotenv import find_dotenv, load_dotenv
from datetime import datetime, timedelta
import json
from openai import OpenAI

load_dotenv()
client = OpenAI()

########  GENERAL APP INFORMATION  ##############

APP_TITLE = "Birthday App"
APP_INTRO = """This is a simple app that calculates what year you were born. It is for demonstrating the capabilities of a MicroApp
"""

APP_HOW_IT_WORKS = ""

SHARED_ASSET = ""

########  FORM FIELDS  ##############

fields = {
    "name": {
          "type": "text_input",
          "label": "What is your name?",
          "value": "John"
        },
    "age" : {
        "type": "text_input",
        "label": "How old are you?",
        "value": 30,
        "max_chars": 2,
        "help": "Your current age in years"
        },
    "birth_month": {
          "type": "radio",
          "label": "What is your Birth month?",
          "options": ["January", "February", "March","April","May","June","July","August","September","October","November","December"],
          "horizontal": True
        },
    "warning": {
          "type": "warning",
          "body": "You are too young to use this app."
        }
}

actions = {
    "submit": {
          "type": "button",
          "on_click": "ai_handler",
          "label": "Submit"
        }
}

########  PROMPT FOR AI  ##############

# The prompt is a dictionary because a future task is to make parts of the prompt conditional. 
prompt = {
    "prompt": "Hello! My name is {name}. My age is {age}.",
    "prompt2": "I was born in the month of {birth_month}",
    "prompt3": "Please tell me what year I was born."
}

final_prompt = ""

######## AI CONFIGURATION #############
AI_MODEL = "gpt-3.5-turbo-0125"
FREQUENCY_PENALTY = 0
MAX_TOKENS = 1000
PRESENCE_PENALTY = 0
TEMPERATURE = 1
TOP_P = 1


####### END OF CONFIGURATION ###########

user_input = {}

function_map = {
    "text_input": st.text_input,
    "warning": st.warning,
    "button": st.button,
    "radio": st.radio
}

# Create variables based on the keys in the fields dictionary
for key, value in fields.items():
    globals()[key] = None

def build_fields(i, my_dict):

    field_name = list(my_dict.keys())[i]
    field_dict = list(my_dict.values())[i]
    field_type = field_dict.get("type","")
    field_label = field_dict.get("label","")
    field_body = field_dict.get("body","")
    field_value = field_dict.get("value","")
    field_max_chars = field_dict.get("max_chars",None)
    field_help = field_dict.get("help","")
    field_on_click = field_dict.get("on_click",None)
    field_options = field_dict.get("options","")
    field_horizontal = field_dict.get("horizontal",False)

    kwargs = {}
    if field_label:
        kwargs['label'] = field_label
    if field_body:
        kwargs['body'] = field_body
    if field_value:
        kwargs['value'] = field_value
    if field_options:
        kwargs['options'] = field_options
    if field_max_chars:
        kwargs['max_chars'] = field_max_chars
    if field_help:
        kwargs['help'] = field_help
    if field_on_click:
        kwargs['on_click'] = field_on_click
    if field_horizontal:
        kwargs['horizontal'] = field_horizontal



    if field_type == "button":
        if field_on_click:
            # If there's an on_click action defined, attach it to the button
            on_click_action_name = field_on_click
            if st.button(field_label):
                action_map[on_click_action_name]()
    else:
        # Example of dynamically accessing the function
        my_input_function = function_map[field_type]

        user_input[field_name] = my_input_function(**kwargs)

        # Create a text input field
        #user_input[field_name] = st.text_input(label=field_label,value=field_value,max_chars=field_max_chars,help=field_help,)
        globals()[field_name] = user_input[field_name]

    

# Define a function for the button click
def ai_handler():
    ai_prompt = build_prompt()
    response = client.chat.completions.create(
    model=AI_MODEL,
    frequency_penalty=FREQUENCY_PENALTY,
    max_tokens=MAX_TOKENS,
    presence_penalty=PRESENCE_PENALTY,
    temperature=TEMPERATURE,
    top_p=TOP_P,
    messages=[
        {"role": "user", "content": ai_prompt}
        ],
    stream=True   
    )
    st.write(response)

def build_prompt():

    final_prompt=""

    for key, value in prompt.items():
        # Use a regular expression to find all placeholders in the string
        import re
        placeholders = re.findall(r'\{(.*?)\}', value)

        # Format the prompt with the corresponding variables
        formatted_prompt = value.format(**{placeholder: globals()[placeholder] for placeholder in placeholders})

        # Concatenate the formatted prompts
        final_prompt += formatted_prompt + " "

    # Remove trailing whitespace
    final_prompt = final_prompt.strip()
    return final_prompt

# Function to map action names to functions
action_map = {
    "ai_handler": ai_handler  # Map the string "ai_handler" to the ai_handler function
}


# Main function to create Streamlit app
def main():
    st.title(APP_TITLE)
    st.markdown(APP_INTRO)

    if APP_HOW_IT_WORKS:
        with st.expander("Learn how this works", expanded=False):
            st.markdown(APP_HOW_IT_WORKS)


    if SHARED_ASSET:
        # Download button for the PDF
        with open(SHARED_ASSET["path"], "rb") as asset_file:
            st.download_button(label=SHARED_ASSET["button_text"],
                        data=asset_file,
                        file_name=SHARED_ASSET["name"],
                        mime="application/octet-stream")



    # Iterate through each dictionary in the list and print the 'title' key
    for i in range(len(fields)):
        # Access each dictionary by its index
        build_fields(i, fields)
    
    with st.expander("Show prompt"):
        final_prompt = st.write(build_prompt())

    for i in range(len(actions)):
        # Access each dictionary by its index
        build_fields(i, actions)


if __name__ == "__main__":
    main()
