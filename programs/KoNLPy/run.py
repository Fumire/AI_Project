import functools
import os
import time
import gtts
import konlpy
import nltk
import pydub
import pymysql

kkma_grammar = """
MP: {<M.*>*}
NP: {(<NR|ON><NNM>)+<J.*>*}
    {<NR|ON>(<SP><NR|ON>)*<NN.*>*<J.*>*}
    {<MP>?<NN.*><XSN>?(<JC|SP|JKG>?<NN.*><XSN>?)*<J.*>*}
    {<MP>?<N.*><XSN>?(<SP>?<N.*><XSN>?)*<J.*>*}
VP: {<MP>?(<V.*><E.*>*)+}
    {<NP><XSV><E.*><J.*>*}
    {<NP><VC.*><E.*>?}
AP: {<MP>?<A.*>+}
"""

kkma = konlpy.tag.Kkma()
okt = konlpy.tag._okt.Okt()

with open("password.txt", "r") as f:
    password = f.readline().strip()

connection = pymysql.connect(host="fumire.moe", user="fumiremo_remote", password=password, db="fumiremo_AI", charset="utf8", port=3306)
cursor = connection.cursor(pymysql.cursors.DictCursor)

query = "SELECT * FROM `SpeechList` WHERE `Algorithm` LIKE 'kkma' AND `Status` LIKE 'wait' ORDER BY `UploadTime` ASC"
cursor.execute(query)


def join_phrase(phrase):
    adding = {"ㄴ": 4, "ㄹ": 8, "ㅁ": 16}
    answer = phrase[0]
    for p in phrase[1:]:
        if (p[0] in adding) and ((ord(answer[-1]) - ord("가")) % 28 == 0):
            answer = answer[:-1] + chr(ord(answer[-1]) + adding[p[0]]) + p[1:]
        else:
            answer += p
    return answer


for row in cursor.fetchall():
    mp3_count = 0
    mp3_file = pydub.AudioSegment.silent(duration=0)
    raw_sentences = row["Sentence"]

    if functools.reduce(lambda a, b: a if a > len(b) else len(b), raw_sentences.split(), 0) > 20:
        sentences = "".join(list(map(lambda x: (x[0]) if (x[1] in ["Josa", "Unknown"]) else (" " + x[0]), okt.pos(raw_sentences.strip()))))
    else:
        sentences = raw_sentences.strip()

    for sentence in kkma.sentences(sentences):
        words = kkma.pos(sentence)
        tree = nltk.RegexpParser(kkma_grammar).parse(words)
        for subtree in tree:
            print(subtree)
            if isinstance(subtree, nltk.tree.Tree):
                phrase = join_phrase(list(map(lambda x: x[0], subtree.leaves())))
            elif isinstance(subtree, tuple):
                phrase = subtree[0]
            else:
                raise ValueError(str(type(subtree)) + str(subtree))

            try:
                tts = gtts.gTTS(phrase, lang="ko-KR", lang_check=False)
                tts.save("/tmp/" + str(mp3_count) + ".mp3")
            except AssertionError:
                pydub.AudioSegment.silent(duration=100).export("/tmp/" + str(mp3_count) + ".mp3", format="mp3")
            finally:
                mp3_count += 1

    for i in range(mp3_count):
        print(i, "/", mp3_count)
        tmp_mp3 = pydub.AudioSegment.from_file("/tmp/" + str(i) + ".mp3")[:-200].fade_in(100).fade_out(100)
        mp3_file += tmp_mp3
        os.remove("/tmp/" + str(i) + ".mp3")

    mp3_file.export("/data/" + row["Identification"] + ".data", format="mp3")
    query = "UPDATE `SpeechList` SET `Status`='complete', `Link`='https://fumire.moe/made/speech/TTS/" + row["Identification"] + ".data' WHERE `Identification` LIKE '" + row["Identification"] + "'"
    cursor.execute(query)
    print("Done!!")

time.sleep(1)
