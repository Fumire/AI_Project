import time
import gtts
import konlpy
import nltk
import pymysql

speech = """
아버지가방에들어가신다:)
"""

grammar = """
NP: {<NR><NNM><J.*>*}
    {<NR>+<SP><NR>}
    {<N.*>+<XSN>?<J.*>*}
VP: {<V.*>+<E.*>*}
    {<N.*><XSV><E.*><J.*>*}
AP: {<A.*>*}
MP: {<M.*>*}
"""
parser = nltk.RegexpParser(grammar)

kkma = konlpy.tag.Kkma()
komoran = konlpy.tag._komoran.Komoran()

with open("password.txt", "r") as f:
    password = f.readline().strip()

# connection = pymysql.connect(host="fumire.moe", user="fumiremo_remote", password=password, db="fumiremo_AI", charset="utf8", port=3306)
# cursor = connection.cursor(pymysql.cursors.DictCursor)

# query = "SELECT * FROM `SpeechList` WHERE `Algorithm` LIKE 'kkma' AND `Status` LIKE 'wait' ORDER BY `UploadTime` ASC"
# cursor.execute(query):

for sentence in kkma.sentences(speech):
    words = komoran.pos(sentence)
    chunks = parser.parse(words)

    chunks.pprint()
