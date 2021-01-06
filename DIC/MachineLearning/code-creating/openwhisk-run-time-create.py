import os
from configparser import ConfigParser

conf = ConfigParser()
conf.read("Settings_values.cfg")
docker_file_path = conf['BBServerless']['docker_file_path']
version = conf['BBServerless']['version']
abs_dir = conf['BBServerless']['abs_dir']


def runtime_create():
    global docker_files
    for root, dirs, files in os.walk(docker_file_path, topdown=False):
        docker_files = files
    for f in docker_files:
        # df = docker_file_path + f
        name = f.split('-')[1].lower()
        docker_tag = 'tinker.siat.ac.cn/tinker/siat-serverless-{name}:{version}'.format(name=name,
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


