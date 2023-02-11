import time
import random
import requests
import wndrng.auth as auth


def get_response(text, max_tokens=32):
    time.sleep(0.3)
    try:
        response = requests.post(
            'https://api.openai.com/v1/completions',
            headers={"Authorization": "Bearer %s" % auth.key},
            json={
                "model": "text-davinci-003",
                "max_tokens": max_tokens,
                "temperature": 0.9,
                "top_p": 0.2,
                "n": 3,
                "prompt": text,
            }
        )
        resp = response.json()
        if resp["choices"]:
            idx = int(random.random() * 3 + 0.5)
            return resp["choices"][idx]["text"]
        else:
            return "Error: No response."
    except Exception as e:
        return "Error: %s" % e
