from fastapi import APIRouter, HTTPException, Request
import httpx
import base64
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create router
router = APIRouter()

# Get FHIR server URL from environment variable or use default
FHIR_SERVER_URL = "http://127.0.0.1:8080/csp/healthshare/demo/fhir/r4"

@router.post("/new")
async def create_patient(request: Request):
    try:
        # Get the request body
        patient_data = await request.json()
        
        # Print the request body
        print("Request body:")
        print(json.dumps(patient_data, indent=2))
        
        # Create Basic Auth header
        auth_str = "_SYSTEM:ISCDEMO"
        auth_bytes = auth_str.encode('ascii')
        base64_bytes = base64.b64encode(auth_bytes)
        auth_header = f"Basic {base64_bytes.decode('ascii')}"
        
        # Set up headers for the FHIR server request
        headers = {
            "Content-Type": "application/fhir+json",
        }
        
        # Print the FHIR server URL being used
        fhir_endpoint = f"{FHIR_SERVER_URL}/Patient"
        print(f"Connecting to FHIR server at: {fhir_endpoint}")
        
        # Forward the request to the FHIR server
        try:
            async with httpx.AsyncClient() as client:
                fhir_response = await client.post(
                    FHIR_SERVER_URL,
                    headers=headers,
                    json=patient_data,
                    timeout=30.0
                )
                
                # Try to get JSON response, fall back to text if not JSON
                try:
                    response_data = fhir_response.json()
                    # Print the response data
                    print("Response data:")
                    print(json.dumps(response_data, indent=2))
                except json.JSONDecodeError:
                    response_data = {"text": fhir_response.text}
                    # Print the text response
                    print("Response text:")
                    print(fhir_response.text)
                
                # If the FHIR server returned an error, raise an HTTPException
                if fhir_response.status_code >= 400:
                    error_message = response_data.get("issue", [{}])[0].get("diagnostics", "Unknown error")
                    raise HTTPException(
                        status_code=fhir_response.status_code,
                        detail=error_message or f"FHIR server returned {fhir_response.status_code}"
                    )
                
                # Return the FHIR server's response
                return response_data
        except httpx.ConnectError as e:
            print(f"Connection error: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"Could not connect to FHIR server at {fhir_endpoint}. Make sure the FHIR server is running and accessible."
            )
            
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log and wrap other exceptions
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")