import os

functions_dir = '../../MachineLearning/Inference-of-ml/'

model_path = '../models/'

tpl_py = './function-templates/openwhisk_function_tpl_py.py'


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


def generate_func(path, name):
    path += '__main__.py'
    with open(tpl_py, 'r') as tpl:
        tpl_script = tpl.readlines()
    tp = ''.join(tpl_script)

    import_modules = 'from sklearn.linear_model import Perceptron'
    model_container_path = '/model/{}'.format(name)
    data_path = '/data/{}'.format(name)
    alg_name = 'Perceptron'
    model = '{}()'.format(alg_name)
    s = tp.format(import_modules=import_modules, model_path=model_container_path, data_path=data_path, model=model)
    s += "\n    return {'token':  'inference finished', 'startTime': int(round(startTime * 1000))}"
    with open(path, 'w') as func:
        func.write(s)


def generate_invoke_shell(path, name):
    return


def generate_action_update_shell(path, name):
    return


generate_func('', '')
