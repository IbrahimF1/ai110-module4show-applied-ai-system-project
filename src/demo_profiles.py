"""
Demonstration script showing different user profiles and their recommendations.

This script demonstrates how different taste profiles affect recommendations.
"""

from recommender import load_songs, recommend_songs
from user_profiles import get_profile, list_profiles


def demonstrate_profile(profile_name: str, songs: list) -> None:
    """
    Demonstrate recommendations for a specific user profile.
    
    Args:
        profile_name: Name of the profile to demonstrate
        songs: List of song dictionaries
    """
    print("=" * 70)
    print(f"PROFILE: {profile_name.upper()}")
    print("=" * 70)
    
    user_prefs = get_profile(profile_name)
    
    print(f"\nUser Preferences:")
    print(f"  Favorite Genre: {user_prefs['favorite_genre']}")
    print(f"  Favorite Mood: {user_prefs['favorite_mood']}")
    print(f"  Target Energy: {user_prefs['target_energy']}")
    print(f"  Likes Acoustic: {user_prefs['likes_acoustic']}")
    
    # Get recommendations
    recommendations = recommend_songs(user_prefs, songs, k=3)
    
    print(f"\nTop 3 Recommendations:")
    print("-" * 70)
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']}, Mood: {song['mood']}")
        print(f"   Energy: {song['energy']:.2f}, Tempo: {song['tempo_bpm']:.0f} BPM")
        print(f"   Score: {score:.3f}")
        print(f"   {explanation}")
    
    print("\n")


def main():
    """Demonstrate all available user profiles."""
    # Load songs
    songs = load_songs("data/songs.csv")
    
    # List all available profiles
    print("Available User Profiles:")
    for profile in list_profiles():
        print(f"  - {profile}")
    print("\n")
    
    # Demonstrate a few different profiles
    profiles_to_demo = [
        "chill_lofi_lover",
        "energetic_pop_fan",
        "intense_rocker",
        "relaxed_jazz_listener",
    ]
    
    for profile_name in profiles_to_demo:
        demonstrate_profile(profile_name, songs)


if __name__ == "__main__":
    main()
