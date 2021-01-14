docker build . -f customized-bigdata.Dockerfile -t  tinker.siat.ac.cn/kubeless/demo:1.0.0 &&\
docker push  tinker.siat.ac.cn/kubeless/demo:1.0.0 &&\
kubeless function deploy --runtime-image tinker.siat.ac.cn/kubeless/demo:1.0.0 --from-file ./handler.py --handler handler.handler --runtime python3.7 demo