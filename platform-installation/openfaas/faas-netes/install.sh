echo Installing with helm 👑

helm repo add openfaas https://openfaas.github.io/faas-netes/

kubectl apply -f namespaces.yml

# generate a random password

kubectl -n openfaas create secret generic basic-auth \
--from-literal=basic-auth-user=admin \
--from-literal=basic-auth-password=siatcloud2021

echo "Installing chart 🍻"
helm upgrade \
    --install \
    openfaas \
    openfaas/openfaas \
    --namespace openfaas  \
    -f ./helm-modify.yaml
