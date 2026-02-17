import gradio as gr
from .caption_single import caption_uploaded_image
from .scrape_and_caption import scrape_and_caption_to_textfile

def build_ui(processor, model):
    with gr.Blocks(title="Image Caption Suite") as demo:
        gr.Markdown("# Image Caption Suite (BLIP)\nUpload one image or scrape a page and caption its images.")

        with gr.Tabs():
            with gr.Tab("Caption one image"):
                img = gr.Image(type="pil", label="Upload image")
                max_new = gr.Slider(5, 80, value=30, step=1, label="max_new_tokens")
                beams = gr.Slider(1, 10, value=5, step=1, label="num_beams")
                btn1 = gr.Button("Generate caption")
                out1 = gr.Textbox(label="Caption")

                btn1.click(
                    fn=lambda im, m, b: caption_uploaded_image(processor, model, im, max_new_tokens=int(m), num_beams=int(b)),
                    inputs=[img, max_new, beams],
                    outputs=[out1],
                )

            with gr.Tab("Scrape a link and caption images"):
                url = gr.Textbox(label="Page URL", placeholder="https://en.wikipedia.org/wiki/IBM")
                max_imgs = gr.Slider(1, 60, value=20, step=1, label="Max images to process")
                min_area = gr.Slider(100, 200_000, value=10_000, step=100, label="Min image area (width*height)")
                prompt = gr.Textbox(label="Optional prompt (leave empty for pure captioning)", value="")
                btn2 = gr.Button("Scrape + caption")
                out2 = gr.Textbox(label="Captions (tab-separated: url<TAB>caption)", lines=12)
                file_out = gr.File(label="Download captions.txt")



                def run_scrape(u, mi, ma, p):
                    p = p.strip() or None
                    text, path = scrape_and_caption_to_textfile(
                        processor, model, u,
                        max_images=int(mi),
                        min_area=int(ma),
                        prompt=p
                    )
                    return text, path

                btn2.click(
                    fn=run_scrape,
                    inputs=[url, max_imgs, min_area, prompt],
                    outputs=[out2, file_out],
                )
            
        gr.Markdown("""
            ---
            **About**

            Developed by Ali A as part of the IBM AI Developer Professional Certificate (Coursera).

            Licensed under the MIT License.
            """)
    return demo
