import time
from app.llm_service import ollama_service

# Model loading and warmup logic
class ModelWarmup:
    def __init__(self):
        self.warmed_up = False
    
    def warmup(self, test_prompt: str = "Hello!") -> bool:
        if not self.warmed_up:
            try:
                start = time.time()
                ollama_service.generate(test_prompt)
                end = time.time()
                self.warmed_up = True
                print(f"Warmup complete, took {round(end-start, 2)}s")
            except Exception as e:
                print(f"Warmup failed: {e}")
        return self.warmed_up

model_warmup = ModelWarmup()
