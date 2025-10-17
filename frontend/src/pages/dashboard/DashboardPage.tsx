import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
  Chip,
  Button,
  Paper
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import { RFP } from '../../types';

interface DashboardStats {
  total_rfps: number;
  active_rfps: number;
  pending_responses: number;
  completed_rfps: number;
}

const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentRFPs, setRecentRFPs] = useState<RFP[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch dashboard stats
      const statsResponse = await api.get('/rfps/stats');
      setStats(statsResponse.data);
      
      // Fetch recent RFPs
      const rfpsResponse = await api.get('/rfps?limit=5&sort=-created_at');
      setRecentRFPs(rfpsResponse.data.items || rfpsResponse.data);
      
    } catch (err: any) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'default';
      case 'published': return 'primary';
      case 'closed': return 'secondary';
      case 'awarded': return 'success';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Welcome back, {user?.first_name || user?.username?.split('@')[0] || 'User'}!
        </Typography>
        {user?.role === 'Buyer' && (
          <Button 
            variant="contained" 
            color="primary"
            onClick={() => navigate('/rfps/create')}
          >
            Create New RFP
          </Button>
        )}
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom color="textSecondary">
                Total RFPs
              </Typography>
              <Typography variant="h3" component="p" color="primary">
                {stats?.total_rfps || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom color="textSecondary">
                Active RFPs
              </Typography>
              <Typography variant="h3" component="p" color="success.main">
                {stats?.active_rfps || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom color="textSecondary">
                Pending Responses
              </Typography>
              <Typography variant="h3" component="p" color="warning.main">
                {stats?.pending_responses || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom color="textSecondary">
                Completed
              </Typography>
              <Typography variant="h3" component="p" color="info.main">
                {stats?.completed_rfps || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6" component="h2">
                Recent RFPs
              </Typography>
              <Button 
                variant="outlined" 
                onClick={() => navigate('/rfps')}
              >
                View All
              </Button>
            </Box>
            
            {recentRFPs.length === 0 ? (
              <Typography color="textSecondary" textAlign="center" py={3}>
                No RFPs found. {user?.role === 'Buyer' ? 'Create your first RFP to get started!' : 'Check back later for new opportunities.'}
              </Typography>
            ) : (
              <List>
                {recentRFPs.map((rfp) => (
                  <ListItem 
                    key={rfp.id} 
                    divider
                    sx={{ 
                      cursor: 'pointer',
                      '&:hover': { backgroundColor: 'action.hover' }
                    }}
                    onClick={() => navigate(`/rfps/${rfp.id}`)}
                  >
                    <ListItemText
                      primary={rfp.title}
                      secondary={
                        <Box>
                          <Typography variant="body2" color="textSecondary">
                            {rfp.description?.substring(0, 100)}...
                          </Typography>
                          <Box mt={1}>
                            <Chip 
                              label={rfp.status} 
                              size="small" 
                              color={getStatusColor(rfp.status) as any}
                              sx={{ mr: 1 }}
                            />
                            <Typography variant="caption" color="textSecondary">
                              Due: {new Date(rfp.submission_deadline).toLocaleDateString()}
                            </Typography>
                          </Box>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage;