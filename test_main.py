"""
Test suite for FastAPI Checksum Application
Tests the welcome endpoint, checksum generation, and error handling.
"""

import pytest
import hashlib
from fastapi.testclient import TestClient
from main import app


# Initialize TestClient for testing
client = TestClient(app)


class TestWelcomeEndpoint:
    """Test cases for the GET / welcome endpoint"""
    
    def test_welcome_endpoint_status_code(self):
        """Test that the welcome endpoint returns status code 200"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_welcome_message_content(self):
        """Test that the welcome endpoint returns the correct message"""
        response = client.get("/")
        data = response.json()
        assert data["message"] == "Welcome Rabbagonda Krishna Koushik"
    
    def test_welcome_response_has_status_field(self):
        """Test that the welcome response includes the status field"""
        response = client.get("/")
        data = response.json()
        assert "status" in data
        assert data["status"] == "API is running successfully"
    
    def test_welcome_endpoint_response_type(self):
        """Test that the welcome endpoint returns JSON"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"


class TestChecksumEndpoint:
    """Test cases for the POST /generate checksum endpoint"""
    
    def test_generate_endpoint_status_code(self):
        """Test that the generate endpoint returns status code 200 on success"""
        response = client.post("/generate", json={"text": "Hello"})
        assert response.status_code == 200
    
    def test_generate_endpoint_response_type(self):
        """Test that the generate endpoint returns JSON"""
        response = client.post("/generate", json={"text": "test"})
        assert response.headers["content-type"] == "application/json"
    
    def test_generate_endpoint_response_structure(self):
        """Test that the response has the correct structure"""
        response = client.post("/generate", json={"text": "Hello"})
        data = response.json()
        assert "text" in data
        assert "sha256" in data
    
    def test_checksum_calculation_hello_world(self):
        """Test SHA-256 checksum calculation for 'Hello, World!'"""
        text = "Hello, World!"
        expected_hash = hashlib.sha256(text.encode()).hexdigest()
        
        response = client.post("/generate", json={"text": text})
        data = response.json()
        
        assert data["sha256"] == expected_hash
        assert data["text"] == text
    
    def test_checksum_calculation_simple_text(self):
        """Test SHA-256 checksum calculation for simple text"""
        text = "test"
        expected_hash = hashlib.sha256(text.encode()).hexdigest()
        
        response = client.post("/generate", json={"text": text})
        data = response.json()
        
        assert data["sha256"] == expected_hash
    
    def test_checksum_calculation_name(self):
        """Test SHA-256 checksum calculation for a name"""
        text = "Rabbagonda Krishna Koushik"
        expected_hash = hashlib.sha256(text.encode()).hexdigest()
        
        response = client.post("/generate", json={"text": text})
        data = response.json()
        
        assert data["sha256"] == expected_hash
        assert data["text"] == text
    
    def test_checksum_calculation_special_characters(self):
        """Test SHA-256 checksum calculation with special characters"""
        text = "Hello! @#$%^&*()_+-=[]{}|;:',.<>?"
        expected_hash = hashlib.sha256(text.encode()).hexdigest()
        
        response = client.post("/generate", json={"text": text})
        data = response.json()
        
        assert data["sha256"] == expected_hash
    
    def test_checksum_calculation_numbers(self):
        """Test SHA-256 checksum calculation with numbers"""
        text = "1234567890"
        expected_hash = hashlib.sha256(text.encode()).hexdigest()
        
        response = client.post("/generate", json={"text": text})
        data = response.json()
        
        assert data["sha256"] == expected_hash
    
    def test_checksum_calculation_unicode(self):
        """Test SHA-256 checksum calculation with Unicode characters"""
        text = "Hello 世界 🌍"
        expected_hash = hashlib.sha256(text.encode()).hexdigest()
        
        response = client.post("/generate", json={"text": text})
        data = response.json()
        
        assert data["sha256"] == expected_hash
    
    def test_checksum_deterministic(self):
        """Test that the same text always produces the same checksum"""
        text = "consistent test"
        
        response1 = client.post("/generate", json={"text": text})
        response2 = client.post("/generate", json={"text": text})
        
        assert response1.json()["sha256"] == response2.json()["sha256"]
    
    def test_checksum_different_text_different_hash(self):
        """Test that different texts produce different checksums"""
        response1 = client.post("/generate", json={"text": "text1"})
        response2 = client.post("/generate", json={"text": "text2"})
        
        assert response1.json()["sha256"] != response2.json()["sha256"]


