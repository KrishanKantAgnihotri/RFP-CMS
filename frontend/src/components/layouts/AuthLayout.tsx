import React from 'react';
import { Outlet } from 'react-router-dom';
import { Container, Paper, Typography, Box } from '@mui/material';
import { styled } from '@mui/material/styles';

const AuthContainer = styled(Container)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '100vh',
  padding: theme.spacing(2),
}));

const AuthPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  maxWidth: 400,
  width: '100%',
  boxShadow: theme.shadows[3],
}));

const AuthLayout: React.FC = () => {
  return (
    <AuthContainer maxWidth="sm">
      <AuthPaper>
        <Typography component="h1" variant="h4" gutterBottom>
          RFP Contract Management System
        </Typography>
        <Box sx={{ width: '100%', mt: 2 }}>
          <Outlet />
        </Box>
      </AuthPaper>
    </AuthContainer>
  );
};

export default AuthLayout;
