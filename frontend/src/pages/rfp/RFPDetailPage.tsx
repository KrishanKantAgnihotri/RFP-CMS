import React from 'react';
import { Box, Typography, Button, Paper, Grid } from '@mui/material';
import { useParams, Link } from 'react-router-dom';

const RFPDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          RFP Details
        </Typography>
        <Button component={Link} to="/rfps" variant="outlined">
          Back to List
        </Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              RFP ID: {id}
            </Typography>
            <Typography paragraph>
              This is a placeholder for RFP details. In a real application, you would see the RFP information here.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default RFPDetailPage;