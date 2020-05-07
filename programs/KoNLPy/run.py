import time
import gtts
import konlpy
import nltk
import pymysql

speeches = ["""
유구한 역사와 전통에 빛나는 우리 대한국민은 3·1운동으로 건립된 대한민국임시정부의 법통과 불의에 항거한 4·19민주이념을 계승하고, 조국의 민주개혁과 평화적 통일의 사명에 입각하여 정의·인도와 동포애로써 민족의 단결을 공고히 하고, 모든 사회적 폐습과 불의를 타파하며, 자율과 조화를 바탕으로 자유민주적 기본질서를 더욱 확고히 하여 정치·경제·사회·문화의 모든 영역에 있어서 각인의 기회를 균등히 하고, 능력을 최고도로 발휘하게 하며, 자유와 권리에 따르는 책임과 의무를 완수하게 하여, 안으로는 국민생활의 균등한 향상을 기하고 밖으로는 항구적인 세계평화와 인류공영에 이바지함으로써 우리들과 우리들의 자손의 안전과 자유와 행복을 영원히 확보할 것을 다짐하면서 1948년 7월 12일에 제정되고 8차에 걸쳐 개정된 헌법을 이제 국회의 의결을 거쳐 국민투표에 의하여 개정한다.
""", '@ninsho111 ㄴ슫ㅋㅋㄱㅋㄷㄷㄱㄱㄷㄱㅋ아진ㄴㄴ자거위님ㅁㅁ넘유쾤ㄱ핵ㅋㄱㅋㄷㄱㄱㅋㄱㅋㄱㄱㅋㅅ후..저..자야조..eㅎㅇㄱㄱ.....ㄹ오늘ㄹ은ㅁ샐라고한거아닌ㄴ데...츄우기....거위님ㅁ보니가치킨ㄴ먹ㄱ고싶어요...꿈ㅁ에서 네네치킨ㄴ먹ㄱ을래욛...(기절']

kkma_grammar = """
NP: {<NR><NNM><J.*>*}
    {<NR>+<SP><NR>}
    {<N.*>+<XSN>?<J.*>*}
VP: {<V.*>+<E.*>*}
    {<N.*><XSV><E.*><J.*>*}
AP: {<A.*>*}
MP: {<M.*>*}
"""

kkma = konlpy.tag.Kkma()
okt = konlpy.tag._okt.Okt()

with open("password.txt", "r") as f:
    password = f.readline().strip()

# connection = pymysql.connect(host="fumire.moe", user="fumiremo_remote", password=password, db="fumiremo_AI", charset="utf8", port=3306)
# cursor = connection.cursor(pymysql.cursors.DictCursor)

# query = "SELECT * FROM `SpeechList` WHERE `Algorithm` LIKE 'kkma' AND `Status` LIKE 'wait' ORDER BY `UploadTime` ASC"
# cursor.execute(query):


def join_phrase(phrase):
    adding = {"ㄴ": 4, "ㄹ": 8, "ㅁ": 16}
    answer = phrase[0]
    for p in phrase[1:]:
        if (p[0] in adding) and ((ord(answer[-1]) - ord("가")) % 28 == 0):
            answer = answer[:-1] + chr(ord(answer[-1]) + adding[p[0]]) + p[1:]
        else:
            answer += p
    return answer


for raw_sentences in speeches:
    mp3_count = 0
    sentences = "".join(list(map(lambda x: x[0] if x[1] == "Josa" else " " + x[0], okt.pos(raw_sentences.strip()))))
    for sentence in kkma.sentences(sentences):
        words = kkma.pos(sentence)
        tree = nltk.RegexpParser(kkma_grammar).parse(words)
        for subtree in tree:
            if isinstance(subtree, nltk.tree.Tree):
                phrase = join_phrase(list(map(lambda x: x[0], subtree.leaves())))
            elif isinstance(subtree, tuple):
                phrase = subtree[0]
            else:
                raise ValueError(str(type(subtree)) + str(subtree))
            print(phrase)
