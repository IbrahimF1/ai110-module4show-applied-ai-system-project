"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs
from user_profiles import get_profile, list_profiles, DEFAULT_PROFILE


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Use a predefined user profile
    # Available profiles: chill_lofi_lover, energetic_pop_fan, intense_rocker,
    #                    relaxed_jazz_listener, ambient_meditation, synthwave_enthusiast, indie_pop_fan
    user_prefs = get_profile("chill_lofi_lover")
    
    print(f"Using profile: chill_lofi_lover")
    print(f"  Favorite Genre: {user_prefs['favorite_genre']}")
    print(f"  Favorite Mood: {user_prefs['favorite_mood']}")
    print(f"  Target Energy: {user_prefs['target_energy']}")
    print(f"  Likes Acoustic: {user_prefs['likes_acoustic']}")
    print()

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
