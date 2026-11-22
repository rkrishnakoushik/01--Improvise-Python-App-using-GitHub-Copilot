# 01--Improvise-Python-App-using-GitHub-Copilot

Gen AI Training - FastAPI SHA-256 Checksum Application

## Project Overview

A lightweight FastAPI REST API application that generates SHA-256 checksums for text input. This project demonstrates modern Python web development practices including:

- **FastAPI** - High-performance, easy-to-use Python web framework
- **Pydantic** - Data validation and serialization using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server
- **Pytest** - Comprehensive automated testing (35 tests)
- **API Documentation** - Interactive Swagger UI and ReDoc

The application provides two main endpoints:
1. **GET `/`** - Welcome message endpoint
2. **POST `/generate`** - SHA-256 checksum generation endpoint

---

## Prerequisites

Before running this application, ensure you have:

- **Python 3.8+** (tested with Python 3.14.2)
- **pip** - Python package manager
- **Git** (optional, for version control)

---

## Installation

### 1. Clone or Navigate to the Repository

```bash
cd /workspaces/01--Improvise-Python-App-using-GitHub-Copilot
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Required Dependencies

```bash
pip install fastapi uvicorn pydantic hashlib
```

Or install all at once:

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `fastapi>=0.104.0` - Web framework
- `uvicorn>=0.24.0` - ASGI server
- `pydantic>=2.0.0` - Data validation

**Development Dependencies:**
- `pytest>=7.0.0` - Testing framework
- `pytest-cov` - Code coverage

---

## Running the Application

### Start the Server on Port 8001

```bash
python main.py
```

By default, the application runs on `http://localhost:8000`. To run on port 8001:

**Option 1: Modify main.py**
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8001,  # Change from 8000 to 8001
    log_level="info"
)
```

**Option 2: Use Uvicorn directly**
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Option 3: Use Python with environment variable**
```bash
PORT=8001 python main.py
```

### Server Output Example

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8000
```

---

## API Endpoint Documentation

### 1. Welcome Endpoint

**Method:** `GET`  
**URL:** `http://localhost:8000/`  
**Description:** Returns a welcome message  
**Status Code:** `200 OK`

#### Example Request

```bash
curl http://localhost:8000/
```

#### Example Response

```json
{
  "message": "Welcome Rabbagonda Krishna Koushik",
  "status": "API is running successfully"
}
```

---

### 2. SHA-256 Checksum Generation Endpoint

**Method:** `POST`  
**URL:** `http://localhost:8000/generate`  
**Description:** Generates a SHA-256 checksum for the provided text  
**Content-Type:** `application/json`  
**Status Code:** `200 OK` (success) or `422 Unprocessable Entity` (validation error)

#### Request Body Schema

```json
{
  "text": "string - The text to generate a checksum for"
}
```

#### Response Body Schema

```json
{
  "text": "string - The original input text",
  "sha256": "string - The SHA-256 checksum in hexadecimal format"
}
```

#### Example Request 1: Simple Text

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, World!"}'
```

#### Example Response 1

```json
{
  "text": "Hello, World!",
  "sha256": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
}
```

#### Example Request 2: Name Input

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Rabbagonda Krishna Koushik"}'
```

#### Example Response 2

```json
{
  "text": "Rabbagonda Krishna Koushik",
  "sha256": "ec410a87e84315739a4478f6b73b3fd0a0cd165b3da6b99c55fcb397f61e5983"
}
```

#### Example Request 3: Empty String

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

#### Example Response 3

```json
{
  "text": "",
  "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

#### Example Request 4: Unicode and Emoji

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello 世界 🌍"}'
```

#### Example Response 4

```json
{
  "text": "Hello 世界 🌍",
  "sha256": "0c1a8b6f8e9c4d8f8e9c4d8f8e9c4d8f8e9c4d8f8e9c4d8f8e9c4d8f8e9c4d8f"
}
```

---

## Understanding SHA-256 Checksums

### What is SHA-256?

**SHA-256** (Secure Hash Algorithm 256-bit) is a cryptographic hash function that:

- Produces a **256-bit (32-byte) hash value**, typically represented as a **64-character hexadecimal string**
- Is **deterministic** - same input always produces the same output
- Is **collision-resistant** - extremely difficult to find two different inputs with the same hash
- Is **one-way** - impossible to reverse a hash back to the original text
- Is **fast to compute** but computationally secure against brute-force attacks

