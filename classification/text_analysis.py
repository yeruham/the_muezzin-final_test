def num_word_in_text(word: str, text: list):
    """ calculates how many times a word appears in text."""
    num_matches = 0
    for i in range(len(text)):
        if text[i] == word:
            print(text[i])
            num_matches += 1

    return num_matches



def num_sentence_in_text(sentence: str, text: list):
    """ calculates how many times a sentence appears in text. """
    sentence = sentence.split(" ")
    num_matches = 0
    num_loop = len(text) - len(sentence) + 1
    for i in range(num_loop):
        if text[i: i + len(sentence)] == sentence[:]:
            print(text[i: i + len(sentence)])
            num_matches += 1

    return num_matches


def num_words_in_text(words: list, text: list):
    """ gets a list of problematic words to search in another list.
        return how many times were problematic words detected. """
    num_matches = 0
    for word in words:
        # if the current word it's a sentence
        if len(word.split(" ")) > 1:
            num_matches += num_sentence_in_text(word, text)
        else:
            # if the current word it's a single word
            num_matches += num_word_in_text(word, text)

    return num_matches