from PIL import Image

def caption_uploaded_image(processor, model, pil_image: Image.Image,
                          max_new_tokens=30, num_beams=5):
    pil_image = pil_image.convert("RGB")
    from .model import generate_caption
    caption = generate_caption(
        processor, model, pil_image,
        prompt=None,
        max_new_tokens=max_new_tokens,
        num_beams=num_beams,
        no_repeat_ngram_size=3,
        repetition_penalty=1.2
    )
    return caption
