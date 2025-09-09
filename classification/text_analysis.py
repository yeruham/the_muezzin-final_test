less_hostile_words = "RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=="
hostile_words = "R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT"


def num_word_in_text(self, word: str, text: str):
    num_matches = 0
    list_text = text.split(' ')
    for i in range(len(list_text)):
        if list_text[i] == word:
            num_matches += 1

    return num_matches



def num_sentence_in_text(self, sentence: str, text: str):
    sentence = sentence.split(" ")
    list_text = text.split(" ")
    num_matches = 0
    num_loop = len(list_text) - len(sentence) + 1
    for i in range(num_loop):
        print(list_text[i])
        if list_text[i: i + len(sentence)] == sentence[:]:
            num_matches += 1

    return num_matches