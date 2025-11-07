# Step 1: Import all required libraries
import gradio as gr
from groq import Groq
import os  # <-- Import the os library to read environment variables

# --- --- --- --- --- --- --- --- --- --- --- --- ---
# Step 2: Get the Groq API Key from Hugging Face Secrets
# --- --- --- --- --- --- --- --- --- --- --- --- ---

print("Attempting to initialize Groq client...")

# Read the API key from an environment variable named "GROQ_API_KEY"
# You must set this in your Hugging Face Space "Secrets" settings.
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("--- ERROR: GROQ_API_KEY secret not found ---")
    print("Please set the GROQ_API_KEY secret in your Hugging Face Space settings.")
    # Stop the app if the key is not found
    raise ValueError("GROQ_API_KEY not found in environment variables.")

try:
    # Initialize the client with the key
    client = Groq(api_key=GROQ_API_KEY)
    # Test the key
    client.models.list() 
    print("Groq client initialized successfully!")

except Exception as e:
    print(f"Failed to initialize Groq client: {e}")
    print("Please check if your GROQ_API_KEY is correct.")
    raise SystemExit("Exiting due to API key error.")


# --- --- --- --- --- --- --- --- --- --- --- --- ---
# Step 3: Define the Chatbot Logic (No changes here)
# --- --- --- --- --- --- --- --- --- --- --- --- ---

def chatbot_response(message, history):
    
    messages_for_api = []
    for user_msg, bot_msg in history:
        messages_for_api.append({"role": "user", "content": user_msg})
        messages_for_api.append({"role": "assistant", "content": bot_msg})
    
    messages_for_api.append({"role": "user", "content": message})
    
    try:
        response = client.chat.completions.create(
            # We are using the correct, active model
            model="llama-3.1-8b-instant",
            messages=messages_for_api,
            temperature=0.7
        )
        
        bot_reply = response.choices[0].message.content
        return bot_reply
        
    except Exception as e:
        print(f"An error occurred during chat completion: {e}")
        return f"Sorry, I encountered an error: {e}"

# --- --- --- --- --- --- --- --- --- --- --- --- ---
# Step 4: Create and Launch the Gradio Interface
# --- --- --- --- --- --- --- --- --- --- --- --- ---

print("Launching Gradio Chat Interface...")

iface = gr.ChatInterface(
    fn=chatbot_response,
    title="My Groq Chatbot",
    description="Ask me anything! I'm powered by Groq (Llama 3.1 8B).",
    examples=["What is Groq?", "Write a poem about a fast robot", "Explain Python dictionaries"]
)

# .launch() will be run by the Hugging Face server
iface.launch()