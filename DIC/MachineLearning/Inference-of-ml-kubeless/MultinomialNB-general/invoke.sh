docker build . -f kubeless-customized.Dockerfile -t  multinomialnb-general:1.0.0 &&\
docker push  multinomialnb-general:1.0.0  &&\
kubeless function deploy --runtime-image multinomialnb-general:1.0.0  --from-file ./handler.py --handler handler.handler --runtime python3.7 multinomialnb-general