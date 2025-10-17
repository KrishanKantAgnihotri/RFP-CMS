import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Paper,
  Grid,
  Chip,
  Divider,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import { RFP, RFPResponse } from '../../types';

const RFPDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [rfp, setRfp] = useState<RFP | null>(null);
  const [responses, setResponses] = useState<RFPResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [responseDialogOpen, setResponseDialogOpen] = useState(false);
  const [responseText, setResponseText] = useState('');
  const [submittingResponse, setSubmittingResponse] = useState(false);

  useEffect(() => {
    if (id) {
      fetchRFPDetails();
    }
  }, [id]);

  const fetchRFPDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [rfpResponse, responsesResponse] = await Promise.all([
        api.get(`/rfps/${id}`),
        api.get(`/rfps/${id}/responses`).catch(() => ({ data: [] })), // Handle case where responses endpoint might not exist
      ]);
      
      setRfp(rfpResponse.data);
      setResponses(responsesResponse.data);
      
    } catch (err: any) {
      console.error('Failed to fetch RFP details:', err);
      if (err.response?.status === 404) {
        setError('RFP not found.');
      } else {
        setError('Failed to load RFP details. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitResponse = async () => {
    if (!responseText.trim()) return;
    
    setSubmittingResponse(true);
    try {
      await api.post(`/rfps/${id}/responses`, {
        proposal_text: responseText,
      });
      
      setResponseDialogOpen(false);
      setResponseText('');
      fetchRFPDetails(); // Refresh to show new response
      
    } catch (err: any) {
      console.error('Failed to submit response:', err);
      // Handle error - could show a toast or alert
    } finally {
      setSubmittingResponse(false);
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

  const canSubmitResponse = () => {
    return user?.role === 'Supplier' && rfp?.status === 'published';
  };

  const canEditRFP = () => {
    return user?.role === 'Buyer' && rfp?.buyer_id === user?.id;
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !rfp) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error || 'RFP not found'}
        </Alert>
        <Button onClick={() => navigate('/rfps')} variant="outlined">
          Back to RFPs
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          {rfp.title}
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          {canSubmitResponse() && (
            <Button
              variant="contained"
              color="primary"
              onClick={() => setResponseDialogOpen(true)}
            >
              Submit Response
            </Button>
          )}
          {canEditRFP() && (
            <Button
              variant="outlined"
              onClick={() => navigate(`/rfps/${id}/edit`)}
            >
              Edit RFP
            </Button>
          )}
          <Button onClick={() => navigate('/rfps')} variant="outlined">
            Back to List
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box sx={{ mb: 2 }}>
              <Chip
                label={rfp.status}
                color={getStatusColor(rfp.status) as any}
                sx={{ mb: 2 }}
              />
            </Box>
            
            <Typography variant="h6" gutterBottom>
              Description
            </Typography>
            <Typography paragraph>
              {rfp.description}
            </Typography>
            
            <Divider sx={{ my: 2 }} />
            
            <Typography variant="h6" gutterBottom>
              Requirements
            </Typography>
            <Typography paragraph style={{ whiteSpace: 'pre-wrap' }}>
              {rfp.requirements}
            </Typography>
            
            {rfp.evaluation_criteria && (
              <>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Evaluation Criteria
                </Typography>
                <Typography paragraph style={{ whiteSpace: 'pre-wrap' }}>
                  {rfp.evaluation_criteria}
                </Typography>
              </>
            )}
            
            {rfp.terms_conditions && (
              <>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Terms and Conditions
                </Typography>
                <Typography paragraph style={{ whiteSpace: 'pre-wrap' }}>
                  {rfp.terms_conditions}
                </Typography>
              </>
            )}
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              RFP Information
            </Typography>
            
            <Typography variant="body2" color="textSecondary" gutterBottom>
              Submission Deadline
            </Typography>
            <Typography paragraph>
              {new Date(rfp.submission_deadline).toLocaleDateString()}
            </Typography>
            
            {rfp.budget && (
              <>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Budget
                </Typography>
                <Typography paragraph>
                  ${rfp.budget.toLocaleString()}
                </Typography>
              </>
            )}
            
            {rfp.categories && rfp.categories.length > 0 && (
              <>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Categories
                </Typography>
                <Box sx={{ mb: 2 }}>
                  {rfp.categories.map((category) => (
                    <Chip
                      key={category}
                      label={category}
                      size="small"
                      sx={{ mr: 1, mb: 1 }}
                    />
                  ))}
                </Box>
              </>
            )}
            
            <Typography variant="body2" color="textSecondary" gutterBottom>
              Created
            </Typography>
            <Typography>
              {new Date(rfp.created_at).toLocaleDateString()}
            </Typography>
          </Paper>
          
          {responses.length > 0 && (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Responses ({responses.length})
              </Typography>
              
              <List>
                {responses.map((response) => (
                  <ListItem key={response.id} divider>
                    <ListItemText
                      primary={`Response from ${response.supplier_company || 'Supplier'}`}
                      secondary={`Submitted: ${new Date(response.created_at).toLocaleDateString()}`}
                    />
                  </ListItem>
                ))}
              </List>
            </Paper>
          )}
        </Grid>
      </Grid>

      {/* Response Dialog */}
      <Dialog
        open={responseDialogOpen}
        onClose={() => setResponseDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Submit Response to RFP</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            multiline
            rows={8}
            label="Your Proposal"
            value={responseText}
            onChange={(e) => setResponseText(e.target.value)}
            placeholder="Describe your proposal, approach, timeline, and any other relevant details..."
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setResponseDialogOpen(false)}>
            Cancel
          </Button>
          <Button
            onClick={handleSubmitResponse}
            variant="contained"
            disabled={!responseText.trim() || submittingResponse}
          >
            {submittingResponse ? <CircularProgress size={24} /> : 'Submit Response'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default RFPDetailPage;