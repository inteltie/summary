from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Meeting, Transcript, Summary
import requests, json
import torch
import re
from ctransformers import AutoModelForCausalLM

import logging
# from .custom_permission import ApiKeyPermission
logger = logging.getLogger('django')
 

class SummaryView(APIView):
    # permission_classes = [ApiKeyPermission]

    def eliminate_repeats(self, text):
        x = 3  # The threshold for the number of consecutive repeats

        # Ensure x is valid
        if x < 1:
            return "x must be at least 1"

        pattern = re.compile(r"(.+?)\1{" + str(x - 1) + ",}")
        modified_text = pattern.sub(r"\1", text)
        return modified_text
    
    def extract_text_from_transcript(self, transcript):
        try:
            data = json.loads(transcript)
            text_values = [item["text"] for item in data]
            return " ".join(text_values)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

    def remove_summary_prefix(self, input_string):
        prefix = "Summary: "
        if input_string.startswith(prefix):
            return input_string[len(prefix):].strip()
        return input_string

    def get(self, request, meeting_id):
        try:
            meeting_obj = get_object_or_404(Meeting, id=meeting_id)
            transcript_obj = Transcript.objects.get(meeting=meeting_obj)
            raw_transcript = transcript_obj.raw_transcript
            transcript_text = self.extract_text_from_transcript(raw_transcript)

            llm = AutoModelForCausalLM.from_pretrained("TheBloke/Mistral-7B-Instruct-v0.2-GGUF", model_file="mistral-7b-instruct-v0.2.Q4_K_M.gguf", gpu_layers=50)
            max_chunk_length = 256
            summary = []

            words = transcript_text.split()
            chunks = [' '.join(words[i:i + max_chunk_length]) for i in range(0, len(words), max_chunk_length)]

            for chunk in chunks:
                output = llm(f"[INST]Summarize the following text in third-person without using speaker labels or introductory phrases: {chunk}[/INST]")
                output_i = ''.join(output)
                output_i = self.remove_summary_prefix(output_i)
                output_i = self.eliminate_repeats(output_i)
                output_i = re.sub(r'\s+', ' ', output_i.replace('\n', ' ')).strip()
                summary.append(output_i)

            final_output = '\n\n'.join(summary)

            try:
                summary_obj = Summary(meeting=meeting_obj, summary_text=final_output, transcript=transcript_obj)
                summary_obj.save()
                return Response({"summary": final_output})
            except Exception as e:
                return Response({"error": str(e)}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=400)