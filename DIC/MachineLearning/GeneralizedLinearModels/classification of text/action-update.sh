docker run --rm -v "$PWD:/tmp" ibmfunctions/action-python-v3.7 bash -c \
"cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirement.txt" &&
zip -r env.zip ./* &&
wsk -i  action update  TextClassification  env.zip --kind python:3