# app.py
import streamlit as st
from config import *
from datetime import datetime, timedelta
import json
from openai import OpenAI


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
            if st.button(field_label):
                action_map[field_on_click]()
    else:
        # Example of dynamically accessing the function
        my_input_function = function_map[field_type]
        user_input[field_name] = my_input_function(**kwargs)
        # Create a text input field
        #user_input[field_name] = st.text_input(label=field_label,value=field_value,max_chars=field_max_chars,help=field_help,)
        globals()[field_name] = user_input[field_name]
def ai_handler():
    ai_prompt = build_prompt()
    selected_llm = st.session_state['selected_llm']
    llm_configuration = LLM_CONFIGURATIONS[selected_llm]
    if selected_llm == "openai":
        openai_client = OpenAI()
        openai_response = openai_client.chat.completions.create(
            model=llm_configuration["model"],
            frequency_penalty=llm_configuration.get("frequency_penalty", 0),
            max_tokens=llm_configuration.get("max_tokens", 1000),
            presence_penalty=llm_configuration.get("presence_penalty", 0),
            temperature=llm_configuration.get("temperature", 1),
            top_p=llm_configuration.get("top_p", 1),
            messages=[
                {"role": "user", "content": ai_prompt}
            ],
            stream=True
        )
        st.write("OpenAI Response:")
        st.write(openai_response)
    if selected_llm == "gemini":
        st.warning("Work in progress")
    if selected_llm == "claude":
        st.warning("Work in progress")

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


action_map = {"ai_handler": ai_handler}

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
    selected_llm = st.selectbox("Select Language Model", options=LLM_CONFIGURATIONS.keys(),key="selected_llm")

    for i in range(len(actions)):
        # Access each dictionary by its index
        build_fields(i, actions)


if __name__ == "__main__":
    main()
