docker run --rm -v "$PWD:/tmp" ibmfunctions/action-python-v3.7 bash -c \
"cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirement.txt" && \
zip -r env.zip ./*.py virtualenv && \

wsk -i  action update  Kmeans env.zip --kind python:3