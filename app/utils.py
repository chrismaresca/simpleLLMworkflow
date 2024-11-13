# Built in modules
import os
import requests
import json
import re
from typing import Tuple, List, Dict
from uuid import uuid4
from json import JSONDecodeError

# Logger
from app.logger import logger, LoggerSingleton


# Request Exceptions
from requests.exceptions import Timeout, HTTPError


# Custom modules
from app.core.config import BASE_URL_TEMPLATE, TRANSCRIPT_FILE_PATH
from app.core.errors import InvalidLinkError, TranscriptFetchError, TranscriptProcessingError

# -----------------------------------------------------------------------------
# Logger Utilities
# -----------------------------------------------------------------------------


def clean_up_logger() -> None:
    """Cleans up the logger when the application shuts down."""
    log_file = LoggerSingleton.get_log_file_path()

    
    if os.path.exists(log_file) and os.path.getsize(log_file) == 0:
        os.remove(log_file)
    else:
        logger.info("Application shutting down...")


# -----------------------------------------------------------------------------
# File Utilities
# -----------------------------------------------------------------------------

def ensure_directory_exists(directory: str) -> None:
    """Ensures that the directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_file_path(base_directory: str, filename: str, extension: str = "json") -> str:
    """Returns the full file path, ensuring the directory exists."""
    ensure_directory_exists(base_directory)
    return f"{os.path.join(base_directory, filename)}.{extension}"


def save_transcript_to_file(meeting_transcript: list, file_subpath: str) -> None:
    """Saves the meeting transcript to a JSON file."""
    file_path = get_file_path(f"{TRANSCRIPT_FILE_PATH}/{file_subpath}", "transcript")

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(meeting_transcript, f, ensure_ascii=False, indent=4)
        logger.info(f"Transcript saved successfully to {file_path}")

    except Exception as e:
        logger.warning(f"Failed to save meeting transcript to file: {e}")


def save_output_to_file(output: dict, file_subpath: str) -> None:
    """Saves the given output dictionary to a JSON file."""
    file_path = get_file_path(f"{TRANSCRIPT_FILE_PATH}/{file_subpath}", "output")

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
        logger.info(f"Output saved successfully to {file_path}")

    except Exception as e:
        logger.warning(f"Failed to save output to file: {e}")


# -----------------------------------------------------------------------------
# Fetch Utilities
# -----------------------------------------------------------------------------


def extract_id(link: str) -> str:
    """Extracts the meeting ID from a CircleBack meeting link."""
    pattern = r"circleback\.ai(?:/view)?/([a-zA-Z0-9]+)"
    match = re.search(pattern, link)

    if not match:
        raise InvalidLinkError("The provided link is invalid. Could not extract meeting ID.")

    return match.group(1)


def fetch_transcript(link: str) -> Tuple[str, List]:
    """
    Fetches and concatenates transcripts by unique segment ID across paginated API responses.
    Returns the meeting ID and transcripts as a list.
    """
    transcripts = []
    meeting_id = extract_id(link)

    try:
        base_url = BASE_URL_TEMPLATE.format(meeting_id=meeting_id)
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        meeting_id = data.get("meetingId", str(uuid4()))
        segments = data.get("segments", [])

        if not segments:
            raise TranscriptProcessingError("No segments found in the transcript data.")

        # Process each segment to collect unique segment data
        for segment in segments:
            speaker = segment.get("speaker", "Unknown")
            words = segment.get("words", [])
            spoken_text = " ".join([word.get('text', '') for word in words])

            # Store transcript by unique segment ID
            transcripts.append({
                "person": speaker,
                "said": spoken_text
            })

    except Timeout:
        raise TranscriptFetchError("The request timed out. Please try again later.")
    except HTTPError as e:
        raise TranscriptFetchError(f"HTTP error occurred: {e}")
    except JSONDecodeError:
        raise TranscriptProcessingError("Failed to parse the JSON response from the API.")
    except Exception as e:
        raise TranscriptFetchError(f"An error occurred while fetching transcripts: {e}")

    return str(meeting_id), transcripts


# -----------------------------------------------------------------------------
# Format Utilities
# -----------------------------------------------------------------------------


def format_transcript(raw_transcript: List) -> str:
    """Formats a transcript list of dictionaries into a readable string."""
    formatted_conversations = ""
    for entry in raw_transcript:
        formatted_conversations += f"Person: {entry['person']}\nSaid: {entry['said']}\n"
    return formatted_conversations


def format_analyst_output(data: Dict[str, Dict[str, List[str]]]) -> str:
    """Formats structured analyst output with bullet points into a complete string."""
    formatted_output = ""

    for section, content in data.items():
        # Capitalize the section titles and add a newline
        formatted_output += f"{section.replace('_', ' ').title()}:\n"

        # Iterate over the bullet points
        for bullet in content.get('bullet_points', []):
            formatted_output += f" - {bullet}\n"

        formatted_output += "\n"

    # Remove any trailing newlines
    return formatted_output.strip()
