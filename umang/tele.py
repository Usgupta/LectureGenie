import telegram
import http.client
import json
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace YOUR_TOKEN with your actual bot token obtained from BotFather
bot = telegram.Bot(token='5797976305:AAG2NCAyVjkawPju9QdiXrD3gMtBVuYG_KE')

# This function will handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a bot that can summarize lectures into Q&A.")

def qnavid(update, context):
    print("ssup")
    print(update.message)
    # Check if the message contains a video file
    if update.message.video:
        print("file is there")
        video_file = update.message.video.file_id
        video = context.bot.get_file(video_file)
        
        # Download the video file to the local machine
        video.download()
        
        # Send the video file to the API for processing
        conn = http.client.HTTPSConnection("api.pawan.krd")
        headers = {
            'Authorization': 'Bearer YOUR_API_KEY',
            'Content-Type': 'multipart/form-data'
        }
        with open(video.file_path, "rb") as f:
            payload = f.read()
        conn.request("POST", "/v1/video_summarizer", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data)
        
        # Send the summarized text as a message
        res_dict = json.loads(data.decode("utf-8"))
        context.bot.send_message(chat_id=update.effective_chat.id, text=res_dict["summary"])
        
        # Delete the local video file
        os.remove(video.file_path)
    else:
        print("no file bro")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please upload a video file.")


# This function will handle the /qna command
def qna(update, context):
    link = update.message.text[5:]
    print(link)
    conn = http.client.HTTPSConnection("api.hypere.app")
    payload = json.dumps({ 
        "model": "text-davinci-003",
        "prompt": "Convert the following lecture transcript into question and answers: {link}",
        "temperature": 0.2,
        "max_tokens": 256,
        "stop": [
            "Human:",
            "AI:"
        ]
    })

    headers = {
        'Authorization': '',
        'Content-Type': 'application/json'
    }

    conn.request("POST", "/v1/completions", payload, headers)

    res = conn.getresponse()
    # print(res)
    # print(type(res))
    data = res.read()
    print(data)

    res_dict = json.loads(data.decode("utf-8"))
    # print(res_dict["choices"][0])
    # print(type(res_dict["choices"][0]))
    # textres = json.loads(res_dict["choices"][0])


    context.bot.send_message(chat_id=update.effective_chat.id, text=res_dict["choices"][0]["text"])

def handle_everything_else(update,context):
    # print(update)
    print(update.message.document)
    print(update.message.document.file_id)


    video = context.bot.get_file(update.message.document.file_id)

        
    # Download the video file to the local machine
    video.download()
    
    # Send the video file to the API for processing
    conn = http.client.HTTPSConnection("api.pawan.krd")
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'multipart/form-data'
    }
    with open(video.file_path, "rb") as f:
        payload = f.read()
    conn.request("POST", "/v1/video_summarizer", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
        
    # Send the summarized text as a message
    res_dict = json.loads(data.decode("utf-8"))
    context.bot.send_message(chat_id=update.effective_chat.id, text=res_dict["summary"])
    
    # Delete the local video file
    os.remove(video.file_path)

# Create the Updater and pass it your bot's token.
updater = Updater('5797976305:AAG2NCAyVjkawPju9QdiXrD3gMtBVuYG_KE', True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Add handlers for commands
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('qna', qna))
dispatcher.add_handler(CommandHandler('qnavid', qnavid))

# Add a handler to handle video uploads
dispatcher.add_handler(MessageHandler(Filters.video, qnavid))
dispatcher.add_handler(MessageHandler(Filters.all, handle_everything_else))
# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
updater.idle()
