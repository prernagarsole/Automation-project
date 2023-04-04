import random
import emoji
from flask import Flask, request, render_template, jsonify
import nlpaug
import random
import emoji
import string
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.char as nac
import nltk
import random
from textaugment import EDA, Wordnet

nltk.download('stopwords')

app = Flask(__name__)

# instantiate augmenters outside of routes for better performance
t = EDA()
t1 = Wordnet()
syn_aug = naw.SynonymAug(aug_src='wordnet')
ocr_aug = nac.OcrAug()
kb_aug = nac.KeyboardAug()
char_ins_aug = nac.RandomCharAug('insert')
char_swap_aug = nac.RandomCharAug('swap')
char_del_aug = nac.RandomCharAug('delete')
ant_aug = naw.AntonymAug()


@app.route('/')
def my_form():
    return render_template('index.html', input_text="")


@app.route('/index', methods=['POST'])
def my_form_post():
    text = request.form['text']
    result = []
    if request.form['group1'] == 'Positive':
        result = [
            ["Random word swap: ", t.random_swap(text)],
            ["Random word delete: ", t.random_deletion(text, p=0.3)],
            ["Random word insert: ", t.random_insertion(text)],
            ["Synonym Augmentation: ", syn_aug.augment(text, n=1)],
            ["OCR Augmentation: ", ocr_aug.augment(text, n=1)],
            ["KeyBoard Augmentation: ", kb_aug.augment(text, n=1)],
            ["Random Char insert", char_ins_aug.augment(text, n=1)],
            ["Random Char swap", char_swap_aug.augment(text, n=1)],
            ["Random Char delete", char_del_aug.augment(text, n=1)],
        ]
    else:
        result = evaluate_negative_augmentation(text)

    return render_template('index.html', result=result, input_text=text)


def evaluate_negative_augmentation(text):
    t = EDA()
    words = text.split(" ")

   # half_txt = " ".join(words[:int(len(words) / 2)])
    rem_txt = " ".join(words[int(len(words) / 2):])
    n = int(len(words) / 2)
    result = []

    # 0. replace with emojis
    result.append(["Text to emoji: ", text_to_emoji(text)])
    # 1. make antonym of whole text
    result.append(["Antonym of text: ", naw.AntonymAug().augment(text, n=1)])
    # 2. insert n words in the half sentence, where n = half of size of sentence
    try:
        rand_index = random.randint(0, n)
        result.append(["Insert sentence: ", t.random_insertion(sentence=words[rand_index], n=n) + " " + rem_txt])
        #result.append(["Insert sentence: ", t.random_insertion(sentence=words[rand_index], n=n) + " " + " ".join(words)])
    except:
        pass
    # 3. make antonym of whole text and insert a special character at any position
    result.append(["Special character insertion: ", get_with_special_char(text)])
    # 4. swap half of the sentence
    #result.append(["Swap in the sentence: ", t.random_swap(half_txt) + " " + rem_txt])
    half_txt = " ".join(words[:n])
    shuffled_half_txt = " ".join(random.sample(half_txt.split(), len(half_txt.split())))
    result.append(["Swap in the sentence: ", shuffled_half_txt + " " + " ".join(words[n:])])
    # 5. insert one random word in half text
    result.append(["Sentence insertion: ", t.random_insertion(half_txt) + " " + rem_txt])
    return result


# This function is used to convert words in a sentence to corresponding emojis.
# def text_to_emoji(text):
#     """
#     Replaces words with possible emojis.
#     """
#     text = text.replace(",", "").replace(".", "")
#     new_sentence = " ".join([":" + s + ":" for s in text.split(" ")])
#     emojized = emoji.emojize(new_sentence).split(" ")
#
#     sent = []
#     for each in emojized:
#         if each in emoji.UNICODE_EMOJI['en']:
#             sent.append(each)
#         else:
#             sent.append(each.replace(":", ""))
#     return " ".join(sent)


def text_to_emoji(text):
    """
    Replaces words with possible emojis.
    """
    text = text.replace(",", "").replace(".", "")
    new_sentence = " ".join([":" + s + ":" for s in text.split(" ")])
    emojized = emoji.emojize(new_sentence, use_aliases=True).split(" ")

    sent = []
    for each in emojized:
        if each in emoji.UNICODE_EMOJI['en']:
            sent.append(each)
        else:
            sent.append(each.replace(":", ""))

    if len(sent) > 0:
        index = random.randrange(len(sent))
        sent[index] = "🤔"
    else:
        sent.append("😕")  # add a default emoji if no emojis were found
    return " ".join(sent)


def get_with_special_char(text):
    """
        replace char in text
        """
    # get random indexes to be replaced with special characters which will be 35% of sentence but not more than 15 chars
    indexes = random.sample(range(0, len(text)), min(round(len(text) * 35 / 100), 15))
    for index in indexes:
        text = text[:index] + random.choice(string.punctuation) + text[index + 1:]

    return text


if __name__ == "__main__":
    app.run(debug=True)
