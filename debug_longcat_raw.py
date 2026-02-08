
import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv(".env")

async def test_raw_request():
    api_key = os.getenv("LONGCAT_API_KEY")
    base_url = os.getenv("LONGCAT_API_URL")
    
    # Construct the chat completions URL
    # OpenAI client usually appends /chat/completions to the base_url if it ends in /v1
    # Or simply appends /chat/completions.
    
    url = f"{base_url.rstrip('/')}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "LongCat-Flash-Lite",
        "messages": [{"role": "user", "content": "Hello"}]
    }
    
    print(f"Testing URL: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {data}")
    
    timeout = httpx.Timeout(30.0)
    
    urls_to_test = [
        "https://api.longcat.chat/openai/v1/chat/completions",
        "https://api.longcat.chat/openai/chat/completions",
        "https://api.longcat.chat/chat/completions"
    ]

    for url in urls_to_test:
        print(f"\nTesting URL: {url}")
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
                response = await client.post(url, headers=headers, json=data)
                print(f"Status Code: {response.status_code}")
                try:
                    print(f"Response JSON: {response.json()}")
                except:
                    print(f"Response Content: {response.text}")
        except Exception as e:
            print(f"Error: {repr(e)}")

if __name__ == "__main__":
    asyncio.run(test_raw_request())
