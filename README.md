# Summarization Workflow Engine

This project implements a simple workflow engine using **FastAPI**.  
The selected example workflow performs **Text Summarization**:  
Split → Summarize → Merge → Output Final Summary

---

## ⚙️ What the Workflow Engine Supports

✔ Multiple nodes executed in sequence  
✔ Node-based workflow graph  
✔ Shared state passed from step to step  
✔ Clean and reusable engine design  
✔ JSON-based REST API  
✔ Simple and lightweight — no external APIs required  

The current workflow includes 3 nodes:
1️⃣ Split text into smaller chunks  
2️⃣ Summarize each chunk (simple rule-based logic)  
3️⃣ Merge summaries into a final short output  

---




## 📊 Workflow Architecture

```
               ┌────────────────────────┐
               │       Input Text        │
               └─────────────┬──────────┘
                             ↓
                    split_text (Node 1)
                             ↓
                 summarize_chunks (Node 2)
                             ↓
                  merge_summaries (Node 3)
                             ↓
                    check_length (Branch)
                    ┌─────────┴─────────┐
                    │                   │
                 shorten              done
                    │                   │
                    └──────→ split_text │
                                        ↓
                         final_output (Result)
```


## ▶️ How to Run

Install dependencies:
```bash
pip install fastapi uvicorn


Start server:
uvicorn app.main:app --reload

Open in browser:
👉 http://127.0.0.1:8000/docs


Use POST /run-workflow endpoint with body:

{
  "input_text": "Your long text here..."
}


You will get back:

{
  "final_summary": "Shortened summary of the text"
}


🚀 What I Would Improve With More Time

🔹 Use advanced AI models for better summarization
🔹 Add loop-based decision nodes for dynamic refinement
🔹 Store workflow results in a database
🔹 Build more workflow types (Sentiment, Chatbot, etc.)
🔹 Add a frontend UI for document upload and results


👤 Author

Lakshya (AI/ML Enthusiast)