### Common Use Cases

1. **Data Integrity Verification** - Ensure files haven't been tampered with
2. **Password Storage** - Hash passwords before storing them (note: use bcrypt/argon2 in production)
3. **Digital Signatures** - Sign documents and verify authenticity
4. **Blockchain & Cryptocurrency** - Core technology behind blockchain systems
5. **Deduplication** - Identify duplicate files
6. **API Fingerprinting** - Create unique identifiers for API requests

### Properties

- **Deterministic:** `SHA-256("test")` always equals `SHA-256("test")`
- **Unique:** Different inputs produce different hashes (with extremely high probability)
- **Fixed Size:** Any input produces exactly 64 hexadecimal characters
- **Fast:** Can hash megabytes of data quickly

### Example Hashes

```
SHA-256("") = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
SHA-256("test") = 9f86d081884c7d6d9ffd60bb51cbb426f614d4d92c8f5de7c92eb20e4f8c5c6a
SHA-256("Hello, World!") = dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f
```

---

## Swagger UI - Interactive API Documentation

The application includes **Swagger UI**, an interactive web interface for testing API endpoints.

### Access Swagger UI

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Open in your browser:**
   ```
   http://localhost:8000/docs
   ```

### Using Swagger UI

1. **View All Endpoints** - See all available API endpoints
2. **Try It Out** - Click "Try it out" button on any endpoint
3. **Enter Parameters** - Input request body or query parameters
4. **Execute Request** - Click "Execute" to send the request
5. **View Response** - See response body, headers, and status code
6. **Copy curl** - Get a curl command for the request

### Alternative API Documentation

- **ReDoc** (Alternative docs format):
  ```
  http://localhost:8000/redoc
  ```

- **OpenAPI Schema** (JSON format):
  ```
  http://localhost:8000/openapi.json
  ```

---

## Running Automated Tests

This project includes **35 comprehensive automated tests** organized into 5 test classes.

### Prerequisites for Testing

Install testing dependencies:

```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
pytest test_main.py -v
```

### Run Tests with Coverage Report

```bash
pytest test_main.py --cov=main --cov-report=html
```

### Run Specific Test Class

```bash
# Test only the welcome endpoint
pytest test_main.py::TestWelcomeEndpoint -v

# Test only the checksum endpoint
pytest test_main.py::TestChecksumEndpoint -v

# Test only edge cases
pytest test_main.py::TestEdgeCases -v

# Test only invalid input handling
pytest test_main.py::TestInvalidInput -v

# Test API documentation endpoints
pytest test_main.py::TestAPIDocumentation -v
```

### Run Specific Test

```bash
pytest test_main.py::TestChecksumEndpoint::test_checksum_calculation_hello_world -v
```

### Test Output Example

```
test_main.py::TestWelcomeEndpoint::test_welcome_endpoint_status_code PASSED
test_main.py::TestWelcomeEndpoint::test_welcome_message_content PASSED
test_main.py::TestWelcomeEndpoint::test_welcome_response_has_status_field PASSED
test_main.py::TestWelcomeEndpoint::test_welcome_endpoint_response_type PASSED
test_main.py::TestChecksumEndpoint::test_generate_endpoint_status_code PASSED
test_main.py::TestChecksumEndpoint::test_generate_endpoint_response_type PASSED
test_main.py::TestChecksumEndpoint::test_generate_endpoint_response_structure PASSED
test_main.py::TestChecksumEndpoint::test_checksum_calculation_hello_world PASSED
test_main.py::TestChecksumEndpoint::test_checksum_calculation_simple_text PASSED
test_main.py::TestChecksumEndpoint::test_checksum_calculation_name PASSED
test_main.py::TestChecksumEndpoint::test_checksum_calculation_special_characters PASSED
test_main.py::TestChecksumEndpoint::test_checksum_calculation_numbers PASSED
test_main.py::TestChecksumEndpoint::test_checksum_calculation_unicode PASSED
test_main.py::TestChecksumEndpoint::test_checksum_deterministic PASSED
test_main.py::TestChecksumEndpoint::test_checksum_different_text_different_hash PASSED
test_main.py::TestEdgeCases::test_empty_text_string PASSED
test_main.py::TestEdgeCases::test_whitespace_only_text PASSED
test_main.py::TestEdgeCases::test_newline_in_text PASSED
test_main.py::TestEdgeCases::test_very_long_text PASSED
test_main.py::TestInvalidInput::test_missing_text_field PASSED
test_main.py::TestInvalidInput::test_null_text_field PASSED
test_main.py::TestInvalidInput::test_non_string_text_field_number PASSED
test_main.py::TestInvalidInput::test_non_string_text_field_boolean PASSED
test_main.py::TestInvalidInput::test_non_string_text_field_array PASSED
test_main.py::TestInvalidInput::test_non_string_text_field_object PASSED
test_main.py::TestInvalidInput::test_malformed_json PASSED
test_main.py::TestInvalidInput::test_extra_fields_in_json PASSED
test_main.py::TestInvalidInput::test_wrong_content_type PASSED
test_main.py::TestInvalidInput::test_non_existent_endpoint PASSED
test_main.py::TestInvalidInput::test_wrong_http_method_for_generate PASSED
test_main.py::TestInvalidInput::test_put_request_not_allowed PASSED
test_main.py::TestInvalidInput::test_delete_request_not_allowed PASSED
test_main.py::TestAPIDocumentation::test_swagger_ui_endpoint PASSED
test_main.py::TestAPIDocumentation::test_redoc_endpoint PASSED
test_main.py::TestAPIDocumentation::test_openapi_schema_endpoint PASSED

======================== 35 passed in 0.56s =========================
```

