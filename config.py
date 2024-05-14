

APP_TITLE = "Birthday App"
APP_INTRO = """This is a simple app that calculates what year you were born. It is for demonstrating the capabilities of a MicroApp
"""

APP_HOW_IT_WORKS = ""

SHARED_ASSET = ""

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
        "help": "Your current age in years"
        },
    "birth_month": {
          "type": "radio",
          "label": "What is your Birth month?",
          "options": ["January", "February", "March","April","May","June","July","August","September","October","November","December"],
          "horizontal": True
        }
}

conditions = {
    "name": {
        "len(name) < 4": "Name should be more than 4 characters"
    },
    "age": {
        "not str(age).isdigit()": "Age must be a number",
        "int(age) < 0 or int(age) > 120": "Age must be between 0 and 120"
    }
}

actions = {
    "submit": {
          "type": "button",
          "on_click": "ai_handler",
          "label": "Submit"
        }
}

prompt = {
    "prompt": "Hello! My name is {name}. My age is {age}.",
    "prompt2": "I was born in the month of {birth_month}",
    "prompt3": "Please tell me what year I was born.",
    "prompt4": "Today is May 9, 2024"
}

LLM_CONFIGURATIONS = {
    "gpt-3.5": {
        "model": "gpt-3.5-turbo-0125",
        "frequency_penalty": 0,
        "max_tokens": 1000,
        "presence_penalty": 0,
        "temperature": 1,
        "top_p": 1,
        "price_input_token_1M":0.50,
        "price_output_token_1M":1.50
    },
    "gemini-pro": {
        "model":"gemini-pro",
        "price_input_token_1M":7,
        "price_output_token_1M":21
    },
    "claude-opus":{
        "model":"claude-3-opus-20240229",
        "max_tokens":1000,
        "temperature":1,
        "price_input_token_1M":15,
        "price_output_token_1M":75
    }
}
