import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
from dotenv import load_dotenv
from data_store import *

# Load environment variables
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

# Initialize the LLM
llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=api_key,
    temperature=0
)

st.title("📧 Cold Mail Generator")

# Input URL
url = st.text_input("Enter the URL of the career page:", "https://jobs.nike.com/job/R-36827?from=job%20search%20funnel")

if st.button("Generate Cold Email"):
    if url:
        # Load and process the webpage
        loader = WebBaseLoader(url)
        page_data = loader.load()[0].page_content.replace("\n", "").strip()

        # Extract job information
        prompt_extract = ChatPromptTemplate.from_template(
            """
            ####SCRAPED TEXT FROM THE WEBSITE:
            {page_data}
            ####INSTRUCTIONS:
            This is the scraped text from a career's page website.
            Your job is to extract the job postings and return them
            in JSON format (don't put in a list) containing the following keys:
            'role', 'experience', 'skills', 'description'.
            Only return the valid JSON. Do not include explanations, code, or any other text.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        prompt = prompt_extract.format_messages(page_data=page_data)
        res = llm.invoke(prompt)

        # Parse the response
        json_parser = JsonOutputParser()
        job = None
        links_list = []

        try:
            json_res = json_parser.parse(res.content)
            job = json_res
            # If you have a vector store collection, you can query it here
            links_list = collection.query(query_texts=job['skills'], n_results=2).get('metadatas', [])
        except Exception:
            st.error("The response was not valid JSON. Please check the LLM output.")

        if job:
            # Generate the cold email
            prompt_email = ChatPromptTemplate.from_template(
                """
                    ##JOB DESCRIPTION:
                    {job_description}
                    ##INSTRUCTIONS:
                    You are Farukh, a business development executive at Datics AI. Datics AI is an AI & Software Consulting company that helps businesses streamline their operations with cutting-edge technology solutions.
                    Highlight how Datics AI can meet the requirements of the job posting with relevant examples of past work. Use clear, concise language.
                    
                    Incorporate relevant portfolio links from the following: {links_list}. These should be highly relevant to the job description and showcase Datics AI's expertise in similar projects.

                    Ensure the email is professional, respectful, and brief, focusing on how Datics AI can add value without going into too much technical detail.

                    ### COLD EMAIL FORMAT:
                    - Start with a personalized greeting.
                    - Mention that you came across the job posting and highlight a key skill or requirement.
                    - Briefly introduce Datics AI and mention how the company can help based on the specific needs of the job description.
                    - Add one or two links from the portfolio in bullet points(from {links_list}) relevant to the job requirements.
                    - Offer a call or meeting to discuss further.
                    - Close professionally.

                    ### EMAIL (NO PREAMBLE):

                """
            )
            prompt1 = prompt_email.format_messages(job_description=job, links_list=links_list)
            response = llm.invoke(prompt1)
            print(links_list)
            print(job)
            st.text_area("Generated Cold Email:", response.content, height=300)
        else:
            st.error("Failed to extract job information.")
    else:
        st.warning("Please enter a valid URL.")
