import os

dic = "/home/tinker/bbserverless/DIC"


def deploy_ml():
    os.chdir(dic)
    current_path = os.getcwd()
    path = os.path.join(current_path, "MachineLearning/Inference-of-ml-kubeless")
    models = []
    for root, dirs, files in os.walk(path, topdown=False):
        models = dirs
    for m in models:
        os.chdir(os.path.join(path, m))
        shell = os.path.join(path, m, 'invoke.sh')
        with open(shell, 'r') as f:
            sh = f.readlines()
        shell_string = ''.join(sh)
        os.popen(shell_string).read()


def deploy_web():
    os.chdir(dic)
    current_path = os.getcwd()
    path = os.path.join(
        current_path, "WebServices/kubeless/python-code/")
    models = []
    for root, dirs, files in os.walk(path, topdown=False):
        models = dirs
    for m in models:
        os.chdir(os.path.join(path, m))
        shell = os.path.join(path, m, 'invoke.sh')
        with open(shell, 'r') as f:
            sh = f.readlines()
        shell_string = ''.join(sh)
        os.popen(shell_string).read()


def deploy_stream():
    os.chdir(dic)
    current_path = os.getcwd()
    shell_path = os.path.join(current_path, "Stream/kubeless/")
    os.chdir(shell_path)

    with open(shell_path+'invoke.sh', 'r') as f:
        sh = f.readlines()
        shell_string = ''.join(sh)
        os.popen(shell_string).read()


def deploy_bigdata():
    os.chdir(dic)
    current_path = os.getcwd()
    shell_path = os.path.join(
        current_path, "BigData/kubeless/")
    os.chdir(shell_path)
    with open(shell_path+'invoke.sh', 'r') as f:
        sh = f.readlines()
        shell_string = ''.join(sh)
        os.popen(shell_string).read()


if __name__ == '__main__':
    deploy_ml()
    deploy_web()
    deploy_stream()
    deploy_bigdata()
