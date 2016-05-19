import sys
from os import path
from wordcloud import WordCloud

def load_data(file_path):
  data = []
  with open(file_path) as file:
    for line in file:
      sentence = line.split('-')
      words = sentence[5].strip()
      score = float(sentence[-1].strip())
      data.append((words, score))

  return data

def make_word_cloud(data):
  text = ''
  for d in data:
    text = text + d[0] + ' '

  # Generate a word cloud image
  wordcloud = WordCloud().generate(text)

  # Display the generated image:
  # the matplotlib way:
  import matplotlib.pyplot as plt
  plt.imshow(wordcloud)
  plt.axis("off")

  # take relative word frequencies into account, lower max_font_size
  wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
  plt.figure()
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.show()


def main():
  path = 'logs/candy.log'
  if len(sys.argv) > 1:
      path = sys.argv[1]
  data = load_data(path)
  make_word_cloud(data)

if __name__ == '__main__':
  main()