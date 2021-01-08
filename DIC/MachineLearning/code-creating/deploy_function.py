from configparser import ConfigParser
import os

conf = ConfigParser()
conf.read("Settings_values.cfg")
openfaas_functions_dir = conf['openfaas-config']['functions_dir']


def deploy_openwhisk():
    global models
    os.chdir("..")
    current_path = os.getcwd()
    path = os.path.join(current_path, "Inference-of-ml-openwhisk")
    for root, dirs, files in os.walk(path, topdown=False):
        models = dirs
    for m in models:
        os.chdir(os.path.join(path, m))
        shell = os.path.join(path, m, 'action_update.sh')
        with open(shell, 'r') as f:
            sh = f.readlines()
        shell_string = ''.join(sh)
        os.popen(shell_string).read()


def deploy_openfaas():
    os.chdir("..")
    current_path = os.getcwd()
    path = os.path.join(current_path, "Inference-of-ml-openfaas")
    os.chdir(path)
    action_build = 'action_build.sh'
    action_deploy = 'action_build.sh'
    action_push = 'action_build.sh'

    with open(action_build, 'r') as f:
        acts = f.readlines()
    action_build_shell = ''.join(acts)
    r = os.popen(action_build_shell).read()
    print(r)

    with open(action_push, 'r') as f:
        acts = f.readlines()
    action_build_shell = ''.join(acts)
    r = os.popen(action_build_shell).read()
    print(r)

    with open(action_deploy, 'r') as f:
        acts = f.readlines()
    action_build_shell = ''.join(acts)
    r = os.popen(action_build_shell).read()
    print(r)

deploy_openfaas()
