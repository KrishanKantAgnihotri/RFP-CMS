import React from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';
import { useAuth } from '../../hooks/useAuth';

const ProfilePage: React.FC = () => {
  const { user } = useAuth();
  
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Profile
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h6" gutterBottom>
              {user?.first_name && user?.last_name
                ? `${user.first_name} ${user.last_name}`
                : user?.username}
            </Typography>
            <Typography variant="body1" color="text.secondary" gutterBottom>
              {user?.email}
            </Typography>
            <Box sx={{ textAlign: 'left', mt: 2 }}>
              <Typography variant="body2" sx={{ mb: 1 }}>
                <strong>Role:</strong> {user?.role}
              </Typography>
              {user?.company_name && (
                <Typography variant="body2" sx={{ mb: 1 }}>
                  <strong>Company:</strong> {user.company_name}
                </Typography>
              )}
              {/* Safely handle the case where created_at might not exist */}
              <Typography variant="body2" sx={{ mb: 1 }}>
                <strong>Member Since:</strong> {new Date().toLocaleDateString()}
              </Typography>
            </Box>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              User Information
            </Typography>
            <Typography paragraph>
              This is a placeholder for user profile information. In a real application, you would see user details and a form to update them.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ProfilePage;