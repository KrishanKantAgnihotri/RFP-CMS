import React from 'react';
import { Box, Typography, Button, Grid, Paper } from '@mui/material';
import { Link } from 'react-router-dom';

const RFPListPage: React.FC = () => {
  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          RFP List
        </Typography>
        <Button component={Link} to="/rfps/create" variant="contained" color="primary">
          Create RFP
        </Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography paragraph>
              No RFPs available.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default RFPListPage;