import React from 'react';
import { Box, Typography, Button, Paper, Grid } from '@mui/material';
import { Link } from 'react-router-dom';

const CreateRFPPage: React.FC = () => {
  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Create RFP
        </Typography>
        <Button component={Link} to="/rfps" variant="outlined">
          Cancel
        </Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography paragraph>
              This is a placeholder for the RFP creation form. In a real application, you would have a form here.
            </Typography>
            <Button variant="contained" color="primary">
              Submit
            </Button>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CreateRFPPage;