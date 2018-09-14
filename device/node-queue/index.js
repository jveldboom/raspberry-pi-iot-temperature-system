const fs = require('fs')
let config = {
  queuePath: `queue`
}

const saveSensorReadings = () => {
  let filename = new Date().getTime()
  let data = { temperature: Math.random(), humidity: Math.random() }
  fs.writeFileSync(`${config.queuePath}/${filename}`, JSON.stringify(data))
}

const processQueue = () => {
  fs.readdir(config.queuePath, (err, files) => {
    if (files.length === 0) return

    console.log(`Files in queue: ${files.length}`)

    for (let file of files) {
      fs.readFile(`${config.queuePath}/${file}`, (err, data) => {
        console.log(data.toString())

        fs.unlink(`${config.queuePath}/${file}`, (err) => {
          if (err) throw err
        })
      })
    }
  })
}

const getRemoteConfig = () => {
  return new Promise((resolve, reject) => {
    return resolve(Math.random())
  })
}

saveSensorReadings()

setInterval(async () => {
  config.remote = await getRemoteConfig()
  console.log(`${JSON.stringify(config)}`)
}, 1000)

setInterval(() => {
  console.log(`${JSON.stringify(config)} - second`)
}, 2000)

// setInterval(() => {
//     saveSensorReadings()
// }, 1000);
//
// setInterval(() => {
//     processQueue()
// },10000);
