import torch
from transformers import AutoProcessor, BlipForConditionalGeneration

MODEL_ID = "Salesforce/blip-image-captioning-base"

def load_model():
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = BlipForConditionalGeneration.from_pretrained(MODEL_ID)
    model.eval()
    return processor, model

@torch.inference_mode()
def generate_caption(processor, model, image, *, prompt=None,
                     max_new_tokens=30, num_beams=5,
                     no_repeat_ngram_size=3, repetition_penalty=1.2):
    # Pure captioning by default; optional prompt if you want to steer
    if prompt:
        inputs = processor(images=image, text=prompt, return_tensors="pt")
    else:
        inputs = processor(images=image, return_tensors="pt")

    out = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        num_beams=num_beams,
        no_repeat_ngram_size=no_repeat_ngram_size,
        repetition_penalty=repetition_penalty,
        early_stopping=True,
    )
    return processor.decode(out[0], skip_special_tokens=True)
