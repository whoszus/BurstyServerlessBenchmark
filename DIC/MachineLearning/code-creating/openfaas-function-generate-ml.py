import os
import shutil
from configparser import ConfigParser

conf = ConfigParser()
conf.read("Settings_values.cfg")
docker_file_path = conf['BBServerless']['docker_file_path']
version = conf['BBServerless']['version']
prefix = conf['openfaas-config']['prefix']
conf_file = conf['openfaas-config']['conf_file']
conf_tpl = conf['openfaas-config']['conf_tpl']
tpl_py = conf['openfaas-config']['tpl_py']
functions_dir = conf['openfaas-config']['functions_dir']
model_path = conf['openfaas-config']['model_path']
data_path = conf['openfaas-config']['data_path']


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
        # generate_invoke_shell(func_abs_path, m)
        generate_requirement(func_abs_path)
    generate_config_file(functions_dir, models)
    generate_action_build_shell(functions_dir)
    generate_action_push_shell(functions_dir)
    generate_action_deploy_shell(functions_dir)
    # get_action_url(functions_dir)
    get_action_url_v2(functions_dir, models)
    copy_model_data(model_path, functions_dir, postfix='/model/')
    copy_model_data(data_path, functions_dir, postfix='/data/')


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
    path += 'handler.py'
    with open(tpl_py, 'r') as tpl:
        tpl_script = tpl.readlines()
    tp = ''.join(tpl_script)

    model = name.split("-")[0]
    imp_name = get_sub_pack(model)

    import_modules = 'from {} import {}'.format(imp_name, model)
    model_container_path = './function/model/{}'.format(name)
    data_path = './function/data/{}'.format(name)
    model = '{}()'.format(model)
    s = tp.format(import_modules=import_modules, model_path=model_container_path, data_path=data_path, model=model)
    s += "\n    return {'token':  'inference finished', 'startTime': int(round(startTime * 1000))}"
    with open(path, 'w') as func:
        func.write(s)


def generate_action_build_shell(path):
    path += 'action_build.sh'
    command = 'faas-cli build -f {}'.format(conf_file)
    with open(path, 'w') as f:
        f.write(command)


def generate_action_deploy_shell(path):
    path += 'action_deploy.sh'
    command = 'faas-cli deploy -f {}'.format(conf_file)
    with open(path, 'w') as f:
        f.write(command)


def generate_action_push_shell(path):
    path += 'action_push.sh'
    command = 'faas-cli push -f {}'.format(conf_file)
    with open(path, 'w') as f:
        f.write(command)


def get_action_url(path):
    shell_path = path + 'action_deploy.sh'
    with open(shell_path, 'r') as f:
        cmd = f.readlines()
    command = ''.join(cmd)
    urls = []
    url = os.popen(command).readlines()
    if ''.join(url).find('Accepted') != -1:
        for u in url:
            if u.find("URL: http") != -1:
                urls.append(u)
    urls_path = path + 'urls'
    url_string = '/n'.join(urls)
    with  open(urls_path, 'w') as f:
        f.write(url_string)


def generate_requirement(func_abs_path):
    path = func_abs_path + 'requirements.txt'
    init_py = func_abs_path + '__init__.py'
    requirements = 'scikit-learn'
    with open(path, 'w') as rq:
        rq.write(requirements)

    with open(init_py, 'w') as rq:
        rq.write('')


def get_action_url_v2(path, models):
    s = ''
    for m in models:
        s += '\n' + prefix.format(func_name=m.lower())
    urls_path = path + 'urls'
    with open(urls_path, 'w') as f:
        f.write(s)


def generate_config_file(functions_dir, models):
    with open(conf_tpl, 'r') as ctpl:
        tpl = ctpl.readlines()

    configs = ''.join(tpl)
    for m in models:
        configs += "\n  {func_name}: \n    lang: python3-debian\n    handler: ./{model_path}    \n    image: tinker.siat.ac.cn/openfaas-fn/{func_name}:{version}\n    configuration: \n     copy:\n      - ./data\n      - ./model\n" \
            .format(func_name=m.lower(), version=version, model_path=m)
    config_file = functions_dir + conf_file
    with open(config_file, 'w') as cfg:
        cfg.write(configs)


def copy_model_data(path, func_path, postfix='/model/'):
    global ros, file_array
    for root, dirs, files in os.walk(path, topdown=False):
        file_array = files
    for f in file_array:
        dest = func_path + f + postfix
        if not os.path.exists(dest):
            os.makedirs(dest)
        shutil.copy2(path + f, dest)


main()
