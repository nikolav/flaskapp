#!/usr/bin/bash

API_HOST=45.77.54.126
APP_PATH=/root/app/flaskapp

scp ./.env root@$API_HOST:$APP_PATH
# scp ./db/.env root@$API_HOST:$APP_PATH/db
scp ./deploy-vars.sh root@$API_HOST:$APP_PATH
scp ./src/config/vars.py root@$API_HOST:$APP_PATH/config/vars.py
# scp ./jfejcxjyujx-firebase-adminsdk-ci75i-a4ad90c0ca.json root@$API_HOST:$APP_PATH
# scp ./redis/redis.conf root@$API_HOST:$APP_PATH/redis
