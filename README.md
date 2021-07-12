# nlphose : Command-line 🛠️tools for creating NLP pipelines

Nlphose is a set of command-line tools that enables creation of complex NLP pipelines within seconds. 
It currently supports following operation on static files and streaming data:

 

* Sentiment Analysis (AFINN)
* NER (Spacy)
* Language Identification (FastText)
* Chunking (NLTK)
* Sentiment Analysis (Transformers)
* Question Answering (Transformers)
* Zero shot Classification (Transformers)


👇🏻Below is a sample pipeline that streams in 🗨️ tweets containing the term ⛈️'rainfall' and tries to guess the 🏙️ place it rained using extractive question answering.

```shell
twint -s 'rainfall' |\
./twint2json.py |\
./xformer.py --pipeline question-answering --param 'where did it rain' |\
jq '{"text":.text,"answer":.xfrmr_question_answering.answer}'
```

## 😮😮😮 Looks interesting ??

Checkout the 🔗[installation guide ](https://github.com/code2k13/nlphose/wiki/Installing) and 🔎[some usage examples](https://github.com/code2k13/nlphose/wiki/Quickstart). Please refer to the wiki for 📖[detailed documentation](https://github.com/code2k13/nlphose/wiki/Introduction)

## GUI Pipeline Builder (WIP)
I am also working on a GUI Pipeline buider tool which allows users to create a pipeline by simply drag-and-drop

![](https://github.com/code2k13/nlphoseGUI/blob/main/images/drag_drop_nlphose.gif?raw=true)

For more details visit it's repository : [https://github.com/code2k13/nlphoseGUI](https://github.com/code2k13/nlphoseGUI)