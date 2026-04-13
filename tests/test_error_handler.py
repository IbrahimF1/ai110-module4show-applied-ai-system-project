"""
Unit tests for Error Handler.
"""

import pytest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.error_handler import (
    ErrorHandler, 
    MusicRecommenderError, 
    ErrorType,
    validate_preferences
)


@pytest.fixture
def error_handler():
    """Create an error handler fixture."""
    return ErrorHandler()


class TestErrorHandler:
    """Test suite for ErrorHandler class."""
    
    def test_handle_api_error(self, error_handler):
        """Test handling API errors."""
        original_error = Exception("API call failed")
        error = error_handler.handle_api_error(original_error)
        
        assert isinstance(error, MusicRecommenderError)
        assert error.error_type == ErrorType.API_ERROR
        assert error.user_message is not None
    
    def test_handle_extraction_error(self, error_handler):
        """Test handling extraction errors."""
        error = error_handler.handle_extraction_error(
            "test query",
            "Could not parse JSON"
        )
        
        assert isinstance(error, MusicRecommenderError)
        assert error.error_type == ErrorType.EXTRACTION_ERROR
        assert "test query" in error.context["query"]
    
    def test_handle_validation_error(self, error_handler):
        """Test handling validation errors."""
        error = error_handler.handle_validation_error(
            "energy",
            1.5,
            "between 0.0 and 1.0"
        )
        
        assert isinstance(error, MusicRecommenderError)
        assert error.error_type == ErrorType.VALIDATION_ERROR
        assert error.context["field"] == "energy"
    
    def test_handle_retrieval_error(self, error_handler):
        """Test handling retrieval errors."""
        error = error_handler.handle_retrieval_error({"genre": "unknown"})
        
        assert isinstance(error, MusicRecommenderError)
        assert error.error_type == ErrorType.RETRIEVAL_ERROR
        assert "genre" in error.context["criteria"]
    
    def test_handle_configuration_error(self, error_handler):
        """Test handling configuration errors."""
        error = error_handler.handle_configuration_error("API_KEY")
        
        assert isinstance(error, MusicRecommenderError)
        assert error.error_type == ErrorType.CONFIGURATION_ERROR
        assert "API_KEY" in error.context["missing_key"]
    
    def test_handle_unknown_error(self, error_handler):
        """Test handling unknown errors."""
        original_error = Exception("Something went wrong")
        error = error_handler.handle_unknown_error(original_error)
        
        assert isinstance(error, MusicRecommenderError)
        assert error.error_type == ErrorType.UNKNOWN_ERROR


class TestMusicRecommenderError:
    """Test suite for MusicRecommenderError class."""
    
    def test_error_initialization(self):
        """Test error initialization."""
        error = MusicRecommenderError("Test error", ErrorType.API_ERROR)
        
        assert str(error) == "Test error"
        assert error.error_type == ErrorType.API_ERROR
        assert error.user_message is not None
    
    def test_error_with_context(self):
        """Test error with context."""
        context = {"query": "test", "reason": "invalid"}
        error = MusicRecommenderError(
            "Test error",
            ErrorType.VALIDATION_ERROR,
            context
        )
        
        assert error.context == context
    
    def test_error_to_dict(self):
        """Test converting error to dictionary."""
        error = MusicRecommenderError("Test error", ErrorType.API_ERROR)
        error_dict = error.to_dict()
        
        assert "error_type" in error_dict
        assert "message" in error_dict
        assert "user_message" in error_dict
        assert "context" in error_dict
    
    def test_user_message_generation(self):
        """Test user-friendly message generation."""
        error = MusicRecommenderError("Test", ErrorType.API_ERROR)
        assert "ai service" in error.user_message.lower()
        
        error = MusicRecommenderError("Test", ErrorType.EXTRACTION_ERROR)
        assert "understand" in error.user_message.lower()


class TestValidatePreferences:
    """Test suite for validate_preferences function."""
    
    def test_valid_preferences(self):
        """Test validation of valid preferences."""
        preferences = {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.7,
            "likes_acoustic": True
        }
        
        is_valid, error = validate_preferences(preferences)
        assert is_valid is True
        assert error is None
    
    def test_invalid_genre(self):
        """Test validation with invalid genre."""
        preferences = {
            "favorite_genre": "invalid_genre"
        }
        
        is_valid, error = validate_preferences(preferences)
        assert is_valid is False
        assert error is not None
        assert "genre" in error.lower()
    
    def test_invalid_mood(self):
        """Test validation with invalid mood."""
        preferences = {
            "favorite_mood": "invalid_mood"
        }
        
        is_valid, error = validate_preferences(preferences)
        assert is_valid is False
        assert error is not None
        assert "mood" in error.lower()
    
    def test_invalid_energy(self):
        """Test validation with invalid energy."""
        preferences = {
            "target_energy": 1.5
        }
        
        is_valid, error = validate_preferences(preferences)
        assert is_valid is False
        assert error is not None
        assert "energy" in error.lower()
    
    def test_invalid_tempo(self):
        """Test validation with invalid tempo."""
        preferences = {
            "target_tempo": 250
        }
        
        is_valid, error = validate_preferences(preferences)
        assert is_valid is False
        assert error is not None
        assert "tempo" in error.lower()
    
    def test_invalid_valence(self):
        """Test validation with invalid valence."""
        preferences = {
            "target_valence": -0.5
        }
        
        is_valid, error = validate_preferences(preferences)
        assert is_valid is False
        assert error is not None
        assert "valence" in error.lower()
    
    def test_invalid_danceability(self):
        """Test validation with invalid danceability."""
        preferences = {
            "target_danceability": 2.0
        }
        
        is_valid, error = validate_preferences(preferences)
        assert is_valid is False
        assert error is not None
        assert "danceability" in error.lower()
    
    def test_impossible_combination(self):
        """Test validation of impossible combination."""
        preferences = {
            "target_energy": 0.9,
            "likes_acoustic": True,
            "target_acousticness": 0.8
        }
        
        is_valid, error = validate_preferences(preferences)
        assert is_valid is False
        assert error is not None
        assert "unusual" in error.lower()
    
    def test_empty_preferences(self):
        """Test validation of empty preferences."""
        preferences = {}
        
        is_valid, error = validate_preferences(preferences)
        assert is_valid is True
        assert error is None
    
    def test_null_preferences(self):
        """Test validation with null values."""
        preferences = {
            "favorite_genre": None,
            "target_energy": None
        }
        
        is_valid, error = validate_preferences(preferences)
        assert is_valid is True
        assert error is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
