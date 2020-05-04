import gtts
import pymysql

tts = gtts.gTTS('hello')
tts.save('/data/hello.mp3')
