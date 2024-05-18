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
  # print("---- before cleaning ----")
  # print(text)
  # [2]のような文字列を削除
  text = re.sub(r"\[\d+\]", "", text)
  # [b]のような文字列を削除
  text = re.sub(r"\[\w+\]", "", text)
  # print("---- after cleaning ----")
  # print(text)
  return text

def text2SentenceTable(sentence, page, SentenceTable):
  nlp = spacy.load("en_core_web_sm")
  text = _clean_text(sentence)
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
    SentenceTable.objects.create(page=page, word=text, lemma=lemma, pos=pos)


def s2a_tag(s, reverse, new_tab=False):
  # アルファベットを含まない場合はそのまま表示
  for w in list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    if w in s.lemma:
      break
  else:
    return s.word
  if new_tab:
    html = f'<a href="{reverse("english:s2dic", args=[s.id])}" target="_blank" rel="noopener noneferrer">{s.word}</a>'
  else:
    html = f'<a href="{reverse("english:s2dic", args=[s.id])}">{s.word}</a>'
  return html

def sentence2html(sentence, reverse, no_html=False, new_tab=False):
  html = ""
  top_flag = True
  tail_flag = False
  h_counter = 0
  # 記号や空白、数字はそのまま
  # 他の単語はaタグ
  # 改行ごとにpタグ
  # ただし文頭が#6個までの場合はh1からh6タグを使う
  for s in sentence:
    if top_flag:
      end_flag = False
      if s.word == "#":
        if h_counter < 6:
          h_counter += 1
      else:
        top_flag = False
        if h_counter > 0:
          if no_html:
            html += "#" * h_counter + " " + s.word
          else:
            html += f'<h{h_counter} class="subtitle is-{h_counter}">' + f"{s2a_tag(s, reverse, new_tab=new_tab)}"
        else:
          if no_html:
            html += s.word
          else:
            html += f"<p>" + f"{s2a_tag(s, reverse, new_tab=new_tab)}"
    else:
      if "\n" in s.word:
        if h_counter > 0:
          if no_html:
            html += f" {s.word}\n"
          else:
            html += f" {s2a_tag(s, reverse, new_tab=new_tab)}</h{h_counter}>\n"
        else:
          if no_html:
            html += f" {s.word}\n"
          else:
            html += f" {s2a_tag(s, reverse, new_tab=new_tab)}</p>\n"
        top_flag = True
        end_flag = True
        h_counter = 0
      else:
        if s.word in [",", ".", "!", "?", ":", ";"] or s.word[0]=="'":
          html += s.word
        else:
          if no_html:
            html += f" {s.word}"
          else:
            html += f" {s2a_tag(s, reverse, new_tab=new_tab)}"
  if end_flag:
    return html
  else:
    if h_counter > 0:
      if no_html:
        return html+"\n"
      else:
        return html + f"</h{h_counter}>"
    else:
      if no_html:
        return html+"\n"
      else:
        return html + "</p>"


















