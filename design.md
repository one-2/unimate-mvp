# UniMate System Design

This document outlines the system design of the UniMate MVP backend: the rationale behind its structure, major components, key architectural patterns, and the engineering tradeoffs I made in its implementation.

---
## 🎯 Goals

- Scrape and structure event data from heterogeneous web sources.
- Enrich and classify the data using large language models (GPT).
- Store, version, and export the processed data in formats suitable for upload directly to a user-facing site.
- Build quickly, with minimal tooling, as a single engineer under time constraints.
- Validate product-market fit before scaling.

---

## 🧱 High-Level Architecture

```text
+--------------+        +----------------+        +-------------------+        +----------------+
|   Raw HTML   | ---->  |   Scraper.py   | ---->  |    Scripts.py     | ---->  |  Output.py     |
| (Club sites) |        | (Data fetcher) |        | (Script parsers)  |        | (CSV/Bin I/O)  |
+--------------+        +----------------+        +-------------------+        +----------------+
                                                   ↓
                                             +----------------+
                                             |   Tagger.py    |
                                             |(GPT Classifier)|
                                             +----------------+

```
---

## 🧭 System Summary

- **CLI interface** in `Interface.py` lets users choose from scraping/tagging subroutines.
- **Filesystem abstraction** (`Filesystem.py`) handles versioned output and directory structure.
- **Custom HTML parsing** avoids reliance on heavy tools like Selenium, using substring and regex logic.
- **GPT classifier** performs binary tag prediction for semantic enrichment.

---
## ⚙️ Components

### `scraper/` – Handles data acquisition
- `Scraper.py`: Event & club scraping logic  
- `Scripts.py`: Parses JavaScript-embedded JSON objects  
- `InfaticaRequests.py`: Routes requests through mobile/residential proxies (Infatica)

### `processor/` – Adds semantic structure
- `Tagger.py`: GPT-based binary classification into multiple event tags

### `utils/` – Supports shared logic
- `Parser.py`: Substring/regex HTML extraction  
- `Utils.py`: Timestamp validation, URL helpers, sleep logic

### `io/` – Manages persistence
- `Filesystem.py`: Path and directory logic with versioning  
- `Output.py`: Saves data (CSV and binary)  
- `Input.py`: Loads saved inputs and dumps

### `core/` – Control logic
- `Interface.py`: CLI orchestration for full runs  
- `Debug.py`: Standalone test runner  
- `Config.py`: Hardcoded prompts and constants (should be moved to `.env` or config file in production)  
- `Env.py`: Shared imports (acts as a basic import consolidation hack)

---

## 🧠 Patterns and Principles

### Patterns
- **Pipeline Pattern**: Data flows through clearly defined modular stages.
- **Strategy Pattern**: Each GPT classifier prompt is treated as an independent strategy.
- **CLI Controller**: Central control logic enables modular interaction.
- **Lightweight Factory**: Filesystem generates path structures and avoids duplication.
- **Observer-like Logging**: HTML dump storage enables reproducible debugging.

### Principles
- **YAGNI and Lean MVP**: Avoided building unnecessary infrastructure (e.g., web backend, database).
- **Delayed Automation**: Introduced automation only once manual work became a bottleneck.
- **Design for Debuggability**: Saved response bodies and used partial restarts to recover from failures.

---

## 📉 Tradeoffs

| **Decision**                | **Rationale**                             | **Cost**                                       |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| No Selenium                 | Performance, simplicity                   | More fragile DOM parsing                       |
| No database                 | Fast iteration, easier CSV output         | Harder to scale and query                      |
| OpenAI tagging via GPT      | Fast to implement, minimal code           | Expensive, needs better response validation    |
| Hardcoded config + secrets  | Simplicity                                | Security risk and bad practice (not for prod)  |
| Single-threaded scraping    | Easier debugging                          | Slower run times                               |
| No tests                    | Speed of development                      | Hard to refactor with confidence               |

---

## 🔄 Future Improvements

- Replace hardcoded API keys with `.env` or config loader  
- Structured logging and exception handling
- Introduce async scraping  
- Implement unit and integration tests  
- Replace CSV-based workflows with SQLite or PostgreSQL for structured querying  
- Use FastAPI or Flask for a minimal backend (!)  

---

## 🧑‍💻 About the Engineer

This system was solo-built by a second-year CS student. It was their first real-world MVP, for a business venture they started with a friend. The codebase is intentionally minimal, focused on value over engineering polish.

📝 [Read the full retrospective](https://stelliott.online/2025/03/31/unimate-retrospective-of-a-first-time-engineering-founder/) for the backstory, lessons, and business-technical tradeoffs.
