from pytube import YouTube
import ffmpeg
import whisper
import scrapetube
from trtokenizer.tr_tokenizer import WordTokenizer


# YouTube video URL
channel_id = "UCZDdMa-BSGZdRcFgjb80jgg"

# Download YouTube video and extract audio
def download_and_extract_audio(video_url):
    try:
        # Download YouTube video
        # print("Downloading video...")
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(filename='video')

        # Extract audio using ffmpeg
        # print("Extracting audio...")
        input_file = 'video'
        output_file = 'audio_extracted.mp3'
        ffmpeg.input(input_file).output(output_file).run(overwrite_output=True)

        return output_file

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Transcribe audio file using Whisper
def transcribe_audio(audio_file):
    try:
        # Load audio file
        model = whisper.load_model("base")
        
        # Perform transcription
        result = model.transcribe(audio_file)
        
        return result["text"]
        # Print transcription result
        # print("Transcription:")
        # print(result["text"])
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    dict = {}
    word_tokenizer_object = WordTokenizer()
    # Download and extract audio
    videos = scrapetube.get_channel(channel_id)
    for video_url in videos:
        audio_file_path = download_and_extract_audio("https://www.youtube.com/watch?v=" + video_url["videoId"])
        if audio_file_path:
            # Transcribe extracted audio
            transcription = transcribe_audio(audio_file_path)
            tokenized = word_tokenizer_object.tokenize(transcription)
            for word in tokenized:
                if word in dict:
                    dict[word] += 1
                else:
                    dict[word] = 1
    print(dict)

