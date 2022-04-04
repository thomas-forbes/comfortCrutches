import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Typography,
  Stack,
  Container,
  Grid,
  Card,
  CardContent,
} from '@mui/material'

export default function App() {
  const theme = createTheme({
    palette: {
      mode: 'dark',
    },
  })
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container sx={{ marginTop: 5 }}>
        <Stack direction="column" alignItems="center" justifyContent="center">
          <Typography variant="h2">Comfort Crutches</Typography>
          <Grid container spacing={4} justifyContent="center">
            <Grid item>
              <Card>
                <CardContent>yo</CardContent>
              </Card>
            </Grid>
          </Grid>
        </Stack>
      </Container>
    </ThemeProvider>
  )
}
