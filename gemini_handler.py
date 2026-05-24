"""
Insight Flow — Gemini AI Handler
Context-constrained AI interaction with .env persistence and gemini-2.5-flash.
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv, set_key

load_dotenv()

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

SYSTEM_PROMPT = """You are the Insight Flow AI Analytics Assistant embedded in a business analytics dashboard.

STRICT RULES:
1. You may ONLY discuss the uploaded dataset, its metrics, KPIs, trends, and analytics.
2. You must REFUSE any question about sports, weather, politics, jokes, general knowledge, coding, or anything unrelated to the dataset.
3. If asked something outside scope, respond: "This query is outside the uploaded analytics scope. Please ask about the dataset metrics, trends, or KPIs."
4. Keep responses concise, professional, analytical, and business-oriented.
5. Do NOT write long essays. Use bullet points when listing insights.
6. Reference specific numbers from the analytics summary provided.
7. You do NOT calculate metrics yourself — all numbers come from the analytics engine.
"""

class GeminiHandler:
    def __init__(self):
        self.model = None
        self.connected = False
        self.api_key = None

    def connect(self, api_key):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content("Respond with OK")
            if response and response.text:
                self.model = model
                self.connected = True
                self.api_key = api_key
                return True, "Connected successfully."
        except Exception as e:
            self.connected = False
            err = str(e)
            if "API_KEY_INVALID" in err or "invalid" in err.lower():
                return False, "Invalid API key. Please check your Gemini API key."
            return False, f"Connection failed: {err}"
        return False, "Unknown error during connection."

    def auto_connect_from_env(self):
        """Attempt silent connection using .env key on startup."""
        key = os.getenv('GEMINI_API_KEY', '').strip()
        if key and key != 'your_gemini_api_key_here':
            return self.connect(key)
        return False, "No API key found in environment."

    def save_key_to_env(self, api_key):
        """Persist the API key to the .env file."""
        try:
            set_key(ENV_PATH, 'GEMINI_API_KEY', api_key)
        except Exception:
            pass

    def generate_summary(self, analytics_text, metadata):
        if not self.connected:
            return "AI is not connected. Please provide a valid Gemini API key."
        context = f"""ANALYTICS CONTEXT:
{analytics_text}

DATASET METADATA:
- Rows: {metadata.get('total_rows', 'N/A')}
- Date Range: {metadata.get('date_range_start', 'N/A')} to {metadata.get('date_range_end', 'N/A')}
- Metrics: {', '.join(metadata.get('numeric_columns', []))}
- Categories: {', '.join(metadata.get('categorical_columns', []))}

Generate a concise executive summary of key business insights from this data. Use bullet points. Maximum 150 words."""
        try:
            response = self.model.generate_content(SYSTEM_PROMPT + "\n\n" + context)
            return response.text if response and response.text else "Unable to generate summary."
        except Exception as e:
            return f"AI summary generation failed: {str(e)}"

    def ask_question(self, question, analytics_text, metadata):
        if not self.connected:
            return "AI is not connected. Please provide a valid Gemini API key."
        context = f"""ANALYTICS CONTEXT:
{analytics_text}

DATASET METADATA:
- Rows: {metadata.get('total_rows', 'N/A')}
- Date Range: {metadata.get('date_range_start', 'N/A')} to {metadata.get('date_range_end', 'N/A')}
- Metrics: {', '.join(metadata.get('numeric_columns', []))}
- Categories: {', '.join(metadata.get('categorical_columns', []))}

USER QUESTION: {question}

Answer ONLY if the question relates to the dataset above. If unrelated, refuse politely. Be concise and analytical."""
        try:
            response = self.model.generate_content(SYSTEM_PROMPT + "\n\n" + context)
            return response.text if response and response.text else "Unable to process your question."
        except Exception as e:
            return f"Error processing question: {str(e)}"

    def disconnect(self):
        self.model = None
        self.connected = False
        self.api_key = None
