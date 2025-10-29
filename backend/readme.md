# RAG Builder - FastAPI Backend

This is the backend service for the RAG Builder application, built using **FastAPI**, Python 3.11+, and Uvicorn.  
It provides APIs for project creation, document ingestion, retrieval, and chat-based querying.

---

## 🚀 Run Locally

### ✅ Prerequisites
- Python 3.11+
- pip
- (Optional) Conda or venv for virtual environments

---

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<username>/<repo>.git
cd <repo-folder>
2️⃣ Create & activate virtual environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate      # Mac / Linux
venv\Scripts\activate         # Windows
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the service
bash
Copy code
uvicorn backend.main:app --reload
✅ API will be available at:
👉 http://localhost:8000/docs

📁 Project Structure
bash
Copy code
backend/
│── main.py          # FastAPI app entrypoint
│── apps/            # Modules / Features
│
├── requirements.txt # Python Dependencies
├── .gitignore
└── README.md
📜 API Docs
FastAPI auto-generates API documentation:

Swagger UI → http://localhost:8000/docs

ReDoc → http://localhost:8000/redoc

🛠 Tech Stack
Component	Technology
Backend Framework	FastAPI
Web Server	Uvicorn
Language	Python
Auth	TBD
Vector DB	TBD
LLM Provider	TBD