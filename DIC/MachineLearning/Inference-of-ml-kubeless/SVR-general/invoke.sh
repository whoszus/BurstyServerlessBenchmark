docker build . -f kubeless-customized.Dockerfile -t  tinker.siat.ac.cn/kubelss/svr:1.0.0 &&\
docker push  tinker.siat.ac.cn/kubelss/svr:1.0.0  &&\
kubeless function deploy --runtime-image tinker.siat.ac.cn/kubelss/svr:1.0.0  --from-file ./handler.py --handler handler.handler --runtime python3.7 svr