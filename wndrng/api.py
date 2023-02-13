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
                "temperature": 0.8,
                "top_p": 0.1,
                "n": 3,
                "prompt": text,
            }
        )
        resp = response.json()
        if "choices" in resp:
            idx = int(random.random() * len(resp["choices"]))
            return resp["choices"][idx]["text"]
        else:
            return "Error： %s" % resp
    except Exception as e:
        return "Error: %s" % e
