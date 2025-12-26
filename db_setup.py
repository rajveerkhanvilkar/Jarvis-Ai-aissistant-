import sqlite3
import csv
import os

# ================== DB CONNECTION ==================

DB_PATH = "jarvis.db"   # same file name you already use in command.py
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ================== TABLE CREATION ==================

# 1) System commands table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sys_command (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    path VARCHAR(1000)
)
""")

# 2) Web commands table
cursor.execute("""
CREATE TABLE IF NOT EXISTS web_command (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    url VARCHAR(1000)
)
""")

# 3) Knowledge base table
cursor.execute("""
CREATE TABLE IF NOT EXISTS knowledge_base (
    id INTEGER PRIMARY KEY,
    question VARCHAR(1000),
    answer  VARCHAR(1000)
)
""")

# 🔹 IMPORTANT: index for fast search
cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_kb_question
ON knowledge_base(question)
""")

# 4) Contacts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    name  VARCHAR(200),
    Phone VARCHAR(255),
    email VARCHAR(255) NULL
)
""")

conn.commit()

# ================== SEED DEFAULT Q/A ==================

cursor.execute(
    "INSERT OR IGNORE INTO knowledge_base (id, question, answer) VALUES (?, ?, ?)",
    (1, 'what is your name', 'My name is Jarvis')
)

cursor.execute(
    "INSERT OR IGNORE INTO knowledge_base (id, question, answer) VALUES (?, ?, ?)",
    (2, 'who are you', 'I am Jarvis, a voice assistant created and trained by Rajveer Khanvilkar')
)

conn.commit()

# ================== MAKE ROW COUNT ZERO (YOUR REQUEST) ==================

# 🔥 The FIX: Delete all old data before importing CSV
cursor.execute("DELETE FROM knowledge_base")
conn.commit()

print("🗑️ Old knowledge_base data cleared.")

# ============ IMPORT YOUR CSV: knowledge_base_india.csv ===========

CSV_PATH = os.path.join("backend", "knowledge_base_india.csv")

if os.path.exists(CSV_PATH):
    print(f"📄 Found {CSV_PATH}, importing into knowledge_base...")

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)

        header_lower = [h.strip().lower() for h in header] if header else []

        if "question" in header_lower and "answer" in header_lower:
            q_idx = header_lower.index("question")
            a_idx = header_lower.index("answer")
            for row in reader:
                if len(row) <= max(q_idx, a_idx):
                    continue
                q = row[q_idx].strip()
                a = row[a_idx].strip()
                if q and a:
                    cursor.execute(
                        "INSERT INTO knowledge_base (question, answer) VALUES (?, ?)",
                        (q.lower(), a)
                    )
        else:
            for row in reader:
                if len(row) < 2:
                    continue
                q = row[0].strip()
                a = row[1].strip()
                if q and a:
                    cursor.execute(
                        "INSERT INTO knowledge_base (question, answer) VALUES (?, ?)",
                        (q.lower(), a)
                    )

    conn.commit()
    print("✅ knowledge_base_india.csv data imported successfully.")
else:
    print(f"⚠️ CSV not found at: {CSV_PATH}")
    print("   Make sure knowledge_base_india.csv is in the correct folder.")

# ================== SUMMARY ==================

cursor.execute("SELECT COUNT(*) FROM knowledge_base")
kb_count = cursor.fetchone()[0]
print(f"🧠 knowledge_base rows: {kb_count}")

cursor.execute("SELECT COUNT(*) FROM contacts")
contacts_count = cursor.fetchone()[0]
print(f"📇 contacts rows: {contacts_count}")

conn.close()
print("✅ Database setup finished.")
