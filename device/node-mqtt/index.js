const awsIot = require('aws-iot-device-sdk')

const device = awsIot.device({
  keyPath: '../device/certs/private-pi1.key',
  certPath: '../device/certs/cert-pi1.pem',
  caPath: '../device/certs/rootCA.pem',
  clientId: process.env.CLIENT_ID,
  host: 'a5vux812u5uae.iot.us-east-1.amazonaws.com',
  will: {
    topic: 'lastwill',
    payload: JSON.stringify({ type: `${process.env.CLIENT_ID} down!!` }),
    properties: {
      willDelayInterval: 60
    }
  }
})

device
  .on('connect', () => {
    console.log('connect')
    device.subscribe('topic_1')
    device.subscribe('lastwill')
    device.publish('topic_1', JSON.stringify({ test_data: 1 }))
  })

device
  .on('message', (topic, payload) => {
    console.log('message', topic, payload.toString())
  })
