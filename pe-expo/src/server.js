const app = require('express')(),
  fs = require('fs'),
  bodyParser = require('body-parser'),
  { exec } = require('child_process')

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.text())
app.use(bodyParser.json())

let data = []
exec(
  'python3 ../../dataAnalysis/plotter.py -p --all-data-json',
  (error, stdout, stderr) => {
    if (error) {
      console.log(`error: ${error.message}`)
      return
    }
    if (stderr) {
      console.log(`stderr: ${stderr}`)
      return
    }
    data = JSON.parse(stdout)
    console.log(data)
  }
)

app.get('/data', (req, res) => {
  res.send(JSON.stringify(data))
})

app.post('/getGraph', (req, res) => {
  let stu = req.body
  res.send(stu)
})

app.listen(3001, () => {
  console.log('Running on port 3001')
})
