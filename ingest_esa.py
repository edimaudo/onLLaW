from utils import *

# --- Configure APIs ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
EMBED_MODEL = "models/embedding-001"

# --- TiDB Connection ---
def get_connection():
    return pymysql.connect(
        host=os.getenv("TIDB_HOST"),
        user=os.getenv("TIDB_USER"),
        password=os.getenv("TIDB_PASSWORD"),
        database=os.getenv("TIDB_DATABASE"),
        ssl={"ssl": True}
    )

# --- Fetch ESA Law Text ---
def fetch_esa_text():
    url = "https://www.ontario.ca/laws/statute/00e41"
    r = requests.get(url)
    r.raise_for_status()
    text = r.text

    # crude cleanup: strip HTML tags
    clean = re.sub(r"<.*?>", " ", text)
    clean = re.sub(r"\s+", " ", clean)
    return clean

# --- Chunking ---
def chunk_text(text, max_words=200):
    words = text.split()
    chunks, current = [], []
    for word in words:
        current.append(word)
        if len(current) >= max_words:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks

# --- Embedding ---
def embed_text(text):
    result = genai.embed_content(model=EMBED_MODEL, content=text)
    return result["embedding"]

# --- Store in TiDB ---
def store_chunks(chunks):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO labor_law_chunks (section, chunk, embedding) VALUES (%s, %s, %s)"
    for i, chunk in enumerate(chunks):
        emb = embed_text(chunk)
        cursor.execute(sql, (f"Chunk {i}", chunk, json.dumps(emb)))

    conn.commit()
    cursor.close()
    conn.close()

# --- Main ---
if __name__ == "__main__":
    print("Fetching ESA law text...")
    esa_text = fetch_esa_text()

    print("✂️ Chunking text...")
    chunks = chunk_text(esa_text, max_words=200)
    print(f"Created {len(chunks)} chunks")

    print("Embedding and storing in TiDB...")
    store_chunks(chunks)

    print("Ingestion complete!")
