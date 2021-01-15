docker build . -f sgdregressor-general.Dockerfile -t  tinker.siat.ac.cn/kubeless/sgdregressor:1.0.0 &&\
docker push  tinker.siat.ac.cn/kubeless/sgdregressor:1.0.0  &&\
kubeless function deploy --runtime-image tinker.siat.ac.cn/kubeless/sgdregressor:1.0.0  --from-file ./handler.py --handler handler.handler --runtime python3.7 sgdregressor