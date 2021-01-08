import os
from configparser import ConfigParser

conf = ConfigParser()
conf.read("Settings_values.cfg")
docker_file_path = conf['BBServerless']['docker_file_path']
version = conf['BBServerless']['version']
functions_dir = '../Inference-of-ml-openwhisk/'

tpl_py = conf['openwhisk']['tpl_py']
model_path = conf['BBServerless']['model_path']

data_path = '../../envs/Runtimes/ml-inference-with-data-RT/testData/'
basic_docker_file = 'templates/openwhisk-python3.Dockerfile'

conf = ConfigParser()
conf.read("Settings_values.cfg")
abs_dir = conf['BBServerless']['abs_dir']


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

    # 运行时环境
    generate_rt()
    openfaas_runtime_create()


def generate_rt():
    global datas, models
    for root, dirs, files in os.walk(model_path, topdown=False):
        models = files

    for root, dirs, files in os.walk(data_path, topdown=False):
        datas = files

    # copy models
    for m in models:
        model = 'models/' + m
        with open(basic_docker_file, 'r') as basic:
            commands = basic.readline()

        new_docker_file_name = docker_file_path + 'openwhisk-python3.Dockerfile-' + m
        copy_model_command = '\nCOPY {model} /model/'.format(model=model)
        commands += copy_model_command

        with open(new_docker_file_name, 'w') as docker_file:
            docker_file.write(commands)
            docker_file.close()
        basic.close()

    # copy Platform-Testing data
    for d in datas:
        model_data_path = 'testData/' + d
        if models.__contains__(d):
            copy_model_command = '\nCOPY {data} /data/'.format(data=model_data_path)
            new_docker_file_name = docker_file_path + 'openwhisk-python3.Dockerfile-' + d
            with open(new_docker_file_name, 'a+') as docker_file:
                docker_file.write(copy_model_command)
                docker_file.close()
            basic.close()


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

    s = 'wsk -i  action invoke  {model_name} --result'.format(model_name=model.lower())
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


def openfaas_runtime_create():
    global docker_files
    for root, dirs, files in os.walk(docker_file_path, topdown=False):
        docker_files = files
    for f in docker_files:
        # df = docker_file_path + f
        name = f.split('-')[1].lower()
        docker_tag = 'tinker.siat.ac.cn/tinker/siat-serverless-OF-{name}:{version}'.format(name=name,
                                                                                           version=version)
        run_command = 'cd {abs} && docker build . -f {dockerfile} -t {tag}'.format(abs=abs_dir, dockerfile=f,
                                                                                   tag=docker_tag)

        upload_command = 'docker push {tag}'.format(tag=docker_tag)
        # p = subprocess.Popen(run_command, stdout=subprocess.PIPE, shell=True)
        # (output, err) = p.communicate()
        # p_status = p.wait()
        # print("Command output: " + run_command)
        os.popen(run_command).read()
        os.popen(upload_command).read()


main()
