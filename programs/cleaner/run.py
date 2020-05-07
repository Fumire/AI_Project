import os
import time
import pymysql

with open("password.txt", "r") as f:
    password = f.readline().strip()

connection = pymysql.connect(host="fumire.moe", user="fumiremo_remote", password=password, db="fumiremo_AI", charset="utf8", port=3306)
cursor = connection.cursor(pymysql.cursors.DictCursor)

query = "SELECT * FROM `SpeechList` WHERE `Status` LIKE 'complete' ORDER BY `UploadTime` ASC"
cursor.execute(query)

for row in cursor.fetchall():
    if os.path.isfile("/data/" + row["Identification"] + ".data"):
        if (os.path.getatime("/data/" + row["Identification"] + ".data") - time.time() / 1000) > (60 * 60 * 24):
            os.remove("/data/" + row["Identification"] + ".data")
            query = "UPDATE `SpeechList` SET `Status`='expired', `Link`=NULL WHERE `Identification` LIKE '" + row["Identification"] + "'"
            cursor.execute(query)
            print(row["Identification"], "Complete!")
    else:
        query = "UPDATE `SpeechList` SET `Status`='expired', `Link`=NULL WHERE `Identification` LIKE '" + row["Identification"] + "'"
        cursor.execute(query)
        print(row["Identification"], "Complete!")

print("Done!!")

connection.close()

time.sleep(60)
