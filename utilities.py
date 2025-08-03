import os
from dotenv import load_dotenv
import math
import videodb


load_dotenv()
api_key = os.getenv('VIDEO_DB_API_KEY')
conn = videodb.connect(api_key=api_key)


def upload_video(path):
    # video = conn.upload(file_path=path)
    video = conn.upload(url=path)
    print("video uploaded successfully")
    # video.generate_stream()
    # video.play()
    return video

# video = upload_video("https://www.youtube.com/watch?v=yfsTZbwgMSE")
# video =upload_video("https://www.youtube.com/watch?v=DNBaUCCST3I")

def new_function():
    pass

def index_video(video):
    # video.index_spoken_words()
    # text_json = video.get_transcript()
    try:
        video.index_spoken_words()
    except Exception as e:
        if "already exists" in str(e).lower():
            print("[INFO] Spoken word index already exists, skipping indexing.")
        else:
            raise e  # re-raise any other unexpected error
    text_json = video.get_transcript()
    # print(text_json)
    print("video indexed successfully")
    return text_json

# transcript = index_video(video)


def transcript_to_words(transcript):
    if not transcript:
        return ""
    
    # words=[item['text'] for item in transcript]
    words= [item['text']+ ","+str(item['start']) for item in transcript if item['text']!='-']
    print(words)
    return " ".join(words)

# # data=transcript_to_line(transcript)




def format_timestamp(total_seconds):
    """
    Converts a total number of seconds into HH:MM:SS format.
    """
    total_seconds = int(math.floor(total_seconds)) # Ensure integer seconds

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def transcript_to_line(transcript):
    if not transcript:
        return ""
    
    words_with_formatted_timestamps = []
    for item in transcript:
        if item['text'] != '-':
            # Get the raw start time (which is in seconds)
            raw_start_time = item['start']
            
            # Format this raw start time into HH:MM:SS
            formatted_time = format_timestamp(raw_start_time)
            
            # Combine the word and the formatted timestamp
            words_with_formatted_timestamps.append(f"{item['text']},{formatted_time}")
            
    # print(words_with_formatted_timestamps) # Uncomment for debugging
    print("Formatted transcript:", words_with_formatted_timestamps)
    return " ".join(words_with_formatted_timestamps)

# data = transcript_to_line(transcript)
