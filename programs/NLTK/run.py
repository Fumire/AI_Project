import nltk

speeches = ["For the second time in the lives of most of us, we are at war.", "I ask them to stand calm and firm and united in this time of trial.", "I am running", "Over and over again, we have tried to find a peaceful way out of the differences between ourselves and those who are now our enemies; but it has been in vain.", "We have been forced into a conflict, for we are called, with our allies, to meet the challenge of a principle which, if it were to prevail, would be fatal to any civilized order in the world.", "It is a principle which permits a state, in the selfish pursuit of power, to disregard its treaties and its solemn pledges, which sanctions the use of force or threat of force against the sovereignty and independence of other states.", "Such a principle, stripped of all disguise, is surely the mere primitive doctrine that might is right, and if this principle were established through the world, the freedom of our own country and of the whole British Commonwealth of nations would be in danger.", "But far more than this, the peoples of the world would be kept in bondage of fear, and all hopes of settled peace and of the security, of justice and liberty, among nations, would be ended.", "This is the ultimate issue which confronts us.  For the sake of all that we ourselves hold dear, and of the world order and peace, it is unthinkable that we should refuse to meet the challenge."]

grammar = r"""
NP: {<PRP\$><JJ.*><NN.*>}
    {<RB>?<DT>?<CD|JJ.*|PRP\$>*<NN.*|PRP.?|VBG>+((<,><CD|JJ.*|PRP\$>*<NN.*|PRP.?|VBG>+)*<CC><CD|JJ.*|PRP\$>*<NN.*|PRP.?|VBG>+)?}
    {<JJS><IN><PRP|PRP\$>}
    {<DT>?<WDT|WP><VB|VBP|VBZ>}
    {<DT>}

SP: {<NP><VB|VBZ>}
    {<NP><VBP><VBG|VBN>*}
    {<NP><VBD><RB>?<VB>}
    {<NP><VBD><VBN>}
    {<NP><VBD>}
    {<NP><VBZ><VBN>}

VP: {<MD><VB><VBN>?}

IP: {<IN>+<NP>((<,><NP>)*<CC><NP>)?}
    {<IN>+<CC><RB>+}
    {<IN>+<DT|PDT>}

TN: {<TO><NP>}
TV: {<TO><VB>}

AP: {<DT|RB>?<JJ.*>}
"""

for speech in speeches:
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
