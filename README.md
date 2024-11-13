## Project Overview
This project demonstrates a FastAPI-based solution combined with Jinja2 templates and LlamaIndex to transform discovery call recordings into structured outputs that can be directly used in a value pyramid slide.

The core idea behind this project is to create a flexible and scalable v1 solution that the ExampleCompany team can iterate on as they refine the approach. To support future enhancements, every run of the application is logged in the logs/ directory, and all inputs and outputs are stored in the meetings/ directory. This enables future iterations to leverage more advanced prompt engineering techniques, such as multi-shot learning across different meeting examples, thereby improving the LLM's ability to produce the precise language that the ExampleCompany team expects.

## Project Structure
The project follows a modular structure, with the core functionality organized within the app/ directory. Each subdirectory serves a distinct purpose:

### AI Module (app/ai/)
This module is responsible for all AI-related functionality:

- prompts.py: Contains the Pydantic base models used for structured outputs from OpenAI’s API.
- ai.py: Handles the functionality for invoking LLM (Large Language Model) calls and processing the returned results.

### API Module (app/api/)
This directory houses the main FastAPI application:

- main.py: The entry point for the FastAPI application, handling the primary API endpoints and lifespan events such as startup and shutdown.
- Health Checks: API health check routes are located here to ensure smooth operation.

### Core Module (app/core/)
The core directory contains essential configuration and utility files:

- config.py: Contains configuration data such as environment variables.
- errors.py: Defines a simple error-handling system using a decorator pattern for centralized exception management.
- models.py: Stores the API models that define the structure of incoming requests and outgoing responses.

### Utilities & Logging
- logger.py: Manages logging operations, ensuring that each run is logged and can be reviewed later for debugging or optimization.
- utils.py: Contains general-purpose utility functions that support the core functionality of the project.


## Templating Engine
Simple HTML templates for interacting with the application can be found in the templates/ directory. These are rendered using Jinja2, which FastAPI supports natively, providing a simple interface for running the application in a web environment.

## Logging & Storage
- Logs (logs/): Every run of the application is logged with the timestamp, which can help in debugging and performance tracking over time.
- Meetings (meetings/): Each meeting’s input and output data is stored here, allowing for easy reference and future refinement based on LLM-generated outputs.


## How To Run

### Prerequisites
- Docker and Docker Compose installed locally.
- OpenAI API key.

### Steps to Run

1. Create a .env file in the root directory of the project and define the following environment variable:

```zsh
OPENAI_API_KEY=your_openai_api_key
```

2. Build the Docker image:

```zsh
docker-compose build
```

3. Run the application:

```zsh
docker-compose run
```

Once the application is running, you can access it via the exposed port in your browser or use tools like curl or Postman to interact with the endpoints.