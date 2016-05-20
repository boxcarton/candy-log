import sys
from os import path
from wordcloud import WordCloud, STOPWORDS
from collections import defaultdict
from pprint import pprint

def load_data(file_path):
  data = []
  pos_data = []
  neg_data = []

  with open(file_path) as file:
    for line in file:
      sentence = line.split('-')
      words = sentence[5].strip()
      if len(words.split()) > 2: #remove less than 3 words
        score = float(sentence[-1].strip())
        if ' negative ' in sentence:
          score = score * -1
          neg_data.append((words, score))
        else:
          pos_data.append((words, score))
        data.append((words, score))
  return pos_data, neg_data, data

def make_word_cloud(data):
  text = ''
  for d in data:
    text = text + d[0] + ' '

  # Generate a word cloud image
  wordcloud = WordCloud(stopwords=STOPWORDS.add('watson')).generate(text)

  # Display the generated image:
  # the matplotlib way:
  import matplotlib.pyplot as plt
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.show()

def get_stats(data):
  sum_score = 0
  sum_pos_score = 0
  sum_neg_score = 0

  stats = {
    'max_positive': 0.0,
    'max_positive_sentence': '',
    'max_negative': 0.0,
    'max_negative_sentence': '',
    'num_positive': 0,
    'num_neutral': 0,
    'num_negative': 0,
    'average_pos_score': 0.0,
    'average_neg_score': 0.0,
    'average_score': 0.0,
  }  

  for d in data:
    if d[1] == 0:
        stats['num_neutral'] += 1
    elif d[1] > 0:
      stats['num_positive'] += 1
      sum_pos_score += d[1]
      if d[1] > stats['max_positive']:
        stats['max_positive'] = d[1]
        stats['max_positive_sentence'] = d[0]
    else:
      stats['num_negative'] += 1
      sum_neg_score += d[1]
      if d[1] < stats['max_negative']:
        stats['max_negative'] = d[1]
        stats['max_negative_sentence'] = d[0]
    sum_score += d[1]

  total = stats['num_positive'] +\
          stats['num_negative'] + stats['num_neutral']
  total_no_neutral = stats['num_positive'] + stats['num_negative']

  stats['total'] = total
  stats['total_no_neutral'] = sum_score/total_no_neutral
  stats['average_pos_score'] = sum_pos_score/stats['num_positive']
  stats['average_neg_score'] = sum_neg_score/stats['num_negative']
  stats['average_score'] = sum_score/total

def print_to_file(data, filename='output.txt'):
  with open(filename, 'w') as f:
    for d in data:
      f.write(d[0] + ' (' + str(d[1]) + ') ' + '\n')

def main():
  path = 'logs/candy.log'
  if len(sys.argv) > 1:
      path = sys.argv[1]
  pos_data, neg_data, data = load_data(path)
  get_stats(data)
  print_to_file(data)
  make_word_cloud(data)

if __name__ == '__main__':
  main()