# docker build . -f facerecognition-general.Dockerfile -t  k.harbor.siat.ac.cn/kubeless/facerecognition-general:1.0.0 &&\
# docker push  k.harbor.siat.ac.cn/kubeless/facerecognition-general:1.0.0  &&\
kubeless function deploy --runtime-image k.harbor.siat.ac.cn/kubeless/facerecognition-general:1.0.0  --from-file ./handler.py --handler handler.handler --runtime python3.7 facerecognition-general -n kl --cpu 1000m