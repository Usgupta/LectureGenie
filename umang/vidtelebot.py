import telebot
import os
import math
import urllib.request
import subprocess
import speech_recognition as sr

# replace with your own Telegram Bot token
TOKEN = '5797976305:AAG2NCAyVjkawPju9QdiXrD3gMtBVuYG_KE'
bot = telebot.TeleBot(TOKEN)

# handler function to process incoming video files
@bot.message_handler(content_types=['video'])
def handle_video(message):
    # get the file id and download the file

    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    file_path = "https://api.telegram.org/bot{0}/getFile?file_id={1}".format(TOKEN,file_id)
    print(file_path)
    print(file_info.file_path)
    file_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(os.environ.get('5797976305:AAG2NCAyVjkawPju9QdiXrD3gMtBVuYG_KE'), file_info.file_path)
    print("URLLLLL",file_url)
    file_name = file_url.split('/')[-1]
    urllib.request.urlretrieve(file_url, file_name)
    
    # break the video into smaller parts if it is larger than 20MB
    file_size = os.path.getsize(file_name)
    max_size = 20 * 1024 * 1024 # maximum file size in bytes
    if file_size > max_size:
        num_parts = math.ceil(file_size / max_size)
        print("File too large, splitting into {} parts".format(num_parts))
        part_size = math.ceil(file_size / num_parts)
        for i in range(num_parts):
            start_byte = i * part_size
            end_byte = min((i + 1) * part_size - 1, file_size - 1)
            part_name = "{}_part{}.mp4".format(file_name[:-4], i+1)
            subprocess.call(['ffmpeg', '-i', file_name, '-ss', str(start_byte/1000), '-t', str((end_byte-start_byte)/1000), '-c', 'copy', part_name])
            transcribe_video(part_name, message.chat.id)
            os.remove(part_name)
    else:
        transcribe_video(file_name, message.chat.id)
    
    # remove the original video file
    os.remove(file_name)

# function to transcribe a video file
def transcribe_video(file_name, chat_id):
    # extract audio from video using ffmpeg
    audio_file = "{}.wav".format(file_name[:-4])
    subprocess.call(['ffmpeg', '-i', file_name, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', audio_file])
    
    # transcribe audio using SpeechRecognition
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    transcript = r.recognize_google(audio)
    
    # send transcript as message to user
    bot.send_message(chat_id, transcript)
    
    # remove audio file
    os.remove(audio_file)

# start the bot
bot.polling()
