import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from the .env file
load_dotenv()

# =====================================
# Gemini API Key (Loaded Securely from .env)
# =====================================

API_KEY = os.getenv("GEMINI_API_KEY")

# Create the client using the secure environment variable
client = genai.Client(api_key=API_KEY)


# =====================================
# Generate Embedding
# =====================================

def generate_embedding(text):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


# =====================================
# Testing
# =====================================

if __name__ == "__main__":

    sample_text = "Student Zaid is present today."

    embedding = generate_embedding(sample_text)

    print("Embedding Generated Successfully")
    print("Embedding Length :", len(embedding))
