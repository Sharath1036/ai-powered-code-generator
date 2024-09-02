import streamlit as st
from langchain import PromptTemplate, LLMChain
from langchain_groq import ChatGroq
from langchain.chains import SimpleSequentialChain
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
# print(api_key)

llm = ChatGroq(temperature=0, model_name="llama-3.1-70b-versatile") 

prompt_template = """
You are an AI code generator. Based on the user's description, generate the corresponding code.
Description: {description}
Generated Code:
"""

template = PromptTemplate(input_variables=["description"], template=prompt_template)
chain = LLMChain(llm=llm, prompt=template)

st.title("AI-Powered Code Generator")

if 'conversations' not in st.session_state:
    st.session_state['conversations'] = []

# Function to check if the prompt is asking for code
def is_code_related(prompt):
    # Basic keyword checking
    keywords = ["code", "function", "script", "program", "class", "loop", "method", "tutorial"]
    return any(keyword in prompt.lower() for keyword in keywords)

user_input = st.text_area("Enter your description of the code:", height=150)

if st.button("Generate Code"):
    if user_input:
        # Check if the prompt is asking for code
        if is_code_related(user_input):
            # Run the chain to generate code
            generated_code = chain.run(description=user_input)
            
            # Save the conversation
            conversation = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "description": user_input,
                "generated_code": generated_code
            }
            st.session_state['conversations'].append(conversation)
            st.code(generated_code, language="python")
        else:
            st.error("The input does not seem to be a request for code. Please describe a coding task or request.")
    else:
        st.error("Please enter a description to generate code.")

st.subheader("Conversation History")
for conv in st.session_state['conversations']:
    st.write(f"**Timestamp:** {conv['timestamp']}")
    st.write(f"**Description:** {conv['description']}")
    st.code(conv['generated_code'], language="python")