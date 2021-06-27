# nlphose
![nlphose](whatisnlphose.gif)
This is a collection of python scripts that perform NLP tasks on output of [twint](https://github.com/twintproject/twint).
Idea is to simply pipe output from twint to these 
scripts. Every script perfroms a different type of NLP operation on tweets, and it's output can be in turn piped to another script.

Currently following scripts are present:
* twint2json.py - converts from default twint format to json
* senti.py - perfroms AFINN based sentiement analysis on the json formatted tweet and appends *afinn_score* field with AFINN afinn_score
* entity.py - performs named entity recognition on json fromatted tweets using [spacy](https://github.com/explosion/spaCy)
* lang.py - performs language identificiation using FastText and [lid.176.ftz](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz) model
* chunk.py - extracts chunks using [NLTK's regex based chunking](https://www.nltk.org/book_1ed/ch07.html) feature. You need to supply a regex and a name for the regex
* xformer.py - Adds power of transformers to the tool. It currently supports these three tasks: 'sentiment-analysis',
                             'question-answering' and 'zero-shot-classification'

  Examples of usage:
  * For 'sentiment-analysis' task, the --pipeline has to be specified as 'sentiment-analysis'
    ```
     ... |  ./xformer.py --pipeline sentiment-analysis  --param "sports#news#history"
    ```
  * For 'question-answering' task, the --param should be the question we want to ask
    ```
    ... |  ./xformer.py --pipeline question-answering  --param 'By how many runs did India win ?'
    ```
  * For 'zero-shot-classification' the --param should be a single string containing labels seperated by '#'
    ```
    ... |  ./xformer.py --pipeline zero-shot-classification  --param "sports#news#history"
    ```           
  Additionally, a GPU device can be specified by adding a optional parameter '--device'


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
cd nlphose/scripts
chmod +x *.py
```


Get positive tweets containing term netflix (AFINN) :
```shell
twint -s netflix |\
./twint2json.py |\
./senti.py |\
./entity.py |\
jq 'if (.afinn_score) > 5 then .text else empty  end'
```
Get positive tweets containing term netflix (transformers) :
```shell
twint -s netflix |\
./twint2json.py |\
./xformer.py --pipeline sentiment-analysis |\
jq 'if (.xfrmr_sentiment_analysis[0].label) == "POSITIVE" then .text else empty  end'
```
Get works of art (TV shows or movie names) in positive tweets containing term netflix :
```shell
twint -s netflix |\
./twint2json.py |\
./senti.py |\
./entity.py |\
jq 'if (.afinn_score) > 5 then .entities|.[]| select(.label == "WORK_OF_ART") | .entity else empty end'
```

Get works of art (TV shows or movie names) in negative tweets containing term netflix :
```shell
twint -s netflix |\
./twint2json.py |\
./senti.py |\
./entity.py |\
jq 'if (.afinn_score) < -5 then .entities|.[]| select(.label == "WORK_OF_ART") | .entity else empty end'
```

Get tweet and people mentioned in postive tweets about premierleague :
```shell
twint -s premierleague |\
./twint2json.py |\
./senti.py |\
./entity.py |\
jq ' if (.afinn_score) > 5 then . as $parent | .entities|.[]| select((.label == "PERSON") and .entity != "Netflix") | [$parent.text,.entity] else empty end'
```
Get tweets about India in hindi
```shell
twint -s india |\
./twint2json.py |\
./lang.py |\
jq ' if .lang == "hi" then .text  else empty  end'
```
Get noun phrases that match (adjective * noun/ noun * noun) in all tweets containing foldscope
```shell
twint -s foldscope |\
./twint2json.py |\
./chunk.py  observation '{<JJ>|<NN?>*<NN>}' |\
jq ' if (.chunks | length) > 0 then .chunks else empty end'
```

Get all tweets containing the word 'rainfall' and extract location which experienced rainfall using quantion-answering task
```shell
twint -s 'rainfall' |\
./twint2json.py |\
./xformer.py --pipeline question-answering --param 'where did it rain' |\
jq '{"text":.text,"answer":.xfrmr_question_answering.answer}'
```

Get all tweets containing the word 'food' and classify if the tweet was about Indian, Italian, Mexican or Chinese food
```shell
twint -s 'food' |\
./twint2json.py |\
./xformer.py --pipeline zero-shot-classification --param 'indian#italian#mexican#chinese'    
```

## Stopping the pipeline without loosing data
Because the output of programs is piped to each other there is always a 'performace mismatch'. Some scripts run faster than others, so buffering needs to be used.
Thankfully, this is automatically handled by the operating system, we need not worry. However, this will lead to increased memory usage over time.
To stop the piped command without loosing any data, you just need to terminate the first command, which in above cases is *twint*.

First we need to find the process id of the process running twint using below command:
```shell
ps -aux |grep twint
```

then kill it using:
```shell
kill - KILL xxxxx
```
Even if the first command is killed, the data is processed by subsequent commands. DO NOT stop the piped command using CTRL+C if you care about data loss. 

## Monitoring progress
Every command in the pipeline will have different rate of processing data. You can easily monitor the progress of each command in the pipeline 
using the *pv* command.

First you will have to download and install *pv* if you dont have it :
```shell
apt-get install pv
```
Once you have the *pv* command installed you need to modify your pipeline to use it at points where you want to monitor output/progress. 

For example, let us look at a sample NLP pipeline:
```shell
twint -s premierleague | ./twint2json.py | ./senti.py | ./entity.py |./chunk.py  observation '{<JJ>|<NN?>*<NN>}' > output.txt
```
The above pipeline finds tweets about *premierleague* and performs sentiment analysis, named entity recognition and chunk extraction before saving 
the output to *output.txt*. Now let us say we want to know how many tweets are being read per second and how many per second complete processing.
To do that we can use *pv -N INPUT -i 2 -l* command. This command reads count  of lines *(-l)* piped into it and shows count of lines received per seconds.
The display is refreshed after two seconds *(-i 2)*. The count is shown with a unique label i.e *INPUT* in this case. 

We can use the *pv* command at multiple positions in our pipes (with different labels), so that we can monitor the performance of overall pipeline at various points.
In the sample below, I have used *pv* command twice, with labels *INPUT* (for incoming tweets) and *PROCESSED* (for processed records).
```shell
twint -s premierleague |pv -N INPUT-i 2 -l|  ./twint2json.py | ./senti.py | ./entity.py |./chunk.py  observation '{<JJ>|<NN?>*<NN>}' | pv -N PROCESSED -i 2 -l > output.txt
```
You should see similar output, when you run the command :

![nlphose.gif](nlphosepv.gif)

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
