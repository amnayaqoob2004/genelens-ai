# 🧬 GeneLens AI

**GeneLens AI** is an AI-powered bioinformatics research explorer. Enter a gene symbol (e.g. `BRCA1`, `TP53`, `EGFR`, `CFTR`) and instantly retrieve real data from NCBI and PubMed, view calculated sequence statistics, and generate an evidence-grounded AI research brief.

## ✨ Features

- 🔎 **Gene Search** — retrieves gene symbol, ID, organism, chromosomal location, and description from NCBI Gene
- 🧬 **Nucleotide/GenBank Record** — fetches a relevant mRNA sequence with accession number and length
- 📊 **Sequence Analysis** — calculates A/T/G/C counts, base percentages, and GC% directly from the retrieved sequence
- 🧪 **Protein Record** — retrieves protein name, accession, organism, length, and sequence from NCBI Protein
- 📚 **PubMed Literature Search** — finds relevant papers with title, authors, publication year, PMID, and abstract
- 🤖 **AI Research Brief** — an AI-generated summary that clearly separates `[RETRIEVED FACT]` from `[AI INTERPRETATION]`, and never invents data not present in the retrieved evidence
- 💬 **Ask GeneLens** — ask follow-up questions, answered strictly from the same retrieved evidence

## 🧠 How It Stays Grounded (Not a Generic Chatbot)

GeneLens AI does not let the AI answer from its own general knowledge. Every AI response is generated from a structured **evidence object** built entirely from real NCBI/PubMed data retrieved during your search. The AI is explicitly instructed to:

- Label every statement as either a **retrieved fact** or an **AI interpretation**
- Say "this information was not found in the retrieved evidence" instead of guessing
- Never invent PMIDs, accession numbers, or biological claims

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend/UI | Streamlit |
| Bioinformatics | Biopython |
| Biological data | NCBI Gene, Nucleotide, Protein (via E-utilities) |
| Literature | PubMed |
| AI | Groq API (Llama-based models) |
| Data processing | Pandas |
| Visualization | Plotly |

## 🚀 Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/genelens-ai.git
cd genelens-ai
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy `.env.example` to a new file named `.env`, then fill in your own values:
NCBI_EMAIL=your_email@example.com
GROQ_API_KEY=your_groq_api_key_here

- **NCBI_EMAIL**: any email address (required by NCBI's API terms of use, not verified)
- **GROQ_API_KEY**: get a free key at [console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## 📁 Project Structure

genelens-ai/
├── app.py
├── services/
│ ├── ncbi.py
│ └── ai.py
├── bioinformatics/
│ └── sequence_analysis.py
├── evidence/
│ └── builder.py
├── requirements.txt
├── .env.example
└── README.md

## ⚠️ Disclaimer

GeneLens AI is a research exploration tool built for demonstration purposes. It is not intended for clinical or diagnostic use. Always verify information against primary sources (NCBI, PubMed) before relying on it.
