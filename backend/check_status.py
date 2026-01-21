#!/usr/bin/env python
"""
ViMax Starter Script - Tests what's working and provides guidance
"""
import asyncio
from google import genai
from google.genai import types
import sys

api_key = "AIzaSyBY3hgYVQsuko7xcBZOhlSCvw1KIxhvdH4"

async def check_api_status():
    """Check API key and available features"""
    print("="*70)
    print("🚀 ViMax API Status Check")
    print("="*70)
    
    client = genai.Client(api_key=api_key)
    
    # Test Chat
    print("\n📝 Testing Chat Model (Gemini)...")
    try:
        response = await client.aio.models.generate_content(
            model='models/gemini-2.5-flash-lite-preview-09-2025',
            contents='Generate a one-sentence story idea about a cat'
        )
        print(f"✅ Chat Model: WORKING")
        print(f"   Response: {response.text.strip()[:80]}...")
        chat_ok = True
    except Exception as e:
        print(f"❌ Chat Model: FAILED - {str(e)[:60]}")
        chat_ok = False
    
    # Test Image Generation
    print("\n🎨 Testing Image Generation...")
    image_ok = False
    for model_name in ['gemini-2.5-flash-image', 'gemini-2.0-flash-exp-image-generation']:
        try:
            response = await client.aio.models.generate_content(
                model=f'models/{model_name}',
                contents=['A cat'],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9"),
                ),
            )
            print(f"✅ Image Generation: WORKING ({model_name})")
            image_ok = True
            break
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️  Image Model {model_name}: Quota exhausted")
            else:
                print(f"❌ Image Model {model_name}: {str(e)[:50]}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 API Status Summary")
    print("="*70)
    print(f"Chat Model (Gemini):     {'✅ READY' if chat_ok else '❌ NOT AVAILABLE'}")
    print(f"Image Generation:        {'✅ READY' if image_ok else '⚠️  QUOTA LIMIT'}")
    print(f"Video Generation (Veo):  ⏳ Will be tested during video creation")
    print("="*70)
    
    if not image_ok:
        print("\n💡 IMAGE GENERATION QUOTA EXHAUSTED")
        print("   Your API key has hit the free tier quota limit for image generation.")
        print("   Options:")
        print("   1. Wait ~24 hours for quota reset")
        print("   2. Enable billing: https://aistudio.google.com/app/billing")
        print("   3. Get a new API key: https://aistudio.google.com/app/apikey")
    
    if chat_ok:
        print("\n✅ GOOD NEWS: Chat model works!")
        print("   You can use ViMax for script generation and text processing.")
        print("   Full video generation will work once image quota resets.")
    
    return chat_ok, image_ok

async def main():
    await check_api_status()
    print("\n" + "="*70)
    print("📚 Next Steps:")
    print("="*70)
    print("To run full video generation (when quota available):")
    print("  cd /app && source .venv/bin/activate && python main_idea2video.py")
    print("  cd /app && source .venv/bin/activate && python main_script2video.py")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
