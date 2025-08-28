from utils import *

# Fetch and parse ESA
URL = "https://www.ontario.ca/laws/statute/00e41"
res = requests.get(URL)
soup = BeautifulSoup(res.text, "html.parser")

# Extract all text from sections
sections = soup.find_all("div", class_="section")
esa_texts = []
for s in sections:
    header = s.find("h3")
    text = s.get_text(separator=" ", strip=True)
    esa_texts.append({
        "section": header.get_text(strip=True) if header else "General",
        "text": text
    })

print(f"Extracted {len(esa_texts)} sections")



# Chunk and Embed
genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def embed_text(text):
    result = genai.embed_content(model=EMBED_MODEL, content=text)
    return result["embedding"]

chunks = []
for s in esa_texts:
    # Keep chunks short (e.g., 500-700 tokens)
    if len(s["text"]) > 2000:
        parts = [s["text"][i:i+2000] for i in range(0, len(s["text"]), 2000)]
    else:
        parts = [s["text"]]
    for part in parts:
        chunks.append((s["section"], part, embed_text(part)))

# load into TIDB
ssl_ca = os.getenv("TIDB_SSL_CA")
conn = pymysql.connect(
    host=os.getenv("TIDB_HOST"),
    port=int(os.getenv("TIDB_PORT", 4000)),
    user=os.getenv("TIDB_USER"),
    password=os.getenv("TIDB_PASSWORD"),
    database=os.getenv("TIDB_DATABASE"),
    ssl={"ca": ssl_ca} if ssl_ca and os.path.exists(ssl_ca) else {"ssl": True}
)

with conn.cursor() as cursor:
    for section, text, embedding in chunks:
        sql = """
        INSERT INTO esa_chunks (section, chunk, embedding)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (section, text, json.dumps(embedding)))
    conn.commit()

conn.close()
