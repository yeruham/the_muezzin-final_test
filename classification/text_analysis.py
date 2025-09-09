def num_word_in_text(word: str, text: list):
    num_matches = 0
    for i in range(len(text)):
        if text[i] == word:
            print(text[i])
            num_matches += 1

    return num_matches



def num_sentence_in_text(sentence: str, text: list):
    sentence = sentence.split(" ")
    num_matches = 0
    num_loop = len(text) - len(sentence) + 1
    for i in range(num_loop):
        if text[i: i + len(sentence)] == sentence[:]:
            print(text[i: i + len(sentence)])
            num_matches += 1

    return num_matches


def num_words_in_text(words: list, text: list):
    num_matches = 0
    for word in words:
        if len(word.split(" ")) > 1:
            num_matches += num_sentence_in_text(word, text)
        else:
            num_matches += num_word_in_text(word, text)
    return num_matches