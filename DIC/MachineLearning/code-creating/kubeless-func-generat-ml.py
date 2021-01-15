import os
import shutil
from configparser import ConfigParser

conf = ConfigParser()
conf.read("Settings_values.cfg")
docker_file_path = conf['BBServerless']['docker_file_path']
version = conf['BBServerless']['version']

model_path = conf['openfaas-config']['model_path']
data_path = conf['openfaas-config']['data_path']

functions_dir = conf['kubeless']['functions_dir']
func_tpl = conf['kubeless']['func_tpl']
docker_tpl = conf['kubeless']['docker_tpl']
shell_tpl = conf['kubeless']['shell_tpl']


def create_docker_file(path, name):
    path += '{model_name}.Dockerfile'.format(model_name=name.lower())
    with open(docker_tpl, 'r') as tpl:
        tpl_script = tpl.readlines()
    tp = ''.join(tpl_script)
    with open(path, 'w') as func:
        func.write(tp)


def main():
    global models
    for root, dirs, files in os.walk(model_path, topdown=False):
        models = files

    create_function_dockerfile(models)
    # get_action_url(functions_dir)
    copy_model_data(model_path, functions_dir, postfix='/model/')
    copy_model_data(data_path, functions_dir, postfix='/data/')


def create_function_dockerfile(models):
    for m in models:
        func_abs_path = functions_dir + m + '/'
        if not os.path.exists(func_abs_path):
            # print(func_abs_path)
            os.makedirs(func_abs_path)
        generate_func(func_abs_path, m)
        create_docker_file(func_abs_path, m)
        create_invoker(func_abs_path, m)


def generate_func(path, name):
    path += 'handler.py'
    with open(func_tpl, 'r') as tpl:
        tpl_script = tpl.readlines()
    tp = ''.join(tpl_script)
    model_container_path = '"/kubeless/model/{}"'.format(name)
    data_path = '"/kubeless/data/{}"'.format(name)
    s = tp.format(model_path=model_container_path, data_path=data_path)
    s += "\n    return {'token':  'inference finished', 'startTime': int(round(startTime * 1000))}"
    with open(path, 'w') as func:
        func.write(s)


def create_invoker(path, name):
    name = name.split("-")[0]
    path += 'invoke.sh'
    tag = "tinker.siat.ac.cn/kubelss/"+ name.lower() + ':' + version

    with open(shell_tpl, 'r') as tpl:
        tpl_script = tpl.readlines()
    
    tp = ''.join(tpl_script).format(tag=tag, func_name=name.lower())

    with open(path, 'w') as f:
        f.write(tp)


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
    requirements = 'scikit-learn\nnumpy\npickle'
    with open(path, 'w') as rq:
        rq.write(requirements)

    with open(init_py, 'w') as rq:
        rq.write('')


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
