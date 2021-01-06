docker build . -f kubeless-customized.Dockerfile -t  svr-general:1.0.0 &&\
docker push  svr-general:1.0.0  &&\
kubeless function deploy --runtime-image svr-general:1.0.0  --from-file ./handler.py --handler handler.handler --runtime python3.7 svr-general