#  Mahal Event Planning Chatbot

##  Overview
The **Mahal Event Planning Chatbot** is an AI-powered assistant designed to help users explore venues, check availability, and book events seamlessly.  
It combines a beautiful **frontend** (HTML, CSS, JavaScript) with a **Flask backend** powered by **Gemini/Groq AI** and **SQLite database**.

 With this chatbot, users can:
- Discover our **magnificent Mahals** (Royal, Grand, Imperial)
- Check **availability** for a given date
- Book events with **guest count, packages, catering, and decoration**
- Chat naturally with an **AI-powered assistant**

---

##  Features
- **Venue Information** – Royal, Grand, and Imperial Mahals with capacity & price.
- **Availability Check** – See if a hall is free for your chosen date.
- **Booking System** – Store event bookings in SQLite.
- **AI Responses** – Gemini API (primary) with Groq fallback for natural chat.
- **Responsive Chatbot UI** – Floating chat window inside the site.
- **Frontend + Backend** – Clean separation with API-based communication.

<img width="935" height="410" alt="image" src="https://github.com/user-attachments/assets/8160f4d0-ce6b-4268-b49f-b9392a8bc80b" />

<img width="876" height="409" alt="image" src="https://github.com/user-attachments/assets/d40673aa-066b-4700-9b93-d91fea908b74" />
<img width="883" height="418" alt="image" src="https://github.com/user-attachments/assets/a5756433-9df2-4049-86ec-3f522903fc8a" />

---

##  Technologies Used
**Frontend**
- HTML5, CSS3, JavaScript  
- Chatbot widget inside `index.html`  

**Backend**
- Python (Flask)  
- SQLite (bookings & halls)  
- Gemini API (`gemini-1.5-flash`)  
- Groq API (`llama3-8b-8192`)  

---

##  Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/mahal-event-chatbot.git
cd mahal-event-chatbot
```
2. Backend Setup
Install dependencies:

```
pip install -r requirements.txt
```
requirements.txt should include:

flask
sqlite3-binary
google-generativeai
groq


Set your API keys (replace with your actual keys):

```
export GEMINI_API_KEY="your_gemini_key"
export GROQ_API_KEY="your_groq_key"

```
Run the Flask server:
```
python app.py
```
Your backend will be running on http://localhost:5000.

3. Frontend Setup
Just open index.html in your browser, or host it on GitHub Pages.
Make sure the JS fetch URL points to your Flask backend (Render/Railway/etc.).

 How to Use
Open the website.

Click the  chatbot icon (bottom-right).

Ask questions like:

“Tell me about Royal Mahal”

“Is Imperial Mahal available on 2025-09-20?”

“Book an event for 300 guests on Grand Mahal”

The chatbot will check availability (via SQLite) and guide you through booking.

## Deployment
Frontend
Host index.html + assets on GitHub Pages (free).

Backend
Deploy Flask API on:

Render (free tier)

Railway

Deta Space

Update index.html:

javascript

const response = await fetch('https://your-backend.onrender.com/process_question', { ... })

## Future Enhancements
User authentication & login.

Payment gateway integration.

Multi-language chatbot support.

Integration with Google Calendar for auto-scheduling.

## Developer
Kishore M
 • AI Developer • Passionate about Event-Tech 

## License
This project is licensed under the MIT License.









