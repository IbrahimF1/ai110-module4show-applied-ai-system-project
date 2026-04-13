"""
Edge Case Testing Script

This script tests the recommender with three distinct edge-case profiles
designed to potentially trick the scoring logic or produce unexpected results.

Profiles tested:
1. Paradoxical High-Energy Acoustic - Wants high energy but acoustic (contradictory)
2. Impossible Slow Metal - Wants rock/intense but very low energy and slow tempo
3. Hyper-Fast Ambient - Wants ambient/chill but very fast tempo and high energy
"""

from recommender import load_songs, recommend_songs, calculate_score, Song, UserProfile
from user_profiles import get_profile


def analyze_edge_case(profile_name: str, songs: list) -> None:
    """
    Analyze recommendations for an edge case profile.
    
    Args:
        profile_name: Name of the edge case profile
        songs: List of song dictionaries
    """
    print("=" * 80)
    print(f"EDGE CASE TEST: {profile_name.upper()}")
    print("=" * 80)
    
    user_prefs = get_profile(profile_name)
    
    print(f"\n📊 Profile Configuration:")
    print(f"   Favorite Genre: {user_prefs['favorite_genre']}")
    print(f"   Favorite Mood: {user_prefs['favorite_mood']}")
    print(f"   Target Energy: {user_prefs['target_energy']}")
    print(f"   Likes Acoustic: {user_prefs['likes_acoustic']}")
    print(f"   Target Tempo: {user_prefs['target_tempo']} BPM")
    print(f"   Target Valence: {user_prefs['target_valence']}")
    print(f"   Target Danceability: {user_prefs['target_danceability']}")
    print(f"   Target Acousticness: {user_prefs['target_acousticness']}")
    
    print(f"\n⚠️  Potential Contradictions:")
    if profile_name == "paradoxical_high_energy_acoustic":
        print("   • HIGH ENERGY (0.95) but WANTS ACOUSTIC (0.90)")
        print("   • Acoustic music typically has LOW energy")
        print("   • This profile wants impossible combination")
    elif profile_name == "impossible_slow_metal":
        print("   • ROCK/INTENSE genre but LOW ENERGY (0.15)")
        print("   • SLOW TEMPO (50 BPM) for intense rock")
        print("   • Rock/intense music typically has HIGH energy and FAST tempo")
    elif profile_name == "hyper_fast_ambient":
        print("   • AMBIENT/CHILL genre but HIGH ENERGY (0.80)")
        print("   • VERY FAST TEMPO (180 BPM) for ambient music")
        print("   • Ambient/chill music typically has LOW energy and SLOW tempo")
    
    # Get recommendations
    recommendations = recommend_songs(user_prefs, songs, k=5)
    
    print(f"\n🎵 Top 5 Recommendations:")
    print("-" * 80)
    
    if not recommendations:
        print("   No recommendations generated!")
        return
    
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']}, Mood: {song['mood']}")
        print(f"   Energy: {song['energy']:.2f}, Tempo: {song['tempo_bpm']:.0f} BPM")
        print(f"   Valence: {song['valence']:.2f}, Danceability: {song['danceability']:.2f}")
        print(f"   Acousticness: {song['acousticness']:.2f}")
        print(f"   ⭐ Score: {score:.4f}")
        
        # Analyze if this is a good match
        genre_match = "✓" if song['genre'] == user_prefs['favorite_genre'] else "✗"
        mood_match = "✓" if song['mood'] == user_prefs['favorite_mood'] else "✗"
        energy_diff = abs(song['energy'] - user_prefs['target_energy'])
        tempo_diff = abs(song['tempo_bpm'] - user_prefs['target_tempo'])
        
        print(f"   Match Analysis:")
        print(f"      Genre: {genre_match}, Mood: {mood_match}")
        print(f"      Energy diff: {energy_diff:.2f}, Tempo diff: {tempo_diff:.0f} BPM")
        
        # Check for contradictions
        if profile_name == "paradoxical_high_energy_acoustic":
            if song['energy'] > 0.8 and song['acousticness'] > 0.7:
                print(f"      ⚠️  Found: High energy + High acoustic (RARE!)")
            elif song['energy'] > 0.8:
                print(f"      ⚠️  High energy but LOW acoustic (contradicts preference)")
            elif song['acousticness'] > 0.7:
                print(f"      ⚠️  High acoustic but LOW energy (contradicts target)")
        
        print(f"   {explanation}")
    
    # Calculate average score for all songs
    print(f"\n📈 Score Distribution Analysis:")
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
    
    user = UserProfile(
        favorite_genre=user_prefs['favorite_genre'],
        favorite_mood=user_prefs['favorite_mood'],
        target_energy=user_prefs['target_energy'],
        likes_acoustic=user_prefs['likes_acoustic'],
    )
    
    all_scores = [calculate_score(song, user) for song in song_objects]
    avg_score = sum(all_scores) / len(all_scores)
    max_score = max(all_scores)
    min_score = min(all_scores)
    
    print(f"   Average score across all songs: {avg_score:.4f}")
    print(f"   Maximum score: {max_score:.4f}")
    print(f"   Minimum score: {min_score:.4f}")
    print(f"   Score range: {max_score - min_score:.4f}")
    
    # Check if scores are suspicious
    if max_score < 0.5:
        print(f"   ⚠️  WARNING: Maximum score is very low ({max_score:.4f})")
        print(f"      This profile may be too restrictive or contradictory!")
    
    print("\n")


def main():
    """Run edge case tests."""
    # Load songs
    songs = load_songs("data/songs.csv")
    
    # Test each edge case
    edge_cases = [
        "paradoxical_high_energy_acoustic",
        "impossible_slow_metal",
        "hyper_fast_ambient",
    ]
    
    for profile_name in edge_cases:
        analyze_edge_case(profile_name, songs)
    
    print("=" * 80)
    print("EDGE CASE TESTING COMPLETE")
    print("=" * 80)
    print("\n🔍 Key Observations:")
    print("   • Check if the recommender found any songs matching impossible criteria")
    print("   • Look at score distribution - are scores suspiciously low?")
    print("   • See which features the recommender prioritized")
    print("   • Identify if any songs 'tricked' the system with high scores")


if __name__ == "__main__":
    main()
