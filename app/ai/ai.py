# Built in modules
from typing import List, Dict, Optional
from typing import List, Dict
import json

# Base LLM
from app.core.config import LLM_4o

# Logger
from app.logger import logger

# Errors
from app.core.errors import LLMInteractionError, TranscriptProcessingError, TranscriptValidationError

# Utils
from app.utils import format_transcript, format_analyst_output

# Prompts
from app.ai.prompts import AnalysisOutput, TRANSCRIPT_PROMPT_TEMPLATE, VALIDATION_PROMPT_TEMPLATE


# -----------------------------------------------------------------------------
# LLM Call
# -----------------------------------------------------------------------------


def call_llm(messages: str, output_cls: type) -> Dict:
    """Handles interaction with LLM and returns the parsed content as a dictionary."""
    try:
        # Turn into structured outputs LLM for validation
        sllm = LLM_4o.as_structured_llm(output_cls=output_cls)
        # Call Chat functionality
        output = sllm.chat(messages=messages)

        # Parse content into dict
        return json.loads(output.message.content)
    except Exception as e:
        logger.error(f"Error during LLM interaction: {e}")
        raise LLMInteractionError(f"Failed to interact with LLM: {str(e)}")

# -----------------------------------------------------------------------------
# Transcript processing
# -----------------------------------------------------------------------------


def process_transcript(raw_transcript: List[Dict]) -> Dict:
    """Processes a raw transcript and returns the structured LLM output as a dictionary."""
    try:
        # Format messages using the transcript analyst template
        formatted_transcript = format_transcript(raw_transcript)
        messages = TRANSCRIPT_PROMPT_TEMPLATE.format_messages(formatted_transcript_str=formatted_transcript)

        # Get the initial analyst output
        logger.info("Transcript processing started")
        processed_transcript = call_llm(messages, AnalysisOutput)
        logger.info(f"Transcript processing (phase one) completed: {processed_transcript}")
        return processed_transcript
    except LLMInteractionError as e:
        logger.error(f"Error in LLM interaction during transcript processing: {e}")
        raise TranscriptProcessingError(f"Error in transcript processing: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during transcript processing: {e}")
        raise TranscriptProcessingError(f"Unexpected error: {str(e)}")

# -----------------------------------------------------------------------------
# Validation of analyst output
# -----------------------------------------------------------------------------


def validate_transcript(raw_analyst_output: Dict) -> Dict:
    """Validates the analyst output using the structured LLM."""
    try:
        # Format messages using the validation template
        formatted_output = format_analyst_output(raw_analyst_output)
        messages = VALIDATION_PROMPT_TEMPLATE.format_messages(formatted_analyst_str=formatted_output)

        # Get the validation output
        logger.info("Validating transcript")
    
        validated_output = call_llm(messages, AnalysisOutput)
        logger.info(f"Transcript validation (phase two) completed: {validated_output}")
        return validated_output
    except LLMInteractionError as e:
        logger.error(f"Error in LLM interaction during validation: {e}")
        raise TranscriptValidationError(f"Error in validation: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during validation: {e}")
        raise TranscriptValidationError(f"Unexpected error: {str(e)}")
