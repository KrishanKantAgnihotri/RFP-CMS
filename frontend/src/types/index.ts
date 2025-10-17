// User types
export interface User {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: 'Buyer' | 'Supplier';
  company_name: string;
  is_active: boolean;
  is_verified: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface UserRegister {
  email: string;
  username: string;
  password: string;
  role: 'Buyer' | 'Supplier';
  first_name?: string;
  last_name?: string;
  company_name?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

// RFP types
export interface RFP {
  id: string;
  title: string;
  description: string;
  buyer_id: string;
  requirements: string;
  submission_deadline: string;
  budget?: number;
  categories?: string[];
  evaluation_criteria?: string;
  terms_conditions?: string;
  status: 'draft' | 'published' | 'closed' | 'awarded';
  attachments?: string[];
  created_at: string;
  updated_at: string;
}

export interface RFPCreate {
  title: string;
  description: string;
  requirements: Record<string, any>;
  deadline?: string;
  category?: string;
  tags?: string[];
}

export interface RFPUpdate {
  title?: string;
  description?: string;
  requirements?: Record<string, any>;
  deadline?: string;
  category?: string;
  tags?: string[];
  status?: 'Draft' | 'Published' | 'Under Review' | 'Completed' | 'Cancelled';
}

// RFP Response types
export interface RFPResponse {
  id: string;
  rfp_id: string;
  supplier_id: string;
  supplier_company?: string;
  proposal_text: string;
  attachments?: string[];
  status: 'submitted' | 'under_review' | 'approved' | 'rejected';
  feedback?: string;
  created_at: string;
  updated_at: string;
}

export interface RFPResponseCreate {
  content: Record<string, any>;
}

export interface RFPResponseUpdate {
  content?: Record<string, any>;
  status?: 'Submitted' | 'Under Review' | 'Approved' | 'Rejected';
  feedback?: string;
}

// Document types
export interface Document {
  id: string;
  filename: string;
  original_filename: string;
  file_path: string;
  file_size: number;
  file_type: string;
  content_type: string;
  user_id: string;
  rfp_id?: string;
  response_id?: string;
  is_public: boolean;
  version: number;
  previous_versions: string[];
  created_at: string;
  updated_at: string;
}

export interface DocumentCreate {
  original_filename: string;
  file_type: string;
  content_type: string;
  is_public?: boolean;
}

// Notification types
export interface Notification {
  id: string;
  user_id: string;
  type: 'email' | 'in_app' | 'sms';
  title: string;
  message: string;
  data: Record<string, any>;
  is_read: boolean;
  is_sent: boolean;
  sent_at?: string;
  read_at?: string;
  created_at: string;
}

export interface NotificationCreate {
  user_id: string;
  type: 'email' | 'in_app' | 'sms';
  title: string;
  message: string;
  data?: Record<string, any>;
}
