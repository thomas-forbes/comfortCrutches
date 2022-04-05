import { useState, useEffect } from 'react'
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Typography,
  Stack,
  Container,
  CardContent,
  Autocomplete,
  TextField,
} from '@mui/material'
import { CanvasJSChart } from 'canvasjs-react-charts'

const theme = createTheme({
  palette: {
    mode: 'dark',
  },
})
export default function App() {
  const [subList, setSubList] = useState([])
  const [subject, setSubject] = useState('')
  const [subData, setSubData]: [any[], any] = useState([])

  const [data, setData]: [any, any] = useState([])

  const updateSubData = (stu) => {
    let out: any[] = []

    out.push({
      name: 'ours',
      type: 'spline',
      showInLegend: true,
      dataPoints: stu.ours.map((x, i) => ({ y: x, x: i })),
    })
    out.push({
      name: 'notours',
      type: 'spline',
      showInLegend: true,
      dataPoints: stu.notours.map((x, i) => ({ y: x, x: i })),
    })
    return out
  }
  useEffect(() => {
    fetch('http://localhost:3001/data')
      .then((resp) => resp.json())
      .then((data) => {
        let tempSublist = data.map((x: any) => x.name)
        setSubList(tempSublist)
        setSubject(tempSublist[0])
        setSubData(updateSubData(data[0]))
        setData(data)
      })
  }, [])

  useEffect(() => {
    if (subject) setSubData(updateSubData(data.find((x) => x.name == subject)))
  }, [subject])
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container sx={{ marginTop: 5 }}>
        <Stack
          direction="column"
          spacing={5}
          alignItems="center"
          justifyContent="center"
        >
          <Typography variant="h2">Comfort Crutches</Typography>
          <Autocomplete
            disablePortal
            options={subList}
            sx={{ width: 200 }}
            value={subject}
            onChange={(e, s) => setSubject(s ? s : subject)}
            autoHighlight={true}
            loading={subList.length == 0}
            renderInput={(params) => (
              <TextField
                {...params}
                // onChange={(e) =>}
                label={'Subject Name'}
              />
            )}
          />
          <CanvasJSChart
            options={{
              theme: 'dark2',
              title: {
                text: subject,
              },
              axisY: {
                title: 'Pressure (KPa)',
              },
              axisX: {
                title: 'Time (s)',
              },
              data: subData,
              // data: [
              //   {
              //     type: 'line',
              //     // xValueFormatString: 'MMM YYYY',
              //     // yValueFormatString: '$#,##0.00',
              //     dataPoints: [{ x: 1, y: 2 }],
              //   },
              // ],
            }}
          />
          {/* <LineChart width={800} height={300} data={subData}>
          <XAxis
            dataKey="name"
            label={{
              value: 'Time (s)',
              // offset: -1,
              position: 'bottom',
            }}
          />
          <YAxis
          // label={{
          //   value: 'Pressure (KPa)',
          //   angle: -90,
          //   position: 'outsideLeft',
          // }}
          />
          <Legend verticalAlign="top" height={36} />
          <Line type="monotone" dataKey="ours" stroke="#8884d8" />
          <Line type="monotone" dataKey="notours" stroke="#82ca9d" />
        </LineChart> */}
        </Stack>
      </Container>
    </ThemeProvider>
  )
}
