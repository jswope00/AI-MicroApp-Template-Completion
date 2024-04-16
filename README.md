# AI MicroApp (Completion)

## Overview
This AI MicroApp template is a simple Streamlit application that demonstrates how to integrate AI models with a web interface using Streamlit. It means that you can build and share AI "MicroApps" as simply as building a form. 

It works with the Completion API and similar. Meaning, it is a "one-shot" request and there is no memory of a conversation like with a chatbot. It is most suitable for one-off requests where prompting is important. For example, "Write me MCQs from this content..." or "Generate a storyboard based on these learning objectives..."

It also doesn't store data anywhere except for some storage required in the local browser which is cleared after the session ends. 

## Prerequisites
- Python 3.6 or later
- pip
- virtualenv (optional but recommended)
- OpenAI, Claude, and/or Google Gemini API key(s)

## Local Setup Instructions

### 1. Clone the repository

Navigate to a location where you'd like to run this app from, and clone the repo:

```bash
git clone https://github.com/jswope00/AI-MicroApp-Template-Completion.git
```

### 2. Create a Virtual Environment

To create a virtual environment, navigate to your project directory in the terminal:
```bash
cd AI-MicroApp-Template-Completion
```

It's recommended to isolate the project's dependencies using a virtual environment. You can utilize tools like venv or virtualenv to achieve this. Refer to official documentation for specific commands based on your chosen tool. Here is the command from a mac shell:
```bash
python3 -m venv venv
```

Finally, activate your virtual environment:
```bash
source venv/bin/activate
```

### 3. Install Requirements
Activate your virtual environment and install the required packages using pip:
```bash
pip3 install -r requirements.txt
```

### 3. Add your API key(s):
Create a file named .env in your project's root directory. Paste your API key(s) inside the file. See .env_sample file for required format. 

## Running the App

### Running Locally

Navigate to your project directory in the terminal and execute the following command to launch the Streamlit app:
```bash
streamlit run main.py
```

This will open the Birthday App in your web browser, typically at http://localhost:8501.

### Running a Web App

This app is built to be hosted on Streamlit and can be deployed with [Streamlit's 3-step deployment process]([url](https://docs.streamlit.io/get-started/tutorials/create-an-app#share-your-app)): 

1. Put your app in a public GitHub repo (and make sure it has a requirements.txt!)
2. Sign into share.streamlit.io
3. Click 'Deploy an app' and then paste in your GitHub URL

Streamlit is a platform for hosting and sharing web apps. Community (public) apps are free to host. In addition, this template is built using only temporary local storage and no database, for ease of setup and data privacy. 

Deployment outside of Streamlit is certainly possible but outside the scope of this README.

### Explanation

The app leverages Streamlit to create a user interface and OpenAI's API for interacting with a large language model. Here's a breakdown of the key functionalities:

-   **User Input:**  The app gathers user information through text input fields and radio buttons for name, age, and birth month.
-   **Prompt Building:**  Based on user input, the app constructs a prompt for the OpenAI API, incorporating placeholders for dynamic values.
-   **API Interaction:**  The app sends the constructed prompt to the OpenAI API using your provided key and retrieves the response.
-   **Output:**  The AI's response is displayed within the Streamlit app.

### Customization

The code includes sections for various app aspects you can customize:

-   `APP_TITLE`: Update the application title displayed at the top.
-   `APP_INTRO`: Modify the introductory text providing a brief description of the app.
-   `APP_HOW_IT_WORKS`: (Optional) Include a detailed explanation of the app's functionality within an expandable section.
-   `SHARED_ASSET`: (Optional) If you have an asset (like a PDF) to share, configure its download button here.
-   `fields`: This dictionary defines the user input fields, including their types, labels, default values, and formatting options.
-   `actions`: This dictionary defines buttons within the app, including their labels and the functions they trigger.
-   `prompt`: This dictionary holds the message prompts sent to the OpenAI API, with placeholders for user-entered data.
-   `AI_CONFIGURATION`: This section configures various parameters for the OpenAI API call, such as the model to use, temperature, and token limits.

Feel free to experiment with these configurations to tailor the app's behavior and appearance to your preferences.


