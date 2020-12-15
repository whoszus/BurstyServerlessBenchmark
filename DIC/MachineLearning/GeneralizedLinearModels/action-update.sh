docker run --rm -v "$PWD:/tmp" ibmfunctions/action-python-v3.7 bash -c \
"cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirement.txt" &&
zip -r env.zip ./* &&
wsk -i  action update  glm_score  env.zip --kind python:3