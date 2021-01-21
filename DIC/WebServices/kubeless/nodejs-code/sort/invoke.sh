kubeless function deploy sort-nodejs --runtime nodejs6 \
                                --env REQ_MB_LIMIT=50 \
                                --handler sort.foo \
                                --from-file sort.js