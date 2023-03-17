import telegram
from telegram.ext import Updater, MessageHandler, Filters
from transformers import pipeline
from pydub import AudioSegment
from pydub.generators import Sine

# Set up ChatGPT pipeline
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')


# Define function to generate text response
def generate_response(text):
    response = generator(text)[0]['generated_text']
    return response.strip()


def TextToSpeech(text):
    audio = AudioSegment.silent(duration=100)
    for word in text.split():
        duration = len(word) * 50
        frequency = len(word) * 200
        sine_wave = Sine(frequency).to_audio_segment(duration=duration)
        audio = audio.append(sine_wave, crossfade=10)
        audio = audio.append(AudioSegment.silent(duration=50), crossfade=10)
    return audio


# Define function to convert text to audio
def text_to_audio(text):
    audio = TextToSpeech(text)
    audio.export('response.mp3', format="mp3")
    return 'response.mp3'


# Define message handler function
def handle_message(update, context):
    user_message = update.message.text
    response = generate_response(user_message)
    audio_file = text_to_audio(response)
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_file, 'rb'))


# Set up Telegram bot
TOKEN = '6268136991:AAHrY9UEnWve3Zu2AUShnquI38KIz7KcwT8'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
message_handler = MessageHandler(Filters.text, handle_message)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
updater.idle()
