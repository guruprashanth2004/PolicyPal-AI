#!/usr/bin/env python3
"""
Test script for the LLM-Powered Intelligent Query-Retrieval System
This script helps verify that the deployment is working correctly.
"""

import requests
import json
import sys
import time

# Configuration
BASE_URL = "http://localhost:8000/api/v1"  # Change this to your Render URL
API_TOKEN = "9834d259844d94cfbab31ff7181aa68a50717db4ea92cd1765fb58aabd68cc23"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    print("🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", headers=HEADERS)
        if response.status_code == 200:
            print("✅ Root endpoint passed!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Root endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {str(e)}")
        return False

def test_hackrx_test():
    """Test the hackrx test endpoint."""
    print("🔍 Testing hackrx test endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/hackrx/test", headers=HEADERS)
        if response.status_code == 200:
            print("✅ Hackrx test endpoint passed!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Hackrx test endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Hackrx test endpoint error: {str(e)}")
        return False

def test_main_query_endpoint():
    """Test the main query endpoint with a sample request."""
    print("🔍 Testing main query endpoint...")
    
    # Sample request data
    sample_request = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?"
        ]
    }
    
    try:
        print("   Sending request...")
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=HEADERS,
            json=sample_request,
            timeout=60  # 60 second timeout for processing
        )
        
        if response.status_code == 200:
            print("✅ Main query endpoint passed!")
            result = response.json()
            print(f"   Number of answers: {len(result.get('answers', []))}")
            for i, answer in enumerate(result.get('answers', [])):
                print(f"   Answer {i+1}: {answer[:100]}...")
            return True
        else:
            print(f"❌ Main query endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("❌ Main query endpoint timed out (60 seconds)")
        return False
    except Exception as e:
        print(f"❌ Main query endpoint error: {str(e)}")
        return False

def test_authentication():
    """Test authentication with invalid token."""
    print("🔍 Testing authentication...")
    try:
        # Test with invalid token
        invalid_headers = {
            "Authorization": "Bearer invalid_token",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{BASE_URL}/hackrx/test", headers=invalid_headers)
        if response.status_code == 401:
            print("✅ Authentication working correctly (rejected invalid token)")
            return True
        else:
            print(f"❌ Authentication test failed - expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Authentication test error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting deployment tests...")
    print(f"📍 Testing against: {BASE_URL}")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Authentication", test_authentication),
        ("Hackrx Test", test_hackrx_test),
        ("Main Query", test_main_query_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        if test_func():
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Deployment is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the deployment.")
        return 1

if __name__ == "__main__":
    # Allow custom base URL
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
        print(f"Using custom base URL: {BASE_URL}")
    
    exit_code = main()
    sys.exit(exit_code) 