from utils import *

st.title(APP_NAME)
st.header(ABOUT_HEADER)

st.write("""
    This app helps workers and employers in Ontario understand their rights and obligations 
    under the [Employment Standards Act (ESA)](https://www.ontario.ca/laws/statute/00e41).
    The goal is to better empower employees especially in an uncertain job market.
    
    **Features:**
    - Ask questions about labor law 
    - Analyze labor contracts for compliance/areas of concernts
    - Find lawyers  
    
    **Powered by:**  
    - [Streamlit](https://docs.streamlit.io) for UI  
    - [TiDB Serverless](https://www.pingcap.com/) for data storage  
    - [Gemini API](https://ai.google.dev/) for embeddings + reasoning  
             
     **N/B**: This app is not a substitute for a qualified lawyer. 
    """)