import streamlit as st
from config import *
from datetime import datetime, timedelta
import json
import os
from openai import OpenAI
from google import generativeai
import anthropic

from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
gemini_api_key = os.getenv('GOOGLE_API_KEY')
claude_api_key = os.getenv('CLAUDE_API_KEY')

user_input = {}
function_map = {
    "text_input": st.text_input,
    "button": st.button,
    "radio": st.radio,
    "text_area": st.text_area
}

# Initialize session state for revision count and other variables
if 'revision_count' not in st.session_state:
    st.session_state['revision_count'] = 0
if 'output' not in st.session_state:
    st.session_state['output'] = ""
if 'show_revise' not in st.session_state:
    st.session_state['show_revise'] = False
if 'full_prompt' not in st.session_state:
    st.session_state['full_prompt'] = ""
if 'history' not in st.session_state:
    st.session_state['history'] = []

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
            # If there's an on_click action defined, attach it to the button with a unique key
            if st.button(field_label, key=f"{field_name}_button_{i}"):
                action_map[field_on_click]()
    else:
        # Example of dynamically accessing the function
        my_input_function = function_map[field_type]
        user_input[field_name] = my_input_function(**kwargs)
        errors = validate_input(field_name, user_input[field_name], conditions)
        if errors:
            for error in errors:
                st.error(f"{field_name}: {error}")
        globals()[field_name] = user_input[field_name]

def validate_input(field_name, field_value, conditions):
    errors = []
    field_conditions = conditions.get(field_name, {})
    for condition, message in field_conditions.items():
        try:
            # Dynamically replace the field name in the condition with the actual value
            if eval(condition.replace(field_name, f'"{field_value}"')):
                errors.append(message)
        except Exception as e:
            st.error(f"Error evaluating condition: {condition} for field: {field_name}. Error: {e}")
    return errors

def ai_handler(revision_prompt=""):
    if revision_prompt:
        st.session_state['full_prompt'] += " " + revision_prompt
    else:
        st.session_state['full_prompt'] = build_prompt()

    selected_llms = st.session_state['selected_llms']
    for selected_llm in selected_llms:
        if selected_llm in ["gpt-3.5-turbo","gpt-4-turbo","gpt-4o"]:
            llm_configuration = LLM_CONFIGURATIONS[selected_llm]
            try:
                openai_client = OpenAI(api_key=openai_api_key)
                openai_response = openai_client.chat.completions.create(
                    model=llm_configuration["model"],
                    frequency_penalty=llm_configuration.get("frequency_penalty", 0),
                    max_tokens=llm_configuration.get("max_tokens", 1000),
                    presence_penalty=llm_configuration.get("presence_penalty", 0),
                    temperature=llm_configuration.get("temperature", 1),
                    top_p=llm_configuration.get("top_p", 1),
                    messages=[
                        {"role": "user", "content": st.session_state['full_prompt']}
                    ]
                )
                print(openai_response)
                input_price = int(openai_response.usage.prompt_tokens) * llm_configuration["price_input_token_1M"] / 1000000
                output_price = int(openai_response.usage.completion_tokens) * llm_configuration["price_output_token_1M"] / 1000000
                total_price = input_price + output_price
                st.session_state['output'] = openai_response.choices[0].message.content
                st.write(f"**OpenAI Response:** {selected_llm}")
                st.success(st.session_state['output'])
                st.write("Price : ${:.6f}".format(total_price))
                st.session_state['show_revise'] = True
                # Save to history
                st.session_state['history'].append({"prompt": st.session_state['full_prompt'], "response": st.session_state['output']})
            except Exception as e:
                st.write(f"**OpenAI Response:** {selected_llm}")
                st.error(f"Make sure the api key is correct and you have access to these models. GPT-4 and later requires you to buy at least $5 credits to access them. Error: {e}")
        if selected_llm == "gemini-pro":
            llm_configuration = LLM_CONFIGURATIONS[selected_llm]
            try:
                generativeai.configure(api_key=gemini_api_key)
                model = generativeai.GenerativeModel(llm_configuration["model"])
                gemini_response = model.generate_content(st.session_state['full_prompt'])
                st.session_state['output'] = gemini_response
                st.markdown("**Gemini Response:**")
                st.success(st.session_state['output'])
                st.session_state['show_revise'] = True
                # Save to history
                st.session_state['history'].append({"prompt": st.session_state['full_prompt'], "response": st.session_state['output']})
            except Exception as e:
                st.write("**Gemini Response:**")
                st.error(f"Make sure the api key is correct. Error: {e}")
        if selected_llm in ["claude-opus","claude-sonnet","claude-haiku"]:
            llm_configuration = LLM_CONFIGURATIONS[selected_llm]
            try:
                client = anthropic.Anthropic(api_key=claude_api_key)
                anthropic_response = client.messages.create(
                    model=llm_configuration["model"],
                    max_tokens=llm_configuration["max_tokens"],
                    temperature=llm_configuration["temperature"],
                    messages=[
                        {"role": "user", "content": st.session_state['full_prompt']}
                    ]
                )
                input_price = int(anthropic_response.usage.input_tokens) * llm_configuration["price_input_token_1M"] / 1000000
                output_price = int(anthropic_response.usage.output_tokens) * llm_configuration["price_output_token_1M"] / 1000000
                total_price = input_price + output_price
                response_cleaned = '\n'.join([block.text for block in anthropic_response.content if block.type == 'text'])
                st.session_state['output'] = response_cleaned
                st.write(f"**Anthropic Response: {selected_llm}**")
                st.success(st.session_state['output'])
                st.write("Price : ${:.6f}".format(total_price))
                st.session_state['show_revise'] = True
                # Save to history
                st.session_state['history'].append({"prompt": st.session_state['full_prompt'], "response": st.session_state['output']})
            except Exception as e:
                st.write(f"**Anthropic Response: {selected_llm}**")
                st.error(f"Make sure the api key is correct. Error: {e}")

