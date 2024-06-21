APP_TITLE = "Narrative Feedback Generator for Clinical Scenarios"
APP_INTRO = """This application generates feedback in narrative form based on numeric scores. 
"""

APP_HOW_IT_WORKS = """1. Fill in the details of the assessment.
2. Choose the language model.
3. Configure the prompt and additional options.
4. Generate MCQs with hints and feedback if desired.
"""

#TO-DO: Organize the feedback by areas of greatest strengths and greatest weaknesses?

SHARED_ASSET = ""

fields = {
    "exam_name": {
        "type": "text_input",
        "label": "Exam Name",
        "value": "PCM501 CLINICAL SKILLS",
        "key": "exam_name"
    },
    "priorities": {
        "type": "number_input",
        "label": "Negotiates priorities & sets agenda",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "priorities"
    },
    "timeline": {
        "type": "number_input",
        "label": "Timeline",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "timeline"
    },
    "organization": {
        "type": "number_input",
        "label": "Organization",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "organization"
    },
    "transition": {
        "type": "number_input",
        "label": "Transitional statement",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "transition"
    },
    "question_types": {
        "type": "number_input",
        "label": "Questioning skills – types of questions",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "question_types"
    },
    "question_relevance": {
        "type": "number_input",
        "label": "Questioning skills – Relevance and Content",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "question_relevance"
    },

    "question_summarizing": {
        "type": "number_input",
        "label": "Questioning Skills – Summarizing",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "question_summarizing"
    },
    "question_verification": {
        "type": "number_input",
        "label": "Questioning Skills – Verification of Patient Information",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "question_verification"
    },
    "support_systems": {
        "type": "number_input",
        "label": "Support Systems",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "support_systems"
    },
    "education": {
        "type": "number_input",
        "label": "Patient’s Education & Understanding",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "education"
    },
    "consent": {
        "type": "number_input",
        "label": "Informed Consent for Investigations & Procedures",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "consent"
    },
    "shared_plan": {
        "type": "number_input",
        "label": "Achieve a Shared Plan",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "shared_plan"
    },
    "closure": {
        "type": "number_input",
        "label": "Closure",
        "min_value": 0,
        "max_value": 4,
        "value": 2,
        "step": 1,
        "key": "closure"
    }
}

actions = {
    "submit": {
          "type": "button",
          "on_click": "ai_handler",
          "label": "Submit"
        }
}

LLM_CONFIGURATIONS = {
    "gpt-3.5-turbo": {
        "model": "gpt-3.5-turbo-0125",
        "frequency_penalty": 0,
        "max_tokens": 1000,
        "presence_penalty": 0,
        "temperature": .75,
        "top_p": 1,
        "price_input_token_1M": 0.50,
        "price_output_token_1M": 1.50
    },
    "gpt-4-turbo": {
        "model": "gpt-4-turbo",
        "frequency_penalty": 0,
        "max_tokens": 1000,
        "presence_penalty": 0,
        "temperature": 1,
        "top_p": 1,
        "price_input_token_1M": 10,
        "price_output_token_1M": 30
    },
    "gpt-4o": {
        "model": "gpt-4o",
        "frequency_penalty": 0,
        "max_tokens": 1000,
        "presence_penalty": 0,
        "temperature": 1,
        "top_p": 1,
        "price_input_token_1M": 5,
        "price_output_token_1M": 15
    },
    "gemini-pro": {
        "model": "gemini-pro",
        "price_input_token_1M": 7,
        "price_output_token_1M": 21
    },
    "claude-opus": {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000,
        "temperature": 1,
        "price_input_token_1M": 15,
        "price_output_token_1M": 75
    },
    "claude-sonnet": {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 1000,
        "temperature": 1,
        "price_input_token_1M": 3,
        "price_output_token_1M": 15
    },
    "claude-haiku": {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1000,
        "temperature": 1,
        "price_input_token_1M": 0.25,
        "price_output_token_1M": 1.25
    }
}

# config = {'exam_name': 'PCM501 CLINICAL SKILLS', 'priorities': 2, 'timeline': 2, 'organization': 2, 'transition': 2, 'question_types': 2, 'question_relevance': 2, 'question_summarizing': 2, 'question_verification': 2, 'support_systems': 2, 'education': 2, 'consent': 2, 'shared_plan': 2, 'closure': 2}

# def generate_prompt(config):
#     exam_name = config.get("exam_name", "")
    
#     prompt_parts = []
    
