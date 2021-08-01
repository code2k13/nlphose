 
 # Realtime Language Identification On Tweets Containing Netflix 

 To run this example you need following software
 * Docker
 * ngrok (optional, not required if your OS has GUI)
 * Internet Browser


## Lets start nlphose docker container

Run the below code at shell/command prompt. It should start *'bash'* inside the container 
```shell
docker run --rm -it -p 3000:3000 code2k13/nlphose:latest
```   
Copy  paste the below command inside the container's shell prompt. It will start the nlphose pipeline
## Lets run the pipeline inside the container
```shell
twint -s "netflix" |\
./twint2json.py |\
./lang.py |\
jq -c '[.id,.lang]' |\
./ws.js
```

## Let's expose the port on internet (optional)
If you are running this pipeline on a headless server (no browser), you can expose port 3000 of your host machine over the internet using ngrok. 
```shell
./ngrok http 3000
```

## Run the demo
Edit the *'netflix_languages_demo'* page. Update the following line in the file with ngrok url
```javascript
var endpointUrl = "https://your_ngrok_url"
```

If you are not using ngrok, and have browser installed on your system (which is running the docker container), simply change the line to:
```javascript
var endpointUrl = "http://localhost:3000"
```

You should a webpage like the one shown below:

 