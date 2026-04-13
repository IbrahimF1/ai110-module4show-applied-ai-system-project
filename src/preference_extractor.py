"""
Preference Extractor for RAG-Enhanced Music Recommender.

Extracts structured music preferences from natural language queries using Gemma.
"""

from typing import Dict, Optional, Tuple
from gemini_client import GeminiClient
from knowledge_base import KnowledgeBase
from error_handler import ErrorHandler, validate_preferences
from logger import get_logger


class PreferenceExtractor:
    """
    Extracts structured music preferences from natural language queries.
    
    Uses Gemma 3 27b to understand user queries and extract
    structured preferences that can be used by the recommender.
    """
    
    def __init__(self, gemma_client: GeminiClient, knowledge_base: KnowledgeBase):
        """
        Initialize the preference extractor.
        
        Args:
            gemma_client: Gemma client for AI processing
            knowledge_base: Knowledge base for song context
        """
        self.gemma_client = gemma_client
        self.knowledge_base = knowledge_base
        self.error_handler = ErrorHandler(get_logger())
        self.logger = get_logger()
        
        # Get song context once
        self.song_context = knowledge_base.get_all_song_descriptions()
        
        # Cache for similar queries
        self.extraction_cache: Dict[str, Tuple[Dict, float]] = {}
    
    def extract_preferences(self, query: str) -> Tuple[Dict, float, Optional[str]]:
        """
        Extract structured preferences from a natural language query.
        
        Args:
            query: User's natural language query
            
        Returns:
            Tuple of (preferences_dict, confidence_score, error_message)
        """
        self.logger.log_user_query(query)
        
        # Check cache
        cache_key = query.lower().strip()
        if cache_key in self.extraction_cache:
            self.logger.log_info(f"Using cached extraction for query: {query}")
            return self.extraction_cache[cache_key] + (None,)
        
        try:
            # Call Gemma to extract preferences
            self.logger.log_debug(f"Calling Gemma for preference extraction: {query}")
            preferences = self.gemma_client.extract_preferences(query, self.song_context)
            
            if not preferences:
                # No preferences extracted - query too vague
                self.logger.log_warning(f"No preferences extracted from query: {query}")
                return {}, 0.0, "I couldn't understand your request. Could you be more specific about what you're looking for?"
            
            # Validate preferences
            is_valid, validation_error = validate_preferences(preferences)
            if not is_valid:
                self.logger.log_warning(f"Invalid preferences extracted: {validation_error}")
                return {}, 0.0, f"{validation_error} Please try again."
            
            # Calculate confidence score
            confidence = self._calculate_confidence(query, preferences)
            
            # Log successful extraction
            self.logger.log_preference_extraction(query, preferences, confidence)
            
            # Cache the result
            self.extraction_cache[cache_key] = (preferences, confidence)
            
            return preferences, confidence, None
            
        except Exception as e:
            error = self.error_handler.handle_extraction_error(
                query, 
                str(e),
                {"exception_type": type(e).__name__}
            )
            return {}, 0.0, error.user_message
    
    def _calculate_confidence(self, query: str, preferences: Dict) -> float:
        """
        Calculate a confidence score for the extracted preferences.
        
        Args:
            query: The original query
            preferences: Extracted preferences
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        confidence = 0.0
        
        # Check if any categorical preferences were extracted
        if preferences.get('favorite_genre'):
            confidence += 0.3
        if preferences.get('favorite_mood'):
            confidence += 0.3
        
        # Check if any numerical preferences were extracted
        numerical_prefs = [
            'target_energy', 'target_tempo', 'target_valence', 
            'target_danceability', 'target_acousticness'
        ]
        num_numerical = sum(1 for pref in numerical_prefs if preferences.get(pref) is not None)
        confidence += min(num_numerical * 0.1, 0.3)
        
        # Check for boolean preference
        if preferences.get('likes_acoustic') is not None:
            confidence += 0.1
        
        # Check query length (longer queries tend to be more specific)
        if len(query.split()) > 5:
            confidence += 0.1
        
        # Cap at 1.0
        return min(confidence, 1.0)
    
    def needs_clarification(self, query: str) -> bool:
        """
        Determine if a query needs clarification.
        
        Args:
            query: The user's query
            
        Returns:
            True if clarification is needed
        """
        # Very short queries likely need clarification
        if len(query.split()) < 3:
            return True
        
        # Vague words
        vague_words = ['something', 'anything', 'good', 'nice', 'music']
        if any(word in query.lower() for word in vague_words):
            return True
        
        # Question without specific criteria
        if '?' in query and not any(word in query.lower() for word in ['genre', 'mood', 'energy', 'tempo']):
            return True
        
        return False
    
    def get_clarification_request(self, query: str) -> str:
        """
        Generate a clarification request for an ambiguous query.
        
        Args:
            query: The ambiguous query
            
        Returns:
            Clarification request message
        """
        self.logger.log_info(f"Generating clarification for query: {query}")
        
        try:
            clarification = self.gemma_client.get_clarification(query)
            return clarification
        except Exception as e:
            self.logger.log_error("ClarificationError", str(e))
            return (
                "I need more information to help you find the perfect playlist. "
                "Could you tell me more about:\n"
                "- What mood are you looking for? (chill, happy, intense, relaxed, etc.)\n"
                "- What genre do you prefer? (pop, lofi, rock, jazz, etc.)\n"
                "- What activity will you be doing? (studying, working out, relaxing, etc.)"
            )
    
    def get_available_options(self) -> Dict[str, list]:
        """
        Get available genres and moods for user reference.
        
        Returns:
            Dictionary with 'genres' and 'moods' lists
        """
        return {
            'genres': self.knowledge_base.get_genres(),
            'moods': self.knowledge_base.get_moods()
        }
    
    def clear_cache(self) -> None:
        """Clear the extraction cache."""
        self.extraction_cache.clear()
        self.logger.log_info("Extraction cache cleared")
