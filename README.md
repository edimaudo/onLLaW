# 🎈 onllaw

Application powered by TiDB Serverless and Gemini AI that helps workers explore Ontario’s Employment Standards Act (ESA).

## Features
**About Page**
- Overview of the app and purpose (Ontario ESA insights).
**Labor Law Information**
- Ask natural language questions about ESA.
 - Uses Gemini embeddings + TiDB vector search for retrieval.
**Contract Insights**
- Ability to upload an employee labor contract
 - Extract text and get compliance insights.
**Lawyer Information**
- Search for Ontario labour lawyers.


## Setup
1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run app.py
   ```
