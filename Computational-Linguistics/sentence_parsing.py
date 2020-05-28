import nltk
nltk.download('treebank')
from nltk.corpus import treebank


# Define CFG
my_grammar = nltk.CFG.fromstring("""
  S -> NP VP
  PP -> P NP
  N -> N PP
  NP -> PN | PRN | DT N | PN
  VP -> TV NP | VP PP | ADV VP | DTV NP NP | DTV NP PP | SV S | IV
  N -> 'put' | 'block' | 'box' | 'table' | 'hallway' | 'outside' | 'bedroom'| 'stairs' | 'window' | N PP | ADJ N
  DTV -> 'put' | 'gave' | 'sent' | 'offer' | 'supply'
  P -> 'in' | 'on' | 'outside' | 'near' | 'by'
  ADV -> 'in' | 'on' | 'near' | 'by' | 'really'
  ADJ -> 'in' | 'on' | 'table' | 'outside' | 'bedroom' | 'near'
  SV -> 'thought' | 'feared' | 'denied' | 'shouted' | 'wished'
  TV -> 'block' | 'box' | 'table' | 'print'
  PN -> 'France' | 'Australia' | 'Tom' | 'Bharat' | 'Italy'
  PRN -> 'I' | 'it' | 'we' | 'she' | 'he'
  DT -> 'a' | 'the' | 'each' | 'a' | 'most' 
  IV -> 'died' | 'smiled' | 'fainted' | 'shouted' | 'arrived'
""")

# Input to be parsed (as a list of tokens)
sent = ['I', 'put', 'the', 'block', 'in', 'the', 'box', 'on', 'the', 'table', 'in', 'the', 'hallway', 'outside', 'the', 'bedroom', 'near', 'the', 'stairs', 'by', 'the', 'window']

# Load parser
parser = nltk.ChartParser(my_grammar)

# Show all parses
for num, tree in enumerate(parser.parse(sent)):
  print(num, tree)