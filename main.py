"""
FastAPI Application for SHA-256 Checksum Generation
This module provides a simple REST API for generating SHA-256 checksums of text input.

This application demonstrates:
- FastAPI framework for building high-performance REST APIs
- Pydantic for data validation and serialization
- Uvicorn ASGI server for serving the application
- Automatic API documentation with Swagger UI and ReDoc
- Cryptographic hashing with SHA-256
"""

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
import hashlib

# Initialize FastAPI application with comprehensive metadata for API documentation
app = FastAPI(
    title="Text Checksum API",
    description="A simple API to generate SHA-256 checksums for text input",
    version="1.0.0"
)


# Pydantic model for validating incoming POST request data
# Using ConfigDict (Pydantic V2) for model configuration - modern approach
class TextInput(BaseModel):
    """
    Pydantic model for text input validation.
    
    This model enforces that incoming requests must contain a 'text' field
    of type string. Any other format or missing field will trigger a 422
    Unprocessable Entity response with detailed validation errors.
    
    Attributes:
        text (str): The text string for which to generate a SHA-256 checksum
    
    Example:
        {"text": "Hello, World!"}
    """
    text: str
    
    # ConfigDict provides schema documentation and validation hints
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"text": "Hello, World!"}
        }
    )


class ChecksumResponse(BaseModel):
    """
    Pydantic model for checksum endpoint response validation.
    
    This model ensures all responses from /generate endpoint have exactly
    these two fields with the specified types. FastAPI automatically uses
    this model to validate the response before sending it to the client.
    
    Attributes:
        text (str): The original input text that was hashed
        sha256 (str): The SHA-256 checksum in hexadecimal format (64 characters)
    
    Example:
        {
            "text": "Hello, World!",
            "sha256": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
        }
    """
    text: str
    sha256: str
    
    # ConfigDict provides schema documentation and validation hints
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Hello, World!",
                "sha256": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
            }
        }
    )


@app.get(
    "/",
    summary="Welcome Endpoint",
    description="Returns a welcome message"
)
def read_root():
    """
    GET endpoint that returns a welcome message.
    
    This is the root endpoint of the API. It demonstrates a simple GET request
    and returns a JSON response with a greeting message and API status.
    
    Returns:
        dict: A dictionary containing:
            - message (str): Welcome message with user name
            - status (str): Current API status
    
    Example:
        GET http://localhost:8000/
        
        Response:
            {
                "message": "Welcome Rabbagonda Krishna Koushik",
                "status": "API is running successfully"
            }
    """
    return {
        "message": "Welcome Rabbagonda Krishna Koushik",
        "status": "API is running successfully"
    }


@app.post(
    "/generate",
    response_model=ChecksumResponse,
    summary="Generate SHA-256 Checksum",
    description="Generates a SHA-256 checksum for the provided text"
)
def generate_checksum(text_input: TextInput):
    """
    POST endpoint that generates a SHA-256 checksum for the input text.
    
    This endpoint accepts a JSON request containing a text field, computes the
    SHA-256 cryptographic hash of that text, and returns both the original text
    and its checksum in the response. The response model (ChecksumResponse) ensures
    consistent output format.
    
    Args:
        text_input (TextInput): A validated Pydantic model containing the text field.
                                If validation fails, FastAPI automatically returns
                                a 422 Unprocessable Entity response.
    
    Returns:
        ChecksumResponse: A response model containing:
            - text (str): The original input text
            - sha256 (str): The SHA-256 checksum in hexadecimal format
    
    Example:
        POST http://localhost:8000/generate
        Content-Type: application/json
        
        Request body:
            {
                "text": "Hello, World!"
            }
        
        Response:
            {
                "text": "Hello, World!",
                "sha256": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
            }
    
    Note:
        SHA-256 properties:
        - Deterministic: Same input always produces same hash
        - One-way: Impossible to reverse hash back to original text
        - Fixed size: Always produces 64 hexadecimal characters (256 bits)
        - Collision-resistant: Extremely difficult to find two inputs with same hash
    """
    # Encode the text string to bytes and generate SHA-256 checksum
    # The .hexdigest() method returns the hash as a hexadecimal string
    sha256_hash = hashlib.sha256(text_input.text.encode()).hexdigest()
    
    # Return ChecksumResponse model with validated structure
    # FastAPI will automatically serialize this to JSON and validate it matches
    # the response_model type annotation
    return ChecksumResponse(
        text=text_input.text,
        sha256=sha256_hash
    )


# Entry point for running the application
# This block executes only when the script is run directly (not when imported)
if __name__ == "__main__":
    import uvicorn
    
    # Run the FastAPI application with Uvicorn ASGI server
    # Configuration:
    # - host="0.0.0.0": Accept connections from any network interface
    # - port=8000: Listen on port 8000 (HTTP)
    # - log_level="info": Show INFO level logs and above
    # 
    # To run on a different port, modify: port=8001
    # To enable auto-reload during development, add: reload=True
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
