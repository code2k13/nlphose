# nlppipe
This is a collection of python scripts that perform NLP tasks on output of [twint](https://github.com/twintproject/twint).
Idea is to simply pipe output from twint to these 
scripts. Every script perfroms a different type of NLP operation on tweets, and it's output can be in turn piped to another script.

Currently following scripts are present:
* twint2json.py - converts from default twint format to json
* senti.py - perfroms AFINN based sentiement analysis on the json formatted tweet and appends *afinn_score* field with AFINN afinn_score
* entity.py - performs named entity recognition on json fromatted tweets using [spacy](https://github.com/explosion/spaCy)

## Prerequisites

* Python 3 
* Linux

## Installations
Execute the below commands to install everything that is required.
```shell
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

If jq is not installed on your system, you will need to install it aswell
```shell
apt-get install jq
```



## Usage Examples

Make sure you are in the */scripts* folder:
```shell
cd scripts
```


Get positive tweets containing term netflix :
```shell
twint -s netflix | python3 twint2json.py | python3 senti.py | python3 entity.py | jq 'if (.afinn_score) > 5 then .tweet else empty  end'
```

Get works of art (TV shows or movie names) in positive tweets containing term netflix :
```shell
twint -s netflix | python3 twint2json.py | python3 senti.py | python3 entity.py | jq 'if (.afinn_score) > 5 then .entities|.[]| select(.label == "WORK_OF_ART") | .entity    else empty  end'
```

Get works of art (TV shows or movie names) in negative tweets containing term netflix :
```shell
twint -s netflix | python3 twint2json.py | python3 senti.py | python3 entity.py | jq 'if (.afinn_score) < -5 then .entities|.[]| select(.label == "WORK_OF_ART") | .entity    else empty  end'
```

Get tweet and people mentioned in postive tweets about premierleague :
```shell
twint -s premierleague | python3 twint2json.py | python3 senti.py | python3 entity.py | jq ' if (.afinn_score) > 5 then . as $parent | .entities|.[]| select((.label == "PERSON") and .entity != "Netflix") | [$parent.tweet,.entity]     else empty  end'
```

 

## Acknowledgements

> Finn Årup Nielsen, “A new ANEW: evaluation of a word list for sentiment analysis in microblogs”, Proceedings of the ESWC2011 Workshop on ‘Making Sense of Microposts’: Big things come in small packages. Volume 718 in CEUR Workshop Proceedings: 93-98. 2011 May. Matthew Rowe, Milan Stankovic, Aba-Sah Dadzie, Mariann Hardey (editors)