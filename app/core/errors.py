# Built in modules
from typing import Union
from functools import wraps


# Logger
from app.logger import logger

# FastAPI HTTP Exception
from fastapi import HTTPException


class TranscriptFetchError(Exception):
    """Custom exception raised when fetching transcripts fails."""
    pass


class TranscriptProcessingError(Exception):
    """Custom exception raised when processing transcripts fails."""
    pass


class TranscriptValidationError(Exception):
    """Custom exception raised when validating transcripts fails."""
    pass


class InvalidLinkError(Exception):
    """Custom exception raised when a provided link is invalid."""
    pass


class LLMInteractionError(Exception):
    """Custom exception raised when an LLM interaction fails."""
    pass


# Utility to map exceptions to HTTP responses
def handle_exceptions(exc: Exception) -> Union[HTTPException, None]:
    """Maps exceptions to appropriate HTTP responses."""
    if isinstance(exc, InvalidLinkError):
        logger.error(f"Invalid link: {str(exc)}")
        return HTTPException(status_code=400, detail=str(exc))

    elif isinstance(exc, TranscriptFetchError):
        logger.error(f"Error fetching transcript: {str(exc)}")
        return HTTPException(status_code=502, detail=str(exc))

    elif isinstance(exc, TranscriptProcessingError):
        logger.error(f"Error processing transcript: {str(exc)}")
        return HTTPException(status_code=500, detail=f"Transcript processing failed: {str(exc)}")

    elif isinstance(exc, TranscriptValidationError):
        logger.error(f"Error validating transcript: {str(exc)}")
        return HTTPException(status_code=500, detail=f"Transcript validation failed: {str(exc)}")

    else:
        logger.error(f"Unexpected error: {str(exc)}")
        return HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(exc)}")



def exception_handler(func):
    """Decorator to handle exceptions for FastAPI routes."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # Execute the wrapped function
            return await func(*args, **kwargs)
        except Exception as e:
            # Handle the exception and map to an HTTP response
            http_exception = handle_exceptions(e)
            if http_exception:
                raise http_exception
            raise  # In case there's an unexpected issue with error mapping
    return wrapper