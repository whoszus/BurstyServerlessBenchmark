import os
from configparser import ConfigParser

conf = ConfigParser()
conf.read("Settings_values.cfg")
docker_file_path = conf['BBServerless']['docker_file_path']
version = conf['BBServerless']['version']
functions_dir = '../../MachineLearning/Inference-of-ml/'
model_path = 'ml-inference-with-data-RT/models/'
tpl_py = './templates/openwhisk_function_tpl_py.py'


def main():
    global models
    for root, dirs, files in os.walk(model_path, topdown=False):
        models = files
    for m in models:
        func_abs_path = functions_dir + m + '/'
        if not os.path.exists(func_abs_path):
            # print(func_abs_path)
            os.makedirs(func_abs_path)
        generate_func(func_abs_path, m)
        generate_invoke_shell(func_abs_path, m)
        generate_action_update_shell(func_abs_path, m)


def get_sub_pack(name):
    package = {
        'RandomForestRegressor': 'sklearn.ensemble',
        'SVR': 'sklearn.svm',
        'SGDRegressor': 'sklearn.linear_model',
        'SGDClassifier': 'sklearn.linear_model',
        'Perceptron': 'sklearn.linear_model',
        'MultinomialNB': 'sklearn.naive_bayes',
        'PassiveAggressiveClassifier': 'sklearn.linear_model',
        'FaceRecognition': 'sklearn.GridSearchCV',

    }
    return package[name]


def generate_func(path, name):
    path += '__main__.py'
    with open(tpl_py, 'r') as tpl:
        tpl_script = tpl.readlines()
    tp = ''.join(tpl_script)

    model = name.split("-")[0]
    imp_name = get_sub_pack(model)

    import_modules = 'from {} import {}'.format(imp_name, model)
    model_container_path = '/model/{}'.format(name)
    data_path = '/data/{}'.format(name)
    model = '{}()'.format(model)
    s = tp.format(import_modules=import_modules, model_path=model_container_path, data_path=data_path, model=model)
    s += "\n    return {'token':  'inference finished', 'startTime': int(round(startTime * 1000))}"
    with open(path, 'w') as func:
        func.write(s)


def generate_invoke_shell(path, name):
    path += 'action_invoke.sh'
    model = name.split("-")[0]

    s = 'wsk -i  action invoke  {model_name}'.format(model_name=model.lower())
    with open(path, 'w') as func:
        func.write(s)


def generate_action_update_shell(path, name):
    path += 'action_update.sh'
    model = name.split("-")[0]
    docker_tag = 'tinker.siat.ac.cn/tinker/siat-serverless-{name}:{version}'.format(name=model.lower(),
                                                                                    version=version)
    s = 'wsk -i  action update  {model_name} __main__.py --docker {tag}'.format(model_name=model.lower(),
                                                                                tag=docker_tag)
    with open(path, 'w') as func:
        func.write(s)


main()
