"""
Integration tests for RAG-Enhanced Music Recommender.

Tests the end-to-end workflow from user query to playlist generation.
"""

import pytest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.knowledge_base import KnowledgeBase
from src.song_retriever import SongRetriever
from src.error_handler import ErrorHandler, validate_preferences


@pytest.fixture
def knowledge_base():
    """Create a knowledge base fixture."""
    return KnowledgeBase("data/songs.csv")


@pytest.fixture
def song_retriever(knowledge_base):
    """Create a song retriever fixture."""
    return SongRetriever(knowledge_base)


@pytest.fixture
def error_handler():
    """Create an error handler fixture."""
    return ErrorHandler()


class TestRAGIntegration:
    """Test suite for RAG integration."""
    
    def test_end_to_end_workflow(self, knowledge_base, song_retriever):
        """Test complete workflow from query to recommendations."""
        # Simulate a user query
        query = "I want chill lofi music"
        
        # Extract preferences (simulated)
        preferences = {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.4,
            "likes_acoustic": True
        }
        
        # Validate preferences
        is_valid, error = validate_preferences(preferences)
        assert is_valid is True
        assert error is None
        
        # Retrieve songs
        songs = song_retriever.retrieve_by_preferences(preferences, top_k=5)
        assert len(songs) > 0
        
        # Verify songs match preferences
        for song in songs:
            assert song.genre.lower() == "lofi"
            assert song.mood.lower() == "chill"
    
    def test_keyword_retrieval_workflow(self, knowledge_base, song_retriever):
        """Test keyword-based retrieval workflow."""
        query = "happy pop songs"
        
        # Retrieve by keywords
        songs = song_retriever.retrieve_by_keywords(query, top_k=5)
        assert len(songs) > 0
        
        # Verify songs contain keywords
        for song in songs:
            has_keyword = (
                "happy" in song.keywords or
                "pop" in song.keywords or
                "happy" in song.title.lower() or
                "happy" in song.mood.lower() or
                "pop" in song.genre.lower()
            )
            assert has_keyword
    
    def test_hybrid_retrieval_workflow(self, knowledge_base, song_retriever):
        """Test hybrid retrieval workflow."""
        query = "energetic rock music"
        preferences = {
            "favorite_genre": "rock",
            "target_energy": 0.8
        }
        
        # Hybrid retrieval
        songs = song_retriever.hybrid_retrieve(query, preferences, top_k=5)
        assert len(songs) > 0
        
        # Verify songs match criteria
        for song in songs:
            assert song.genre.lower() == "rock"
    
    def test_similar_songs_workflow(self, knowledge_base, song_retriever):
        """Test similar songs workflow."""
        # Get a reference song
        reference_song = knowledge_base.get_song_by_id(1)
        assert reference_song is not None
        
        # Find similar songs
        similar_songs = song_retriever.get_similar_songs(1, top_k=3)
        assert len(similar_songs) > 0
        
        # Verify similar songs are different from reference
        for song in similar_songs:
            assert song.id != reference_song.id
    
    def test_genre_filter_workflow(self, knowledge_base, song_retriever):
        """Test genre filtering workflow."""
        preferences = {"favorite_genre": "jazz"}
        
        songs = song_retriever.retrieve_by_preferences(preferences, top_k=10)
        assert len(songs) > 0
        
        # All songs should be jazz
        for song in songs:
            assert song.genre.lower() == "jazz"
    
    def test_mood_filter_workflow(self, knowledge_base, song_retriever):
        """Test mood filtering workflow."""
        preferences = {"favorite_mood": "intense"}
        
        songs = song_retriever.retrieve_by_preferences(preferences, top_k=10)
        assert len(songs) > 0
        
        # All songs should be intense
        for song in songs:
            assert song.mood.lower() == "intense"
    
    def test_energy_preference_workflow(self, knowledge_base, song_retriever):
        """Test energy preference workflow."""
        preferences = {"target_energy": 0.8}
        
        songs = song_retriever.retrieve_by_preferences(preferences, top_k=5)
        assert len(songs) > 0
        
        # Songs should have high energy
        for song in songs:
            assert song.energy > 0.5  # Should be relatively high
    
    def test_acoustic_preference_workflow(self, knowledge_base, song_retriever):
        """Test acoustic preference workflow."""
        preferences = {"likes_acoustic": True}
        
        songs = song_retriever.retrieve_by_preferences(preferences, top_k=5)
        assert len(songs) > 0
        
        # Songs should have high acousticness
        for song in songs:
            assert song.acousticness > 0.5  # Should be relatively high
    
    def test_empty_preferences_workflow(self, knowledge_base, song_retriever):
        """Test workflow with empty preferences."""
        preferences = {}
        
        songs = song_retriever.retrieve_by_preferences(preferences, top_k=5)
        # Should return all songs (no filtering)
        assert len(songs) > 0
    
    def test_no_matches_workflow(self, knowledge_base, song_retriever):
        """Test workflow when no songs match."""
        preferences = {
            "favorite_genre": "nonexistent_genre"
        }
        
        songs = song_retriever.retrieve_by_preferences(preferences, top_k=5)
        # Should return empty list
        assert len(songs) == 0
    
    def test_multiple_preferences_workflow(self, knowledge_base, song_retriever):
        """Test workflow with multiple preferences."""
        preferences = {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.4,
            "likes_acoustic": True
        }
        
        songs = song_retriever.retrieve_by_preferences(preferences, top_k=5)
        assert len(songs) > 0
        
        # All songs should match all criteria
        for song in songs:
            assert song.genre.lower() == "lofi"
            assert song.mood.lower() == "chill"
            assert abs(song.energy - 0.4) < 0.3  # Within reasonable range
            assert song.acousticness > 0.5  # High acousticness
    
    def test_knowledge_base_integration(self, knowledge_base):
        """Test knowledge base integration."""
        # Get all songs
        songs = knowledge_base.get_all_songs()
        assert len(songs) == 18
        
        # Get song descriptions
        descriptions = knowledge_base.get_all_song_descriptions()
        assert len(descriptions) > 0
        
        # Get genres and moods
        genres = knowledge_base.get_genres()
        moods = knowledge_base.get_moods()
        assert len(genres) > 0
        assert len(moods) > 0
    
    def test_error_handling_integration(self, error_handler):
        """Test error handling integration."""
        # Test API error
        original_error = Exception("API failed")
        error = error_handler.handle_api_error(original_error)
        assert error.user_message is not None
        
        # Test extraction error
        error = error_handler.handle_extraction_error("test", "reason")
        assert error.user_message is not None
        
        # Test validation error
        error = error_handler.handle_validation_error("field", "value", "expected")
        assert error.user_message is not None
        
        # Test retrieval error
        error = error_handler.handle_retrieval_error({"criteria": "test"})
        assert error.user_message is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
