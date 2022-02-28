docker build . -f {model}.Dockerfile -t  {tag} &&\
docker push  {tag}  &&\
kubeless function deploy --runtime-image {tag}  --from-file ./handler.py --handler handler.handler --runtime python3.7 {func_name} -n kl --cpu 1000m