#!/usr/bin/env python
"""Comprehensive API test with new key"""
import asyncio
from google import genai
from google.genai import types
import sys

api_key = "AIzaSyBY3hgYVQsuko7xcBZOhlSCvw1KIxhvdH4"

async def test_chat():
    """Test Gemini chat model"""
    print("\n🧪 Testing Gemini Chat Model...")
    try:
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model='models/gemini-2.5-flash-lite-preview-09-2025',
            contents='Say "API works!" in exactly 2 words'
        )
        print(f"✅ Chat model SUCCESS: {response.text.strip()}")
        return True
    except Exception as e:
        print(f"❌ Chat model FAILED: {e}")
        return False

async def test_image():
    """Test image generation"""
    print("\n🧪 Testing Image Generation (Nano Banana)...")
    try:
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model='models/gemini-2.5-flash-image',
            contents=['A simple red circle on white background'],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                ),
            ),
        )
        
        # Check if image was generated
        image_found = False
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_found = True
                break
        
        if image_found:
            print(f"✅ Image generation SUCCESS: Image created")
            return True
        else:
            print(f"❌ Image generation FAILED: No image in response")
            return False
    except Exception as e:
        print(f"❌ Image generation FAILED: {e}")
        return False

async def main():
    print("="*70)
    print("🔬 ViMax Comprehensive API Test")
    print("="*70)
    
    chat_ok = await test_chat()
    image_ok = await test_image()
    
    print("\n" + "="*70)
    print("📊 Final Test Results:")
    print("="*70)
    print(f"  ✓ Chat Model (Gemini): {'✅ WORKING' if chat_ok else '❌ FAILED'}")
    print(f"  ✓ Image Generator:     {'✅ WORKING' if image_ok else '❌ FAILED'}")
    print("="*70)
    
    if chat_ok and image_ok:
        print("\n🎉 SUCCESS! All APIs are working correctly!")
        print("📝 Note: Video generation (Veo) will be tested during actual video creation")
        print("\n✅ You can now run:")
        print("   cd /app && source .venv/bin/activate && python main_idea2video.py")
        print("   cd /app && source .venv/bin/activate && python main_script2video.py")
        return 0
    else:
        print("\n⚠️ Some APIs failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
