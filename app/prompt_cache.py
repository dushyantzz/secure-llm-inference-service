import functools
from typing import Any, Dict
import hashlib
import threading

# Simple in-memory cache for repeated prompts
class PromptCache:
    def __init__(self, max_size=128):
        self.cache = dict()
        self.max_size = max_size
        self.lock = threading.Lock()
    
    def _hash_prompt(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode()).hexdigest()
    
    def get(self, prompt: str) -> Any:
        with self.lock:
            key = self._hash_prompt(prompt)
            return self.cache.get(key)
    
    def put(self, prompt: str, value: Any):
        with self.lock:
            key = self._hash_prompt(prompt)
            if len(self.cache) >= self.max_size:
                self.cache.pop(next(iter(self.cache)))
            self.cache[key] = value

prompt_cache = PromptCache(max_size=128)
