docker build . -f kubeless-customized.Dockerfile -t  passiveaggressiveclassifier-general:1.0.0 &&\
docker push  passiveaggressiveclassifier-general:1.0.0  &&\
kubeless function deploy --runtime-image passiveaggressiveclassifier-general:1.0.0  --from-file ./handler.py --handler handler.handler --runtime python3.7 passiveaggressiveclassifier-general