# Image Caption Suite (BLIP) — Gradio App

A small, production-style Gradio application that:

1. **Captions a single uploaded image** using the BLIP image captioning model.
2. **Scrapes a webpage for images and captions them**, returning a downloadable `captions.txt` file containing `image_url<TAB>caption` lines.

This repository is structured to be GitHub-friendly and deployable to **Hugging Face Spaces** (Gradio SDK) or via **Docker**.

---

## Features

- **Single image captioning** (upload → caption).
- **Webpage image scraping + batch captioning** (URL → list of image URLs + captions).
- Downloadable output file (`captions.txt`).
- Reasonable caption generation defaults (beam search + anti-repetition) to avoid repetitive outputs.
- Clean module layout (`app/` package) with a single entrypoint (`app.py`).

---

## Tech Stack

- **Gradio** for the web UI
- **Hugging Face Transformers** for model loading/inference
- **PyTorch** backend for BLIP inference
- **BeautifulSoup4 + Requests** for HTML parsing and image fetching

---

## Model

This project uses:

- `Salesforce/blip-image-captioning-base`

The model weights are downloaded automatically on first run and cached by Hugging Face/Transformers.

---

## Getting Started (Local)

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the app

```bash
python app.py
```

Open:

- `http://localhost:7860`

> Note: The first run will download model files (large). Subsequent runs load from cache.

---

## Usage

### Tab 1 — Caption one image

1. Upload an image.
2. Click **Generate caption**.
3. The caption appears in the text output.

### Tab 2 — Scrape a link and caption images

1. Paste a web page URL (must include `http://` or `https://`).
2. Optionally adjust:
   - **Max images**: maximum number of image tags to process
   - **Min image area**: filters tiny icons/logos
   - **Optional prompt**: leave empty for pure captioning
3. Click **Scrape + caption**.
4. You get:
   - a text preview (one line per image)
   - a downloadable `captions.txt`

Output format:

```
<image_url>\t<caption>
```

---

## Project Structure

```text
image-caption-suit/
├─ app/
│  ├─ __init__.py
│  ├─ model.py                 # load model + shared caption helper
│  ├─ caption_single.py        # single-image captioning
│  ├─ scrape_and_caption.py    # scrape + batch captioning
│  └─ ui.py                    # Gradio Blocks UI
├─ app.py                      # entrypoint
├─ requirements.txt
├─ Dockerfile
├─ LICENSE
└─ README.md
```

---

## Deployment

### Option A — Hugging Face Spaces (recommended)

Create a new Space and choose:

- **SDK: Gradio**

Push the repository (or upload files) including at least:

- `app.py`
- `app/`
- `requirements.txt`
- `README.md`

Hugging Face will install `requirements.txt` and run `app.py` automatically.

> The `Dockerfile` is optional for Gradio Spaces. Hugging Face does not use it unless you choose **SDK: Docker**.

### Option B — Docker (local)

Build and run:

```bash
docker build -t image-caption-suite .
docker run -p 7860:7860 image-caption-suite
```

Open:

- `http://localhost:7860`

### Option C — Hugging Face Spaces (Docker SDK)

If you need full OS-level control (system packages, custom base image), create a Space with:

- **SDK: Docker**

and keep the `Dockerfile` in the repo.

---

## Notes and Troubleshooting

- **Invalid URL ''**
  - The scraper requires a full URL including a scheme.
  - Example: `https://en.wikipedia.org/wiki/IBM`

- **Model download is large**
  - BLIP base downloads ~1GB of weights.
  - This is normal and cached after first run.

- **Caption repetition**
  - The generation config uses beam search and anti-repetition settings.
  - You can tune these in `app/model.py`.

---

## License

This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## Attribution

Developed by **Ali** as part of coursework in the **IBM AI Developer Professional Certificate (Coursera)**.

This project is an educational implementation and is **not** an official IBM product.
