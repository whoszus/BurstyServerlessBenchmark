kubeless function deploy md5-nodejs --runtime nodejs6 \
                                --env REQ_MB_LIMIT=50 \
                                --handler md5.foo \
                                --from-file md5.js