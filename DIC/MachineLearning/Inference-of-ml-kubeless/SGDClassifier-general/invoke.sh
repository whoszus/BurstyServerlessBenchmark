docker build . -f kubeless-customized.Dockerfile -t  sgdclassifier-general:1.0.0 &&\
docker push  sgdclassifier-general:1.0.0  &&\
kubeless function deploy --runtime-image sgdclassifier-general:1.0.0  --from-file ./handler.py --handler handler.handler --runtime python3.7 sgdclassifier-general