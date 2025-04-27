import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup OpenAI client
openai_client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

while True:
    # Take user input
    symptom = input("\n🧑‍⚕️ Enter your symptoms (or type 'exit' to quit): ")

    # Exit if user types 'exit'
    if symptom.lower() == 'exit':
        print("👋 Exiting AI Doctor Recommendation!")
        break

    # Send symptom to OpenAI
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant suggesting the correct doctor specialization based on patient symptoms."},
            {"role": "user", "content": symptom}
        ],
        max_tokens=100
    )

    ai_reply = response.choices[0].message.content.strip() # type: ignore

    # Print AI's recommendation
    print(f"\n🔵 Symptom: {symptom}")
    print(f"🟢 AI Recommendation: {ai_reply}")
    print("------")
