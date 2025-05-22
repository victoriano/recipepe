import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl
import httpx
from bs4 import BeautifulSoup
import instructor
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Recipe Extractor API", version="1.0.0")

# Add CORS middleware for Cloudflare Workers compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client with Instructor
client = instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

# Pydantic models for structured output
class Ingredient(BaseModel):
    """Individual ingredient with amount and unit"""
    name: str = Field(description="The ingredient name")
    amount: Optional[str] = Field(description="The amount/quantity", default=None)
    unit: Optional[str] = Field(description="The unit of measurement", default=None)
    notes: Optional[str] = Field(description="Any special notes or preparations", default=None)

class RecipeStep(BaseModel):
    """Individual recipe step"""
    step_number: int = Field(description="The step number in sequence")
    instruction: str = Field(description="The instruction for this step")
    duration: Optional[str] = Field(description="Time duration for this step if mentioned", default=None)

class Recipe(BaseModel):
    """Structured recipe data extracted from HTML"""
    title: str = Field(description="The recipe title")
    description: Optional[str] = Field(description="Recipe description or summary", default=None)
    prep_time: Optional[str] = Field(description="Preparation time", default=None)
    cook_time: Optional[str] = Field(description="Cooking time", default=None)
    total_time: Optional[str] = Field(description="Total time", default=None)
    servings: Optional[str] = Field(description="Number of servings", default=None)
    difficulty: Optional[str] = Field(description="Difficulty level", default=None)
    cuisine: Optional[str] = Field(description="Type of cuisine", default=None)
    course: Optional[str] = Field(description="Course type (appetizer, main, dessert, etc.)", default=None)
    ingredients: List[Ingredient] = Field(description="List of ingredients")
    steps: List[RecipeStep] = Field(description="List of cooking steps")
    image_urls: List[HttpUrl] = Field(description="URLs of recipe images", default_factory=list)
    nutrition_info: Optional[dict] = Field(description="Nutritional information if available", default=None)
    tags: List[str] = Field(description="Recipe tags or categories", default_factory=list)
    author: Optional[str] = Field(description="Recipe author", default=None)
    source_url: HttpUrl = Field(description="Original recipe URL")

class RecipeRequest(BaseModel):
    """Request model for recipe extraction"""
    url: HttpUrl = Field(description="URL of the recipe to extract")

class RecipeResponse(BaseModel):
    """Response model for recipe extraction"""
    success: bool
    recipe: Optional[Recipe] = None
    error: Optional[str] = None

async def fetch_html(url: str) -> str:
    """Fetch HTML content from a URL"""
    async with httpx.AsyncClient() as client:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = await client.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()
        return response.text

def clean_html(html: str) -> str:
    """Clean and simplify HTML for better parsing"""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    
    # Get text with some structure preserved
    text = soup.get_text(separator='\n', strip=True)
    
    # Also keep the raw HTML for image extraction
    return f"{text}\n\n<!-- RAW HTML FOR IMAGES -->\n{html}"

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Recipe Extractor API",
        "endpoints": {
            "/extract": "POST - Extract recipe data from a URL",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/extract", response_model=RecipeResponse)
async def extract_recipe(request: RecipeRequest):
    """Extract structured recipe data from a URL"""
    try:
        # Fetch HTML content
        html_content = await fetch_html(str(request.url))
        
        # Clean HTML for better parsing
        cleaned_content = clean_html(html_content)
        
        # Extract recipe using OpenAI with Instructor
        recipe = client.chat.completions.create(
            model="gpt-4o-mini",
            response_model=Recipe,
            messages=[
                {
                    "role": "system",
                    "content": """You are a recipe extraction expert. Extract structured recipe data from the provided HTML content.
                    Focus on:
                    - Recipe title and description
                    - All ingredients with amounts and units
                    - Step-by-step instructions
                    - Cooking times and servings
                    - Image URLs (look for img tags with recipe images)
                    - Any nutritional information
                    - Tags, cuisine type, and course
                    Be thorough and extract all available information."""
                },
                {
                    "role": "user",
                    "content": f"Extract the recipe data from this webpage content:\n\n{cleaned_content[:15000]}"  # Limit content to avoid token limits
                }
            ],
            max_retries=2,
        )
        
        # Add source URL
        recipe.source_url = request.url
        
        return RecipeResponse(success=True, recipe=recipe)
        
    except httpx.HTTPError as e:
        return RecipeResponse(
            success=False,
            error=f"Failed to fetch URL: {str(e)}"
        )
    except Exception as e:
        return RecipeResponse(
            success=False,
            error=f"Failed to extract recipe: {str(e)}"
        )

# For Cloudflare Workers deployment, export the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)