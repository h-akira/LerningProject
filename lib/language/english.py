import spacy
import re

POS_DICTIONARY = {
  "NOUN": "名詞",
  "PROPN": "固有名詞",
  "VERB": "動詞",
  "ADJ": "形容詞",
  "ADV": "副詞",
  "ADP": "前置詞",
  "AUX": "助動詞",
  "CONJ": "接続詞",
  "DET": "限定詞",
  "INTJ": "間投詞",
  "NUM": "数詞",
  "PART": "助詞",
  "PRON": "代名詞",
  "PUNCT": "句読点",
  "SCONJ": "連結詞",
  "SYM": "記号",
  "SPACE": "空白",
  "CCONJ": "等位接続詞",
  "X": "その他",
}

POS_CHOICES = (
  ("NOUN", "名詞"),
  ("PROPN", "固有名詞"),
  ("VERB", "動詞"),
  ("ADJ", "形容詞"),
  ("ADV", "副詞"),
  ("ADP", "前置詞"),
  ("AUX", "助動詞"),
  ("CONJ", "接続詞"),
  ("DET", "限定詞"),
  ("INTJ", "間投詞"),
  ("NUM", "数詞"),
  ("PART", "助詞"),
  ("PRON", "代名詞"),
  ("PUNCT", "句読点"),
  ("SCONJ", "連結詞"),
  ("SYM", "記号"),
  ("SPACE", "空白"),
  ("CCONJ", "等位接続詞"),
  ("X", "その他"),
)

def _clean_text(text):
  # Wikipediaに対応するため一律で[2]等を削除
  text = re.sub(r"\[\d+\]", "", text)

def text2SentenceTable(sentence, page, SentenceTable):
  nlp = spacy.load("en_core_web_sm")
  text = _clean_text(text)
  doc = nlp(text)
  data = []  # 各要素は[text, lemma, pos]
  for token in doc:
    data.append([token.text, token.lemma_, token.pos_])
    if token.pos_ not in POS_DICTIONARY.keys():
      raise ValueError(f"Invalid POS: {token.pos_}")
  # SentenceTableでpage=pageであるものを全て削除
  SentenceTable.objects.filter(page=page).delete()
  # SentenceTableに新たに追加
  for text, lemma, pos in data:
    SentenceTable.objects.create(page=page, text=text, lemma=lemma, pos=pos)

def sentence2html(sentence, PrivateDictionaryTable, reverse, name, args):
  html = ""
  top_flag = True
  h_counter = 0
  # 記号や空白、数字はそのまま
  # 他の単語はaタグ
  # 改行ごとにpタグ
  # ただし文頭が#6個までの場合はh1からh6タグを使う
  for token in sentence:
    if top_flag:
      if token.word == "#":
        if h_counter < 6:
          h_counter += 1
      else:
        top_flag = False
        if h_counter > 0:
          html += f'<h{h_counter} class="subtitle is-{h_counter}">' + "{token.word}"
        else:
          html += f"<p>" + "{token.word}"
    else:
      if "\n" in token.word:
        if h_counter > 0:
          html += f" token.word</h{h_counter}>\n"
        else:
          html += f"{token.word}</p>\n"
      else:
        if token.word in [",", ".", "!", "?"]:
          html += token.word
        else:
          html += f" {token.word}"
  return html


















