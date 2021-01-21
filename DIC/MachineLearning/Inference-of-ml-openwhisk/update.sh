wsk -i  action update  facerecognition FaceRecognition/__main__.py --docker tinker.siat.ac.cn/tinker/siat-serverless-facerecognition:1.0.0
wsk -i  action update  multinomialnb MultinomialNB-general/__main__.py --docker tinker.siat.ac.cn/tinker/siat-serverless-multinomialnb:1.0.0
wsk -i  action update  passiveaggressiveclassifier PassiveAggressiveClassifier-general/__main__.py --docker tinker.siat.ac.cn/tinker/siat-serverless-passiveaggressiveclassifier:1.0.0
wsk -i  action update  perceptron Perceptron-general/__main__.py --docker tinker.siat.ac.cn/tinker/siat-serverless-perceptron:1.0.0
wsk -i  action update  randomforestregressor RandomForestRegressor-general/__main__.py --docker tinker.siat.ac.cn/tinker/siat-serverless-randomforestregressor:1.0.0 -m 2048
wsk -i  action update  sgdclassifier SGDClassifier-general/__main__.py --docker tinker.siat.ac.cn/tinker/siat-serverless-sgdclassifier:1.0.0
wsk -i  action update  sgdregressor SGDRegressor-general/__main__.py --docker tinker.siat.ac.cn/tinker/siat-serverless-sgdregressor:1.0.0
wsk -i  action update  svr SVR-general/__main__.py --docker tinker.siat.ac.cn/tinker/siat-serverless-svr:1.0.0