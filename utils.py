"""
Libraries
"""
import streamlit as st
import pandas as pd
import datetime
import os, os.path
import warnings
import random
from google import genai
import requests
import re
import json
import pymysql
import fitz
import docx
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

"""
Dashboard Information
"""
APP_NAME = 'onllaw'
ABOUT_HEADER = 'About'
CONTRACT_INSIGHT_HEADER = "Contract Insights"
LABOUR_LAW_HEADER = 'Labour Law Information'
LAWYER_INFORMATION_HEADER = 'Lawyer Information'
APP_FILTERS = 'Filters'
NO_DATA_INFO = 'No data available to display based on the filters'

warnings.simplefilter(action='ignore', category=FutureWarning)
st.set_page_config(
    page_title=APP_NAME,
    layout="wide"
)



# Load data
@st.cache_data
def load_data(DATA_URL,DATA_TYPE):
    if DATA_TYPE == 'xlsx':
        data = pd.read_excel(DATA_URL)
    elif DATA_TYPE == 'geojson':
        data = pd.read_json(DATA_URL)
    return data


"""
Lawyer Information 
"""
law_df = load_data("data/law_info.xlsx",'xlsx')


"""
TIDB
"""
# Pick your Gemini model
EMBED_MODEL = "models/embedding-001"
LLM_MODEL = "gemini-2.5-flash"

# --- TiDB Serverless Connection ---
conn = pymysql.connect(
    host=os.getenv("TIDB_HOST"),
    user=os.getenv("TIDB_USER"),
    password=os.getenv("TIDB_PASSWORD"),
    database=os.getenv("TIDB_DATABASE"),
    ssl={"ssl": True}
)

def query_tidb(sql, params=None):
    """Run SQL query against TiDB Serverless"""
    with conn.cursor() as cursor:
        cursor.execute(sql, params or ())
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    return pd.DataFrame(result, columns=columns)


def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text("text")
    return text

def extract_text_from_word(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def embed_text(text):
    """Generate embeddings using Gemini"""
    result = genai.embed_content(model=EMBED_MODEL, content=text)
    return result['embedding']

def gemini_chat(prompt, context=""):
    """Chat with Gemini model"""
    chat = genai.GenerativeModel(model_name=LLM_MODEL)
    response = chat.generate_content(f"Context: {context}\n\nUser: {prompt}")
    return response.text