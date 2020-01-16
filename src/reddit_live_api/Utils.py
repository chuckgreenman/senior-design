import re
import string
import collections
from enum import Enum
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class SubmissionType(Enum):
    NEW = 1,
    TOP = 2,
    HOT = 3,
    CONTROVERSIAL = 4


class SubmissionAttribute(Enum):
    TITLE = 1,
    TEXT = 2


class TimeFrame(Enum):
    HOUR = 'hour',
    DAY = 'day',
    WEEK = 'week',
    MONTH = 'month',
    YEAR = 'year',
    ALL = 'all'


def rank_items(items):
    counts = collections.Counter(items)
    new_list = sorted(items, key=lambda x: (counts[x], x), reverse=True)
    items = list(dict.fromkeys(new_list))
    return items


# Removes links and punctuation from input sentence. This allows for easy analysis.
def scrub_text(comment):
    comment = comment.replace('\n', '')
    comment = comment.replace('"', '')

    # Remove all links that are linked via a word
    m = re.search(r'(\[\S+\])\(https?://.*?\)', comment)
    while m:
        word = m.group(1).replace('[', '').replace(']', '')
        comment = comment.replace(m.group(0), word)
        m = re.search(r'(\[\S+\])\(https?://.*?\)', comment)

    # Remove all static links
    comment = re.sub(r'https?://\S+', '', comment)  # remove links

    # Remove all punctuation and make lowercase
    comment = comment.translate(str.maketrans('', '', string.punctuation)).lower()

    # Remove special characters which aren't included in punctuation for some reason
    comment = re.sub('—', ' ', comment)
    comment = re.sub('’', '', comment)
    comment = re.sub('‘', '', comment)

    return comment


# Removes all stopwords from the input sentence. This leaves only "important" words behind for analysis.
# Can either pass sentence as string or as a list of already tokenized words.
def remove_stopwords(sentence, tokenized=False):
    stop_words = set(stopwords.words('english'))
    word_tokens = sentence
    if not tokenized:
        word_tokens = word_tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence
