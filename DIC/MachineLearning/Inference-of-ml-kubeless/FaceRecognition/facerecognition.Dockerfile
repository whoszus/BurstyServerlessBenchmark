# Create a custom image with a python function
FROM tinker.siat.ac.cn/kubeless/siat-kubeless-ml:1.0.1
ENV FUNC_HANDLER=handler MOD_NAME=handler
ADD handler.py /kubeless/
ADD model/FaceRecognition /kubeless/model/
ADD data/FaceRecognition /kubeless/data/
ENTRYPOINT [ "python" ,"/kubeless.py"]