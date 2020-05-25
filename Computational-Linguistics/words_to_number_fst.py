import re

state = 'q0'

text = "thirty" #@param {type:"string"}
text = text.rstrip()
text = text.lower()
text = text.replace("-", " ")
text = text.split(" ")

_state_0_1 ={"twenty":"2", "thirty":"3", "forty":"4", "fifty":"5", "sixty":"6", "seventy":"7", "eighty":"8", "ninety":"9"}
_state_0_2 = {"":"0", "one":"1", "two":"2", "three":"3", "four":"4", "five":"5", "six":"6", "seven":"7", "eight":"8", "nine":"9", "ten":"10", "eleven":"11", "twelve":"12", "thirteen":"13", "fourteen":"14", "fifteen":"15", "sixteen":"16", "seventeen":"17", "eighteen":"18", "nineteen":"19"}

output = ''
exit =False

text.reverse()
while True:
    token = text.pop() if text else ""
    if state == 'q0':
        if token in _state_0_1:
            state = 'q1'
            output += _state_0_1.get(token)
        elif token in _state_0_2:
            state = 'q2'
            output += _state_0_2.get(token)
            break
    if state == 'q1':
            state = 'q0'        

print(output)