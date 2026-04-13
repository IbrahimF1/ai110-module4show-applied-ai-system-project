"""
Knowledge Base for RAG-Enhanced Music Recommender.

Manages song information and provides search functionality.
"""

import csv
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SongInfo:
    """Represents a song with all its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    description: str
    keywords: List[str]


class KnowledgeBase:
    """
    Manages song information and provides search functionality.
    
    Loads songs from CSV, generates natural language descriptions,
    and provides keyword-based retrieval.
    """
    
    def __init__(self, csv_path: str = "data/songs.csv"):
        """
        Initialize the knowledge base.
        
        Args:
            csv_path: Path to the songs CSV file
        """
        self.songs: Dict[int, SongInfo] = {}
        self.load_songs(csv_path)
    
    def load_songs(self, csv_path: str) -> None:
        """
        Load songs from CSV file and generate descriptions.
        
        Args:
            csv_path: Path to the songs CSV file
        """
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    song_info = SongInfo(
                        id=int(row['id']),
                        title=row['title'],
                        artist=row['artist'],
                        genre=row['genre'],
                        mood=row['mood'],
                        energy=float(row['energy']),
                        tempo_bpm=float(row['tempo_bpm']),
                        valence=float(row['valence']),
                        danceability=float(row['danceability']),
                        acousticness=float(row['acousticness']),
                        description=self._generate_description(row),
                        keywords=self._extract_keywords(row)
                    )
                    self.songs[song_info.id] = song_info
            print(f"Loaded {len(self.songs)} songs into knowledge base")
        except FileNotFoundError:
            print(f"Error: File not found at {csv_path}")
        except Exception as e:
            print(f"Error loading songs: {e}")
    
    def _generate_description(self, song_row: Dict) -> str:
        """
        Generate a natural language description for a song.
        
        Args:
            song_row: Dictionary of song attributes
            
        Returns:
            Natural language description
        """
        title = song_row['title']
        artist = song_row['artist']
        genre = song_row['genre']
        mood = song_row['mood']
        energy = float(song_row['energy'])
        tempo = float(song_row['tempo_bpm'])
        valence = float(song_row['valence'])
        danceability = float(song_row['danceability'])
        acousticness = float(song_row['acousticness'])
        
        # Describe energy
        if energy < 0.3:
            energy_desc = "low energy"
        elif energy < 0.6:
            energy_desc = "moderate energy"
        else:
            energy_desc = "high energy"
        
        # Describe tempo
        if tempo < 70:
            tempo_desc = "slow tempo"
        elif tempo < 110:
            tempo_desc = "moderate tempo"
        else:
            tempo_desc = "fast tempo"
        
        # Describe valence
        if valence < 0.4:
            valence_desc = "negative or melancholic"
        elif valence < 0.6:
            valence_desc = "neutral"
        else:
            valence_desc = "positive and upbeat"
        
        # Describe danceability
        if danceability < 0.5:
            dance_desc = "not very danceable"
        elif danceability < 0.7:
            dance_desc = "moderately danceable"
        else:
            dance_desc = "highly danceable"
        
        # Describe acousticness
        if acousticness > 0.7:
            acoustic_desc = "highly acoustic"
        elif acousticness > 0.3:
            acoustic_desc = "somewhat acoustic"
        else:
            acoustic_desc = "electronic with low acousticness"
        
        description = (
            f"{title} by {artist} is a {mood} {genre} song with {energy_desc} "
            f"({energy:.2f}), {tempo_desc} ({tempo:.0f} BPM), and {valence_desc} "
            f"valence ({valence:.2f}). It is {dance_desc} ({danceability:.2f}) "
            f"and {acoustic_desc} ({acousticness:.2f})."
        )
        
        return description
    
    def _extract_keywords(self, song_row: Dict) -> List[str]:
        """
        Extract keywords from song attributes for search.
        
        Args:
            song_row: Dictionary of song attributes
            
        Returns:
            List of keywords
        """
        keywords = []
        
        # Add genre and mood
        keywords.append(song_row['genre'].lower())
        keywords.append(song_row['mood'].lower())
        
        # Add artist and title words
        title_words = song_row['title'].lower().split()
        artist_words = song_row['artist'].lower().split()
        keywords.extend(title_words)
        keywords.extend(artist_words)
        
        # Add energy level keywords
        energy = float(song_row['energy'])
        if energy < 0.3:
            keywords.extend(['low energy', 'calm', 'relaxed'])
        elif energy < 0.6:
            keywords.extend(['moderate energy', 'balanced'])
        else:
            keywords.extend(['high energy', 'energetic', 'upbeat'])
        
        # Add acousticness keywords
        acousticness = float(song_row['acousticness'])
        if acousticness > 0.7:
            keywords.extend(['acoustic', 'natural', 'organic'])
        elif acousticness < 0.3:
            keywords.extend(['electronic', 'synthetic', 'digital'])
        
        return list(set(keywords))  # Remove duplicates
    
    def get_song_by_id(self, song_id: int) -> Optional[SongInfo]:
        """
        Get a song by its ID.
        
        Args:
            song_id: The song ID
            
        Returns:
            SongInfo object or None if not found
        """
        return self.songs.get(song_id)
    
    def get_all_songs(self) -> List[SongInfo]:
        """
        Get all songs in the knowledge base.
        
        Returns:
            List of all SongInfo objects
        """
        return list(self.songs.values())
    
    def get_all_song_descriptions(self) -> str:
        """
        Get all song descriptions formatted for LLM context.
        
        Returns:
            Formatted string of all song descriptions
        """
        descriptions = []
        for song in self.songs.values():
            descriptions.append(
                f"ID {song.id}: {song.description}"
            )
        return "\n\n".join(descriptions)
    
    def search_by_keywords(self, query: str, top_k: int = 5) -> List[SongInfo]:
        """
        Search songs by keyword matching.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of matching SongInfo objects
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_songs = []
        for song in self.songs.values():
            # Count matching keywords
            song_keywords = set(song.keywords)
            matches = query_words.intersection(song_keywords)
            
            # Also check if query words appear in title or artist
            title_words = set(song.title.lower().split())
            artist_words = set(song.artist.lower().split())
            matches.update(query_words.intersection(title_words))
            matches.update(query_words.intersection(artist_words))
            
            if matches:
                score = len(matches)
                scored_songs.append((song, score))
        
        # Sort by score (descending) and return top k
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in scored_songs[:top_k]]
    
    def filter_by_genre(self, genre: str) -> List[SongInfo]:
        """
        Filter songs by genre.
        
        Args:
            genre: Genre to filter by
            
        Returns:
            List of matching SongInfo objects
        """
        genre_lower = genre.lower()
        return [
            song for song in self.songs.values()
            if song.genre.lower() == genre_lower
        ]
    
    def filter_by_mood(self, mood: str) -> List[SongInfo]:
        """
        Filter songs by mood.
        
        Args:
            mood: Mood to filter by
            
        Returns:
            List of matching SongInfo objects
        """
        mood_lower = mood.lower()
        return [
            song for song in self.songs.values()
            if song.mood.lower() == mood_lower
        ]
    
    def get_genres(self) -> List[str]:
        """
        Get all unique genres in the knowledge base.
        
        Returns:
            List of unique genres
        """
        return list(set(song.genre for song in self.songs.values()))
    
    def get_moods(self) -> List[str]:
        """
        Get all unique moods in the knowledge base.
        
        Returns:
            List of unique moods
        """
        return list(set(song.mood for song in self.songs.values()))
