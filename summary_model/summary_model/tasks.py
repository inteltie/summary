from .models import Meeting, Transcript , Summary ,MeetingMeetingprocessing
import requests, json
import torch
from transformers import pipeline
from .celery import app

def extract_text_from_transcript(transcript):
    try:
        data = json.loads(transcript)
        text_values = [item["text"] for item in data]
        return " ".join(text_values)
    except json.JSONDecodeError as e:
        return None


@app.task(bind=True,track_started=True)
def generate_summary(self,meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    mp = MeetingMeetingprocessing.objects.get(meeting=meeting)
    try :
        trans = Transcript.objects.get(meeting=meeting)
        transcript_text = extract_text_from_transcript(trans.raw_transcript)

        summarizer = pipeline("summarization", model="/ultimeet/meeting_summary_model")   

        max_chunk_length=512
        max_summary_length=1028

        words = transcript_text.split()
        chunks = [' '.join(words[i:i + max_chunk_length]) for i in range(0, len(words), max_chunk_length)]
        full_summary = ''
        for chunk in chunks:
            summary = summarizer(chunk,max_length=len(chunk)/6,do_sample=True)
            full_summary += summary[0]['summary_text'] + " "
        summarytext = full_summary
        summary = Summary.objects.create(meeting=meeting,transcript=trans,summary_text=summarytext)
        mp.reason = 'Diarization Started'
        mp.save()
    except Exception as err :
        mp.status = "PARTIAL_FAILURE"
        mp.reason = str(err)
        mp.save()
    return True