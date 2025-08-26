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