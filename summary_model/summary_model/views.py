from .models import Meeting, Transcript
import requests, json
import torch
from rest_framework.views import APIView
from rest_framework.response import Response


class Summary(APIView):
    def extract_text_from_transcript(self, transcript):
        try:
            data = json.loads(transcript)
            text_values = [item["text"] for item in data]
            return " ".join(text_values)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None