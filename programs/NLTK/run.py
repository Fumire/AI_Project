import os
import time
import subprocess
import gtts
import nltk
import pydub

speeches = ["In this grave hour, perhaps the most fateful in our history, I send to every household of my peoples, both at home and overseas, this message, spoken with the same depth of feeling for each one of you as if I were able to cross your threshold and speak to you myself. For the second time in the lives of most of us, we are at war. Over and over again, we have tried to find a peaceful way out of the differences between ourselves and those who are now our enemies; but it has been in vain. We have been forced into a conflict, for we are called, with our allies, to meet the challenge of a principle which, if it were to prevail, would be fatal to any civilized order in the world. It is a principle which permits a state, in the selfish pursuit of power, to disregard its treaties and its solemn pledges, which sanctions the use of force or threat of force against the sovereignty and independence of other states. Such a principle, stripped of all disguise, is surely the mere primitive doctrine that might is right, and if this principle were established through the world, the freedom of our own country and of the whole British Commonwealth of nations would be in danger. But far more than this, the peoples of the world would be kept in bondage of fear, and all hopes of settled peace and of the security, of justice and liberty, among nations, would be ended. This is the ultimate issue which confronts us. For the sake of all that we ourselves hold dear, and of the world order and peace, it is unthinkable that we should refuse to meet the challenge. It is to this high purpose that I now call my people at home, and my peoples across the seas, who will make our cause their own. I ask them to stand calm and firm and united in this time of trial. The task will be hard. There may be dark days ahead, and war can no longer be confined to the battlefield, but we can only do the right as we see the right, and reverently commit our cause to God. If one and all we keep resolutely faithful to it, ready for whatever service or sacrifice it may demand, then with God's help, we shall prevail."]

grammar = r"""
NP: {<PRP\$><JJ.*><NN.*>}
    {<RB>?<DT>?<CD|JJ.*|PRP\$>*<NN.*|PRP.?|VBG>+((<,><CD|JJ.*|PRP\$>*<NN.*|PRP.?|VBG>+)*<CC><CD|JJ.*|PRP\$>*<NN.*|PRP.?|VBG>+)?}
    {<JJS><IN><PRP|PRP\$>}
    {<DT>?<WDT|WP><VB|VBP|VBZ>}
    {<DT>}

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


def text_to_mp3(text, file_name):
    subprocess.call(["espeak", "-w" + file_name, "-s140", "\"" + text + "\""])


for speech in speeches:
    mp3_count = 0
    mp3_file = pydub.AudioSegment.silent(duration=0)

    for sentence in nltk.sent_tokenize(speech):
        words = nltk.pos_tag(nltk.word_tokenize(sentence))
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
                tts = gtts.gTTS(phrase, lang="en-GB", lang_check=False)
                tts.save("/tmp/" + str(mp3_count) + ".mp3")
            mp3_count += 1

    for i in range(mp3_count):
        print(i, "/", mp3_count)
        tmp_file = pydub.AudioSegment.from_file("/tmp/" + str(i) + ".mp3")[:-200].fade_in(200).fade_out(200)
        mp3_file += tmp_file
        os.remove("/tmp/" + str(i) + ".mp3")

    mp3_file.export("/data/tmp.mp3", format="mp3")
    print("Done!!")
