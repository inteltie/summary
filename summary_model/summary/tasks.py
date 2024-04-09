from .models import Meeting, Transcript , Summary ,MeetingMeetingprocessing, Decision
import requests, json
import torch
from transformers import pipeline
from summary_model.celery import app
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def extract_text_from_transcript(transcript):
    try:
        data = json.loads(transcript)
        text_values = [item["text"] for item in data]
        return " ".join(text_values)
    except json.JSONDecodeError as e:
        return None

def split_into_chunks(text, num_chunks=5):
        sentences = text.split('.')
        print(sentences)
        chunk_size = len(sentences) // num_chunks
        print(chunk_size,num_chunks)
        return ['.'.join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]



def important_announcements(final_text,meeting,trans):
    #transcript = extract_text_from_transcript(final_text)
    chunks = split_into_chunks(final_text, 4)
    print('final_text:',final_text,chunks)
    model_dir = '/home/ubuntu/summary/action_items_sentence/'
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
    obj_list = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=30, min_length=10, do_sample=False)
        obj_list.append(summary[0]['summary_text'])
        print("Key Points:", summary[0]['summary_text'])
    obj_list.pop()
    importantdecisions = json.dumps(obj_list)
    print(importantdecisions)
    Decision.objects.create(meeting=meeting,transcript=trans,decision_text=importantdecisions)
    return True


@app.task(bind=True,track_started=True)
def generate_summary(self,meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    mp = MeetingMeetingprocessing.objects.get(meeting=meeting)
    try :
        trans = Transcript.objects.get(meeting=meeting)
        transcript_text = extract_text_from_transcript(trans.raw_transcript)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        summarizer = pipeline("summarization", model="/home/ubuntu/summary/meeting_summary_model", device=device)

        max_chunk_length = 512
        max_summary_length = 1028

        # Split transcript into chunks
        words = transcript_text.split()
        chunks = [' '.join(words[i:i + max_chunk_length]) for i in range(0, len(words), max_chunk_length)]

        # Process chunks in batches for summarization
        chunk_batch_size = 4  # Adjust batch size as needed
        batched_chunks = [chunks[i:i + chunk_batch_size] for i in range(0, len(chunks), chunk_batch_size)]

        full_summary = ''

        for batch in batched_chunks:
            batch_summaries = summarizer(batch, max_length=max_chunk_length // 6, do_sample=True)

            for summary in batch_summaries:
                full_summary += summary['summary_text'] + " "

        summary_text = full_summary
        summary = Summary.objects.create(meeting=meeting,transcript=trans,summary_text=summary_text)
        mp.reason = 'Summary Completed'
        mp.save()
        important_announcements(final_text=summary_text,meeting=meeting,trans=trans)
    except Exception as err :
        print('ERROR::',err)
        mp.status = "PARTIAL_FAILURE"
        mp.reason = str(err)
        mp.save()
    return True