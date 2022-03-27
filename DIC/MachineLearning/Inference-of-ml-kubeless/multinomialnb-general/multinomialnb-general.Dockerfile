# Create a custom image with a python function
FROM k.harbor.siat.ac.cn/kubeless/kubeless-ml-base:v1.0
ENV FUNC_HANDLER=handler MOD_NAME=handler
ADD handler.py /kubeless/
ADD model/multinomialnb-general /kubeless/model/
ADD data/multinomialnb-general /kubeless/data/
ENTRYPOINT [ "python" ,"/_kubeless.py"]