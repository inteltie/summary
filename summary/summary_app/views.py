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


class Summary(APIView):
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
            # Retrieve the meeting object
            meeting_obj = get_object_or_404(Meeting, id=meeting_id)
            transcript_obj = Transcript.objects.get(meeting=meeting_obj)
            raw_transcript = transcript_obj.raw_transcript
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            transcript_text = self.extract_text_from_transcript(raw_transcript)

            llm = AutoModelForCausalLM.from_pretrained("TheBloke/Mistral-7B-Instruct-v0.2-GGUF", model_file="mistral-7b-instruct-v0.2.Q4_K_M.gguf", gpu_layers=50)
            #llm.to(device)
            max_chunk_length = 256
            summary = []
            output_items = []

            words = transcript_text.split()
            chunks = [' '.join(words[i:i + max_chunk_length]) for i in range(0, len(words), max_chunk_length)]

            for chunk in chunks:
                output_items = []
                output = llm(f"[INST]Summarize the following text in third-person without using speaker labels or introductory phrases: {chunk}[/INST]") 
                #print(output)
                print()
                output_items.extend(output)
                output_i = ''.join(output_items)
                output_i = self.remove_summary_prefix(output_i)
                output_i = self.eliminate_repeats(output_i)
                print(output_i)

                if output_items:  # Check if output_items is not empty
                    summary.append(output_i)

            out = ' '.join(summary)
            out = re.sub(r'\s+', ' ', out.replace('\n', ' ')).strip()

            try:
                summary_obj = Summary(meeting=meeting_obj, summary_text=out, transcript=transcript_obj)
                summary_obj.save()  # Directly saving the new summary
                return Response({"summary": out})
            except Exception as e:
                return Response({"error": str(e)}, status=400)

        except Exception as e:
            # Handle errors
            return Response({"error": str(e)}, status=400)