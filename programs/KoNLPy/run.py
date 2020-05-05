import time
import gtts
import konlpy.tag
import pymysql


def okt_token(text):
    okt = konlpy.tag.Okt()
    answer = ""
    for word, pumsa in okt.pos(text, norm=True):
        if pumsa in ["Josa", "PreEomi", "Eomi", "Suffix", "Punctuation"]:
            answer += word
        elif pumsa in ["Noun", "Verb", "Adjective", "Determiner", "Adverb", "Conjunction", "Exclamation"]:
            answer += " " + word
        else:
            answer += " " + word
    return answer


with open("password.txt", "r") as f:
    password = f.readline().strip()

# connection = pymysql.connect(host="fumire.moe", user="fumiremo_remote", password=password, db="fumiremo_AI", charset="utf8", port=3306)
# cursor = connection.cursor(pymysql.cursors.DictCursor)

# query = "SELECT * FROM `SpeechList` WHERE `Algorithm` LIKE 'kkma' AND `Status` LIKE 'wait' ORDER BY `UploadTime` ASC"
# cursor.execute(query)

tts = gtts.gTTS(okt_token(input("Enter:")), lang="ko-KR", lang_check=False)
tts.save("/data/tmp.mp3")
