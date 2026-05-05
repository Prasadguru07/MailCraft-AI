<div align="center">

# ⚡ InboxIQ: AI Email Generation Assistant

A production-grade, locally-hosted AI email assistant powered by **Ollama** with a **Streamlit UI** and evaluated via a custom three-metric LLM pipeline.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=for-the-badge\&logo=ollama\&logoColor=white)
![Model](https://img.shields.io/badge/Model-Qwen3:4b-4B0082?style=for-the-badge\&logo=openai\&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)

[Architecture](#-core-architecture) • [Quick Start](#-quick-start) • [Metrics](#-evaluation-metrics--cards) • [Results](#-results--benchmarks)

</div>

---

## 🏗️ Project Structure

```text
email-gen-assistant/
├── src/
│   ├── email_generator.py   # Core logic + advanced prompt template
│   ├── metrics.py           # Custom evaluation metrics logic
│   ├── evaluate.py          # Evaluation runner (Both strategies)
│   └── app.py               # Streamlit UI (main entry point)
├── data/
│   └── test_scenarios.py    # 10 test scenarios + human reference emails
├── reports/                 # Output dir for CSVs and JSONs
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Environment Setup

Ensure Python 3.10+ and Ollama are installed.

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Windows users: https://ollama.com/download

# Pull model
ollama pull qwen3:4b

# Start server
ollama serve

# Install dependencies
pip install -r requirements.txt
```

---

### 2. Run the Application (Streamlit UI)

```bash
streamlit run src/app.py
```

> The app will launch in your browser where you can:
>
> * Enter email prompts
> * Select tone and context
> * Generate emails instantly
> * Visually inspect outputs

---

### 3. Evaluation Commands

| Command                               | Description                                                     |
| :------------------------------------ | :-------------------------------------------------------------- |
| `python src/evaluate.py`              | Runs full evaluation (Advanced vs Baseline) and exports reports |
| `python src/evaluate.py --scenario 3` | Evaluate a specific test case                                   |

---

## 🧠 Core Architecture

This system compares a **Baseline Prompt** vs an **Advanced Prompting Strategy** combining structured prompting techniques:

> **🎭 Role-Playing**
> Assigns a persona (*Senior Communications Strategist*) for consistent tone and authority.

> **📝 Few-Shot Learning**
> Injects high-quality example emails into the prompt to anchor structure and writing style.

> **🔗 Chain-of-Thought (CoT)**
> Forces structured reasoning:
> *Goal → Audience → Tone → Facts → Structure*

---

## 📊 Evaluation Metrics (Cards)

> ### 🟢 Fact Recall Score (FRS)
>
> **Measures:** % of input facts preserved in output
> **Logic:** Keyword overlap with ≥55% match threshold
> **Range:** `0.0 – 1.0`

> ### 🔵 Tone Alignment Score (TAS)
>
> **Measures:** Tone correctness via LLM-as-a-Judge
> **Logic:** Secondary model scores tone (1–5 → normalized)
> **Range:** `0.0 – 1.0`

> ### 🟣 Professional Quality Score (PQS)
>
> **Measures:** Structural writing quality
> **Logic:** Subject (25%) + Structure (50%) + Conciseness (25%)
> **Range:** `0.0 – 1.0`

> **Overall Score = (FRS + TAS + PQS) / 3**

---

## 🏆 Results & Benchmarks

Using **`qwen3:4b`** via Ollama.

| Metric                         | Advanced Prompt | Baseline Prompt |    Delta   |
| :----------------------------- | :-------------: | :-------------: | :--------: |
| **Fact Recall Score**          |    **63.0%**    |      36.2%      |   +26.8%   |
| **Tone Alignment Score**       |    **87.5%**    |      45.0%      |   +42.5%   |
| **Professional Quality Score** |    **89.4%**    |      75.8%      |   +13.6%   |
| **Overall Score**              |    **79.9%**    |      52.3%      | **+27.6%** |

🔥 **Conclusion:** Advanced prompting significantly improves factual accuracy, tone control, and professional quality — suitable for production deployment.

---

## 📁 Evaluation Outputs

Generated in `/reports` after running evaluation:

* 📄 `evaluation_results_<timestamp>.csv` — Raw scores
* 📄 `evaluation_results_<timestamp>.json` — Full outputs + emails
* 📄 `evaluation_summary_<timestamp>.json` — Aggregated metrics

---

## 🌐 UI Preview (Streamlit)

> Interactive interface for real-time email generation and testing.

* Prompt-based generation
* Tone & context controls
* Instant output visualization
* Ideal for demos and productization

---

## ⚡ Key Takeaways

* Local-first AI (no external API dependency)
* Structured prompting > naive prompting
* Quantifiable evaluation pipeline
* Ready for real-world automation workflows (n8n, APIs, agents)

---
