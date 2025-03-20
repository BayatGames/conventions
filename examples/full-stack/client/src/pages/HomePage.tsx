import { useState, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Button,
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Link,
} from '@mui/material';
import { RootState } from '../store';

const features = [
  {
    title: 'Modern React',
    description: 'Built with the latest React features and best practices',
  },
  {
    title: 'TypeScript',
    description: 'Type safety throughout the entire application',
  },
  {
    title: 'Redux Toolkit',
    description: 'Efficient state management with Redux Toolkit',
  },
  {
    title: 'Material UI',
    description: 'Beautiful and responsive UI components',
  },
  {
    title: 'Node.js Backend',
    description: 'Fast and scalable API with Express and TypeScript',
  },
  {
    title: 'PostgreSQL',
    description: 'Reliable and powerful database for your data',
  },
];

const HomePage = () => {
  const { isAuthenticated, user } = useSelector((state: RootState) => state.auth);

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4, textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Welcome to Bayat Full-Stack App
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          A complete example of a production-ready full-stack application
          following Bayat's development conventions.
        </Typography>
        
        {isAuthenticated ? (
          <Button
            variant="contained"
            color="primary"
            size="large"
            component={RouterLink}
            to="/dashboard"
            sx={{ mt: 2 }}
          >
            Go to Dashboard
          </Button>
        ) : (
          <Box sx={{ mt: 2 }}>
            <Button
              variant="contained"
              color="primary"
              size="large"
              component={RouterLink}
              to="/login"
              sx={{ mr: 2 }}
            >
              Login
            </Button>
            <Button
              variant="outlined"
              color="primary"
              size="large"
              component={RouterLink}
              to="/register"
            >
              Register
            </Button>
          </Box>
        )}
      </Box>

      <Box sx={{ mt: 6, mb: 4 }}>
        <Typography variant="h4" component="h2" gutterBottom align="center">
          Features
        </Typography>
        <Grid container spacing={4} sx={{ mt: 2 }}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h5" component="h3">
                    {feature.title}
                  </Typography>
                  <Typography>{feature.description}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      <Box sx={{ my: 6, textAlign: 'center' }}>
        <Typography variant="h4" component="h2" gutterBottom>
          Ready to get started?
        </Typography>
        <Button
          variant="contained"
          color="secondary"
          size="large"
          component="a"
          href="https://github.com/yourusername/fullstack-example"
          target="_blank"
          rel="noopener noreferrer"
          sx={{ mt: 2 }}
        >
          View on GitHub
        </Button>
      </Box>
    </Container>
  );
};

export default HomePage; 