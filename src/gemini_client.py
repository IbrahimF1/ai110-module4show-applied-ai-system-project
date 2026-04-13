"""
Gemini client wrapper for RAG-Enhanced Music Recommender.

Handles:
- Configuring the Gemma client from the GEMINI_API_KEY environment variable
- Extracting structured preferences from natural language queries
- Generating natural language explanations for recommendations

Uses Gemma 3 27b (gemma-3-27b-it) for cost-efficient, high-quality reasoning.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
from typing import Dict, List, Optional, Tuple

# Load environment variables from .env file
load_dotenv()

# Central place to update the model name if needed.
GEMINI_MODEL_NAME = "gemma-3-27b-it"


class GeminiClient:
    """
    Simple wrapper around the Gemma model.

    Usage:
        client = GeminiClient()
        preferences = client.extract_preferences(query, song_context)
        # or
        explanation = client.generate_response(query, playlist)
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Missing GEMINI_API_KEY environment variable. "
                "Set it in your shell or .env file to enable LLM features."
            )

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    def extract_preferences(self, query: str, song_context: str) -> Dict:
        """
        Extract structured preferences from natural language query.
        
        Args:
            query: User's natural language query
            song_context: Available songs and their descriptions
            
        Returns:
            Dictionary with extracted preferences
        """
        prompt = f"""
You are a music preference analyzer. Extract structured preferences from user queries.

Available genres: pop, lofi, rock, jazz, ambient, synthwave, indie pop, hip-hop, folk, electronic, blues, classical, r&b, reggae, metal
Available moods: happy, chill, intense, relaxed, focused, moody, peaceful, hopeful, nostalgic, dramatic, romantic, playful, energetic, angry

Available songs in our catalog:
{song_context}

Extract the following if mentioned:
- favorite_genre: str or null
- favorite_mood: str or null
- target_energy: float (0.0-1.0) or null
- likes_acoustic: bool or null
- target_tempo: int (BPM) or null
- target_valence: float (0.0-1.0) or null
- target_danceability: float (0.0-1.0) or null

Return as JSON. Use null for unmentioned preferences.

User query: {query}
"""
        try:
            response = self.model.generate_content(prompt)
            result = (response.text or "").strip()
            
            # Try to parse JSON from response
            # Gemma might wrap JSON in markdown code blocks
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                result = result.split("```")[1].split("```")[0].strip()
            
            return json.loads(result)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return empty dict
            print(f"Warning: Could not parse JSON from Gemma response: {e}")
            print(f"Raw response: {result}")
            return {}
        except Exception as e:
            print(f"Error extracting preferences: {e}")
            return {}

    def generate_response(self, query: str, playlist: List[Tuple[Dict, float]]) -> str:
        """
        Generate natural language explanation of recommendations.
        
        Args:
            query: User's original query
            playlist: List of (song_dict, score) tuples
            
        Returns:
            Natural language explanation
        """
        playlist_text = "\n".join([
            f"{i+1}. {song['title']} by {song['artist']} - Score: {score:.2f}"
            for i, (song, score) in enumerate(playlist)
        ])
        
        prompt = f"""
You are a helpful music recommendation assistant.

User query: {query}

Recommended playlist:
{playlist_text}

Provide a brief, friendly explanation of why these songs were recommended.
Mention the key features that match the user's request.
Keep it conversational and helpful.
Keep it under 150 words.
"""
        try:
            response = self.model.generate_content(prompt)
            return (response.text or "").strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I couldn't generate an explanation for these recommendations."

    def get_clarification(self, query: str) -> str:
        """
        Generate a clarification request when query is ambiguous.
        
        Args:
            query: The ambiguous user query
            
        Returns:
            Natural language clarification request
        """
        prompt = f"""
The user asked: "{query}"

This query is too vague to extract clear music preferences. 
Generate a friendly, conversational response asking for clarification.

Ask about:
- What mood they're looking for (chill, happy, intense, relaxed, etc.)
- What genre they prefer (pop, lofi, rock, jazz, etc.)
- What activity they'll be doing (studying, working out, relaxing, etc.)
- Whether they prefer acoustic or electronic music

Keep it brief and helpful. Under 100 words.
"""
        try:
            response = self.model.generate_content(prompt)
            return (response.text or "").strip()
        except Exception as e:
            print(f"Error generating clarification: {e}")
            return "I need more information to help you find the perfect playlist. Could you tell me more about what mood, genre, or activity you have in mind?"
