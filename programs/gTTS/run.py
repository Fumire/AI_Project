import time
import gtts
import pymysql

with open("password.txt", "r") as f:
    password = f.readline().strip()

connection = pymysql.connect(host="fumire.moe", user="fumiremo_remote", password=password, db="fumiremo_AI", charset="utf8", port=3306)
cursor = connection.cursor(pymysql.cursors.DictCursor)

query = "SELECT * FROM `SpeechList` WHERE `Algorithm` LIKE 'gTTS' AND `Status` LIKE 'wait' ORDER BY `UploadTime` ASC"
cursor.execute(query)

for row in cursor.fetchall():
    tts = gtts.gTTS(row["Sentence"], lang=row["Language"], lang_check=False)
    tts.save("/data/" + row["Identification"] + ".data")

    query = "UPDATE `SpeechList` SET `Status`='complete', `Link`='https://fumire.moe/made/speech/TTS/" + row["Identification"] + ".data' WHERE `Identification` LIKE '" + row["Identification"] + "'"
    cursor.execute(query)

    print(row["Identification"], "Complete!")

print("Done!!")

connection.close()

time.sleep(60)
