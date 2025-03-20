import { Box, Container, Typography, Link } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.primary.main,
        color: 'white',
      }}
    >
      <Container maxWidth="lg">
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexDirection: { xs: 'column', sm: 'row' },
            gap: 2,
          }}
        >
          <Typography variant="body1">
            © {new Date().getFullYear()} Bayat Full-Stack Application
          </Typography>
          <Box>
            <Link
              component={RouterLink}
              to="/about"
              color="inherit"
              sx={{ mx: 1 }}
            >
              About
            </Link>
            <Link
              component={RouterLink}
              to="/contact"
              color="inherit"
              sx={{ mx: 1 }}
            >
              Contact
            </Link>
            <Link
              component={RouterLink}
              to="/privacy"
              color="inherit"
              sx={{ mx: 1 }}
            >
              Privacy
            </Link>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer; 