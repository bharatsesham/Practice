# Load Python's RE library
import re
import random

# References: https://www.nltk.org/api/nltk.chat.html
# The conversation is designed to discuss about a person dream and the feelings associated with it.

def eliza_chatbot(text):
  output_text = None

  # Hello or Hey, -> Hey, how are you today? 
  pattern = '(Hello|Hey|Hi)\.?'
  responses = random.choice(['Hey, how are you feeling today?', 'Hello, Hope you are having a good day.'])
  if output_text is None and re.match(pattern, text): output_text = re.sub(pattern, responses, text)
  
  # dream(s|t|ed)? -> Questions to direct the conversation towards feelings or persons assosiated with the dream.
  pattern = '(.*)?dream(s|t|ed)?(.*)?'
  if output_text is None and re.match(pattern, text):
    responses = random.choice(['Really, \g<2>?', 'Is this the first time you dreamed \g<2>?', 'Have you ever fantasized \g<2> when you are awake?', 'Have you ever dreamed \g<2> before?'])
    if re.search('(?<=I )dreamed', text): output_text = re.sub('(.*)I dreamed(.*)\.?', responses, text)
    responses = random.choice(['How do you feel after you wake up from the dream.', 'How often do you dream?', 'What persons appear in your dreams?'])
    if re.match('(.*)dream(s)?(.*)', text) and output_text is None: output_text = re.sub('(.*)dream(s)?(.*)', responses, text)

  # Collecting more data about the person feelings about relations. 
  pattern = '(.*)?(mother|father|parent(s)?|friend(s)?|co-worker(s)?|child(ren)?)(.*)?'
  if output_text is None and re.match(pattern, text):
    responses = random.choice(['How does this relate to your feelings?', 'Tell me more about your \g<2>.', 'How do you feel about your \g<2>?', 'How did your \g<2> make you feel?', 'What was your relationship with your \g<2> like?'])
    if re.match(pattern, text): output_text = re.sub(pattern, responses, text)

  # Responses for feelings and permissions. 
  pattern = '(.*)sorry(.*)'
  if output_text is None and re.match(pattern, text, flags=re.IGNORECASE): output_text = re.sub(pattern,'Apologies are not necessary.', text, flags=re.IGNORECASE)
  pattern = '(.*)(maybe|perhaps)(.*)'
  if output_text is None and re.match(pattern, text, flags=re.IGNORECASE): output_text = re.sub(pattern, random.choice(['Why the uncertain tone ?', 'You don\'t seem quite certain.']), text, flags=re.IGNORECASE)
  if re.match('^Can I.*', text): output_text = re.sub('Can I (.*)\??', 'If you could \g<1>, would you?', text)
  pattern = '(.*)I feel\s?(.*)(^\?|.?)'
  responses = random.choice(['Tell me more about these feelings.','Do you often feel \g<2>?','When you feel \g<2>, what do you do?','When do you usually feel \g<2>?'])
  if output_text is None and re.match(pattern, text): output_text = re.sub(pattern, responses, text)

  # Responses for No.
  responses = random.choice(['Why \'No\'?', 'Why not?', 'Are you saying no just to be negative?'])
  if output_text is None and re.match('(.*)?No(.*)?', text):output_text = re.sub('(.*)?No(.*)?', responses,text) 

  # Question Samples.
  if output_text is None and re.match('^Yes.*', text):output_text = re.sub('^Yes.*','Why do you say that?',text)
  if output_text is None and re.match(r'^I am\b', text): output_text = re.sub(r'^I am\b','You are',text)
  if output_text is None and re.match('You are (.*)\.', text): output_text == re.sub('You are (.*)\.','I am \g<1>?',text)
  if output_text is None and re.match('.* don\'t feel (.*)', text): output_text = re.sub('.* don\'t feel (.*)\.?','Why do you think you are not \g<1>?',text)
  if output_text is None and re.search('.*((?<=!I\s)feel|am|seem to be)(.*)\.', text): output_text = re.sub('.*(feel|am|seem to be)(.*)\.','When did you start feeling \g<2>?',text)
  if output_text is None and re.match('I need (your)?(.*)\.?', text): output_text = re.sub('I need (your)?(.*)\.?', 'Why do you need \g<2>?', text)

  # Responses tailoured to you & me type of texts. 
  if output_text is None and re.match('^You (.*)', text):output_text = re.sub('^You (.*)', 'Why do you say that about me?', text)
  if output_text is None and re.match('^My (.*)', text):output_text = re.sub('^My (.*)', 'When your \g<1>, how do you feel?', text)

  #Any uncovered question -> Generic Response. (Interrogative Sentences)
  pattern = '(.*)\?'
  responses = random.choice(['Maybe, but I am not entirely sure.','Sorry, I don\'t know.','Why do you ask that?','Why don\'t you tell me?','Life is strange.', 'Perhaps the answer lies within yourself?'])
  if output_text is None and re.match(pattern, text): output_text = re.sub(pattern, responses, text)

  #Any uncovered exclamatory patterns -> Generic Responses. (Exclamatory Sentences) 
  pattern = '(.*)!'
  responses = random.choice(['You seems to have a really some strong emotion today.', 'Oh!'])
  if output_text is None and re.match(pattern, text): output_text = re.sub(pattern, responses, text, flags=re.IGNORECASE) 

  pattern = '(.*)\.?'
  responses = random.choice(['Let\'s change focus a bit... Tell me about your dreams.','I see.  And what does that tell you?', 'How does that make you feel?', 'How do you feel when you say that?', 'Please tell me more...', 'Can you elaborate on that?', 'I see.'])
  if output_text is None and re.match(pattern, text): output_text = re.sub(pattern, responses, text, flags=re.IGNORECASE) 

  if output_text is None: output_text = 'Sorry, I don\'t understand what you are trying to say.'

  # Returning computed response 
  return output_text

if __name__ == "__main__":
  exit_keywords = re.compile('Bye|Goodbye|Exit|Quit', re.IGNORECASE)
  print('Eliza: Hello.  How are you feeling today?')
  while True:
    text = input('You  : ')
    if exit_keywords.search(text):
      break
    else: 
      print('Eliza: '+eliza_chatbot(text))
  print('Eliza: '+ random.choice(['Good-bye', 'Have a nice day.']))
