import os
from groq import Groq
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY")
        print(f"DEBUG LLM: API Key Loaded? {bool(self.api_key)}")
        if self.api_key:
             print(f"DEBUG LLM: Key starts with {self.api_key[:4]}...")
        
        self.client = None
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                print("DEBUG LLM: Groq Client Initialized")
            except Exception as e:
                print(f"DEBUG LLM: Failed to init Groq: {e}")
        
    def generate_response(self, user_text: str, context: dict = None) -> str:
        """
        Generates a conversational response using Groq (Llama3).
        """
        if not self.client:
            print("DEBUG LLM: No Client, using Fallback")
            return self._fallback_response(context)
            
        try:
            print("DEBUG LLM: Sending request to Groq...")
            # Construct System Prompt
            system_prompt = (
                "You are an empathetic memory assistant for an elderly person with dementia. "
                "Your goal is to be kind, patient, and helpful. "
                "Use the provided CONTEXT to answer the user's question. "
                "Keep answers short (1-2 sentences) and conversational. "
                "If the context provides a name and relation, use them warmly. "
                "Do NOT mention 'database' or 'records'. Speak naturally. "
                "The Context includes 'Has Audio' and 'Has Image' flags. "
                "Use them: If user asks about voice and Has Audio=False, say you don't recall their voice. "
                "If user asks about appearance and Has Image=False, say you don't have a photo. "
                "Otherwise, focus on the identity and notes."
            )
            
            # Construct Context String
            context_str = "No specific memory found."
            if context:
                name = context.get("name", "Unknown")
                relation = context.get("relation", "Unspecified")
                notes = context.get("notes", "")
                location = context.get("location", "")
                has_audio = context.get("has_audio", False)
                has_image = context.get("has_image", False)
                context_str = f"Memory: Name={name}, Relation={relation}, Notes={notes}, Location={location}, Has Audio={has_audio}, Has Image={has_image}"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context_str}\n\nUser: {user_text}"}
            ]
            
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=100,
            )
            
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            print(f"LLM Error: {e}")
            return self._fallback_response(context)

    def _fallback_response(self, context: dict) -> str:
        """Rule-based responses when LLM is offline."""
        if not context:
            return "I am listening."
            
        name = context.get("name", "them")
        return f"That is {name}. {context.get('notes', '')}"

llm_service = LLMService()
