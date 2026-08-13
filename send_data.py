import os
import requests
from pathlib import Path

from dotenv import load_dotenv

def env_check():

    local = (Path(__file__).parent)

    path_env = local / ".env"

    if not path_env.exists():
        raise FileNotFoundError(f".env file is missing")

    load_dotenv(path_env)

    SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")
    API_KEY = os.getenv("GOOGLE_API_KEY")

    if not SCRIPT_URL or not API_KEY:
        raise RuntimeError(
            "GOOGLE_SCRIPT_URL or GOOGLE_API_KEY is missing from the .env file."
        )
    
    return(SCRIPT_URL, API_KEY)
    
def main(results=[{"participant":"empty"},{"participant":"empty"}]):
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