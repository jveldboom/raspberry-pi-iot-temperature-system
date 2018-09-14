const sensor = require('node-dht-sensor')

const readSensor = () => {
  sensor.read(22, 4, function (err, temperature, humidity) {
    if (!err) {
      console.log(`${new Date().toISOString()} temp: ${(temperature.toFixed(1) * 9 / 5 + 32)}°F humidity: ${humidity.toFixed(1)}%`)
    }
  })
}

setInterval(readSensor, 5000)
