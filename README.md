
# TODO list

Make sure you have an instance of mongodb running. Alternatively you can use a docker image

## Requirements

- python 3.6+


```sh
docker run -d -p 27017:27017 mongo:3.6.5-jessie
```

## Install dependencies

```sh
pip install flask mongoengine
```

## Run server

```
python app.py
```