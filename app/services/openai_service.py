
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def get_doctor_recommendations(symptoms:str):
    """
    Sends patient symptoms to OpenAI and returns a list of recommended doctor specializations.
    """
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can also use "gpt-4o" later if needed
      messages=[
    {"role": "system", "content": "You are a helpful healthcare assistant. Based on the patient's symptoms, return ONLY a JSON array of doctor specializations, no extra text, no friendly message. Example output: [\"Cardiologist\", \"Pulmonologist\"]."},
    {"role": "user", "content": symptoms}],
        max_tokens=50,
        temperature=0.3  # Low randomness for consistent responses
    )
    
    ai_reply =response.choices[0].message.content.strip() # type: ignore
    
    # Split into a clean list
  
    
    specializations=[spec.strip() for spec in ai_reply.split(',') if spec.split()]
    
    return specializations