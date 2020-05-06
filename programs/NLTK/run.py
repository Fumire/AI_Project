import nltk

speech = input("Enter: ")

for sentence in nltk.sent_tokenize(speech):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged)

    parser = nltk.parse.corenlp.CoreNLPParser()
    parsed_sentence = parser.raw_parse(sentence)

    print(parsed_sentence)
