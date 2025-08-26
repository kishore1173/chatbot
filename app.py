from flask import Flask, render_template, request, jsonify
import sqlite3, os

# Gemini + Groq clients
try:
    import google.generativeai as genai
except:
    genai = None

try:
    from groq import Groq
except:
    Groq = None

# ---------------- Flask ----------------
app = Flask(__name__)

# ---------------- SQLite Setup ----------------
conn = sqlite3.connect("event.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS halls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    capacity INTEGER,
    base_price INTEGER,
    description TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact TEXT,
    event_type TEXT,
    date TEXT,
    hall TEXT,
    guests INTEGER
)
""")

c.execute("SELECT COUNT(*) FROM halls")
if c.fetchone()[0] == 0:
    halls = [
        ("Royal Mahal", 1000, 35000, "Elegant interior, chandeliers, outdoor garden."),
        ("Grand Mahal", 5000, 65000, "Spacious ballroom, breakout rooms, valet services."),
        ("Imperial Mahal", 10000, 110000, "Colossal hall, multiple stages, on-site rooms.")
    ]
    c.executemany("INSERT INTO halls (name, capacity, base_price, description) VALUES (?, ?, ?, ?)", halls)
    conn.commit()

# ---------------- Helper Functions ----------------
def check_availability(hall_name, date_str):
    c.execute("SELECT * FROM bookings WHERE hall=? AND date=?", (hall_name, date_str))
    return c.fetchone() is None

def book_event(name, contact, event_type, date_str, hall_name, guests):
    if not check_availability(hall_name, date_str):
        return False, f"{hall_name} is not available on {date_str}."
    c.execute("INSERT INTO bookings (name, contact, event_type, date, hall, guests) VALUES (?, ?, ?, ?, ?, ?)",
              (name, contact, event_type, date_str, hall_name, guests))
    conn.commit()
    return True, f"Booking confirmed for {hall_name} on {date_str} for {guests} guests."

def get_hall_info():
    c.execute("SELECT name, capacity, base_price, description FROM halls")
    halls = c.fetchall()
    return "\n".join([f"{h[0]}: Capacity {h[1]}, Price ₹{h[2]}, {h[3]}" for h in halls])

# ---------------- LLM Setup ----------------
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_GEMINI_KEY"
GROQ_KEY = os.getenv("GROQ_API_KEY") or "YOUR_GROQ_KEY"

system_prompt = """You are Mahal Event Booking Assistant.
You help customers book wedding halls (Mahals). 
Here are the venues:
- Royal Mahal: Capacity 1,000 guests, Price ₹35,000, Elegant interior, chandeliers, outdoor garden.
- Grand Mahal: Capacity 5,000 guests, Price ₹65,000, Spacious ballroom, breakout rooms, valet services.
- Imperial Mahal: Capacity 10,000 guests, Price ₹110,000, Colossal hall, multiple stages, on-site rooms.

Rules:
- If user asks about halls → provide details from above.
- If user asks availability → check SQLite bookings.
- If user asks to book → guide them to provide: Name, Contact, Event type, Date, Hall, Guests.
- Always answer politely, short and helpful.
"""

def call_gemini(user_input):
    if not genai:
        return None
    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(system_prompt + "\nUser: " + user_input)
        return resp.text.strip()
    except Exception as e:
        return None

def call_groq(user_input):
    if not Groq:
        return None
    try:
        client = Groq(api_key=GROQ_KEY)
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None

# ---------------- Chatbot Logic ----------------
def chatbot_response(user_input):
    u = user_input.lower()
    if "hall" in u:
        return get_hall_info()
    if "available" in u and "on" in u:
        try:
            parts = user_input.split("on")
            hall_name = parts[0].strip().split()[-1].title() + " Mahal"
            date_str = parts[1].strip()
            available = check_availability(hall_name, date_str)
            return f"Yes, {hall_name} is available on {date_str}." if available else f"Sorry, {hall_name} is booked on {date_str}."
        except:
            return "Please specify hall and date like: 'Is Royal available on 2025-09-10?'"
    if "book" in u:
        return "To book, please provide: Name, Contact, Event type, Date, Hall, Guests."

    # Try Gemini → fallback to Groq
    reply = call_gemini(user_input)
    if not reply:
        reply = call_groq(user_input)
    return reply or "Sorry, I'm unable to answer that now."

# ---------------- Routes ----------------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/process_question', methods=['POST'])
def process_question():
    data = request.json
    question = data["question"]
    response = chatbot_response(question)
    return jsonify({"result": response})

# ---------------- Run ----------------
if __name__ == '__main__':
    app.run(debug=True)
