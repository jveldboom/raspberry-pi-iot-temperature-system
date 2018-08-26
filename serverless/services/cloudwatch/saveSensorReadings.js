'use strict';

const cloudwatch = require('./cloudwatch');

module.exports.index = (event, context, callback) => {

    // console.log(event)
    let payload = event

    let params = {
        MetricData: [ /* required */
            {
                MetricName: "temperature",
                Dimensions: [
                    {
                        Name: 'client',
                        Value: payload.clientId
                    }
                ],

                Timestamp: new Date(),
                Value: payload.temperature.toString()
            },
            {
                MetricName: "humidity",
                Dimensions: [
                    {
                        Name: 'client',
                        Value: payload.clientId
                    }
                ],

                Timestamp: new Date(),
                Value: payload.humidity.toString()
            },
        ],
        Namespace: 'temperature-system'
    };
    cloudwatch.putMetricData(params, (err, data) => {
        if (err) {
            console.log(err, err.stack);
            return callback(err);
        }
        console.log(`Saved temperature ${payload.temperature.toString()} & humidity ${payload.humidity.toString()}`);
        return callback(null);
    });
};
