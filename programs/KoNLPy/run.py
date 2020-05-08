import functools
import os
import time
import re
import gtts
import konlpy
import nltk
import pydub
import pymysql

kkma_grammar = """
AP: {<NP><XSV><E.*>*<ETD>}
    {<NP><JKM>}
    {<VA|VV><ETD>}
    {<XR><XSA><ECE>}

VP: {<MP>?<V.*><E.*>*(<V.*><E.*>*)*<EC.|EF.|ET.>}
    {<MP>?<NNG>+<XSV><E.*>*<EC.|EF.|ET.>}

NP: {<AP>?<N.*><XSV><ETN>}
    {<UN>}
    {<VP><NNB|NNM>}
    {<N.*><XSV><ETD>?<NNB|NNM>}
    {<AP>?<MDN|MDT>?<N.*>*<XSN>?(<JC|JKG><N.*>*<XSN>?)*}

DP: {<NP><VCN|VCP><ECE|ETD>}
    {<VX.><E.*>*<ETD>}

XJ: {(<NP><JC>)*<NP><J.*>*<JX>}
    {<VP><JX>}
OJ: {(<NP><JC>)*<NP><J.*>*<JKO>}
    {<VP><JKO>}
SJ: {(<NP><JC>)*<NP><J.*>*<JKS>}
MJ: {(<NP><JC>)*<NP><J.*>*<JKM>}
CJ: {(<NP><JC>)*<NP><J.*>*<JKC>}
"""

kkma = konlpy.tag.Kkma()
okt = konlpy.tag._okt.Okt()

with open("password.txt", "r") as f:
    password = f.readline().strip()

connection = pymysql.connect(host="fumire.moe", user="fumiremo_remote", password=password, db="fumiremo_AI", charset="utf8", port=3306)
cursor = connection.cursor(pymysql.cursors.DictCursor)

query = "SELECT * FROM `SpeechList` WHERE `Algorithm` LIKE 'kkma' AND `Status` LIKE 'wait' ORDER BY `UploadTime` ASC"
cursor.execute(query)

regex = re.compile(r"[^ ㄱ-ㅣ|가-힣|0-9|\.,·]+")


def join_phrase(phrase):
    adding = {"ㄴ": 4, "ㄹ": 8, "ㅁ": 16, "ㅂ": 17}
    answer = phrase[0][0]
    for p, pos in phrase[1:]:
        if (p[0] in adding):
            if pos.startswith("J") or pos.startswith("E"):
                answer = answer[:-1] + chr(((ord(answer[-1]) - ord("가")) // 28 * 28) + ord("가") + adding[p[0]]) + p[1:]
            else:
                answer = answer[:-1] + " " + chr(((ord(answer[-1]) - ord("가")) // 28 * 28) + ord("가") + adding[p[0]]) + p[1:]
        else:
            if pos.startswith("J") or pos.startswith("E"):
                answer += p
            else:
                answer += " " + p
    return answer


for row in cursor.fetchall():
    mp3_count = 0
    mp3_file = pydub.AudioSegment.silent(duration=0)
    raw_sentences = regex.sub("", row["Sentence"])

    if functools.reduce(lambda a, b: a if a > len(b) else len(b), raw_sentences.split(), 0) > 20:
        sentences = "".join(list(map(lambda x: (x[0]) if (x[1] in ["Josa", "Unknown"]) else (" " + x[0]), okt.pos(raw_sentences.strip()))))
    else:
        sentences = raw_sentences.strip()

    for sentence in kkma.sentences(sentences):
        words = list(functools.reduce(lambda a, b: a + b, kkma.pos(sentence, flatten=False), []))
        tree = nltk.RegexpParser(kkma_grammar).parse(words)
        for subtree in tree:
            print(subtree)
            if isinstance(subtree, nltk.tree.Tree):
                phrase = join_phrase(subtree.leaves())
            elif isinstance(subtree, tuple):
                phrase = subtree[0]
            else:
                raise ValueError(str(type(subtree)) + str(subtree))
            print(phrase)

            try:
                tts = gtts.gTTS(phrase, lang="ko-KR", lang_check=False)
                tts.save("/tmp/" + str(mp3_count) + ".mp3")
            except AssertionError:
                pydub.AudioSegment.silent(duration=300).export("/tmp/" + str(mp3_count) + ".mp3", format="mp3")
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

time.sleep(60)
