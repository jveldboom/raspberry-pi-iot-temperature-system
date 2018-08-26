const CloudWatch = require('aws-sdk').CloudWatch;

module.exports = new CloudWatch({
    apiVersion: '2010-08-01',
    region: process.env.AWS_REGION
});

