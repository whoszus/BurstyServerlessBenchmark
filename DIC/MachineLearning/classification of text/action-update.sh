docker run --rm -v "$PWD:/tmp" tinker.siat.ac.cn/tinker/siat-serverless-ow-py:t.1.0 bash -c \
"cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirement.txt" &&
zip -r env.zip ./*.py virtualenv &&
wsk -i  action update  TextClassification  env.zip --docker tinker.siat.ac.cn/tinker/siat-serverless-ow-py:t.1.0