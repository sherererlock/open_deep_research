
import os
import asyncio
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv(".env")

async def main():
    model_name = os.getenv("RESEARCH_MODEL")
    print(f"Testing model: {model_name}")
    
    # Simulate the logic in utils.py/deep_researcher.py
    longcat_api_url = os.getenv("LONGCAT_API_URL")
    longcat_api_key = os.getenv("LONGCAT_API_KEY")
    
    print(f"URL: {longcat_api_url}")
    # Mask API key for printing
    print(f"API Key: {longcat_api_key[:4]}...{longcat_api_key[-4:] if longcat_api_key else 'None'}")

    try:
        model = init_chat_model(
            model=model_name,
            # Let init_chat_model infer provider from prefix "openai:"
            api_key=longcat_api_key,
            base_url=longcat_api_url
        )
        
        print("Model initialized. Sending request...")
        response = await model.ainvoke([HumanMessage(content="Hello, are you working?")])
        print(f"Response: {response.content}")
        print("SUCCESS: Model configuration is correct.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
