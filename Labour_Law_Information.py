from utils import *

st.title(LABOUR_LAW_HEADER)
st.write("Ask questions about Ontario’s Employment Standards Act. The system will search the Employment Standards Act and provide an answer.")

user_question = st.text_input("Enter your question")
if st.button("Get Answer") and user_question:
    st.write("🔍 Embedding question and retrieving relevant ESA sections...")

    # --- Example placeholder: in reality you'd load ESA chunks + embeddings from TiDB ---
    esa_chunks = [
            {"section": "Hours of Work", "text": "Maximum daily and weekly hours are restricted..."},
            {"section": "Overtime Pay", "text": "Employees must receive 1.5 times regular pay after 44 hours/week..."},
            {"section": "Vacation", "text": "Employees are entitled to at least 2 weeks vacation..."}
    ]

    # Embed the question
    q_embedding = embed_text(user_question)

        # Dummy similarity scoring (replace with proper vector search in TiDB)
        # Here we just pretend the first 2 are most relevant
    retrieved = esa_chunks[:2]

    st.write("### Retrieved Sections")
    st.dataframe(pd.DataFrame(retrieved))

    # LLM synthesis with context
    context = "\n\n".join([f"{c['section']}: {c['text']}" for c in retrieved])
    answer = gemini_chat(user_question, context)
    st.write("### Answer")
    st.write(answer)