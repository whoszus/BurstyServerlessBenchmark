kubeless function deploy hello-nodejs --runtime nodejs6 \
                                --env REQ_MB_LIMIT=50 \
                                --handler hello.foo \
                                --from-file hello.js