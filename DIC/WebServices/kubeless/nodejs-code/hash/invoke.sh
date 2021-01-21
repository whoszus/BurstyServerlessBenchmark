kubeless function deploy hash-nodejs --runtime nodejs6 \
                                --env REQ_MB_LIMIT=50 \
                                --handler hash.foo \
                                --from-file hash.js