#     criteria = {
#         "priorities": "The patient may have other concerns in addition to the chief complaint. If it is an extensive list, then the issues can be ranked. Aim to explore all matters affecting the patient and involve the patient in the plan for addressing all these issues.",
#         "timeline": "Patients tend to present with a multitude of symptoms. Ensure you ask the relevant questions to establish a chronology of the clinical presentation. This helps to establish a disease course.",
#         "organization": "Your data gathering seems disorganized. Try to ask questions on one topic before exploring another.",
#         "transition": "The use of transitional statements can be a valuable communication technique. It alerts the patient to what is coming next. For example, \"I'd like to ask you some personal questions. I ask these from all my patients, and I will keep your answers confidential.\"",
#         "question_types": "When asking questions from patients, begin with an open-ended question, followed by more specific questions. Limit the use of why questions and leading questions. The aim is to encourage the patient to talk.",
#         "question_relevance": "Symptoms do not occur in isolation. It is imperative to elicit the presence and absence of symptoms associated with the chief complaint to aid in formulating differential diagnoses.",
#         "question_summarizing": "Summarization is a valuable communication technique to do before completing the patient encounter. It allows patients to check for accuracy. The physician also benefits since it serves as a review for clarity and completeness.",
#         "question_verification": "Aim to seek verification and clarity whenever there are ambiguous patient responses.",
#         "support_systems": "You did not investigate the patient's support systems. You have to determine the finances and other resources available to the patient. Furthermore, feasibility for access to healthcare must be determined.",
#         "education": "Aim to check patient understanding of information. Techniques include \"teach-back,\" posing hypotheticals.",
#         "consent": "Diagnostic investigations and procedures play an essential role in patient management- screening, diagnosis, monitoring, prognosis. The patient must understand the risks, benefits, alternatives of these, and the consequences of refusal.",
#         "shared_plan": "Diagnosis and prognosis must be discussed in detail. The patient must be encouraged to participate in this plan, for example, sharing their thoughts. This increases patient satisfaction, understanding, empowerment, responsibility.",
#         "closure": "The physician must inform the patient about their shared plan for the future at the end of the interview. The need or no need for follow-up must be discussed and arranged. Both physician and patient must be cognizant of their responsibilities."
#     }
    
#     for criterion, feedback in criteria.items():
#         if config.get(criterion, 0) <= 2:
#             prompt_parts.append(feedback)
    
#     if prompt_parts:
#         intro = f"Patient History Taking and Management are essential responsibilities of a physician. This e-mail provides notes on the communication and interpersonal skills portion of your {exam_name} exam.\n\n"
#         prompt = intro + "\n\n".join(prompt_parts) + "\n\n"
#         return f"""Please rewrite the following narrative clinical feedback being provided to a medical student who has completed a clinical scenario. 
#     - Use depersonalized language. 
#     - Use passive voice. \n\n
#     {prompt}"""
#     else:
#         high_performance = f"""Patient History Taking and Management are essential responsibilities of a physician. This e-mail provides notes on the communication and interpersonal skills portion of your {exam_name} exam.\n\n
#         High standards in every component of the patient encounter were achieved. 
#         The chief complaint and other issues affecting their daily living were obtained from the patient. 
#         Relevant questions were asked to elicit symptom chronology and thus disease course. 
#         Questions posed to the patient followed a pattern and theme which shows organized data gathering. 
#         The patient was encouraged to talk using open-ended questions, clarifying ambiguous responses. 
#         Pertinent positives and pertinent negatives were drawn, which aided in formulating differential diagnoses. 
#         Communication skills displayed were proficient, evident in transition statements and summarization. 
#         The management plan was practical and collaborative, ensuring the patient was educated and addressed all the issues."""
        
#         return f"""Please rewrite the following narrative clinical feedback being provided to a high performing medical student who has completed a clinical scenario with a very good score. 
#             - Acknowledge the users impressive performance.
#             - Use depersonalized language. 
#             - Use passive voice. \n\n
#             {high_performance}"""


#     return prompt


