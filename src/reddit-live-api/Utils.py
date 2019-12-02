import re
import string
import collections

def rank_items(items):
    counts = collections.Counter(items)
    new_list = sorted(items, key=lambda x: (counts[x], x), reverse=True)
    items = list(dict.fromkeys(new_list))
    return items


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

    return comment