from app.model import load_model
from app.ui import build_ui

processor, model = load_model()
demo = build_ui(processor, model)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
