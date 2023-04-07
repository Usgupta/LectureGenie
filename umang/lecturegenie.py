import http.client
import json
import telegram
from telegram.ext import CommandHandler, MessageHandler, Updater, filters

# Set up the HTTP connection
conn = http.client.HTTPSConnection("api.pawan.krd")

# Set up the Telegram bot
bot = telegram.Bot(token='5797976305:AAG2NCAyVjkawPju9QdiXrD3gMtBVuYG_KE')

# Define the start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Send me a YouTube video link and I'll convert the lecture transcript into question and answers.")

# Define the message handler
def convert_to_qa(update, context):
    # Get the YouTube video link from the user's message
    video_link = update.message.text
    
    # Call the API to convert the lecture transcript to Q&A format
    payload = json.dumps({
        "model": "text-davinci-003",
        "prompt": f"Convert the following lecture transcript into question and answers: {video_link}.",
        "temperature": 0.2,
        "max_tokens": 256,
        "stop": [
            "Human:",
            "AI:"
        ]
    })
    headers = {
        'Authorization': 'Bearer pk-KRnpVmvJKalEqmFseSighmlOoMyIohZiIHwFRqjNIXeylZXR',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data.decode("utf-8"))['choices'][0]['text']
    
    # Split the result into questions and answers
    qa_pairs = result.split('Q: ')[1:]
    qa_pairs = [pair.split('A: ') for pair in qa_pairs]
    questions = [pair[0] for pair in qa_pairs]
    answers = [pair[1] for pair in qa_pairs]
    
    # Send the questions and answers back to the user
    for i in range(len(questions)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Q: {questions[i]}')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'A: {answers[i]}')

# Set up the Telegram bot handlers
start_handler = CommandHandler('start', start)
convert_handler = MessageHandler(filters.Regex('https?://(?:www\.)?youtube\.com/watch\?v=\S+'), convert_to_qa)
dispatcher = Updater('5797976305:AAG2NCAyVjkawPju9QdiXrD3gMtBVuYG_KE', True).dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(convert_handler)

# Start the Telegram bot
updater = Updater(token='5797976305:AAG2NCAyVjkawPju9QdiXrD3gMtBVuYG_KE', use_context=True)
updater.start_polling()
updater.idle()
