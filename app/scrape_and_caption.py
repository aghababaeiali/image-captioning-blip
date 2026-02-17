import re
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from urllib.parse import urljoin

def _is_image_url(url: str) -> bool:
    u = url.lower()
    if ".svg" in u:
        return False
    return any(u.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".gif"]) or True

def scrape_images(url: str, user_agent: str, max_images: int):
    headers = {"User-Agent": user_agent}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")
    imgs = soup.find_all("img")

    urls = []
    for img in imgs:
        img_url = img.get("src") or img.get("data-src")
        if not img_url and img.has_attr("srcset"):
            img_url = img["srcset"].split()[0]

        if not img_url:
            continue

        full = urljoin(url, img_url)
        if not _is_image_url(full):
            continue

        urls.append(full)
        if len(urls) >= max_images:
            break

    return urls

def fetch_pil_image(img_url: str, user_agent: str):
    headers = {"User-Agent": user_agent}
    r = requests.get(img_url, headers=headers, timeout=20)
    r.raise_for_status()
    im = Image.open(BytesIO(r.content)).convert("RGB")
    return im

def scrape_and_caption_to_textfile(processor, model, page_url: str,
                                   max_images: int = 20,
                                   min_area: int = 10_000,
                                   prompt: str | None = None,
                                   user_agent: str = "Mozilla/5.0"):
    from .model import generate_caption

    image_urls = scrape_images(page_url, user_agent=user_agent, max_images=max_images)

    lines = []
    ok = 0

    for i, img_url in enumerate(image_urls, start=1):
        try:
            im = fetch_pil_image(img_url, user_agent=user_agent)
            if im.size[0] * im.size[1] < min_area:
                continue

            caption = generate_caption(
                processor, model, im,
                prompt=prompt,                  # can be None for pure captioning
                max_new_tokens=30,
                num_beams=5,
                no_repeat_ngram_size=3,
                repetition_penalty=1.2,
            )
            lines.append(f"{img_url}\t{caption}")
            ok += 1
        except Exception as e:
            lines.append(f"{img_url}\tERROR: {type(e).__name__}")

    text = "\n".join(lines) if lines else "No images found."
    out_path = "captions.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    summary = f"Found {len(image_urls)} image tags (capped). Captions generated for {ok} images.\n"
    return summary + "\n" + text, out_path
