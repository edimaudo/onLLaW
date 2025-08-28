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
import warnings
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

# Streamlit configuration
warnings.simplefilter(action='ignore', category=FutureWarning)
st.set_page_config(page_title=APP_NAME,layout="wide")

# Gemini settings
EMBED_MODEL = "models/embedding-001"
LLM_MODEL = "gemini-2.5-flash"

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
@st.cache_resource
def get_tidb_connection():
    return pymysql.connect(
        host=os.getenv("TIDB_HOST"),
        port=int(os.getenv("TIDB_PORT", 4000)),
        user=os.getenv("TIDB_USER"),
        password=os.getenv("TIDB_PASSWORD"),
        database=os.getenv("TIDB_DATABASE"),
        ssl={"ca": os.getenv("TIDB_SSL_CA")}  # proper TLS
    )

def query_tidb(sql, params=None):
    conn = get_tidb_connection()
    df = pd.DataFrame()
    with conn.cursor() as cursor:
        cursor.execute(sql, params or ())
        rows = cursor.fetchall()
        if rows:
            df = pd.DataFrame(rows, columns=[col[0] for col in cursor.description])
    return df

# Contract parsing utilities
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join(page.get_text("text") for page in doc)

def extract_text_from_word(file):
    doc = docx.Document(file)
    return "\n".join(para.text for para in doc.paragraphs)

# Gemini embedding
def embed_text(text):
    result = genai.embed_content(model=EMBED_MODEL, content=text)
    return result.get('embedding')

# Gemini chat
def gemini_chat(prompt, context=""):
    chat = genai.GenerativeModel(model_name=LLM_MODEL)
    response = chat.generate_content(f"Context: {context}\n\nUser: {prompt}")
    return response.text