"""
Error handling system for RAG-Enhanced Music Recommender.

Provides centralized error handling and user-friendly error messages.
"""

from typing import Optional, Dict, Any
from enum import Enum


class ErrorType(Enum):
    """Types of errors that can occur in the system."""
    API_ERROR = "APIError"
    EXTRACTION_ERROR = "ExtractionError"
    VALIDATION_ERROR = "ValidationError"
    RETRIEVAL_ERROR = "RetrievalError"
    CONFIGURATION_ERROR = "ConfigurationError"
    UNKNOWN_ERROR = "UnknownError"


class MusicRecommenderError(Exception):
    """Base exception for music recommender errors."""
    
    def __init__(self, message: str, error_type: ErrorType = ErrorType.UNKNOWN_ERROR, 
                 context: Optional[Dict[str, Any]] = None):
        """
        Initialize the error.
        
        Args:
            message: Error message
            error_type: Type of error
            context: Additional context about the error
        """
        super().__init__(message)
        self.error_type = error_type
        self.context = context or {}
        self.user_message = self._generate_user_message()
    
    def _generate_user_message(self) -> str:
        """Generate a user-friendly error message."""
        user_messages = {
            ErrorType.API_ERROR: "Sorry, I'm having trouble connecting to the AI service. Please try again later.",
            ErrorType.EXTRACTION_ERROR: "I couldn't understand your request. Could you rephrase it?",
            ErrorType.VALIDATION_ERROR: "Some of your preferences don't seem quite right. Let me help you fix that.",
            ErrorType.RETRIEVAL_ERROR: "I couldn't find any songs matching your criteria. Try different preferences.",
            ErrorType.CONFIGURATION_ERROR: "There's a configuration issue. Please check your setup.",
            ErrorType.UNKNOWN_ERROR: "Something unexpected happened. Please try again.",
        }
        return user_messages.get(self.error_type, user_messages[ErrorType.UNKNOWN_ERROR])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        return {
            "error_type": self.error_type.value,
            "message": str(self),
            "user_message": self.user_message,
            "context": self.context
        }


class ErrorHandler:
    """
    Centralized error handling for the music recommender.
    
    Provides methods to handle different types of errors and
    generate appropriate user-facing messages.
    """
    
    def __init__(self, logger=None):
        """
        Initialize the error handler.
        
        Args:
            logger: Logger instance for logging errors
        """
        self.logger = logger
    
    def handle_api_error(self, original_error: Exception, context: Optional[Dict[str, Any]] = None) -> MusicRecommenderError:
        """
        Handle an API error.
        
        Args:
            original_error: The original exception
            context: Additional context about the error
            
        Returns:
            MusicRecommenderError with user-friendly message
        """
        error_context = {
            "original_error": str(original_error),
            "error_type": type(original_error).__name__
        }
        if context:
            error_context.update(context)
        
        error = MusicRecommenderError(
            f"API error: {str(original_error)}",
            ErrorType.API_ERROR,
            error_context
        )
        
        if self.logger:
            self.logger.log_error(
                ErrorType.API_ERROR.value,
                str(original_error),
                str(error_context)
            )
        
        return error
    
    def handle_extraction_error(self, query: str, reason: str, 
                               context: Optional[Dict[str, Any]] = None) -> MusicRecommenderError:
        """
        Handle a preference extraction error.
        
        Args:
            query: The user's query that failed
            reason: Reason for the failure
            context: Additional context
            
        Returns:
            MusicRecommenderError with user-friendly message
        """
        error_context = {
            "query": query,
            "reason": reason
        }
        if context:
            error_context.update(context)
        
        error = MusicRecommenderError(
            f"Failed to extract preferences from query: {query}. Reason: {reason}",
            ErrorType.EXTRACTION_ERROR,
            error_context
        )
        
        if self.logger:
            self.logger.log_error(
                ErrorType.EXTRACTION_ERROR.value,
                f"Failed to extract preferences from query: {query}",
                str(error_context)
            )
        
        return error
    
    def handle_validation_error(self, field: str, value: Any, expected: str,
                               context: Optional[Dict[str, Any]] = None) -> MusicRecommenderError:
        """
        Handle a validation error.
        
        Args:
            field: The field that failed validation
            value: The invalid value
            expected: Description of expected value
            context: Additional context
            
        Returns:
            MusicRecommenderError with user-friendly message
        """
        error_context = {
            "field": field,
            "value": value,
            "expected": expected
        }
        if context:
            error_context.update(context)
        
        error = MusicRecommenderError(
            f"Validation error for field '{field}': got {value}, expected {expected}",
            ErrorType.VALIDATION_ERROR,
            error_context
        )
        
        if self.logger:
            self.logger.log_error(
                ErrorType.VALIDATION_ERROR.value,
                f"Validation error for field '{field}'",
                str(error_context)
            )
        
        return error
    
    def handle_retrieval_error(self, criteria: Dict[str, Any], 
                              context: Optional[Dict[str, Any]] = None) -> MusicRecommenderError:
        """
        Handle a retrieval error (no songs found).
        
        Args:
            criteria: The search criteria that failed
            context: Additional context
            
        Returns:
            MusicRecommenderError with user-friendly message
        """
        error_context = {
            "criteria": criteria
        }
        if context:
            error_context.update(context)
        
        error = MusicRecommenderError(
            f"No songs found matching criteria: {criteria}",
            ErrorType.RETRIEVAL_ERROR,
            error_context
        )
        
        if self.logger:
            self.logger.log_error(
                ErrorType.RETRIEVAL_ERROR.value,
                f"No songs found matching criteria",
                str(error_context)
            )
        
        return error
    
    def handle_configuration_error(self, missing_key: str, 
                                  context: Optional[Dict[str, Any]] = None) -> MusicRecommenderError:
        """
        Handle a configuration error.
        
        Args:
            missing_key: The missing configuration key
            context: Additional context
            
        Returns:
            MusicRecommenderError with user-friendly message
        """
        error_context = {
            "missing_key": missing_key
        }
        if context:
            error_context.update(context)
        
        error = MusicRecommenderError(
            f"Configuration error: missing {missing_key}",
            ErrorType.CONFIGURATION_ERROR,
            error_context
        )
        
        if self.logger:
            self.logger.log_error(
                ErrorType.CONFIGURATION_ERROR.value,
                f"Missing configuration: {missing_key}",
                str(error_context)
            )
        
        return error
    
    def handle_unknown_error(self, original_error: Exception, 
                            context: Optional[Dict[str, Any]] = None) -> MusicRecommenderError:
        """
        Handle an unknown error.
        
        Args:
            original_error: The original exception
            context: Additional context
            
        Returns:
            MusicRecommenderError with user-friendly message
        """
        error_context = {
            "original_error": str(original_error),
            "error_type": type(original_error).__name__
        }
        if context:
            error_context.update(context)
        
        error = MusicRecommenderError(
            f"Unknown error: {str(original_error)}",
            ErrorType.UNKNOWN_ERROR,
            error_context
        )
        
        if self.logger:
            self.logger.log_error(
                ErrorType.UNKNOWN_ERROR.value,
                str(original_error),
                str(error_context)
            )
        
        return error


