import telegram
import http.client
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import openai
import speech_recognition as sr
from pydub import AudioSegment
from notion_client import Client
import os
import uuid
import notion_page


# Set up the Notion client
notion = Client(auth="<YOUR-NOTION-KEY>")

def create_notion_page(update, page_title,trans ):
    
    # Get the link to the temporary page
    # print(trans)
    # print(type(trans))
    link = notion_page.createPage(page_title,trans)
    
    # Create a new message with the link to the temporary page
    message = f"Here's the link to the question and answers:\n\n{link}"
    
    # Send the message to the user via the Telegram bot
    bot.send_message(chat_id=update.effective_chat.id, text=message)



THUMBSUP = ['CAACAgIAAxkBAAEIfc1kL_aiKAofS4dy6vRcnLSFKdxzSgACUQcAAhhC7gigGxT6Hgm5gi8E', "Received!"]
PROCESSING = ["CAACAgIAAxkBAAEIfc9kL_eCEG21A2eDF4RqViT0PY4kAANQBwACGELuCBZi8kg5gECWLwQ", "Processing..."]
HEY = ['CAACAgIAAxkBAAEIflRkMCSREswn2-x17mWU97-vqp9YFQACRwcAAhhC7gho2RKsyoN1VC8E',"Hello! I'm a bot that can summarize lectures into Q&A. Simply drop your Lecture video or share youtube link using command \qna <youtube link>"]

def audtotxt(file_name):
    # Initialize recognizer
    r = sr.Recognizer()

    # Load audio file
    audio_file = sr.AudioFile(file_name)

    # Use Google Speech Recognition
    with audio_file as source:
        audio = r.record(source)

    textt = r.recognize_google(audio)

    # Print the transcribed text
    return textt

# Replace YOUR_TOKEN with your actual bot token obtained from BotFather
bot = telegram.Bot(token='<TELEGRAM-BOT-KEY>')


openai.api_key = '' # leave this empty or set it to anything
openai.api_base = 'https://api.hypere.app' # really important

def list_to_str(tr):
    s = ''
    for t in tr:
        s+= t['text'] + ' '
    return s

def convert_to_wav(file_path):
    # Get the file name and extension
    file_name, ext = os.path.splitext(file_path)

    # Load the audio file
    sound = AudioSegment.from_file(file_path)

    # Export the audio file as WAV format
    wav_file = file_name + ".wav"
    sound.export(wav_file, format="wav")
    return wav_file


# This function will handle the /start command
def start(update, context):
    send_sticker(update,context,HEY)

def youtube_id(url):

    yt = YouTube(url)

    video_id = yt.video_id

    # print(video_id)
    return YouTubeTranscriptApi.get_transcript(video_id)

def send_sticker(update, context,file_id):
    context.bot.send_message(chat_id=update.effective_chat.id, text=file_id[1])
    bot.send_sticker(chat_id=update.effective_chat.id, sticker=file_id[0])


# This function will handle the /qna command
def qna(update, context):

    send_sticker(update, context,THUMBSUP)

    if update.message.video:

        video_file = update.message.video.file_id
        vid_to_qna(update, context, video_file)

    elif update.message.document:

        video_file = update.message.document.file_id
        vid_to_qna(update, context, video_file)


    else: 
        # Extract the link from the command message
        link = update.message.text[5:]

        transcript = youtube_id(link)

        transcript = list_to_str(transcript)
        # print(transcript)
        send_sticker(update, context,PROCESSING)
       
        txt_to_qna(update,context,transcript)

def vid_to_qna(update, context, video_file):
    video = context.bot.get_file(video_file)
    # print(video_file)
        
        # Download the video file to the local machine
    mp4vid = video.download()

    send_sticker(update, context,PROCESSING)

    wavvid = convert_to_wav(mp4vid)
    transtxt = audtotxt(wavvid)
    # print(transtxt)

    txt_to_qna(update, context,transtxt)

def txt_to_qna(update, context,transtxt):
    maxtoken = 4097-(len(transtxt)//4)
       
    if (maxtoken<0):
        context.bot.send_message(chat_id=update.effective_chat.id, text="too big")
            
    else:
            
        completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt= "Can you convert the following text into question and answers?: {0}".format(transtxt),
                max_tokens = maxtoken
            )
        
        titlecompletion = openai.Completion.create(
                engine="text-davinci-003",
                prompt= "Can you give me a suitable title for this piece of text?: {0}".format(transtxt),
                max_tokens = maxtoken
            )

        # print(completion)

        page_title = titlecompletion.choices[0].text

        result = completion.choices[0].text

        create_notion_page(update,page_title,result)

        context.bot.send_message(chat_id=update.effective_chat.id, text=result)


# Create the Updater and pass it your bot's token.
updater = Updater(token='<TELEGRAM-BOT-ID>', use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Add handlers for commands
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('qna', qna), )

dispatcher.add_handler(MessageHandler(Filters.video, qna))
dispatcher.add_handler(MessageHandler(Filters.document, qna))


# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
updater.idle()

