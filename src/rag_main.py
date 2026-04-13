"""
RAG-Enhanced Music Recommender - Interactive CLI.

Provides a conversational interface for finding music recommendations.
"""

import os
import sys
from typing import Dict, List, Tuple, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemini_client import GeminiClient
from knowledge_base import KnowledgeBase
from preference_extractor import PreferenceExtractor
from song_retriever import SongRetriever
from recommender import load_songs, recommend_songs, UserProfile
from logger import get_logger
from error_handler import ErrorHandler


class RAGMusicRecommender:
    """
    RAG-Enhanced Music Recommender with conversational interface.
    
    Integrates Gemma AI for natural language understanding with
    the existing mathematical recommender for playlist generation.
    """
    
    def __init__(self):
        """Initialize the RAG music recommender."""
        self.logger = get_logger()
        self.error_handler = ErrorHandler(self.logger)
        
        # Initialize components
        self.logger.log_info("Initializing RAG Music Recommender...")
        
        try:
            # Load knowledge base
            self.knowledge_base = KnowledgeBase()
            
            # Initialize Gemma client
            self.gemma_client = GeminiClient()
            
            # Initialize preference extractor
            self.preference_extractor = PreferenceExtractor(
                self.gemma_client,
                self.knowledge_base
            )
            
            # Initialize song retriever
            self.song_retriever = SongRetriever(self.knowledge_base)
            
            # Load songs for existing recommender
            self.songs = load_songs("data/songs.csv")
            
            self.logger.log_info("RAG Music Recommender initialized successfully")
            
        except Exception as e:
            error = self.error_handler.handle_configuration_error(
                "Failed to initialize system",
                {"exception": str(e)}
            )
            print(f"\n❌ {error.user_message}")
            print(f"   Details: {error}")
            sys.exit(1)
    
    def process_query(self, query: str) -> Tuple[Optional[List[Tuple[Dict, float, str]]], Optional[str]]:
        """
        Process a user query and return recommendations.
        
        Args:
            query: User's natural language query
            
        Returns:
            Tuple of (playlist, error_message)
        """
        print("\n🎵 Understanding your request...")
        
        # Check if query needs clarification
        if self.preference_extractor.needs_clarification(query):
            clarification = self.preference_extractor.get_clarification_request(query)
            return None, clarification
        
        # Extract preferences
        preferences, confidence, error = self.preference_extractor.extract_preferences(query)
        
        if error:
            return None, error
        
        if not preferences:
            return None, "I couldn't extract clear preferences from your query. Please try again with more specific details."
        
        # Display extracted preferences
        self._display_extracted_preferences(preferences, confidence)
        
        # Get recommendations using existing recommender
        try:
            playlist = recommend_songs(preferences, self.songs, k=5)
            
            if not playlist:
                return None, "I couldn't find any songs matching your preferences. Try different criteria."
            
            # Generate AI explanation (convert to expected format)
            playlist_for_ai = [(song, score) for song, score, _ in playlist]
            explanation = self.gemma_client.generate_response(query, playlist_for_ai)
            
            # Log recommendation
            avg_score = sum(score for _, score, _ in playlist) / len(playlist)
            self.logger.log_recommendation(query, len(playlist), avg_score)
            
            return playlist, explanation
            
        except Exception as e:
            error = self.error_handler.handle_unknown_error(e, {"query": query})
            return None, error.user_message
    
    def _display_extracted_preferences(self, preferences: Dict, confidence: float) -> None:
        """
        Display extracted preferences to the user.
        
        Args:
            preferences: Extracted preferences dictionary
            confidence: Confidence score
        """
        print("\n📋 Extracted Preferences:")
        
        if preferences.get('favorite_genre'):
            print(f"   • Genre: {preferences['favorite_genre']}")
        
        if preferences.get('favorite_mood'):
            print(f"   • Mood: {preferences['favorite_mood']}")
        
        if preferences.get('target_energy') is not None:
            print(f"   • Energy: {preferences['target_energy']:.2f}")
        
        if preferences.get('likes_acoustic') is not None:
            acoustic_pref = "yes" if preferences['likes_acoustic'] else "no"
            print(f"   • Acoustic: {acoustic_pref}")
        
        if preferences.get('target_tempo') is not None:
            print(f"   • Tempo: {preferences['target_tempo']:.0f} BPM")
        
        if preferences.get('target_valence') is not None:
            print(f"   • Valence: {preferences['target_valence']:.2f}")
        
        if preferences.get('target_danceability') is not None:
            print(f"   • Danceability: {preferences['target_danceability']:.2f}")
        
        print(f"\n   Confidence: {confidence:.0%}")
    
    def display_playlist(self, playlist: List[Tuple[Dict, float, str]], explanation: str) -> None:
        """
        Display the recommended playlist to the user.
        
        Args:
            playlist: List of (song_dict, score, explanation) tuples
            explanation: AI-generated explanation
        """
        print("\n" + "=" * 60)
        print("🎧 Recommended Playlist")
        print("=" * 60 + "\n")
        
        for i, (song, score, rec_explanation) in enumerate(playlist, 1):
            print(f"{i}. {song['title']} - {song['artist']}")
            print(f"   Genre: {song['genre']} | Mood: {song['mood']}")
            print(f"   Energy: {song['energy']:.2f} | Tempo: {song['tempo_bpm']:.0f} BPM")
            print(f"   ⭐ Score: {score:.3f}")
            print(f"   Why: {rec_explanation.split('Final score')[0].strip()}")
            print()
        
        print("=" * 60)
        print("💬 AI Explanation")
        print("=" * 60)
        print(f"\n{explanation}\n")
    
    def display_available_options(self) -> None:
        """Display available genres and moods to the user."""
        options = self.preference_extractor.get_available_options()
        
        print("\n" + "=" * 60)
        print("📚 Available Options")
        print("=" * 60)
        
        print("\n🎵 Genres:")
        for genre in sorted(options['genres']):
            print(f"   • {genre}")
        
        print("\n😊 Moods:")
        for mood in sorted(options['moods']):
            print(f"   • {mood}")
        
        print("\n" + "=" * 60)
    
    def run(self) -> None:
        """Run the interactive CLI."""
        self.logger.log_conversation_start()
        
        print("\n" + "=" * 60)
        print("🎵 RAG-Enhanced Music Recommender")
        print("=" * 60)
        print("\nI can help you find the perfect playlist based on natural")
        print("language descriptions. Just tell me what you're looking for!")
        print("\nExamples:")
        print("   • \"I want chill lofi music for studying\"")
        print("   • \"Give me energetic pop songs for a workout\"")
        print("   • \"I'm in the mood for something relaxing and acoustic\"")
        print("   • \"Show me all jazz songs\"")
        print("\nCommands:")
        print("   • 'options' - Show available genres and moods")
        print("   • 'help' - Show this help message")
        print("   • 'quit' or 'exit' - Exit the program")
        print("=" * 60 + "\n")
        
        while True:
            try:
                # Get user input
                query = input("Your query (or 'quit' to exit): > ").strip()
                
                # Check for commands
                if query.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thanks for using RAG-Enhanced Music Recommender!")
                    self.logger.log_conversation_end()
                    break
                
                if query.lower() in ['help', 'h']:
                    print("\n" + "=" * 60)
                    print("📖 Help")
                    print("=" * 60)
                    print("\nI can help you find music based on:")
                    print("   • Genre (pop, lofi, rock, jazz, etc.)")
                    print("   • Mood (chill, happy, intense, relaxed, etc.)")
                    print("   • Energy level (low, medium, high)")
                    print("   • Activity (studying, working out, relaxing, etc.)")
                    print("   • Acoustic preference (acoustic or electronic)")
                    print("\nExamples:")
                    print("   • \"I want chill lofi music for studying\"")
                    print("   • \"Give me energetic pop songs for a workout\"")
                    print("   • \"I'm in the mood for something relaxing\"")
                    print("\nCommands:")
                    print("   • 'options' - Show available genres and moods")
                    print("   • 'help' - Show this help message")
                    print("   • 'quit' - Exit the program")
                    print("=" * 60 + "\n")
                    continue
                
                if query.lower() in ['options', 'o']:
                    self.display_available_options()
                    continue
                
                # Skip empty queries
                if not query:
                    continue
                
                # Process the query
                playlist, explanation_or_error = self.process_query(query)
                
                if playlist:
                    # Display playlist
                    self.display_playlist(playlist, explanation_or_error)  # type: ignore
                    
                    # Ask if user wants to continue
                    print("\nWould you like to refine your preferences? (yes/no) > ", end="")
                    refine = input().strip().lower()
                    
                    if refine in ['yes', 'y']:
                        print("\n💡 Tip: You can be more specific by mentioning:")
                        print("   - Specific genre or mood")
                        print("   - Energy level (e.g., \"high energy\" or \"low energy\")")
                        print("   - Activity (e.g., \"studying\", \"working out\")")
                        print("   - Acoustic preference (e.g., \"acoustic\" or \"electronic\")")
                        print()
                else:
                    # Display error or clarification
                    print(f"\n⚠️  {explanation_or_error}")
                    
                    # Show available options if it was an extraction error
                    if explanation_or_error and "couldn't understand" in explanation_or_error.lower():
                        print("\n💡 Type 'options' to see available genres and moods.")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                self.logger.log_conversation_end()
                break
            except Exception as e:
                error = self.error_handler.handle_unknown_error(e)
                print(f"\n❌ {error.user_message}")
                self.logger.log_error("UnexpectedError", str(e))


def main():
    """Main entry point for the RAG music recommender."""
    try:
        recommender = RAGMusicRecommender()
        recommender.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
