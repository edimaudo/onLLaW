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