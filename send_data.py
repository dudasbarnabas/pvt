import os
import requests

from dotenv import load_dotenv

def env_check():
    load_dotenv()

    SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")
    API_KEY = os.getenv("GOOGLE_API_KEY")

    if not SCRIPT_URL or not API_KEY:
        raise RuntimeError(
            "GOOGLE_SCRIPT_URL or GOOGLE_API_KEY is missing from the .env file."
        )
    
    return(SCRIPT_URL, API_KEY)
    
def main(results=[{"id":"empty"},{"id":"empty"}]):
    SCRIPT_URL, API_KEY = env_check()
    payload = {
        "api_key": API_KEY,
        "rows": results,
    }

    response = requests.post(
        SCRIPT_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()
    print(response.json())

if __name__ == "__main__":
    main()