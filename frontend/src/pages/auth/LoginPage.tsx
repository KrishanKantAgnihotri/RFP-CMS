import React from 'react';
import { Box, Typography, Button } from '@mui/material';

const LoginPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h5" component="h2" gutterBottom>
        Login Page
      </Typography>
      <Typography paragraph>
        This is a placeholder login page. In a real application, you would have a login form here.
      </Typography>
      <Button variant="contained" color="primary">
        Login
      </Button>
    </Box>
  );
};

export default LoginPage;