class TestEdgeCases:
    """Test cases for edge cases and error handling"""
    
    def test_empty_text_string(self):
        """Test that empty text string is handled"""
        response = client.post("/generate", json={"text": ""})
        assert response.status_code == 200
        data = response.json()
        # Empty string SHA-256
        expected_hash = hashlib.sha256("".encode()).hexdigest()
        assert data["sha256"] == expected_hash
    
    def test_whitespace_only_text(self):
        """Test that whitespace-only text is handled"""
        text = "   "
        response = client.post("/generate", json={"text": text})
        assert response.status_code == 200
        data = response.json()
        expected_hash = hashlib.sha256(text.encode()).hexdigest()
        assert data["sha256"] == expected_hash
    
    def test_newline_in_text(self):
        """Test that text with newlines is handled"""
        text = "Hello\nWorld"
        response = client.post("/generate", json={"text": text})
        assert response.status_code == 200
        data = response.json()
        expected_hash = hashlib.sha256(text.encode()).hexdigest()
        assert data["sha256"] == expected_hash
    
    def test_very_long_text(self):
        """Test that very long text is handled"""
        text = "a" * 10000
        response = client.post("/generate", json={"text": text})
        assert response.status_code == 200
        data = response.json()
        expected_hash = hashlib.sha256(text.encode()).hexdigest()
        assert data["sha256"] == expected_hash


class TestInvalidInput:
    """Test cases for invalid input and error handling"""
    
    def test_missing_text_field(self):
        """Test that missing 'text' field returns 422 Unprocessable Entity"""
        response = client.post("/generate", json={})
        assert response.status_code == 422
    
    def test_null_text_field(self):
        """Test that null 'text' field returns 422 Unprocessable Entity"""
        response = client.post("/generate", json={"text": None})
        assert response.status_code == 422
    
    def test_non_string_text_field_number(self):
        """Test that non-string text field (number) returns 422"""
        response = client.post("/generate", json={"text": 12345})
        assert response.status_code == 422
    
    def test_non_string_text_field_boolean(self):
        """Test that non-string text field (boolean) returns 422"""
        response = client.post("/generate", json={"text": True})
        assert response.status_code == 422
    
    def test_non_string_text_field_array(self):
        """Test that non-string text field (array) returns 422"""
        response = client.post("/generate", json={"text": ["hello"]})
        assert response.status_code == 422
    
    def test_non_string_text_field_object(self):
        """Test that non-string text field (object) returns 422"""
        response = client.post("/generate", json={"text": {"nested": "value"}})
        assert response.status_code == 422
    
    def test_malformed_json(self):
        """Test that malformed JSON returns 422"""
        response = client.post(
            "/generate",
            json="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_extra_fields_in_json(self):
        """Test that extra fields in JSON are accepted but ignored"""
        response = client.post(
            "/generate",
            json={"text": "hello", "extra_field": "should be ignored"}
        )
        assert response.status_code == 200
        assert response.json()["text"] == "hello"
    
    def test_wrong_content_type(self):
        """Test request with plain text content type"""
        response = client.post(
            "/generate",
            json={"text": "hello"},
            headers={"Content-Type": "text/plain"}
        )
        # Content-Type override doesn't prevent JSON parsing by TestClient
        # This test verifies the endpoint handles mixed content-type gracefully
        assert response.status_code in [200, 422]
    
    def test_non_existent_endpoint(self):
        """Test that non-existent endpoint returns 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_wrong_http_method_for_generate(self):
        """Test that GET request to /generate returns 405 Method Not Allowed"""
        response = client.get("/generate")
        assert response.status_code == 405
    
    def test_put_request_not_allowed(self):
        """Test that PUT request is not allowed"""
        response = client.put("/generate", json={"text": "hello"})
        assert response.status_code == 405
    
    def test_delete_request_not_allowed(self):
        """Test that DELETE request is not allowed"""
        response = client.delete("/generate")
        assert response.status_code == 405


class TestAPIDocumentation:
    """Test cases for API documentation endpoints"""
    
    def test_swagger_ui_endpoint(self):
        """Test that Swagger UI is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()
    
    def test_redoc_endpoint(self):
        """Test that ReDoc is accessible"""
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_openapi_schema_endpoint(self):
        """Test that OpenAPI schema is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
