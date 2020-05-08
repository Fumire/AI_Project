import os
import time
import re
import gtts
import nltk
import pydub
import pymysql

grammar = r"""
NP: {<PRP\$><JJ.*><NN.*>}
    {<RB>?<DT>?<CD|JJ.*|PRP\$>*<NN.*|PRP.?|VBG>+((<,><CD|JJ.*|PRP\$>*<NN.*|PRP.?|VBG>+)*<CC><CD|JJ.*|PRP\$>*<NN.*|PRP.?|VBG>+)?}
    {<JJS><IN><PRP|PRP\$>}
    {<DT>?<WDT|WP><VB|VBP|VBZ>}
    {<DT><RBS>}

SP: {<NP><VB|VBZ><VBN>?}
    {<NP><VBP><VBG|VBN>*}
    {<NP><VBD><RB>?<VB>}
    {<NP><VBD><VBN>}
    {<NP><VBD>}
    {<NP><VBZ><VBN>}
    {<NP><MD><VB>}

VP: {<MD><VB><VBN>?}

IP: {<IN>+<NP>((<,><NP>)*<CC><NP>)?}
    {<IN>+<CC><RB>+}
    {<IN>+<DT|PDT>}
    {<IN>+}

TN: {<TO><NP>}
TV: {<TO><VB>}

AP: {<DT|RB>?<JJ.*>}
"""


with open("password.txt", "r") as f:
    password = f.readline().strip()

connection = pymysql.connect(host="fumire.moe", user="fumiremo_remote", password=password, db="fumiremo_AI", charset="utf8", port=3306)
cursor = connection.cursor(pymysql.cursors.DictCursor)

query = "SELECT * FROM `SpeechList` WHERE `Algorithm` LIKE 'NLTK' AND `Status` LIKE 'wait' ORDER BY `UploadTime` ASC"
cursor.execute(query)

regex = re.compile(r"^[a-zA-Z0-9$@$!%*?&#^-_. +]+$")

for row in cursor.fetchall():
    speech = row["Sentence"]
    mp3_count = 0
    mp3_file = pydub.AudioSegment.silent(duration=0)

    for sentence in nltk.sent_tokenize(speech):
        words = nltk.pos_tag(nltk.word_tokenize(regex.sub("", sentence)))
        tree = nltk.RegexpParser(grammar).parse(words)
        for subtree in tree:
            print(subtree)

            if isinstance(subtree, nltk.tree.Tree):
                phrase = " ".join(list(map(lambda x: x[0], subtree.leaves())))
            elif isinstance(subtree, tuple):
                phrase = subtree[0]
            else:
                raise ValueError(str(type(subtree)) + str(subtree))

            if phrase in [",", ";"]:
                pydub.AudioSegment.silent(duration=300).export("/tmp/" + str(mp3_count) + ".mp3", format="mp3")
            elif phrase in [".", ":"]:
                pydub.AudioSegment.silent(duration=600).export("/tmp/" + str(mp3_count) + ".mp3", format="mp3")
            else:
                tts = gtts.gTTS(phrase, lang=row["Language"], lang_check=False)
                tts.save("/tmp/" + str(mp3_count) + ".mp3")
            mp3_count += 1

    for i in range(mp3_count):
        print(i, "/", mp3_count)
        tmp_file = pydub.AudioSegment.from_file("/tmp/" + str(i) + ".mp3")[:-200].fade_in(200).fade_out(200)
        mp3_file += tmp_file
        os.remove("/tmp/" + str(i) + ".mp3")

    query = "UPDATE `SpeechList` SET `Status`='complete', `Link`='https://fumire.moe/made/speech/TTS/" + row["Identification"] + ".data' WHERE `Identification` LIKE '" + row["Identification"] + "'"
    cursor.execute(query)

    mp3_file.export("/data/" + row["Identification"] + ".data", format="mp3")
    print("Done!!")

time.sleep(60)
