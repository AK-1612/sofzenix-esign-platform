// API client for the AI Call Automation from Excel feature (ai-service).
// Configure NEXT_PUBLIC_AI_SERVICE_URL in .env.local; defaults to local dev.

const AI_SERVICE_URL =
  process.env.NEXT_PUBLIC_AI_SERVICE_URL || "http://localhost:8000";

export type CallStatus =
  | "Not Called"
  | "Calling"
  | "Connected"
  | "No Answer"
  | "Busy"
  | "Failed"
  | "Interested"
  | "Not Interested"
  | "Follow-up"
  | "Appointment"
  | "Converted";

export interface Lead {
  id: string;
  name: string;
  mobile: string;
  service?: string;
  budget?: string;
  city?: string;
  call_status: CallStatus;
  created_at: string;
}

export interface CallResult {
  id: string;
  lead_id: string;
  name: string;
  mobile: string;
  call_status: CallStatus;
  duration_seconds: number;
  interest: "High" | "Medium" | "Low" | "—";
  score: number | null;
  next_action: string;
  transcript?: string | null;
  notes?: string | null;
  updated_at: string;
}

export interface LeadUploadSummary {
  total_rows: number;
  imported: number;
  skipped: number;
  errors: string[];
  leads: Lead[];
}

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`Request failed (${res.status}): ${body}`);
  }
  return res.json();
}

export const leadCallingService = {
  async uploadLeads(file: File): Promise<LeadUploadSummary> {
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch(`${AI_SERVICE_URL}/api/v1/leads/upload`, {
      method: "POST",
      body: formData,
    });
    return handle<LeadUploadSummary>(res);
  },

  async listLeads(): Promise<Lead[]> {
    const res = await fetch(`${AI_SERVICE_URL}/api/v1/leads`);
    return handle<Lead[]>(res);
  },

  async startCall(leadId: string): Promise<CallResult> {
    const res = await fetch(`${AI_SERVICE_URL}/api/v1/leads/${leadId}/call`, {
      method: "POST",
    });
    return handle<CallResult>(res);
  },

  async listResults(status?: CallStatus): Promise<CallResult[]> {
    const query = status ? `?status=${encodeURIComponent(status)}` : "";
    const res = await fetch(`${AI_SERVICE_URL}/api/v1/leads/results${query}`);
    return handle<CallResult[]>(res);
  },

  exportResultsUrl(): string {
    return `${AI_SERVICE_URL}/api/v1/leads/results/export`;
  },
};
