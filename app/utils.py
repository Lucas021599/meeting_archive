from meeting_archive.settings import SENTENCE_MODEL


def embed_text(text):
    return SENTENCE_MODEL.encode(text).tolist()
