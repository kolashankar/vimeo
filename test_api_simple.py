#!/usr/bin/env python
"""Simple test to verify each API component"""
import asyncio
from google import genai
from google.genai import types
import sys

api_key = "AIzaSyCXzRsi1wZNixLZDdzM7We3gZqlhoP3bHc"

async def test_chat():
    """Test Gemini chat model"""
    print("\n🧪 Testing Gemini Chat Model...")
    try:
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model='models/gemini-2.5-flash-lite-preview-09-2025',
            contents='Say hello in one word'
        )
        print(f"✅ Chat model works: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Chat model failed: {e}")
        return False

async def test_image():
    """Test Nano Banana image generation"""
    print("\n🧪 Testing Nano Banana Image Generation...")
    try:
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model='models/gemini-2.5-flash-image',
            contents=['A cute cat'],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                ),
            ),
        )
        print(f"✅ Image generation works! Response has {len(response.candidates[0].content.parts)} parts")
        return True
    except Exception as e:
        print(f"❌ Image generation failed: {e}")
        return False

async def main():
    print("="*60)
    print("🔬 ViMax API Component Testing")
    print("="*60)
    
    chat_ok = await test_chat()
    image_ok = await test_image()
    
    print("\n" + "="*60)
    print("📊 Test Results:")
    print(f"  Chat Model: {'✅ PASS' if chat_ok else '❌ FAIL'}")
    print(f"  Image Gen:  {'✅ PASS' if image_ok else '❌ FAIL'}")
    print("="*60)
    
    if chat_ok and image_ok:
        print("\n🎉 All components are working!")
        return 0
    else:
        print("\n⚠️  Some components failed. Check errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