def generate_prompt(config):
    exam_name = config.get("exam_name", "")
    
    feedback = {
        "positive": [],
        "improvement": []
    }
    
    criteria = {
        "priorities": {
            "positive": "Excellent job exploring all matters affecting the patient and involving them in addressing these issues.",
            "improvement": "The patient may have other concerns in addition to the chief complaint. If it is an extensive list, then the issues can be ranked. Aim to explore all matters affecting the patient and involve the patient in the plan for addressing all these issues."
        },
        "timeline": {
            "positive": "Well done establishing a clear chronology of the clinical presentation.",
            "improvement": "Patients tend to present with a multitude of symptoms. Ensure you ask the relevant questions to establish a chronology of the clinical presentation. This helps to establish a disease course."
        },
        "organization": {
            "positive": "Excellent organization of data gathering. Questions were asked in a logical sequence, focusing on one topic before moving to another.",
            "improvement": "Your data gathering seems disorganized. Try to ask questions on one topic before exploring another."
        },
        "transition": {
            "positive": "Effective use of transitional statements throughout the interview, smoothly guiding the patient through different topics and preparing them for what comes next.",
            "improvement": "The use of transitional statements can be a valuable communication technique. It alerts the patient to what is coming next. For example, \"I'd like to ask you some personal questions. I ask these from all my patients, and I will keep your answers confidential.\""
        },
        "question_types": {
            "positive": "Skillful use of various question types, starting with open-ended questions and following up with specific inquiries. This approach effectively encouraged the patient to share information.",
            "improvement": "When asking questions from patients, begin with an open-ended question, followed by more specific questions. Limit the use of why questions and leading questions. The aim is to encourage the patient to talk."
        },
        "question_relevance": {
            "positive": "Thorough exploration of symptoms associated with the chief complaint, effectively eliciting both pertinent positives and negatives to aid in formulating differential diagnoses.",
            "improvement": "Symptoms do not occur in isolation. It is imperative to elicit the presence and absence of symptoms associated with the chief complaint to aid in formulating differential diagnoses."
        },
        "question_summarizing": {
            "positive": "Excellent use of summarization techniques before concluding the patient encounter, allowing for verification of accuracy and completeness of information gathered.",
            "improvement": "Summarization is a valuable communication technique to do before completing the patient encounter. It allows patients to check for accuracy. The physician also benefits since it serves as a review for clarity and completeness."
        },
        "question_verification": {
            "positive": "Consistently sought verification and clarity for ambiguous patient responses, ensuring accurate understanding of the patient's situation.",
            "improvement": "Aim to seek verification and clarity whenever there are ambiguous patient responses."
        },
        "support_systems": {
            "positive": "Comprehensive investigation of the patient's support systems, including finances and resources available. Excellent assessment of the patient's access to healthcare.",
            "improvement": "You did not investigate the patient's support systems. You have to determine the finances and other resources available to the patient. Furthermore, feasibility for access to healthcare must be determined."
        },
        "education": {
            "positive": "Effective use of techniques such as 'teach-back' and hypothetical scenarios to check and ensure patient understanding of information provided.",
            "improvement": "Aim to check patient understanding of information. Techniques include \"teach-back,\" posing hypotheticals."
        },
        "consent": {
            "positive": "Thorough explanation of diagnostic investigations and procedures, clearly communicating risks, benefits, alternatives, and potential consequences of refusal.",
            "improvement": "Diagnostic investigations and procedures play an essential role in patient management- screening, diagnosis, monitoring, prognosis. The patient must understand the risks, benefits, alternatives of these, and the consequences of refusal."
        },
        "shared_plan": {
            "positive": "Excellent discussion of diagnosis and prognosis, actively encouraging patient participation in the plan. This approach likely increased patient satisfaction, understanding, empowerment, and responsibility.",
            "improvement": "Diagnosis and prognosis must be discussed in detail. The patient must be encouraged to participate in this plan, for example, sharing their thoughts. This increases patient satisfaction, understanding, empowerment, responsibility."
        },
        "closure": {
            "positive": "Clear and comprehensive closure of the interview, including a well-explained shared plan for the future and appropriate discussion of follow-up needs. Both physician and patient responsibilities were clearly outlined.",
            "improvement": "The physician must inform the patient about their shared plan for the future at the end of the interview. The need or no need for follow-up must be discussed and arranged. Both physician and patient must be cognizant of their responsibilities."
        }
        # ... (continue for all other criteria)
    }
    
    for criterion, messages in criteria.items():
        score = config.get(criterion, 0)
        if score >= 3:
            feedback["positive"].append(f"[{criterion}_positive] {messages['positive']}")
        else:
            feedback["improvement"].append(f"[{criterion}_improvement] {messages['improvement']}")
    
    intro = f"Patient History Taking and Management are essential responsibilities of a physician. This e-mail provides feedback on the communication and interpersonal skills portion of your {exam_name} exam.\n\n"
    
    positive_feedback = "\n".join(feedback["positive"]) if feedback["positive"] else "No specific positive feedback provided."
    improvement_feedback = "\n".join(feedback["improvement"]) if feedback["improvement"] else "No specific areas for improvement identified."
    
    prompt = f"""
Please rewrite the following narrative clinical feedback for a medical student who has completed a clinical scenario. Organize the feedback into positive aspects first, followed by areas for improvement. Use depersonalized language and passive voice:

Positive Feedback:
{positive_feedback}

Areas for Improvement:
{improvement_feedback}

Please format your response using the following template:

{intro}

[Brief narrative summary of positive feedback, provided in paragraph format, no more than three sentences. You do not have to incorporate all the positive feedback attributes. Not a bullet list]

Areas for Improvement:
- [Area 1]
- [Area 2]
...

Conclusion:
[A brief summary of the student's performance and encouragement for future improvement]
"""
    
    return prompt
