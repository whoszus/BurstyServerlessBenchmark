# Kubeless Custom Runtime
Example on how to create a custom runtime for kubeless.



## Project explanation
This kubeless runtime image is using python 3.6 (for python 3.7 some different config must be used, check below) with Bottle as a wsgi and has included some extra files. These files are located in the ./custom-lib/ folder and consist of a csv parser (lib.py) and a test CSV (test.csv) file. When building the docker image, this folder will be copied inside the runtime image and will be used by the kubeless function.

The kubeless function (test.py) parses and counts the number of lines and returns this value to the kubeless wrapper.

## Deploying
### 1. Build and push docker image
In order to build the docker image just run 
```
docker build . -f python3.6.Dockerfile -t <your_container_registry>/<image_name>:<image_tag>
docker push <your_container_registry>/<image_name>:<image_tag>
```
**UPDATED** For python 3.7:
```
docker build . -f python3.7.Dockerfile -t <your_container_registry>/<image_name>:<image_tag>
docker push <your_container_registry>/<image_name>:<image_tag>
```

Note: If you like to test it without building your own image, you can use this one: _defrox/runtime:v0.2_ or for python 3.7 use _defrox/runtime:v0.3_

### 2. Update the kubeless-config configmap
In order to use the custom runtime, it is necessary to add the custom runtime in the kubeless-config configmap.
1. Get the current kubeless-config configmap
    ```
    kubectl get kubeless-config -n kubeless -o yaml > kubeless-config.yaml
    ```
2. Add the custom image configuration in json format inside the runtime-images value
    ```
    {
        "ID": "<custom-runtime>",
        "compiled": false,
        "versions": [
            {
            "name": "<custom-runtime>",
            "version": "<custom-runtime-version>",
            "runtimeImage": "<your_container_registry>/<image_name>:<image_tag>",
            "initImage": "python:3.6"
            }
        ],
        "depName": "requirements.txt",
        "fileNameSuffix": ".py"
    }
    ```
    **UPDATED** For python 3.7 use this image configuration:
    ```
    {
        "ID": "<custom-runtime>",
        "depName": "requirements.txt",
        "fileNameSuffix": ".py",
        "versions": [{
            "images": [{
                "command": "pip install --prefix=$KUBELESS_INSTALL_VOLUME -r $KUBELESS_DEPS_FILE",
                "image": "python:3.7",
                "phase": "installation"
            }, {
                "env": {
                    "PYTHONPATH": "$(KUBELESS_INSTALL_VOLUME)/lib/python3.7/site-packages:$(KUBELESS_INSTALL_VOLUME)"
                },
                "image": "<your_container_registry>/<image_name>:<image_tag>",
                "phase": "runtime"
            }],
            "name": "<custom-runtime>",
            "version": "3.7"
        }]
    }
    ```

3. Delete current kubeless-config configmap and deploy new one (else k8s won't update the values)
    ```
    kubectl delete -f ./kubeless-config.yaml && kubectl create -f ./kubeless-config.yaml
    ```
4. Restart the kubeless-controller-manager pod
    ```
    PODNAME=$(kubectl get pod -l kubeless=controller -o jsonpath="{.items[0].metadata.name}")
    kubectl get pod $PODNAME -n kubeless -o yaml | kubectl replace --force -f -
    ```

### 3. Deploy the kubeless function
Use the kubeless-cli and run
```
kubeless function deploy --from-file test.py --handler test.counter --runtime <custom-runtime><custom-runtime-version> counter 
```
### 4. Test the kubeless function
Check if the function has been deployed and is ready
```
kubeless function ls counter
```
Call the function with kubeless-cli
```
kubeless function call counter --data '{"file": "lib/test.csv"}'
```
Or curl directly with
```
kubectl proxy -p 8080 & \
curl -L --data '{"file": "lib/test.csv"}' \
  --header "Content-Type:application/json" \
  localhost:8080/api/v1/namespaces/default/services/counter:http-function-port/proxy/
```

### 5. Setting up a private registry ###

Create a secret to configure your private docker registry:
```
kubectl create secret docker-registry kubeless-registry-credentials \
  --docker-server=<url-to-your-private-registry> \
  --docker-username=<your-user> \
  --docker-password=<your-password> \
  --docker-email=<your-user@example.com>
```
Or if you want to use a secret with a custom name, then create it with:
```
kubectl create secret docker-registry <your-secret-name> \
  --docker-server=<url-to-your-private-registry> \
  --docker-username=<your-user> \
  --docker-password=<your-password> \
  --docker-email=<your-user@example.com>
```
and specify `provision-image-secret` with the new secret name ìn the image configuration.

**NOTE:** check the _Known limitations_ at the end of the doc: https://kubeless.io/docs/building-functions/

---
**Related links:**

[Tutorial article](https://medium.com/@christianaxel.schmidt/how-to-create-a-custom-kubeless-runtime-image-96ad2f8ead19)

https://github.com/kubeless/kubeless/blob/master/docs/implementing-new-runtime.md

https://github.com/kubeless/kubeless/blob/master/docs/runtimes.md#use-a-custom-runtime

https://kubeless.io/docs/implementing-new-runtime/

https://github.com/kubeless/runtimes

https://kubeless.io/docs/building-functions/

https://kubeless.io/docs/function-controller-configuration/