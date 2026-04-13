from __future__ import annotations

import os
import sys


def main() -> int:
    api_key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()
    if not api_key:
        print("Key Missing: GEMINI_API_KEY (or GOOGLE_API_KEY) is not set")
        return 2

    try:
        from google import genai
    except Exception as exc:  # pylint: disable=broad-except
        print(f"SDK Missing: could not import google.genai ({type(exc).__name__}: {exc})")
        return 3

    try:
        client = genai.Client(api_key=api_key)
        models = client.models.list()
        first = None
        try:
            for m in models:
                first = getattr(m, "name", None) or str(m)
                break
        except TypeError:
            first = str(models)
        print("Key Valid")
        if first:
            print(f"First Model: {first}")
        return 0
    except Exception as exc:  # pylint: disable=broad-except
        details = str(exc)
        upper = details.upper()
        print("Key Invalid or API Error")
        print(f"Error Type: {type(exc).__name__}")
        print(f"Error Details: {details}")
        if "API_KEY" in upper or "UNAUTH" in upper or "PERMISSION" in upper or "403" in upper or "401" in upper:
            print("DIAGNOSIS: API key missing/incorrect or lacks permission")
        elif "429" in upper or "RATE" in upper or "RESOURCE_EXHAUSTED" in upper:
            print("DIAGNOSIS: Rate limit exceeded or quota exhausted")
        elif "TIMEOUT" in upper or "DEADLINE" in upper:
            print("DIAGNOSIS: Network timeout contacting Gemini")
        elif "CONNECTION" in upper or "DNS" in upper or "NETWORK" in upper:
            print("DIAGNOSIS: Network/DNS/connectivity issue contacting Gemini")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
