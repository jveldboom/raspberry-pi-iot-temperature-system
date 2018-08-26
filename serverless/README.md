## Serverless API

__Send sensor reading locally:__
```
sls invoke local \
    --function iotSaveSensorReadings \
    --p '{ humidity: 50, temperature: 71.6, clientId: 'pi1', timestamp: 1516159186785 }'
```

__Deploy serverless:__
```
AWS_ACCOUNT_ID=1234567890 sls deploy
```