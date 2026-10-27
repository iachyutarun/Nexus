import os

class LocalModelEngine:
    def __init__(self, model_path, output_callback=None):
        self.model_path = model_path
        self.output_callback = output_callback or (lambda x: x)
        self.model = None
        self.available = False
        self.error = None
        self.backend = None
        self._load()

    def _load(self):
        if not self.model_path or not os.path.exists(self.model_path):
            self.error = "Model file not found."
            return
        try:
            from ctransformers import AutoModelForCausalLM
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                gpu_layers=0
            )
            self.available = True
            self.backend = "ctransformers"
        except Exception as e:
            self.error = f"Failed to load model: {e}"

    def generate(self, text, max_tokens=256, temperature=0.7):
        if not self.available:
            return f"Local model unavailable: {self.error}"
        try:
            output = self.model(
                text,
                max_new_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>", "\n\n"]
            )
            return output
        except Exception as e:
            return f"Inference error: {e}"

    def unload(self):
        self.model = None
        self.available = False
        self.backend = None
