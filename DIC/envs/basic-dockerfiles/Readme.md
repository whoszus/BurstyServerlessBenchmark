The docker for openwhisk should be based on the images of openwhisk version.

Other serverless platform can simply base on the verision of tinker.siat.ac.cn/tinker/siat-serverless-py-basic:1.0.0

The version py3-scikit-learn is very newly in the version of alpine:edge(20201218), which the newest version of python-alpine in docker hub don't implement yet.