def build_prompt():
    final_prompt = ""
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

def revise_handler():
    if st.session_state['revision_count'] < APP_CONFIG['max_revisions']:
        revision_prompt = st.text_input("Enter your revised request:", key=f"revision_input_{st.session_state['revision_count']}")
        if st.button("Double click to submit", key=f"submit_revision_button_{st.session_state['revision_count']}"):
            st.session_state['revision_count'] += 1
            ai_handler(revision_prompt)
            st.write(f"Revisions left: {APP_CONFIG['max_revisions'] - st.session_state['revision_count']}")
    else:
        st.warning("You have reached the maximum number of revisions.")

action_map = {"ai_handler": ai_handler, "revise_handler": revise_handler}

def main():
    st.title(APP_TITLE)
    st.markdown(APP_INTRO)

    if APP_HOW_IT_WORKS:
        with st.expander("Learn how this works", expanded=False):
            st.markdown(APP_HOW_IT_WORKS)

    for i in range(len(fields)):
        # Access each dictionary by its index
        build_fields(i, fields)

    with st.expander("Show prompt"):
        final_prompt = build_prompt()
        st.write(final_prompt)

    # Display LLM selection dropdown
    selected_llms = st.multiselect("Select Language Model", options=LLM_CONFIGURATIONS.keys(), key="selected_llms")

    for i in range(len(actions)):
        # Access each dictionary by its index
        build_fields(i, actions)

    # Show the revise button if the revisable option is enabled and initial output is generated
    if APP_CONFIG['revisable'] and st.session_state['show_revise']:
        revise_handler()

    # Display history
    if st.session_state['history']:
        with st.expander("Session History", expanded=False):
            for i, entry in enumerate(st.session_state['history']):
                st.write(f"**Prompt {i+1}:** {entry['prompt']}")
                st.write(f"**Response {i+1}:** {entry['response']}")

if __name__ == "__main__":
    main()
