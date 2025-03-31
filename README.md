# UniMate Backend (MVP)

UniMate was a real-world MVP built by a second-year computer science student at UNSW. It aggregated and processed event data from student groups across the internet, using distributed proxies for scraping and GPT-based classification for semantic enrichment. The system ran live for over 1,500 users and was designed to validate product-market fit with minimal engineering overhead.

🧊 This repo represents a cleaned and frozen version of the final push of the UniMate MVP. It is not under active development.

📝 [Read the retrospective](https://stelliott.online/2025/03/31/unimate-retrospective-of-a-first-time-engineering-founder/) for the full breakdown of the design process, tradeoffs, and lessons learned.

---

## 🚀 What It Does

- Scrapes club event data using Infatica proxies (residential/mobile IPs).
- Parses inconsistent HTML structures with custom logic and resilient regex-based strategies.
- Enriches raw event data using GPT-3.5 for multi-label classification.
- Outputs structured CSVs and binary dumps.
- Supports manual overrides, partial restarts, and cached recovery.
- Uses a no-code frontend for minimal deployment complexity.

---

## 🧱 Architecture

scraper/ \
├── Scraper.py → Entry point for scraping club and event pages \
├── Scripts.py → Modular extractors for embedded script data \
├── InfaticaRequests.py → Proxy-based HTTP layer 

processor/ \
├── Tagger.py → GPT-based multi-label classifier 

utils/ \
├── Parser.py → HTML substring and regex extraction \
├── Utils.py → Date handling, sleep logic, URL checks 

io/ \
├── Filesystem.py → Handles all folder and file structure \
├── Input.py → Reads from saved files and dumps \
├── Output.py → Writes data to disk (CSV, binary) 

config/ \
├── Config.py → Prompts and constants \
├── Env.py → Shared imports 

core/ \
├── Interface.py → CLI interaction and control logic \
├── Debug.py → Test utilities 


---

## ⚙️ Setup

> **Warning:** This repo contains *legacy MVP code*. It was designed for fast iteration, not safety or polish.

1. **Clone the repo**
2. Set your `infatica_api_key` in `Config.py`  
   *(you should remove or mock this if publishing your version)*  
3. Run `Interface.py` to begin CLI-driven scraping and tagging.

You’ll need:
- Python 3.9+
- OpenAI API key (for `Tagger.py`)
- A valid Infatica account if testing live scraping

---

## 🧠 Design Patterns Used

- **Pipeline Pattern** – Cleanly separated data stages: scraping → processing → output
- **Strategy Pattern** – GPT taggers encapsulated as binary classifiers
- **Factory Pattern (lightweight)** – Filesystem handles path generation
- **CLI Controller** – User input drives pipeline selection
- **Observer-like Logging** – Post-mortem debugging with HTML dumps

---

## 🧪 Known Limitations

- No formal test suite. It's all manual, via CLI and prints
- API keys were originally stored in plain text
- Minimal error handling and no logging framework
- Single-threaded, non-concurrent scraping
- Not intended for production deployment

---

## 📚 Related Reading

For context, lessons learned, and a full breakdown of tradeoffs:  
👉 [UniMate: Retrospective of a First-Time Engineering Founder](https://stelliott.online/2025/03/31/unimate-retrospective-of-a-first-time-engineering-founder/)

---

## 🧑‍💻 Author

Stephen Elliott  
[Sydney, 2023]