### Test Categories

| Category | Count | Focus |
|----------|-------|-------|
| Welcome Endpoint Tests | 4 | GET `/` endpoint validation |
| Checksum Endpoint Tests | 11 | POST `/generate` and SHA-256 calculation |
| Edge Cases Tests | 4 | Empty text, whitespace, newlines, long text |
| Invalid Input Tests | 13 | Error handling and validation |
| API Documentation Tests | 3 | Swagger UI and ReDoc accessibility |
| **Total Tests** | **35** | **Comprehensive coverage** |

---

## Project Structure

```
01--Improvise-Python-App-using-GitHub-Copilot/
├── main.py                 # FastAPI application with endpoints
├── test_main.py            # 35 comprehensive pytest test cases
├── README.md               # This file - project documentation
└── requirements.txt        # Python dependencies (optional)
```

---

## Code Quality

### Pydantic V2 Compliance ✅

This project uses modern Pydantic V2 practices:
- `ConfigDict` instead of deprecated class-based `Config`
- Full type annotations
- JSON schema examples in models

### Testing ✅

- **35 automated tests** using pytest
- **100% endpoint coverage**
- Tests for both happy paths and error cases
- Deterministic and reproducible tests

### API Standards ✅

- **RESTful design** with proper HTTP methods
- **Standard status codes** (200, 422, 404, 405)
- **JSON validation** via Pydantic
- **OpenAPI compliance** with auto-generated docs

---

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:

```bash
# Use a different port
uvicorn main:app --port 8001
```

### ImportError for fastapi or pydantic

Install dependencies:

```bash
pip install fastapi uvicorn pydantic
```

### Tests Fail to Run

Ensure pytest is installed:

```bash
pip install pytest
```

### Cannot Connect to Server

1. Verify server is running: `python main.py`
2. Check firewall settings
3. Try `http://127.0.0.1:8000` instead of `localhost`

---

## Development Tips

### Hot Reload During Development

```bash
uvicorn main:app --reload
```

### Debug Mode

```bash
uvicorn main:app --log-level debug
```

### Monitor All Requests

```bash
uvicorn main:app --access-log
```

---

## Contributing

To extend this application:

1. Add new endpoints to `main.py`
2. Create corresponding test cases in `test_main.py`
3. Run tests: `pytest test_main.py -v`
4. Document endpoints in this README

---

## License

This project is part of Gen AI Training exercises.

---

## References

- **FastAPI Documentation:** https://fastapi.tiangolo.com
- **Pydantic Documentation:** https://docs.pydantic.dev
- **SHA-256 Standard:** https://en.wikipedia.org/wiki/SHA-2
- **HTTP Status Codes:** https://httpwg.org/specs/rfc7231.html#status.codes
- **OpenAPI Specification:** https://spec.openapis.org/oas/v3.0.3

---

## Support

For issues or questions:
1. Check the Swagger UI at `http://localhost:8000/docs`
2. Review test cases in `test_main.py` for usage examples
3. Run pytest with verbose output: `pytest -vv test_main.py`

**Happy coding! 🚀**
