# 📰 ScrapingRepubblica-Main (2025)

This project was developed in **2025** for a client who needed automated scraping of **news, articles, and press releases** from major Italian sources.  
All scraped data is stored in **XML format** for further processing or integration into other systems.

---

## 📌 Supported sources

The solution includes **three independent scrapers**:

1. **Eni**  
   - Extracts press releases and news from [eni.com](https://www.eni.com/).  
   - Data collected: title, date, content.

2. **Leonardo**  
   - Extracts news and press releases from [leonardo.com](https://www.leonardo.com/).  
   - Data collected: title, subtitle, date, content.

3. **Repubblica**  
   - Extracts both **digital** and **print** articles from [ricerca.repubblica.it](https://ricerca.repubblica.it/).  
   - Requires Google login to access restricted content.  
   - Data collected: title, subtitle, author, date, content.

---

## ⚙️ Requirements

- Python 3.10+  
- [Playwright](https://playwright.dev/python/) (for browser automation)

### Installation

```bash
# Install Chromium for Playwright
python3 -m playwright install chromium
```

---

## ▶️ Running the scrapers

### Eni scraper
```bash
python scraping/eni/scraping.py
```
- Downloads **news** and **press releases** from Eni.  
- Output XML is saved under `scraping/eni/`.

---

### Leonardo scraper
```bash
python scraping/leonardo/scraping.py
```
- Downloads **news** and **press releases** from Leonardo.  
- Output XML is saved under `scraping/leonardo/`.

---

### Repubblica scraper
```bash
python scraping/repubblica/scraping.py
```
- Downloads **digital** and **print** articles from Repubblica.  
- Requires Google credentials (set inside `scraping/repubblica/scraping.py`).  
- Output XML is saved under `scraping/repubblica/`.

---

## 📂 Project structure

```
ScrapingRepubblica-main/
│── scraping/
│   ├── eni/          # Eni scraper
│   ├── leonardo/     # Leonardo scraper
│   ├── repubblica/   # Repubblica scraper
│   ├── xml_utils.py  # Common XML save functions
│   └── ...
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📑 Example XML output

```xml
<article>
  <type>digital</type>
  <title>Example article title</title>
  <subtitle>Optional subtitle</subtitle>
  <author>Author name</author>
  <date>2025-09-24</date>
  <content>Full article text...</content>
</article>
```

---

## ⚠️ Notes

- The scrapers depend on the **HTML structure** of the target websites. If those change, selectors may need to be updated.  
- Some content (such as **Repubblica print articles**) requires **Google login**.  
- This project is intended for **internal client use (2025)** and should be used only for research, analysis, or integration with proper authorization.

---
