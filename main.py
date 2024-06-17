from openai import OpenAI
import streamlit as st
from config import *
import os
from dotenv import load_dotenv
import re

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

user_input = {}
function_map = {
    "text_input": st.text_input,
    "button": st.button,
    "radio": st.radio,
    "text_area": st.text_area
}

# Initialize session state for variables
if 'output' not in st.session_state:
    st.session_state['output'] = ""
if 'full_prompt' not in st.session_state:
    st.session_state['full_prompt'] = ""
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'additional_prompt' not in st.session_state:
    st.session_state['additional_prompt'] = ""
if 'initial_prompt' not in st.session_state:
    st.session_state['initial_prompt'] = ""
if 'revision_count' not in st.session_state:
    st.session_state['revision_count'] = 0

# Create variables based on the keys in the fields dictionary
for key, value in fields.items():
    globals()[key] = None

def build_fields(i, my_dict):
    field_name = list(my_dict.keys())[i]
    field_dict = list(my_dict.values())[i]
    field_type = field_dict.get("type", "")
    field_label = field_dict.get("label", "")
    field_body = field_dict.get("body", "")
    field_value = field_dict.get("value", "")
    field_max_chars = field_dict.get("max_chars", None)
    field_help = field_dict.get("help", "")
    field_on_click = field_dict.get("on_click", None)
    field_options = field_dict.get("options", "")
    field_horizontal = field_dict.get("horizontal", False)
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

def ai_handler(initial_prompt=False):
    if initial_prompt:
        st.session_state['full_prompt'] = build_prompt()
        st.session_state['initial_prompt'] = st.session_state['full_prompt']
    else:
        st.session_state['full_prompt'] = st.session_state['initial_prompt'] + " " + st.session_state['output'] + " " + st.session_state['additional_prompt']

    selected_llm = st.session_state['selected_llm']
    if selected_llm in ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4o"]:
        llm_configuration = LLM_CONFIGURATIONS[selected_llm]
        try:
            openai_client = OpenAI(api_key=openai_api_key)
            response = openai_client.chat.completions.create(
                model=llm_configuration["model"],
                messages=[
                    {"role": "user", "content": st.session_state['full_prompt']}
                ],
                max_tokens=llm_configuration.get("max_tokens", 1000),
                temperature=llm_configuration.get("temperature", 1),
                top_p=llm_configuration.get("top_p", 1),
                frequency_penalty=llm_configuration.get("frequency_penalty", 0),
                presence_penalty=llm_configuration.get("presence_penalty", 0)
            )
            st.session_state['output'] = response.choices[0].message.content
            st.session_state['history'].append(
                {"prompt": st.session_state['full_prompt'], "response": st.session_state['output']})
            st.session_state['chat_history'].append({"role": "user", "content": st.session_state['full_prompt']})
            st.session_state['chat_history'].append({"role": "assistant", "content": st.session_state['output']})

            # Ensure history does not exceed limit
            if len(st.session_state['chat_history']) > APP_CONFIG['max_revisions'] * 2:
                st.session_state['chat_history'] = st.session_state['chat_history'][
                                                   -(APP_CONFIG['max_revisions'] * 2):]

            input_price = int(response.usage.prompt_tokens) * llm_configuration["price_input_token_1M"] / 1000000
            output_price = int(response.usage.completion_tokens) * llm_configuration[
                "price_output_token_1M"] / 1000000
            total_price = input_price + output_price

            st.write(f"**OpenAI Response:** {selected_llm}")
            st.success(st.session_state['output'])
            st.write(f"Price: ${total_price:.6f}")

            if st.session_state['revision_count'] < APP_CONFIG['max_revisions']:
                st.session_state['show_revise'] = True
            else:
                st.session_state['show_revise'] = False

        except Exception as e:
            st.write(f"**OpenAI Response:** {selected_llm}")
            st.error(f"Error: {e}")

def build_prompt():
    final_prompt = ""
    for key, value in prompt.items():
        # Use a regular expression to find all placeholders in the string
        placeholders = re.findall(r'\{(.*?)\}', value)

        # Format the prompt with the corresponding variables
        formatted_prompt = value.format(**{placeholder: globals()[placeholder] for placeholder in placeholders})
        # Concatenate the formatted prompts
        final_prompt += formatted_prompt + " "

    # Add the additional prompt from user input
    if st.session_state['additional_prompt']:
        final_prompt += st.session_state['additional_prompt']

    # Remove trailing whitespace
    final_prompt = final_prompt.strip()
    return final_prompt

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
    selected_llm = st.selectbox("Select Language Model", options=LLM_CONFIGURATIONS.keys(), key="selected_llm")

    if st.button("Get Initial Response"):
        ai_handler(initial_prompt=True)

    # Display the initial response
    if st.session_state['output']:
        st.subheader("Response")
        st.write(st.session_state['output'])

        # Input for additional prompt
        st.session_state['additional_prompt'] = st.text_input("Enter additional prompt", value="")

        if st.button("Revise") and st.session_state['revision_count'] < APP_CONFIG[
            'max_revisions']:
            st.session_state['revision_count'] += 1
            ai_handler()

    # Display session history in an expander
    if st.session_state['history']:
        with st.expander("Session History", expanded=False):
            for i, entry in enumerate(st.session_state['history']):
                st.write(f"**Prompt {i + 1}:** {entry['prompt']}")
                st.write(f"**Response {i + 1}:** {entry['response']}")
                st.write("-----")

if __name__ == "__main__":
    main()