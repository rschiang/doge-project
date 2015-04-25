import hashlib
import random
from datetime import datetime
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image

doge_flavors = [
    'wow', 'wow', 'wow', 'wowah', 'amaze', 'shibaaarrr', 'plz no',
]

doge_prefixes = [
    'so {}', 'much {}', 'many {}', 'very {}', 'such {}', 'how to {}?',
    'good {}', 'nice {}'
]

doge_colors = ['#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5',
    '#2196f3', '#03a9f4', '#00bcd4', '#009688', '#4caf50', '#8bc34a',
    '#cddc39', '#ffeb3b', '#ffc107', '#ff9800', '#ff5722', '#795548']

def dogify(keywords):
    sentences = []
    for keyword in keywords:
        sentences.append(random.choice(doge_prefixes).format(keyword))
    sentences += (random.sample(doge_flavors, random.randint(3, 5)))
    return sentences

def generate(keywords, slug=None):
    sentences = dogify(keywords)
    with Drawing() as draw:
        draw.font = 'assets/comic_sans.ttf'
        draw.text_antialias = True
        with Image(filename='assets/doge.jpg') as source:
            with source.convert('png') as doge:
                for sentence in sentences:
                    draw.fill_color = Color(random.choice(doge_colors))
                    draw.font_size = random.randint(24, 48)
                    metrics = draw.get_font_metrics(doge, sentence)
                    x = random.randint(0, int(doge.width - metrics.text_width))
                    y = random.randint(0, int(doge.height - metrics.text_height))
                    draw.text(x, y, sentence)
                draw.draw(doge)
                timestamp = hashlib.sha1(datetime.now().isoformat(' ').encode()).hexdigest()
                if slug:
                    doge.save(filename=('files/{}-{}.png'.format(timestamp, slug)))
                else:
                    doge.save(filename=('files/{}.png'.format(timestamp)))
