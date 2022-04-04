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
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

const theme = createTheme({
  palette: {
    mode: 'dark',
  },
})
export default function App() {
  const [subList, setSubList] = useState([])
  const [subject, setSubject] = useState('')
  const [subData, setSubData]: [any[], any] = useState([])
  useEffect(() => {
    fetch('http://localhost:3001/data')
      .then((resp) => resp.json())
      .then((data) => {
        let tempSublist = data.map((x: any) => x.name)
        setSubList(tempSublist)
        setSubject(tempSublist[0])
        let out: any[] = []
        Object.keys(data[0].ours).forEach((x, i) => {
          out.push({ ours: data[0].ours[x], name: x })
        })
        Object.keys(data[0].notours).forEach((x, i) => {
          if (out[i]) {
            out[i].notours = data[0].notours[x]
          } else {
            out.push({ ours: data[0].notours[x], name: x })
          }
        })
        console.log(out)
        setSubData(out)
      })
  }, [])

  useEffect(() => {
    console.log(subData)
  }, [setSubData])
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
          <LineChart width={800} height={300} data={subData}>
            <XAxis dataKey="name" />
            <YAxis />
            {/* <CartesianGrid stroke="#eee" strokeDasharray="20 20" /> */}
            <Line type="monotone" dataKey="ours" stroke="#8884d8" />
            <Line type="monotone" dataKey="notours" stroke="#82ca9d" />
          </LineChart>
        </Stack>
      </Container>
    </ThemeProvider>
  )
}
