#!/usr/bin/env python
"""Test script to verify ViMax setup and API connectivity"""
import asyncio
from google import genai

async def test_google_api():
    """Test Google AI Studio API connection"""
    api_key = "AIzaSyCXzRsi1wZNixLZDdzM7We3gZqlhoP3bHc"
    
    try:
        client = genai.Client(api_key=api_key)
        print("✅ Google AI Studio client initialized successfully")
        
        # Test chat model (Gemini)
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash-lite-preview-09-2025',
            contents='Say "Hello from ViMax!" in one sentence'
        )
        print(f"✅ Chat model test: {response.text[:100]}")
        
        print("\n🎉 All API tests passed! ViMax is ready to use.")
        return True
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_google_api())
