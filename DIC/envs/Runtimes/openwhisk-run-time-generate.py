import os

model_path = '../models/'
data_path = '../testData/'
basic_docker_file = 'Dockerfile'
docker_file_path = 'ml-inference-with-data-RT/'


def generate_rt():
    global datas, models
    for root, dirs, files in os.walk(model_path, topdown=False):
        models = files

    for root, dirs, files in os.walk(data_path, topdown=False):
        datas = files

    # copy models
    for m in models:
        model = model_path + m
        with open(basic_docker_file, 'r') as basic:
            commands = basic.readline()

        new_docker_file_name = docker_file_path + 'Dockerfile-' + m
        copy_model_command = '\nCOPY {model} /model/'.format(model=model)
        commands += copy_model_command

        with open(new_docker_file_name, 'w') as docker_file:
            docker_file.write(commands)
            docker_file.close()
        basic.close()

    # copy testing data
    for d in datas:
        model_data_path = data_path + d
        if models.__contains__(d):
            copy_model_command = '\nCOPY {data} /data/'.format(data=model_data_path)
            new_docker_file_name = docker_file_path + 'Dockerfile-' + d
            with open(new_docker_file_name, 'a+') as docker_file:
                docker_file.write(copy_model_command)
                docker_file.close()
            basic.close()


generate_rt()
