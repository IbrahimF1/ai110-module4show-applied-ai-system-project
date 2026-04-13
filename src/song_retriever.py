"""
Song Retriever for RAG-Enhanced Music Recommender.

Finds relevant songs based on query context and preferences.
"""

from typing import List, Dict, Optional
from knowledge_base import KnowledgeBase, SongInfo
from logger import get_logger


class SongRetriever:
    """
    Retrieves relevant songs based on various criteria.
    
    Uses a hybrid approach combining keyword matching and
    preference-based filtering.
    """
    
    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialize the song retriever.
        
        Args:
            knowledge_base: Knowledge base containing song information
        """
        self.knowledge_base = knowledge_base
        self.logger = get_logger()
    
    def retrieve_by_keywords(self, query: str, top_k: int = 10) -> List[SongInfo]:
        """
        Retrieve songs by keyword matching.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of matching SongInfo objects
        """
        self.logger.log_debug(f"Retrieving by keywords: {query}")
        
        try:
            songs = self.knowledge_base.search_by_keywords(query, top_k)
            self.logger.log_info(f"Retrieved {len(songs)} songs by keywords")
            return songs
        except Exception as e:
            self.logger.log_error("RetrievalError", str(e), str({"query": query}))
            return []
    
    def retrieve_by_preferences(self, preferences: Dict, top_k: int = 10) -> List[SongInfo]:
        """
        Retrieve songs based on extracted preferences.
        
        Args:
            preferences: Dictionary of extracted preferences
            top_k: Number of results to return
            
        Returns:
            List of matching SongInfo objects
        """
        self.logger.log_debug(f"Retrieving by preferences: {preferences}")
        
        try:
            # Start with all songs
            candidates = self.knowledge_base.get_all_songs()
            
            # Filter by genre if specified
            if preferences.get('favorite_genre'):
                genre = preferences['favorite_genre']
                candidates = [
                    song for song in candidates
                    if song.genre.lower() == genre.lower()
                ]
                self.logger.log_debug(f"Filtered by genre '{genre}': {len(candidates)} candidates")
            
            # Filter by mood if specified
            if preferences.get('favorite_mood'):
                mood = preferences['favorite_mood']
                candidates = [
                    song for song in candidates
                    if song.mood.lower() == mood.lower()
                ]
                self.logger.log_debug(f"Filtered by mood '{mood}': {len(candidates)} candidates")
            
            # If no candidates after filtering, return empty list
            if not candidates:
                self.logger.log_warning(f"No candidates after filtering by preferences")
                return []
            
            # Score remaining candidates based on numerical preferences
            scored_candidates = []
            for song in candidates:
                score = self._calculate_preference_score(song, preferences)
                scored_candidates.append((song, score))
            
            # Sort by score (descending) and return top k
            scored_candidates.sort(key=lambda x: x[1], reverse=True)
            result = [song for song, score in scored_candidates[:top_k]]
            
            self.logger.log_info(f"Retrieved {len(result)} songs by preferences")
            return result
            
        except Exception as e:
            self.logger.log_error("RetrievalError", str(e), str({"preferences": preferences}))
            return []
    
    def hybrid_retrieve(self, query: str, preferences: Dict, top_k: int = 10) -> List[SongInfo]:
        """
        Hybrid retrieval combining keywords and preferences.
        
        Args:
            query: Search query string
            preferences: Dictionary of extracted preferences
            top_k: Number of results to return
            
        Returns:
            List of matching SongInfo objects
        """
        self.logger.log_debug(f"Hybrid retrieval: query='{query}', preferences={preferences}")
        
        try:
            # Get results from both methods
            keyword_results = self.retrieve_by_keywords(query, top_k)
            preference_results = self.retrieve_by_preferences(preferences, top_k)
            
            # Combine and deduplicate
            combined = {}
            
            # Add keyword results with higher weight
            for i, song in enumerate(keyword_results):
                score = (top_k - i) * 2  # Higher weight for keyword matches
                if song.id not in combined or score > combined[song.id][1]:
                    combined[song.id] = (song, score)
            
            # Add preference results
            for i, song in enumerate(preference_results):
                score = (top_k - i)  # Lower weight for preference matches
                if song.id not in combined or score > combined[song.id][1]:
                    combined[song.id] = (song, score)
            
            # Sort by combined score and return top k
            sorted_results = sorted(combined.values(), key=lambda x: x[1], reverse=True)
            
            # Filter by genre if specified
            if preferences.get('favorite_genre'):
                genre = preferences['favorite_genre'].lower()
                sorted_results = [(song, score) for song, score in sorted_results if song.genre.lower() == genre]
                self.logger.log_debug(f"Filtered hybrid results by genre '{genre}': {len(sorted_results)} songs")
            
            result = [song for song, score in sorted_results[:top_k]]
            
            self.logger.log_info(f"Hybrid retrieval returned {len(result)} songs")
            return result
            
        except Exception as e:
            self.logger.log_error("RetrievalError", str(e), str({"query": query, "preferences": preferences}))
            return []
    
    def _calculate_preference_score(self, song: SongInfo, preferences: Dict) -> float:
        """
        Calculate a score for a song based on preferences.
        
        Args:
            song: SongInfo object
            preferences: Dictionary of preferences
            
        Returns:
            Score between 0.0 and 1.0
        """
        score = 0.0
        total_weight = 0.0
        
        # Energy preference
        if preferences.get('target_energy') is not None:
            target = preferences['target_energy']
            diff = abs(song.energy - target)
            energy_score = max(0, 1 - diff)  # Linear penalty
            score += energy_score * 0.3
            total_weight += 0.3
        
        # Tempo preference
        if preferences.get('target_tempo') is not None:
            target = preferences['target_tempo']
            diff = abs(song.tempo_bpm - target)
            # Normalize by 100 BPM max difference
            tempo_score = max(0, 1 - (diff / 100))
            score += tempo_score * 0.2
            total_weight += 0.2
        
        # Valence preference
        if preferences.get('target_valence') is not None:
            target = preferences['target_valence']
            diff = abs(song.valence - target)
            valence_score = max(0, 1 - diff)
            score += valence_score * 0.2
            total_weight += 0.2
        
        # Danceability preference
        if preferences.get('target_danceability') is not None:
            target = preferences['target_danceability']
            diff = abs(song.danceability - target)
            danceability_score = max(0, 1 - diff)
            score += danceability_score * 0.15
            total_weight += 0.15
        
        # Acousticness preference
        if preferences.get('likes_acoustic') is not None:
            if preferences['likes_acoustic']:
                # Prefer high acousticness
                acousticness_score = song.acousticness
            else:
                # Prefer low acousticness
                acousticness_score = 1 - song.acousticness
            score += acousticness_score * 0.15
            total_weight += 0.15
        
        # Normalize score
        if total_weight > 0:
            score = score / total_weight
        
        return score
    
    def get_similar_songs(self, song_id: int, top_k: int = 5) -> List[SongInfo]:
        """
        Get songs similar to a given song.
        
        Args:
            song_id: ID of the reference song
            top_k: Number of similar songs to return
            
        Returns:
            List of similar SongInfo objects
        """
        reference_song = self.knowledge_base.get_song_by_id(song_id)
        if not reference_song:
            self.logger.log_warning(f"Song not found: {song_id}")
            return []
        
        self.logger.log_debug(f"Finding songs similar to song {song_id}")
        
        # Get all other songs
        all_songs = self.knowledge_base.get_all_songs()
        other_songs = [s for s in all_songs if s.id != song_id]
        
        # Score by similarity
        scored_songs = []
        for song in other_songs:
            similarity = self._calculate_similarity(reference_song, song)
            scored_songs.append((song, similarity))
        
        # Sort by similarity and return top k
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        result = [song for song, similarity in scored_songs[:top_k]]
        
        self.logger.log_info(f"Found {len(result)} similar songs")
        return result
    
    def _calculate_similarity(self, song1: SongInfo, song2: SongInfo) -> float:
        """
        Calculate similarity between two songs.
        
        Args:
            song1: First song
            song2: Second song
            
        Returns:
            Similarity score between 0.0 and 1.0
        """
        similarity = 0.0
        
        # Genre match (binary)
        if song1.genre.lower() == song2.genre.lower():
            similarity += 0.3
        
        # Mood match (binary)
        if song1.mood.lower() == song2.mood.lower():
            similarity += 0.2
        
        # Numerical feature similarity
        energy_sim = 1 - abs(song1.energy - song2.energy)
        tempo_sim = 1 - (abs(song1.tempo_bpm - song2.tempo_bpm) / 100)
        valence_sim = 1 - abs(song1.valence - song2.valence)
        danceability_sim = 1 - abs(song1.danceability - song2.danceability)
        acousticness_sim = 1 - abs(song1.acousticness - song2.acousticness)
        
        similarity += (energy_sim + tempo_sim + valence_sim + 
                     danceability_sim + acousticness_sim) * 0.1
        
        return min(similarity, 1.0)
