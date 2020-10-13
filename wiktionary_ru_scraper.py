# coding: utf_8
# Script for looking up Russian word conjugations
# Will prompt for search word and (hopefully) return conjugations

import requests
import csv
from bs4 import BeautifulSoup

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class WordError(Error):
    """Exception raised when search terms not found

    Attributes:
        expression -- search term not found
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

infinitive = input('Which word do you want to search for? ')
translation = input('What is the translation? ')
print('\n')
wiki_url = 'https://en.wiktionary.org/wiki/' + infinitive
try: 
  response = requests.get(wiki_url)
  if response.status_code != 200:
    raise WordError(infinitive, 'Word not found')

  soup = BeautifulSoup(response.content, 'html.parser')

  table = soup.find(class_="inflection-ru")

  if not table:
    raise WordError(infinitive, 'Russian conjugations not found')

  imperfective = bool(table.find(text='imperfective aspect'))

  pronouns = ['I', 'You (inf)', 'He/she', 'We', 'You', 'They']

  if imperfective:
    present_conjugations = [
      ['я', '1|s|pres|ind-form-of'],
      ['ты', '2|s|pres|ind-form-of'],
      ['он/она/оно', '3|s|pres|ind-form-of'],
      ['мы', '1|p|pres|ind-form-of'],
      ['вы', '2|p|pres|ind-form-of'],
      ['они', '3|p|pres|ind-form-of']
    ]

    for conjugation in present_conjugations:
      word = table.find(class_=conjugation[1]).find('a')['title']
      print(f'{conjugation[0]} {word}')
  
  else: 
    future_conjugations = [
      ['я', '1|s|fut|ind-form-of'],
      ['ты', '2|s|fut|ind-form-of'],
      ['он/она/оно', '3|s|fut|ind-form-of'],
      ['мы', '1|p|fut|ind-form-of'],
      ['вы', '2|p|fut|ind-form-of'],
      ['они', '3|p|fut|ind-form-of']
    ]

    for conjugation in future_conjugations:
      word = table.find(class_=conjugation[1]).find('a')['title']
      print(f'{conjugation[0]} {word}')

  past_pronouns = ['He', 'She', 'It', 'They']

  past_conjugations = [
      ['я/ты/он', 'm|s|past|ind-form-of'],
      ['я/ты/она', 'f|s|past|ind-form-of'],
      ['я/ты/оно', 'n|s|past|ind-form-of'],
      ['мы/вы/они', 'p|past|ind-form-of']
    ]

  for conjugation in past_conjugations:
    word = table.find(class_=conjugation[1]).find('a')['title']
    print(f'{conjugation[0]} {word}')

  print('\n')
  for pronoun in pronouns:
    print(f'{pronoun} + {translation}')
  for pronoun in past_pronouns:
    print(f'{pronoun} + {translation} (past)')


except WordError as error:
  print(f'This word could not be found - {error.expression}')
  print(error.message)

