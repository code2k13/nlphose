# nlppipe
This is a collection of python scripts that perform NLP tasks on output of [twint](https://github.com/twintproject/twint).
Idea is to simply pipe output from twint to these 
scripts. Every script perfroms a different type of NLP operation on tweets, and it's output can be in turn piped to another script.

Currently following scripts are present:
* twint2json.py - converts from default twint format to json
* senti.py - perfroms AFINN based sentiement analysis on the json formatted tweet and appends *afinn_score* field with AFINN afinn_score
* entity.py - performs named entity recognition on json fromatted tweets using [spacy](https://github.com/explosion/spaCy)
* lang.py - performs language identificiation using FastText and [lid.176.ftz](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz) model

## Prerequisites

* Python 3 
* Linux

## Installations
Execute the below commands to install everything that is required.
```shell
pip install -r requirements.txt
python -m spacy download en_core_web_sm
git clone https://github.com/code2k13/nlppipe
```

If jq is not installed on your system, you will need to install it aswell
```shell
apt-get install jq
```



## Usage Examples

Make sure you are in the */scripts* folder:
```shell
cd nlppipe/scripts
chmod +x *.py
```


Get positive tweets containing term netflix :
```shell
twint -s netflix | ./twint2json.py | ./senti.py | ./entity.py | jq 'if (.afinn_score) > 5 then .tweet else empty  end'
```

Get works of art (TV shows or movie names) in positive tweets containing term netflix :
```shell
twint -s netflix | ./twint2json.py | ./senti.py | ./entity.py | jq 'if (.afinn_score) > 5 then .entities|.[]| select(.label == "WORK_OF_ART") | .entity    else empty  end'
```

Get works of art (TV shows or movie names) in negative tweets containing term netflix :
```shell
twint -s netflix | ./twint2json.py | ./senti.py | ./entity.py | jq 'if (.afinn_score) < -5 then .entities|.[]| select(.label == "WORK_OF_ART") | .entity    else empty  end'
```

Get tweet and people mentioned in postive tweets about premierleague :
```shell
twint -s premierleague | ./twint2json.py | ./senti.py | ./entity.py | jq ' if (.afinn_score) > 5 then . as $parent | .entities|.[]| select((.label == "PERSON") and .entity != "Netflix") | [$parent.text,.entity]     else empty  end'
```
Get tweets about India in hindi
```shell
 twint -s india | ./twint2json.py | ./lang.py | jq ' if .lang == "hi" then .text  else empty  end'
```
 

## Acknowledgements

> Finn Årup Nielsen, “A new ANEW: evaluation of a word list for sentiment analysis in microblogs”, Proceedings of the ESWC2011 Workshop on ‘Making Sense of Microposts’: Big things come in small packages. Volume 718 in CEUR Workshop Proceedings: 93-98. 2011 May. Matthew Rowe, Milan Stankovic, Aba-Sah Dadzie, Mariann Hardey (editors)

[1] A. Joulin, E. Grave, P. Bojanowski, T. Mikolov, [Bag of Tricks for Efficient Text Classification](https://arxiv.org/abs/1607.01759)
>@article{joulin2016bag,
  title={Bag of Tricks for Efficient Text Classification},
  author={Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Mikolov, Tomas},
  journal={arXiv preprint arXiv:1607.01759},
  year={2016}
}



[2] A. Joulin, E. Grave, P. Bojanowski, M. Douze, H. Jégou, T. Mikolov, [FastText.zip: Compressing text classification models](https://arxiv.org/abs/1612.03651)
>@article{joulin2016fasttext,
  title={FastText.zip: Compressing text classification models},
  author={Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Douze, Matthijs and J{\'e}gou, H{\'e}rve and Mikolov, Tomas},
  journal={arXiv preprint arXiv:1612.03651},
  year={2016}
}