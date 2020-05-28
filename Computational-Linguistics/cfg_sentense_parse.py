import nltk
from nltk import grammar, parse
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
import re

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


gmr = r"""
% start S
############################
# Grammar Rules
#############################
# S
S[SEM = <?subj(?vp)>] -> NP[SEM=?subj] VP[SEM=?vp]
S[SEM = <\x.(?subj(?vp(x)))>] -> NP[SEM=?subj] VP[SEM=?vp]/NP

# N
N[SEM=<\z.(?nom(z) & ?cp(z))>] -> N[SEM=?nom] CP[SEM=?cp]

# NP
NP[SEM=<?det(?nom)>] -> DT[SEM=?det] N[SEM=?nom]
NP[SEM=?np] -> PN[SEM=?np]

# PP
PP[PFORM=?p,SEM=?np] -> P[PFORM=?p] NP[SEM=?np]
PP[PFORM=passive_by]/NP -> P[PFORM=passive_by]

# ADJ
N[SEM=<?adj(?nom)>] -> ADJ[SEM=?adj] N[SEM=?nom]

# VP
VP[SEM=<?v(?pp,?obj)>] -> DTV[SEM=?v] NP[SEM=?obj] PP[PFORM=none,SEM=?pp]
# VP[VC=pass,SEM=<?v(\P.P(w))>]/NP -> TV[VC=pass,SEM=?v] PP[PFORM=passive_by]/NP
VP[SEM=<?vp(?pp)>] -> VP[SEM=?vp] PP[PFORM=none, SEM=?pp]
VP[VC=pass,SEM=<\x y.(?v(\P.P(x))(y))>]/NP -> TV[VC=pass,SEM=?v] PP[PFORM=passive_by]/NP
VP[SEM=<?vp>]/NP -> BE VP[VC=pass,SEM=?vp]/NP

# TV
TV[VC=pass,SEM=<(\R Q z.Q(\w. (((R(\T.T))(w))(z))))(?tv)>] -> TV[VC=act,SEM=?tv]

# CP
CP[SEM=<?s>] -> C S[SEM=?s]


#############################
# Lexical entries
#############################

# Common Nouns
N[SEM=<\x.bar(x)>] -> 'bar'
N[SEM=<\x.waiter(x)>] -> 'waiter'
N[SEM=<\x.detective(x)>] -> 'detective'

# Proper Names
PN[SEM=<\P.P(sam)>] -> 'sam'

# Determiners
DT[SEM=<\P Q.exists x.(P(x) & Q(x))>] -> 'a'
DT[SEM=<\P Q.all x.(P(x) -> Q(x))>] -> 'every'
DT[SEM=<\P Q.exists x.(P(x) & Q(x))>] -> 'the'

# Prepositions
P[PFORM=passive_by] -> 'by'
P[PFORM=none, SEM=<\P Q x.(Q(x) & P(\y.in(x,y)))>] -> 'in'

# Adjectives
ADJ[SEM=<\P x.(P(x) & male(x))>] -> 'male'

# Complementizer
C -> 'that'

# Verb
TV[VC=act,SEM=<\P x.P(\y.arrest(x,y))>] -> 'arrest'
DTV[SEM=<\P Q x.Q(\z.P(\y.interview(x,y,z)))>] -> 'interviewed'

BE -> 'be'


"""
# Load grammar
grammar_exam = nltk.grammar.FeatureGrammar.fromstring(gmr)

# A detective that Sam was arrested by interviewed every male waiter in the bar.
V = r"""
sam => a
female => {f}
detective => {b}
bar => {c}
arrest => {(b,a)}
interview => {(b,c,a)}
male => {a}
waiter => {a,f}
in => {(a,c)}
"""

# Load model valuations
val = nltk.Valuation.fromstring(V)
# Initialize assignment g
g = nltk.Assignment(val.domain)
# Create model
m = nltk.Model(val.domain, val)
parser = nltk.parse.FeatureChartParser(grammar_exam)

def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:          
        return None

def preprocess_sentence(sentence):
    sentence = sentence.lower()
    sentence = sentence.rstrip(r'\.$')
    lemmatizer = WordNetLemmatizer() 
    tokenized_input =  word_tokenize(sentence)
    pos_tags = nltk.pos_tag(tokenized_input)
    pos_tags=[nltk_tag_to_wordnet_tag(x[1]) for x in nltk.pos_tag(tokenized_input)]
    lemmatized_input = [lemmatizer.lemmatize(word,tag) if tag else lemmatizer.lemmatize(word) for word,tag in zip(tokenized_input,pos_tags) ]
    return " ".join(lemmatized_input)

# if __name__ == "__main__":
# A detective that Sam was arrested by interviewed every male waiter in the bar.
inp = "A detective that Sam was arrested by interviewed every male waiter in the bar." 
pre_proc_text = preprocess_sentence(inp)
print(pre_proc_text)
tokens = pre_proc_text.split()
parses = [tree.label()['SEM'] for tree in parser.parse(tokens)] 
# print(parses)
for tree in parser.parse(tokens):
    print(tree)

flag = m.evaluate(str(parses[0]), g)
print(flag)
