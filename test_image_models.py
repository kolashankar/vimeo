#!/usr/bin/env python
"""Test alternative image generation model"""
import asyncio
from google import genai
from google.genai import types

api_key = "AIzaSyBY3hgYVQsuko7xcBZOhlSCvw1KIxhvdH4"

async def test_image_model(model_name):
    """Test specific image generation model"""
    print(f"\n🧪 Testing: {model_name}")
    try:
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model=f'models/{model_name}',
            contents=['A simple red circle'],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                ),
            ),
        )
        
        image_found = any(part.inline_data is not None for part in response.candidates[0].content.parts)
        
        if image_found:
            print(f"✅ SUCCESS with {model_name}")
            return True
        else:
            print(f"❌ No image generated with {model_name}")
            return False
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            print(f"❌ Quota limit for {model_name}")
        else:
            print(f"❌ Error with {model_name}: {error_msg[:100]}")
        return False

async def main():
    print("="*70)
    print("🔬 Testing Alternative Image Generation Models")
    print("="*70)
    
    models_to_test = [
        "gemini-2.0-flash-exp-image-generation",
        "gemini-3-pro-image-preview",
    ]
    
    for model in models_to_test:
        result = await test_image_model(model)
        if result:
            print(f"\n🎉 FOUND WORKING MODEL: {model}")
            return model
        await asyncio.sleep(1)
    
    print("\n⚠️ All image models hit quota limits or failed")
    return None

if __name__ == "__main__":
    working_model = asyncio.run(main())
    if working_model:
        print(f"\n✅ Use this model: {working_model}")
