"""
User Profile Definitions

This module contains predefined user taste profiles with target values
that can be used for testing and demonstration purposes.
"""

# Example user profiles with target values
USER_PROFILES = {
    "chill_lofi_lover": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "likes_acoustic": True,
        # Additional target values for numerical features
        "target_tempo": 80,
        "target_valence": 0.60,
        "target_danceability": 0.60,
        "target_acousticness": 0.75,
    },
    
    "energetic_pop_fan": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "likes_acoustic": False,
        # Additional target values for numerical features
        "target_tempo": 120,
        "target_valence": 0.80,
        "target_danceability": 0.80,
        "target_acousticness": 0.15,
    },
    
    "intense_rocker": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
        # Additional target values for numerical features
        "target_tempo": 140,
        "target_valence": 0.50,
        "target_danceability": 0.70,
        "target_acousticness": 0.10,
    },
    
    "relaxed_jazz_listener": {
        "favorite_genre": "jazz",
        "favorite_mood": "relaxed",
        "target_energy": 0.40,
        "likes_acoustic": True,
        # Additional target values for numerical features
        "target_tempo": 90,
        "target_valence": 0.70,
        "target_danceability": 0.55,
        "target_acousticness": 0.85,
    },
    
    "ambient_meditation": {
        "favorite_genre": "ambient",
        "favorite_mood": "chill",
        "target_energy": 0.30,
        "likes_acoustic": True,
        # Additional target values for numerical features
        "target_tempo": 60,
        "target_valence": 0.65,
        "target_danceability": 0.40,
        "target_acousticness": 0.90,
    },
    
    "synthwave_enthusiast": {
        "favorite_genre": "synthwave",
        "favorite_mood": "moody",
        "target_energy": 0.75,
        "likes_acoustic": False,
        # Additional target values for numerical features
        "target_tempo": 110,
        "target_valence": 0.50,
        "target_danceability": 0.70,
        "target_acousticness": 0.20,
    },
    
    "indie_pop_fan": {
        "favorite_genre": "indie pop",
        "favorite_mood": "happy",
        "target_energy": 0.75,
        "likes_acoustic": False,
        # Additional target values for numerical features
        "target_tempo": 124,
        "target_valence": 0.80,
        "target_danceability": 0.80,
        "target_acousticness": 0.35,
    },
    
    # Edge case profiles designed to test scoring logic
    "paradoxical_high_energy_acoustic": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.95,
        "likes_acoustic": True,
        # Contradictory: high energy but wants acoustic (typically low energy)
        "target_tempo": 130,
        "target_valence": 0.85,
        "target_danceability": 0.85,
        "target_acousticness": 0.90,
    },
    
    "impossible_slow_metal": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.15,
        "likes_acoustic": False,
        # Contradictory: rock/intense but very low energy and slow tempo
        "target_tempo": 50,
        "target_valence": 0.20,
        "target_danceability": 0.20,
        "target_acousticness": 0.10,
    },
    
    "hyper_fast_ambient": {
        "favorite_genre": "ambient",
        "favorite_mood": "chill",
        "target_energy": 0.80,
        "likes_acoustic": True,
        # Contradictory: ambient/chill but very fast tempo and high energy
        "target_tempo": 180,
        "target_valence": 0.70,
        "target_danceability": 0.75,
        "target_acousticness": 0.85,
    },
}

# Default profile used for general testing
DEFAULT_PROFILE = USER_PROFILES["chill_lofi_lover"]


def get_profile(profile_name: str) -> dict:
    """
    Retrieve a user profile by name.
    
    Args:
        profile_name: Name of the profile to retrieve
        
    Returns:
        Dictionary containing the user's taste preferences
    """
    return USER_PROFILES.get(profile_name, DEFAULT_PROFILE).copy()


def list_profiles() -> list:
    """
    List all available profile names.
    
    Returns:
        List of profile names
    """
    return list(USER_PROFILES.keys())
