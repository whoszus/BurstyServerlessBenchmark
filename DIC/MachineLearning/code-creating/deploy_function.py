from configparser import ConfigParser
import os

conf = ConfigParser()
conf.read("Settings_values.cfg")

def deploy_openwhisk():
    global models
    os.chdir("..")
    current_path = os.getcwd()
    path = os.path.join(current_path, "Inference-of-ml-openwhisk")
    for root, dirs, files in os.walk(path, topdown=False):
        models = dirs
    for m in models:
        os.chdir(os.path.join(path,m))
        shell = os.path.join(path, m, 'action_update.sh')
        os.popen(shell).read()



deploy_openwhisk()
