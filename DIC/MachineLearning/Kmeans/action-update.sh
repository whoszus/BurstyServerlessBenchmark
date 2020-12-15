docker run --rm -v "$PWD:/tmp" ibmfunctions/action-python-v3.7 bash -c "cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && apt-get update && apt-get -y install ffmpeg && apt-get clean"



wsk -i  action update  Kmeans __main__.py --kind python:3