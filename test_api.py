#!/usr/bin/env python3
"""
Test script for the Recipe Extractor API
"""

import httpx
import json
import asyncio
from typing import Dict, Any

# Test URLs from different recipe websites
TEST_URLS = [
    "https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/",
    "https://www.bbcgoodfood.com/recipes/brilliant-banana-loaf",
    "https://www.seriouseats.com/the-best-chili-recipe",
]

async def test_recipe_extraction(base_url: str = "http://localhost:8000"):
    """Test the recipe extraction endpoint"""
    
    async with httpx.AsyncClient() as client:
        # Test health endpoint
        print("Testing health endpoint...")
        health_response = await client.get(f"{base_url}/health")
        print(f"Health check: {health_response.json()}\n")
        
        # Test recipe extraction
        for url in TEST_URLS:
            print(f"Testing recipe extraction for: {url}")
            print("-" * 80)
            
            try:
                response = await client.post(
                    f"{base_url}/extract",
                    json={"url": url},
                    timeout=60.0  # Longer timeout for LLM processing
                )
                
                data = response.json()
                
                if data["success"]:
                    recipe = data["recipe"]
                    print(f"✅ Successfully extracted: {recipe['title']}")
                    print(f"   Description: {recipe.get('description', 'N/A')[:100]}...")
                    print(f"   Prep Time: {recipe.get('prep_time', 'N/A')}")
                    print(f"   Cook Time: {recipe.get('cook_time', 'N/A')}")
                    print(f"   Servings: {recipe.get('servings', 'N/A')}")
                    print(f"   Number of ingredients: {len(recipe['ingredients'])}")
                    print(f"   Number of steps: {len(recipe['steps'])}")
                    print(f"   Number of images: {len(recipe.get('image_urls', []))}")
                    
                    # Print first few ingredients
                    print("\n   First 3 ingredients:")
                    for ing in recipe['ingredients'][:3]:
                        print(f"   - {ing['amount']} {ing.get('unit', '')} {ing['name']}")
                    
                    # Print first step
                    if recipe['steps']:
                        print(f"\n   First step: {recipe['steps'][0]['instruction'][:100]}...")
                    
                else:
                    print(f"❌ Error: {data['error']}")
                    
            except Exception as e:
                print(f"❌ Exception occurred: {str(e)}")
            
            print("\n")

def save_example_response():
    """Save an example .env file and response"""
    
    # Create example .env content
    env_content = """# Recipe Extractor API Configuration
# Copy this file to .env and add your OpenAI API key

OPENAI_API_KEY=sk-your-openai-api-key-here
"""
    
    with open("env.example", "w") as f:
        f.write(env_content)
    
    print("Created env.example file. Copy it to .env and add your OpenAI API key.")

if __name__ == "__main__":
    # Create example env file
    save_example_response()
    
    # Run the tests
    print("\nStarting Recipe Extractor API tests...\n")
    asyncio.run(test_recipe_extraction()) 