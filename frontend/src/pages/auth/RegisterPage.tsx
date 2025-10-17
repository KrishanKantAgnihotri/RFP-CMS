import React, { useState } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import {
  TextField,
  Button,
  Typography,
  Link,
  Box,
  Alert,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormHelperText,
} from '@mui/material';
import api from '../../services/api';

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
      confirmPassword: '',
      full_name: '',
      company_name: '',
      role: '',
    },
    validationSchema: Yup.object({
      email: Yup.string().email('Invalid email address').required('Required'),
      password: Yup.string()
        .min(8, 'Password must be at least 8 characters')
        .required('Required'),
      confirmPassword: Yup.string()
        .oneOf([Yup.ref('password')], 'Passwords must match')
        .required('Required'),
      full_name: Yup.string().required('Required'),
      company_name: Yup.string().required('Required'),
      role: Yup.string().oneOf(['buyer', 'supplier'], 'Invalid role').required('Required'),
    }),
    onSubmit: async (values) => {
      setLoading(true);
      setError(null);
      
      const { confirmPassword, full_name, role, ...registerData } = values;
      
      // Split full_name into first_name and last_name
      const nameParts = full_name.trim().split(' ');
      const firstName = nameParts[0] || '';
      const lastName = nameParts.slice(1).join(' ') || '';
      
      // Prepare data to match backend schema
      const backendData = {
        ...registerData,
        username: registerData.email, // Use email as username
        first_name: firstName,
        last_name: lastName,
        role: role.charAt(0).toUpperCase() + role.slice(1), // Capitalize role
      };
      
      try {
        await api.post('/users/register', backendData);
        navigate('/login', {
          state: { message: 'Registration successful! Please log in with your credentials.' },
        });
      } catch (err: any) {
        console.error('Registration error:', err);
        console.error('Error response:', err.response?.data);
        console.error('Request data sent:', backendData);
        
        if (err.response?.data?.detail) {
          if (typeof err.response.data.detail === 'string') {
            setError(err.response.data.detail);
          } else if (Array.isArray(err.response.data.detail)) {
            setError(err.response.data.detail.map((e: any) => e.msg).join(', '));
          } else {
            setError('Registration failed. Please check your information.');
          }
        } else {
          setError('Registration failed. Please try again.');
        }
      } finally {
        setLoading(false);
      }
    },
  });

  return (
    <Box>
      <Typography component="h1" variant="h5" align="center" gutterBottom>
        Sign Up
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      <form onSubmit={formik.handleSubmit}>
        <TextField
          fullWidth
          id="full_name"
          name="full_name"
          label="Full Name"
          value={formik.values.full_name}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          error={formik.touched.full_name && Boolean(formik.errors.full_name)}
          helperText={formik.touched.full_name && formik.errors.full_name}
          margin="normal"
          autoFocus
        />
        
        <TextField
          fullWidth
          id="email"
          name="email"
          label="Email Address"
          value={formik.values.email}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          error={formik.touched.email && Boolean(formik.errors.email)}
          helperText={formik.touched.email && formik.errors.email}
          margin="normal"
          autoComplete="email"
        />
        
        <TextField
          fullWidth
          id="company_name"
          name="company_name"
          label="Company Name"
          value={formik.values.company_name}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          error={formik.touched.company_name && Boolean(formik.errors.company_name)}
          helperText={formik.touched.company_name && formik.errors.company_name}
          margin="normal"
        />
        
        <FormControl
          fullWidth
          margin="normal"
          error={formik.touched.role && Boolean(formik.errors.role)}
        >
          <InputLabel id="role-label">Role</InputLabel>
          <Select
            labelId="role-label"
            id="role"
            name="role"
            value={formik.values.role}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            label="Role"
          >
            <MenuItem value="buyer">Buyer</MenuItem>
            <MenuItem value="supplier">Supplier</MenuItem>
          </Select>
          {formik.touched.role && formik.errors.role && (
            <FormHelperText>{formik.errors.role}</FormHelperText>
          )}
        </FormControl>
        
        <TextField
          fullWidth
          id="password"
          name="password"
          label="Password"
          type="password"
          value={formik.values.password}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          error={formik.touched.password && Boolean(formik.errors.password)}
          helperText={formik.touched.password && formik.errors.password}
          margin="normal"
          autoComplete="new-password"
        />
        
        <TextField
          fullWidth
          id="confirmPassword"
          name="confirmPassword"
          label="Confirm Password"
          type="password"
          value={formik.values.confirmPassword}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          error={formik.touched.confirmPassword && Boolean(formik.errors.confirmPassword)}
          helperText={formik.touched.confirmPassword && formik.errors.confirmPassword}
          margin="normal"
          autoComplete="new-password"
        />
        
        <Button
          type="submit"
          fullWidth
          variant="contained"
          color="primary"
          size="large"
          disabled={loading}
          sx={{ mt: 3, mb: 2 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Sign Up'}
        </Button>
        
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="body2">
            Already have an account?{' '}
            <Link component={RouterLink} to="/login" variant="body2">
              Sign In
            </Link>
          </Typography>
        </Box>
      </form>
    </Box>
  );
};

export default RegisterPage;