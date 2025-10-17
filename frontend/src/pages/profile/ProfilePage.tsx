import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { useAuth } from '../../hooks/useAuth';

const ProfilePage: React.FC = () => {
  const { user, updateUser } = useAuth();
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const formik = useFormik({
    initialValues: {
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      company_name: user?.company_name || '',
    },
    validationSchema: Yup.object({
      first_name: Yup.string().required('First name is required'),
      company_name: Yup.string().required('Company name is required'),
    }),
    onSubmit: async (values) => {
      setLoading(true);
      setError(null);
      setSuccess(null);
      
      try {
        await updateUser(values);
        setSuccess('Profile updated successfully!');
        setEditing(false);
      } catch (err: any) {
        console.error('Failed to update profile:', err);
        if (err.response?.data?.detail) {
          setError(err.response.data.detail);
        } else {
          setError('Failed to update profile. Please try again.');
        }
      } finally {
        setLoading(false);
      }
    },
  });

  if (!user) {
    return (
      <Box>
        <Alert severity="warning">
          Please log in to view your profile.
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Profile
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }}>
          {success}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h6">
                Personal Information
              </Typography>
              {!editing && (
                <Button
                  variant="outlined"
                  onClick={() => setEditing(true)}
                >
                  Edit Profile
                </Button>
              )}
            </Box>

            <form onSubmit={formik.handleSubmit}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    id="first_name"
                    name="first_name"
                    label="First Name"
                    value={editing ? formik.values.first_name : user.first_name}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    error={editing && formik.touched.first_name && Boolean(formik.errors.first_name)}
                    helperText={editing && formik.touched.first_name && formik.errors.first_name}
                    disabled={!editing}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    id="last_name"
                    name="last_name"
                    label="Last Name"
                    value={editing ? formik.values.last_name : user.last_name}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    disabled={!editing}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Email"
                    value={user.email}
                    disabled
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Role"
                    value={user.role}
                    disabled
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    id="company_name"
                    name="company_name"
                    label="Company"
                    value={editing ? formik.values.company_name : user.company_name}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    error={editing && formik.touched.company_name && Boolean(formik.errors.company_name)}
                    helperText={editing && formik.touched.company_name && formik.errors.company_name}
                    disabled={!editing}
                  />
                </Grid>
                {user?.created_at && (
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Member Since"
                      value={new Date(user.created_at).toLocaleDateString()}
                      disabled
                    />
                  </Grid>
                )}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Status"
                    value={user.is_active ? 'Active' : 'Inactive'}
                    disabled
                  />
                </Grid>
              </Grid>

              {editing && (
                <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    disabled={loading}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Save Changes'}
                  </Button>
                  <Button
                    type="button"
                    variant="outlined"
                    onClick={() => {
                      setEditing(false);
                      formik.resetForm();
                      setError(null);
                      setSuccess(null);
                    }}
                  >
                    Cancel
                  </Button>
                </Box>
              )}
            </form>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ProfilePage;