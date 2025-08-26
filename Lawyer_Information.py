from utils import *

st.title(APP_NAME)
st.header(LAWYER_INFORMATION_HEADER)

st.write("""
List of Law Firms that can be contacted to discuss employement issues.  
"""
         
)

with st.sidebar:
        lawyer_options = st.selectbox('Lawyer Options',['All','Recommended by Law Society of Ontario'])

if lawyer_options == 'All':
    law_temp_df = law_df[['Law Firm','Website']]
               
else:
    law_temp_df = law_df[(law_df['Type'] == 'Law Society of Ontario')]
    law_temp_df = law_temp_df[['Law Firm','Website']]
                 
st.dataframe(
                    law_temp_df,
                    column_config={
                        "Law Firm": "Law Firms",
                        "Website": st.column_config.LinkColumn("Website"),
                    },
                    hide_index=True,
)
                
