"""
Logging system for RAG-Enhanced Music Recommender.

Provides comprehensive logging for debugging and monitoring.
"""

import logging
import os
from datetime import datetime
from typing import Optional


class MusicRecommenderLogger:
    """
    Centralized logging system for the music recommender.
    
    Creates separate log files for different types of events:
    - rag_system.log: General system operations
    - api_calls.log: API interactions with Gemma
    - errors.log: Error and exception details
    """
    
    def __init__(self, log_dir: str = "logs", log_level: str = "INFO"):
        """
        Initialize the logging system.
        
        Args:
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.log_dir = log_dir
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Initialize loggers
        self.system_logger = self._setup_logger(
            'system', 
            os.path.join(log_dir, 'rag_system.log')
        )
        self.api_logger = self._setup_logger(
            'api', 
            os.path.join(log_dir, 'api_calls.log')
        )
        self.error_logger = self._setup_logger(
            'error', 
            os.path.join(log_dir, 'errors.log')
        )
        
        self.system_logger.info("Logging system initialized")
    
    def _setup_logger(self, name: str, log_file: str) -> logging.Logger:
        """
        Set up a logger with file handler.
        
        Args:
            name: Logger name
            log_file: Path to log file
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)
        
        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(self.log_level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console
        
        # Formatter
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_user_query(self, query: str) -> None:
        """
        Log a user query.
        
        Args:
            query: The user's query string
        """
        self.system_logger.info(f"User query: {query}")
    
    def log_preference_extraction(self, query: str, preferences: dict, confidence: float = 0.0) -> None:
        """
        Log preference extraction results.
        
        Args:
            query: The original query
            preferences: Extracted preferences dictionary
            confidence: Confidence score (0.0-1.0)
        """
        self.system_logger.info(
            f"Preference extraction - Query: '{query}' | "
            f"Preferences: {preferences} | Confidence: {confidence:.2f}"
        )
    
    def log_api_call(self, endpoint: str, prompt_length: int, response_length: int, 
                    success: bool, error: Optional[str] = None) -> None:
        """
        Log an API call to Gemma.
        
        Args:
            endpoint: API endpoint or method name
            prompt_length: Length of the prompt in characters
            response_length: Length of the response in characters
            success: Whether the call was successful
            error: Error message if failed
        """
        if success:
            self.api_logger.info(
                f"API call - Method: {endpoint} | "
                f"Prompt: {prompt_length} chars | Response: {response_length} chars | Success"
            )
        else:
            self.api_logger.error(
                f"API call - Method: {endpoint} | Error: {error}"
            )
    
    def log_recommendation(self, query: str, num_songs: int, avg_score: float) -> None:
        """
        Log recommendation generation.
        
        Args:
            query: The user's query
            num_songs: Number of songs recommended
            avg_score: Average score of recommendations
        """
        self.system_logger.info(
            f"Recommendation - Query: '{query}' | "
            f"Songs: {num_songs} | Avg Score: {avg_score:.3f}"
        )
    
    def log_error(self, error_type: str, error_message: str, context: Optional[str] = None) -> None:
        """
        Log an error.
        
        Args:
            error_type: Type of error (e.g., APIError, ExtractionError)
            error_message: Error message
            context: Additional context about the error
        """
        log_msg = f"{error_type}: {error_message}"
        if context:
            log_msg += f" | Context: {context}"
        
        self.error_logger.error(log_msg)
        self.system_logger.error(log_msg)
    
    def log_warning(self, warning_message: str) -> None:
        """
        Log a warning.
        
        Args:
            warning_message: Warning message
        """
        self.system_logger.warning(warning_message)
    
    def log_debug(self, debug_message: str) -> None:
        """
        Log a debug message.
        
        Args:
            debug_message: Debug message
        """
        self.system_logger.debug(debug_message)
    
    def log_info(self, info_message: str) -> None:
        """
        Log an info message.
        
        Args:
            info_message: Info message
        """
        self.system_logger.info(info_message)
    
    def log_conversation_start(self) -> None:
        """Log the start of a conversation session."""
        self.system_logger.info("=" * 50)
        self.system_logger.info("New conversation session started")
        self.system_logger.info(f"Timestamp: {datetime.now().isoformat()}")
        self.system_logger.info("=" * 50)
    
    def log_conversation_end(self) -> None:
        """Log the end of a conversation session."""
        self.system_logger.info("=" * 50)
        self.system_logger.info("Conversation session ended")
        self.system_logger.info(f"Timestamp: {datetime.now().isoformat()}")
        self.system_logger.info("=" * 50)


# Global logger instance
_logger: Optional[MusicRecommenderLogger] = None


def get_logger(log_dir: str = "logs", log_level: str = "INFO") -> MusicRecommenderLogger:
    """
    Get or create the global logger instance.
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level
        
    Returns:
        MusicRecommenderLogger instance
    """
    global _logger
    if _logger is None:
        _logger = MusicRecommenderLogger(log_dir, log_level)
    return _logger
