docker build . -f kubeless-customized.Dockerfile -t  sgdregressor-general:1.0.0 &&\
docker push  sgdregressor-general:1.0.0  &&\
kubeless function deploy --runtime-image sgdregressor-general:1.0.0  --from-file ./handler.py --handler handler.handler --runtime python3.7 sgdregressor-general