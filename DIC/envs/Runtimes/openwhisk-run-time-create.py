import os
from configparser import ConfigParser

conf = ConfigParser()
conf.read("Settings_values.cfg")
docker_file_path = conf['BBServerless']['docker_file_path']
version = conf['BBServerless']['version']


def runtime_create():
    global docker_files
    for root, dirs, files in os.walk(docker_file_path, topdown=False):
        docker_files = files

    for f in docker_files:
        df = docker_file_path + f
        name = f.split('-')[1]
        docker_tag = 'tinker.siat.ac.cn/tinker/siat-serverless-{name}:{version}'.format(name=name,
                                                                                        version=version)
        run_command = 'Docker build . -f {dockerfile} -t {tag}'.format(dockerfile=df, tag=docker_tag)

        upload_command = 'docker upload {tag}'.format(tag=docker_tag)
        # p = subprocess.Popen(run_command, stdout=subprocess.PIPE, shell=True)
        # (output, err) = p.communicate()
        # p_status = p.wait()
        # print("Command output: " + output)
        os.popen(run_command).read()
        os.popen(upload_command).read()


runtime_create()
