import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Paper,
  Grid,
  TextField,
  Alert,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  OutlinedInput,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import { RFP } from '../../types';

const EditRFPPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [fetchLoading, setFetchLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [rfp, setRfp] = useState<RFP | null>(null);

  const formik = useFormik({
    initialValues: {
      title: '',
      description: '',
      requirements: '',
      submission_deadline: new Date(),
      budget: '',
      categories: [],
      evaluation_criteria: '',
      terms_conditions: '',
      status: 'draft',
    },
    validationSchema: Yup.object({
      title: Yup.string().required('Title is required'),
      description: Yup.string().required('Description is required'),
      requirements: Yup.string().required('Requirements are required'),
      submission_deadline: Yup.date()
        .min(new Date(), 'Deadline must be in the future')
        .required('Submission deadline is required'),
      budget: Yup.number().positive('Budget must be positive'),
      evaluation_criteria: Yup.string().required('Evaluation criteria are required'),
    }),
    onSubmit: async (values) => {
      if (user?.role !== 'Buyer') {
        setError('Only buyers can edit RFPs');
        return;
      }

      setLoading(true);
      setError(null);
      
      try {
        const rfpData = {
          ...values,
          budget: values.budget ? parseFloat(values.budget) : null,
        };
        
        await api.put(`/rfps/${id}`, rfpData);
        navigate(`/rfps/${id}`);
      } catch (err: any) {
        console.error('Failed to update RFP:', err);
        if (err.response?.data?.detail) {
          if (typeof err.response.data.detail === 'string') {
            setError(err.response.data.detail);
          } else if (Array.isArray(err.response.data.detail)) {
            setError(err.response.data.detail.map((e: any) => e.msg).join(', '));
          } else {
            setError('Failed to update RFP. Please check your information.');
          }
        } else {
          setError('Failed to update RFP. Please try again.');
        }
      } finally {
        setLoading(false);
      }
    },
  });

  useEffect(() => {
    const fetchRFP = async () => {
      if (!id) return;
      
      try {
        setFetchLoading(true);
        const response = await api.get(`/rfps/${id}`);
        const rfpData = response.data;
        setRfp(rfpData);
        
        // Populate form with existing data
        formik.setValues({
          title: rfpData.title || '',
          description: rfpData.description || '',
          requirements: rfpData.requirements || '',
          submission_deadline: new Date(rfpData.submission_deadline),
          budget: rfpData.budget ? rfpData.budget.toString() : '',
          categories: rfpData.categories || [],
          evaluation_criteria: rfpData.evaluation_criteria || '',
          terms_conditions: rfpData.terms_conditions || '',
          status: rfpData.status || 'draft',
        });
      } catch (err: any) {
        console.error('Failed to fetch RFP:', err);
        setError('Failed to load RFP data. Please try again.');
      } finally {
        setFetchLoading(false);
      }
    };

    fetchRFP();
  }, [id]);

  const categoryOptions = [
    'Technology',
    'Construction',
    'Consulting',
    'Marketing',
    'Legal',
    'Finance',
    'Healthcare',
    'Education',
    'Manufacturing',
    'Other',
  ];

  const handleCategoryChange = (event: any) => {
    const value = event.target.value;
    formik.setFieldValue('categories', typeof value === 'string' ? value.split(',') : value);
  };

  // Check if user can edit this RFP
  const canEdit = user?.role === 'Buyer' && rfp?.buyer_id === user?.id;

  if (fetchLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (!rfp) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 3 }}>
          RFP not found or you don't have permission to edit it.
        </Alert>
        <Button onClick={() => navigate('/rfps')} variant="outlined">
          Back to RFPs
        </Button>
      </Box>
    );
  }

  if (!canEdit) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 3 }}>
          You don't have permission to edit this RFP.
        </Alert>
        <Button onClick={() => navigate(`/rfps/${id}`)} variant="outlined">
          Back to RFP
        </Button>
      </Box>
    );
  }

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h4" component="h1">
            Edit RFP
          </Typography>
          <Button onClick={() => navigate(`/rfps/${id}`)} variant="outlined">
            Cancel
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Paper sx={{ p: 3 }}>
          <form onSubmit={formik.handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  id="title"
                  name="title"
                  label="RFP Title"
                  value={formik.values.title}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  error={formik.touched.title && Boolean(formik.errors.title)}
                  helperText={formik.touched.title && formik.errors.title}
                  required
                />
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  id="description"
                  name="description"
                  label="Description"
                  value={formik.values.description}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  error={formik.touched.description && Boolean(formik.errors.description)}
                  helperText={formik.touched.description && formik.errors.description}
                  required
                />
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={6}
                  id="requirements"
                  name="requirements"
                  label="Requirements"
                  value={formik.values.requirements}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  error={formik.touched.requirements && Boolean(formik.errors.requirements)}
                  helperText={formik.touched.requirements && formik.errors.requirements}
                  required
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <DatePicker
                  label="Submission Deadline"
                  value={formik.values.submission_deadline}
                  onChange={(value) => formik.setFieldValue('submission_deadline', value)}
                  slotProps={{
                    textField: {
                      fullWidth: true,
                      error: formik.touched.submission_deadline && Boolean(formik.errors.submission_deadline),
                      helperText: formik.touched.submission_deadline && formik.errors.submission_deadline 
                        ? String(formik.errors.submission_deadline)
                        : undefined,
                      required: true,
                    },
                  }}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  id="budget"
                  name="budget"
                  label="Budget (USD)"
                  type="number"
                  value={formik.values.budget}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  error={formik.touched.budget && Boolean(formik.errors.budget)}
                  helperText={formik.touched.budget && formik.errors.budget}
                />
              </Grid>

              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Categories</InputLabel>
                  <Select
                    multiple
                    value={formik.values.categories}
                    onChange={handleCategoryChange}
                    input={<OutlinedInput label="Categories" />}
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {selected.map((value) => (
                          <Chip key={value} label={value} />
                        ))}
                      </Box>
                    )}
                  >
                    {categoryOptions.map((category) => (
                      <MenuItem key={category} value={category}>
                        {category}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  id="evaluation_criteria"
                  name="evaluation_criteria"
                  label="Evaluation Criteria"
                  value={formik.values.evaluation_criteria}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  error={formik.touched.evaluation_criteria && Boolean(formik.errors.evaluation_criteria)}
                  helperText={formik.touched.evaluation_criteria && formik.errors.evaluation_criteria}
                  required
                />
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  id="terms_conditions"
                  name="terms_conditions"
                  label="Terms and Conditions"
                  value={formik.values.terms_conditions}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                />
              </Grid>

              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>
                  <Select
                    id="status"
                    name="status"
                    value={formik.values.status}
                    onChange={formik.handleChange}
                    label="Status"
                  >
                    <MenuItem value="draft">Draft</MenuItem>
                    <MenuItem value="published">Published</MenuItem>
                    <MenuItem value="closed">Closed</MenuItem>
                    <MenuItem value="awarded">Awarded</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                  <Button
                    type="button"
                    variant="outlined"
                    onClick={() => navigate(`/rfps/${id}`)}
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    disabled={loading}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Update RFP'}
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </form>
        </Paper>
      </Box>
    </LocalizationProvider>
  );
};

export default EditRFPPage;
