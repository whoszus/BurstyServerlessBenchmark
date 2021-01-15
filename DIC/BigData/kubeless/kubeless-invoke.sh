docker build . -f bigdata.Dockerfile -t  bigdata:1.0.0 &&\
docker push  bigdata:1.0.0  &&\
kubeless function deploy --runtime-image bigdata:1.0.0  --from-file ./handler.py --handler handler.handler --runtime python3.7 bigdata