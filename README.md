# Masthishq (Convolve) - AI Memory Assistant

Masthishq is a multimodal AI agent designed to act as an external memory for patients with Alzheimer's and Dementia. It uses Face Recognition, Vector Search (Qdrant), and LLMs (Llama 3 via Groq) to identify people, objects, and provide context-aware conversations.

## 🚀 Prerequisites

Before running the project, ensure you have the following installed:

*   **Python 3.10+**
*   **Node.js 18+** & **npm**
*   **Qdrant Cloud** API Key (or local Qdrant instance).
*   **Groq API Key** (for Llama 3 & Whisper).

---

## 🛠️ Installation & Setup

### 1. clone/Unzip the Repository
Extract the `Convolve_Submission.zip` folder.
```bash
cd Convolve
```

### 2. Backend Setup (FastAPI)
Create a virtual environment and install dependencies.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup (React)
Install the node modules.

```bash
cd frontend
npm install
cd ..
```

### 4. Environment Configuration
Create a `.env` file in the root directory by copying the example.
```bash
cp .env.example .env
```

**Open `.env` and fill in your keys:**
```ini
# Qdrant (Memory)

QDRANT_URL=https://xyz.qdrant.tech, QDRANT_API_KEY=your_key

# Groq (AI Model)
GROQ_API_KEY=gsk_your_groq_api_key_here

# Security
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 5. Important: Embeddings & Qdrant Data
**Why is the Qdrant API Key provided?**
The project comes connected to a cloud Qdrant instance pre-loaded with **VoxCeleb** embeddings. This allows you to test the retrieval and recognition features immediately without spending hours enrolling data.

**Using Your Own Data:**
If you prefer to start fresh or use your own faces:
1.  Change the `QDRANT_URL` and `QDRANT_API_KEY` in `.env` to your own instance.
2.  The database will be empty initially.
3.  Go to the **Caregiver Dashboard** (`/caregiver`) and upload photos/details for the people you want the AI to remember.
4.  Once enrolled, the **Memory Chat** and **Camera** will start recognizing these new individuals.

---

## ▶️ Running the Application

### Step 1: Start Qdrant (Vector Database)
If using local Qdrant with Docker:
```bash
docker run -p 6333:6333 qdrant/qdrant
```
*If using Qdrant Cloud, ensure the URL/Key are in `.env`.*

### Step 2: Start the Backend
Open a terminal in the root folder (ensure `venv` is active):
```bash
uvicorn app.main:app --reload --port 8000
```
*The API will be available at `http://localhost:8000`*

### Step 3: Start the Frontend
Open a **new** terminal, navigate to `frontend`:
```bash
cd frontend
npm run dev
```
*The App will be available at `http://localhost:5173`*

---

## 📱 Features
1.  **Caregiver Dashboard:** Enroll faces and objects (`/remember/patient`).
2.  **Memory Chat:** Speak to the Avatar to ask "Who is this?" or "Where are my keys?".
3.  **Object Scan:** Use the camera to detect objects (Keys, Medicine).

## ⚠️ Troubleshooting
*   **"Qdrant Connection Refused":** Ensure Docker is running or your Cloud URL is correct.
*   **"Groq Error":** Check your API Key quota.
*   **Frontend API Error:** Ensure Backend is running on port `8000`.
