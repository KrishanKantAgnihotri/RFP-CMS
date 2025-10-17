import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  TextField,
  InputAdornment,
  CircularProgress,
  Alert,
  Pagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import { RFP } from '../../types';

const RFPListPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [rfps, setRfps] = useState<RFP[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const itemsPerPage = 10;

  useEffect(() => {
    fetchRFPs();
  }, [page, searchTerm, statusFilter]);

  const fetchRFPs = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const params = new URLSearchParams({
        page: page.toString(),
        limit: itemsPerPage.toString(),
      });
      
      if (searchTerm) {
        params.append('search', searchTerm);
      }
      
      if (statusFilter) {
        params.append('status', statusFilter);
      }
      
      const response = await api.get(`/rfps?${params}`);
      const data = response.data;
      
      setRfps(data.items || data);
      setTotalPages(Math.ceil((data.total || data.length) / itemsPerPage));
      
    } catch (err: any) {
      console.error('Failed to fetch RFPs:', err);
      setError('Failed to load RFPs. Please try again.');
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

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setPage(1); // Reset to first page when searching
  };

  const handleStatusFilterChange = (event: any) => {
    setStatusFilter(event.target.value);
    setPage(1); // Reset to first page when filtering
  };

  const handlePageChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          RFPs
        </Typography>
        {user?.role === 'Buyer' && (
          <Button component={Link} to="/rfps/create" variant="contained" color="primary">
            Create RFP
          </Button>
        )}
      </Box>

      {/* Filters */}
      <Box sx={{ mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              placeholder="Search RFPs..."
              value={searchTerm}
              onChange={handleSearchChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Status</InputLabel>
              <Select
                value={statusFilter}
                onChange={handleStatusFilterChange}
                label="Status"
              >
                <MenuItem value="">All Statuses</MenuItem>
                <MenuItem value="draft">Draft</MenuItem>
                <MenuItem value="published">Published</MenuItem>
                <MenuItem value="closed">Closed</MenuItem>
                <MenuItem value="awarded">Awarded</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      ) : (
        <>
          {rfps.length === 0 ? (
            <Card>
              <CardContent>
                <Typography textAlign="center" color="textSecondary" py={3}>
                  {searchTerm || statusFilter
                    ? 'No RFPs match your search criteria.'
                    : user?.role === 'Buyer'
                    ? 'No RFPs found. Create your first RFP to get started!'
                    : 'No RFPs available at the moment. Check back later for new opportunities.'}
                </Typography>
              </CardContent>
            </Card>
          ) : (
            <Grid container spacing={3}>
              {rfps.map((rfp) => (
                <Grid item xs={12} md={6} lg={4} key={rfp.id}>
                  <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <CardContent sx={{ flexGrow: 1 }}>
                      <Box sx={{ mb: 2 }}>
                        <Chip
                          label={rfp.status}
                          size="small"
                          color={getStatusColor(rfp.status) as any}
                        />
                      </Box>
                      
                      <Typography variant="h6" component="h2" gutterBottom>
                        {rfp.title}
                      </Typography>
                      
                      <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                        {rfp.description?.substring(0, 150)}...
                      </Typography>
                      
                      <Typography variant="caption" color="textSecondary">
                        Deadline: {new Date(rfp.submission_deadline).toLocaleDateString()}
                      </Typography>
                      
                      {rfp.budget && (
                        <Typography variant="caption" display="block" color="textSecondary">
                          Budget: ${rfp.budget.toLocaleString()}
                        </Typography>
                      )}
                    </CardContent>
                    
                    <CardActions>
                      <Button
                        size="small"
                        color="primary"
                        onClick={() => navigate(`/rfps/${rfp.id}`)}
                      >
                        View Details
                      </Button>
                      {user?.role === 'Supplier' && rfp.status === 'published' && (
                        <Button
                          size="small"
                          variant="contained"
                          color="primary"
                          onClick={() => navigate(`/rfps/${rfp.id}/respond`)}
                        >
                          Submit Response
                        </Button>
                      )}
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}

          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={handlePageChange}
                color="primary"
              />
            </Box>
          )}
        </>
      )}
    </Box>
  );
};

export default RFPListPage;