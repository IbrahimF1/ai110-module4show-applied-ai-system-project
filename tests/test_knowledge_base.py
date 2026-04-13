"""
Unit tests for Knowledge Base.
"""

import pytest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.knowledge_base import KnowledgeBase, SongInfo


@pytest.fixture
def knowledge_base():
    """Create a knowledge base fixture."""
    kb = KnowledgeBase("data/songs.csv")
    return kb


class TestKnowledgeBase:
    """Test suite for KnowledgeBase class."""
    
    def test_initialization(self, knowledge_base):
        """Test that knowledge base initializes correctly."""
        assert knowledge_base is not None
        assert len(knowledge_base.songs) > 0
    
    def test_load_songs(self, knowledge_base):
        """Test that songs are loaded correctly."""
        assert len(knowledge_base.songs) == 18  # Based on songs.csv
    
    def test_get_song_by_id(self, knowledge_base):
        """Test retrieving a song by ID."""
        song = knowledge_base.get_song_by_id(1)
        assert song is not None
        assert song.id == 1
        assert song.title == "Sunrise City"
        assert song.artist == "Neon Echo"
    
    def test_get_song_by_id_not_found(self, knowledge_base):
        """Test retrieving a non-existent song."""
        song = knowledge_base.get_song_by_id(999)
        assert song is None
    
    def test_get_all_songs(self, knowledge_base):
        """Test getting all songs."""
        songs = knowledge_base.get_all_songs()
        assert len(songs) == 18
        assert all(isinstance(song, SongInfo) for song in songs)
    
    def test_get_all_song_descriptions(self, knowledge_base):
        """Test getting all song descriptions."""
        descriptions = knowledge_base.get_all_song_descriptions()
        assert len(descriptions) > 0
        assert "Sunrise City" in descriptions
        assert "Neon Echo" in descriptions
    
    def test_search_by_keywords(self, knowledge_base):
        """Test keyword search."""
        results = knowledge_base.search_by_keywords("lofi")
        assert len(results) > 0
        assert all("lofi" in song.genre.lower() or "lofi" in song.keywords for song in results)
    
    def test_search_by_keywords_title(self, knowledge_base):
        """Test keyword search by title."""
        results = knowledge_base.search_by_keywords("Sunrise")
        assert len(results) > 0
        assert results[0].title == "Sunrise City"
    
    def test_search_by_keywords_artist(self, knowledge_base):
        """Test keyword search by artist."""
        results = knowledge_base.search_by_keywords("Neon Echo")
        assert len(results) > 0
        assert results[0].artist == "Neon Echo"
    
    def test_filter_by_genre(self, knowledge_base):
        """Test filtering by genre."""
        results = knowledge_base.filter_by_genre("lofi")
        assert len(results) > 0
        assert all(song.genre.lower() == "lofi" for song in results)
    
    def test_filter_by_mood(self, knowledge_base):
        """Test filtering by mood."""
        results = knowledge_base.filter_by_mood("chill")
        assert len(results) > 0
        assert all(song.mood.lower() == "chill" for song in results)
    
    def test_get_genres(self, knowledge_base):
        """Test getting all unique genres."""
        genres = knowledge_base.get_genres()
        assert len(genres) > 0
        assert "pop" in genres
        assert "lofi" in genres
        assert "rock" in genres
    
    def test_get_moods(self, knowledge_base):
        """Test getting all unique moods."""
        moods = knowledge_base.get_moods()
        assert len(moods) > 0
        assert "happy" in moods
        assert "chill" in moods
        assert "intense" in moods
    
    def test_song_info_attributes(self, knowledge_base):
        """Test that SongInfo has all required attributes."""
        song = knowledge_base.get_song_by_id(1)
        assert hasattr(song, 'id')
        assert hasattr(song, 'title')
        assert hasattr(song, 'artist')
        assert hasattr(song, 'genre')
        assert hasattr(song, 'mood')
        assert hasattr(song, 'energy')
        assert hasattr(song, 'tempo_bpm')
        assert hasattr(song, 'valence')
        assert hasattr(song, 'danceability')
        assert hasattr(song, 'acousticness')
        assert hasattr(song, 'description')
        assert hasattr(song, 'keywords')
    
    def test_description_generation(self, knowledge_base):
        """Test that descriptions are generated correctly."""
        song = knowledge_base.get_song_by_id(1)
        assert song.description is not None
        assert len(song.description) > 0
        assert "Sunrise City" in song.description
        assert "Neon Echo" in song.description
    
    def test_keyword_extraction(self, knowledge_base):
        """Test that keywords are extracted correctly."""
        song = knowledge_base.get_song_by_id(1)
        assert song.keywords is not None
        assert len(song.keywords) > 0
        assert "pop" in song.keywords
        assert "happy" in song.keywords


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
