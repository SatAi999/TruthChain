import re
import json
import logging
import requests
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger("truthchain.llm")

class GroqLLMService:
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "openai/gpt-oss-20b"

    @classmethod
    def generate_chat_completion(cls, system_prompt: str, user_prompt: str, json_mode: bool = True) -> Optional[str]:
        """
        Executes a real LLM call to Groq Cloud API using openai/gpt-oss-20b model.
        Returns the raw response text string or None on failure.
        """
        api_key = settings.GROQ_API_KEY
        if not api_key:
            logger.warning("GROQ_API_KEY is unconfigured. Operating in rule-based fallback mode.")
            return None

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        payload = {
            "model": cls.MODEL,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 1024
        }

        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        try:
            response = requests.post(cls.GROQ_API_URL, headers=headers, json=payload, timeout=12)
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                logger.info(f"Groq Cloud LLM invocation succeeded. Model: {cls.MODEL}")
                return content
            else:
                logger.error(f"Groq API returned error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Groq API request failed: {e}")
            return None

    @classmethod
    def generate_json_output(cls, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        """
        Generates and parses structured JSON output from Groq Cloud LLM.
        """
        raw_text = cls.generate_chat_completion(system_prompt, user_prompt, json_mode=True)
        if not raw_text:
            return None

        try:
            # Extract JSON block
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(raw_text)
        except Exception as e:
            logger.error(f"Failed to parse LLM JSON response: {e}")
            return None