def validate_preferences(preferences: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate extracted preferences.
    
    Args:
        preferences: Dictionary of extracted preferences
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Define valid genres and moods
    valid_genres = [
        'pop', 'lofi', 'rock', 'jazz', 'ambient', 'synthwave', 
        'indie pop', 'hip-hop', 'folk', 'electronic', 'blues', 
        'classical', 'r&b', 'reggae', 'metal'
    ]
    valid_moods = [
        'happy', 'chill', 'intense', 'relaxed', 'focused', 
        'moody', 'peaceful', 'hopeful', 'nostalgic', 'dramatic', 
        'romantic', 'playful', 'energetic', 'angry'
    ]
    
    # Check genre
    if preferences.get('favorite_genre') is not None:
        genre = preferences['favorite_genre']
        if genre not in valid_genres:
            return False, f"Invalid genre '{genre}'. Valid genres: {', '.join(valid_genres)}"
    
    # Check mood
    if preferences.get('favorite_mood') is not None:
        mood = preferences['favorite_mood']
        if mood not in valid_moods:
            return False, f"Invalid mood '{mood}'. Valid moods: {', '.join(valid_moods)}"
    
    # Check energy range
    if preferences.get('target_energy') is not None:
        energy = preferences['target_energy']
        if not (0.0 <= energy <= 1.0):
            return False, f"Energy must be between 0.0 and 1.0, got {energy}"
    
    # Check tempo range
    if preferences.get('target_tempo') is not None:
        tempo = preferences['target_tempo']
        if not (40 <= tempo <= 200):
            return False, f"Tempo must be between 40 and 200 BPM, got {tempo}"
    
    # Check valence range
    if preferences.get('target_valence') is not None:
        valence = preferences['target_valence']
        if not (0.0 <= valence <= 1.0):
            return False, f"Valence must be between 0.0 and 1.0, got {valence}"
    
    # Check danceability range
    if preferences.get('target_danceability') is not None:
        danceability = preferences['target_danceability']
        if not (0.0 <= danceability <= 1.0):
            return False, f"Danceability must be between 0.0 and 1.0, got {danceability}"
    
    # Check for impossible combinations
    target_energy = preferences.get('target_energy')
    target_acousticness = preferences.get('target_acousticness')
    likes_acoustic = preferences.get('likes_acoustic')
    
    if (target_energy is not None and target_energy > 0.8 and 
        likes_acoustic and
        target_acousticness is not None and target_acousticness > 0.7):
        return False, "High energy (>0.8) with high acousticness (>0.7) is an unusual combination. Most high-energy music is electronic."
    
    return True, None
