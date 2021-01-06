docker build . -f kubeless-customized.Dockerfile -t  facerecognition:1.0.0 &&\
docker push  facerecognition:1.0.0  &&\
kubeless function deploy --runtime-image facerecognition:1.0.0  --from-file ./handler.py --handler handler.handler --runtime python3.7 facerecognition