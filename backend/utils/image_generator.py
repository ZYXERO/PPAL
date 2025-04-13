import os
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import google.generativeai as genai
from backend.gemini_ai import call_gemini

# Load API key from environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_cooking_image(step_text):
    """Generate cooking images using Google's imagegeneration model"""
    try:
        prompt = f"""
        Generate a photorealistic cooking image showing: {step_text.strip()}
        - Hands actively performing the step
        - Fresh ingredients and kitchen tools
        - Professional food photography style
        - 4K resolution, natural lighting
        - No text/watermarks
        """

        model = genai.GenerativeModel('imagegeneration')
        response = model.generate_content(
            contents=[prompt],
            generation_config=genai.types.GenerationConfig(temperature=0.3),
            image_generation_config=genai.types.ImageGenerationConfig(width=1024, height=768)
        )

        # Process image response
        if response.candidates:
            image_part = response.candidates[0].content.parts[0]
            if hasattr(image_part, 'inline_data'):
                image_data = image_part.inline_data.data
                img = Image.open(BytesIO(image_data))
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

        return "Error: No image data received"

    except Exception as e:
        return f"Generation failed: {str(e)}"


def describe_image_for_step(step_text):
    """
    Generates a textual visual scene description for a cooking step.
    Useful as a fallback for image generation or for stock image search.
    """
    prompt = f"""
You're creating prompts for an image generation model (like DALL·E or Gemini Vision).

Given this cooking step: "{step_text}"

Describe what this looks like visually — ingredients, actions, tools — in under 30 words.
No instructions or steps. Only a scene description.
"""
    return call_gemini(prompt)
