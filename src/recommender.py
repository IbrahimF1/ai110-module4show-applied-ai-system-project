import math
import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

# Default target values for numerical features by genre
DEFAULT_TARGETS = {
    "pop": {"tempo": 120, "valence": 0.8, "danceability": 0.8},
    "lofi": {"tempo": 80, "valence": 0.6, "danceability": 0.6},
    "rock": {"tempo": 140, "valence": 0.5, "danceability": 0.7},
    "jazz": {"tempo": 90, "valence": 0.7, "danceability": 0.5},
    "ambient": {"tempo": 60, "valence": 0.65, "danceability": 0.4},
    "synthwave": {"tempo": 110, "valence": 0.5, "danceability": 0.7},
    "indie pop": {"tempo": 124, "valence": 0.8, "danceability": 0.8},
}

def gaussian_similarity(value: float, target: float, sigma: float) -> float:
    """
    Calculate Gaussian similarity between value and target.
    
    Uses a bell curve function to reward closeness:
    - Perfect match (difference = 0) → score = 1.0
    - Close match → score ≈ 0.9-1.0
    - Far match → score ≈ 0.0
    
    Args:
        value: The song's feature value
        target: The user's target value
        sigma: Controls the strictness (smaller = stricter)
    
    Returns:
        Similarity score in range [0.0, 1.0]
    """
    difference = value - target
    return math.exp(-(difference ** 2) / (2 * sigma ** 2))

def calculate_score(song: Song, user: UserProfile) -> float:
    """
    Calculate final score for a song given user preferences.
    
    Uses a weighted combination of:
    - Categorical features (genre, mood) - binary matching
    - Numerical features (energy, tempo, valence, danceability) - Gaussian similarity
    - Boolean preference (acousticness) - modified Gaussian
    
    Returns:
        Final score in range [0.0, 1.0]
    """
    # Categorical features (binary)
    score_genre = 1.0 if song.genre == user.favorite_genre else 0.0
    score_mood = 1.0 if song.mood == user.favorite_mood else 0.0
    
    # Numerical features (Gaussian similarity)
    score_energy = gaussian_similarity(song.energy, user.target_energy, sigma=0.15)
    
    # Get defaults for missing targets based on user's favorite genre
    defaults = DEFAULT_TARGETS.get(user.favorite_genre, {})
    target_tempo = defaults.get("tempo", 120)
    target_valence = defaults.get("valence", 0.7)
    target_danceability = defaults.get("danceability", 0.7)
    
    score_tempo = gaussian_similarity(song.tempo_bpm, target_tempo, sigma=20)
    score_valence = gaussian_similarity(song.valence, target_valence, sigma=0.15)
    score_danceability = gaussian_similarity(song.danceability, target_danceability, sigma=0.15)
    
    # Acousticness (modified based on user preference)
    if user.likes_acoustic:
        target_acoustic = 0.9
    else:
        target_acoustic = 0.1
    score_acousticness = gaussian_similarity(song.acousticness, target_acoustic, sigma=0.2)
    
    # Weighted sum of all components
    final_score = (
        0.25 * score_genre +
        0.15 * score_mood +
        0.20 * score_energy +
        0.10 * score_tempo +
        0.10 * score_valence +
        0.10 * score_danceability +
        0.10 * score_acousticness
    )
    
    return final_score

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommend top k songs based on user preferences.
        
        Calculates scores for all songs, sorts by score (descending),
        and returns the top k songs.
        """
        # Calculate scores for all songs
        scored_songs = [
            (song, calculate_score(song, user))
            for song in self.songs
        ]
        
        # Sort by score (descending)
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k songs
        return [song for song, score in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Explain why a song was recommended.
        
        Provides a breakdown of which features matched the user's preferences
        and the final score.
        """
        score = calculate_score(song, user)
        
        # Build explanation based on feature matches
        reasons = []
        
        # Genre match
        if song.genre == user.favorite_genre:
            reasons.append(f"Genre matches your preference ({song.genre})")
        
        # Mood match
        if song.mood == user.favorite_mood:
            reasons.append(f"Mood matches your preference ({song.mood})")
        
        # Energy closeness
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.1:
            reasons.append(f"Energy is very close to your target ({song.energy:.2f} vs {user.target_energy})")
        elif energy_diff < 0.2:
            reasons.append(f"Energy is reasonably close to your target ({song.energy:.2f} vs {user.target_energy})")
        
        # Acousticness preference
        if user.likes_acoustic:
            if song.acousticness > 0.7:
                reasons.append(f"High acousticness fits your preference ({song.acousticness:.2f})")
        else:
            if song.acousticness < 0.3:
                reasons.append(f"Low acousticness fits your preference ({song.acousticness:.2f})")
        
        # Build final explanation
        if reasons:
            explanation = "Recommended because:\n" + "\n".join(f"- {r}" for r in reasons)
        else:
            explanation = "Recommended based on overall similarity to your preferences."
        
        explanation += f"\n\nFinal score: {score:.3f} / 1.0"
        
        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    
    Reads the CSV file and returns a list of dictionaries,
    where each dictionary represents a song with its attributes.
    
    Args:
        csv_path: Path to the CSV file containing song data
        
    Returns:
        List of song dictionaries with all features
    """
    songs = []
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert string values to appropriate types
                song_dict = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                }
                songs.append(song_dict)
        print(f"Loaded {len(songs)} songs from {csv_path}")
    except FileNotFoundError:
        print(f"Error: File not found at {csv_path}")
    except Exception as e:
        print(f"Error loading songs: {e}")
    
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    
    Takes user preferences and a list of song dictionaries,
    calculates scores for each song, and returns the top k
    recommendations with scores and explanations.
    
    Args:
        user_prefs: Dictionary containing user preferences with keys:
            - favorite_genre: str
            - favorite_mood: str
            - target_energy: float
            - likes_acoustic: bool
        songs: List of song dictionaries
        k: Number of recommendations to return
        
    Returns:
        List of tuples (song_dict, score, explanation) for top k songs
    """
    # Create UserProfile from dictionary
    user = UserProfile(
        favorite_genre=user_prefs.get('favorite_genre', 'pop'),
        favorite_mood=user_prefs.get('favorite_mood', 'happy'),
        target_energy=user_prefs.get('target_energy', 0.7),
        likes_acoustic=user_prefs.get('likes_acoustic', False),
    )
    
    # Create Song objects from dictionaries
    song_objects = []
    for song_dict in songs:
        song = Song(
            id=song_dict['id'],
            title=song_dict['title'],
            artist=song_dict['artist'],
            genre=song_dict['genre'],
            mood=song_dict['mood'],
            energy=song_dict['energy'],
            tempo_bpm=song_dict['tempo_bpm'],
            valence=song_dict['valence'],
            danceability=song_dict['danceability'],
            acousticness=song_dict['acousticness'],
        )
        song_objects.append(song)
    
    # Create recommender and get recommendations
    recommender = Recommender(song_objects)
    recommended_songs = recommender.recommend(user, k)
    
    # Build results with scores and explanations
    results = []
    for song in recommended_songs:
        score = calculate_score(song, user)
        explanation = recommender.explain_recommendation(user, song)
        
        # Convert Song back to dictionary
        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness,
        }
        
        results.append((song_dict, score, explanation))
    
    return results
