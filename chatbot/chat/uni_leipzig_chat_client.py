from dotenv import load_dotenv
load_dotenv()
import os
import requests



class UniLeipzigChatClient:
    def __init__(self) -> None:
        self.base_url = "https://chat.sws.informatik.uni-leipzig.de/chat_completion"
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")

    def request(self, messages, **params):
        data = {
            "messages": messages,
            **params
        }
        headers = { "Authorization": self.openai_api_key }
    
        req = requests.post(self.base_url, headers=headers, json=data)
        return req.json()

