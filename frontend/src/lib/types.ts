export type VerdictType = 
  | "SUPPORTED"
  | "PARTIALLY_SUPPORTED"
  | "CONTRADICTED"
  | "INSUFFICIENT_EVIDENCE"
  | "UNRESOLVED_CONFLICT";

export interface AtomicClaim {
  id: string;
  statement: string;
  subject?: string;
  predicate?: string;
  object?: string;
  constraints_json: Record<string, any>;
  verification_requirements_json: string[];
  status: string;
  confidence: number;
  evidence_count: number;
  contradiction_count: number;
}

export interface Source {
  id: string;
  name: string;
  file_type: string;
  source_type: string;
  derived_from_source_id?: string;
  created_at: string;
}

export interface EventItem {
  id: string;
  event_type: string;
  date_iso?: string;
  display_date: string;
  location?: string;
  description: string;
  is_deadline: boolean;
  source_name?: string;
}

export interface Contradiction {
  id: string;
  contradiction_type: string;
  statement_a: string;
  source_a_name?: string;
  statement_b: string;
  source_b_name?: string;
  severity: string;
  status: string;
  resolution_summary?: string;
}

export interface Hypothesis {
  id: string;
  contradiction_id?: string;
  statement: string;
  search_requirements_json: string[];
  status: string;
  findings?: string;
}

export interface EvidenceGap {
  id: string;
  description: string;
  why_it_matters: string;
  next_best_evidence: string;
  status: string;
}

export interface InvestigationStep {
  step_number: number;
  step_type: string;
  title: string;
  detail: string;
  timestamp: string;
}

export interface CaseDetail {
  id: string;
  title: string;
  claim_statement: string;
  mode: string;
  status: string;
  verdict?: VerdictType;
  verdict_reasoning?: string;
  evidence_strength_json?: Record<string, any>;
  created_at: string;
  atomic_claims: AtomicClaim[];
  sources: Source[];
  events: EventItem[];
  contradictions: Contradiction[];
  hypotheses: Hypothesis[];
  evidence_gaps: EvidenceGap[];
  steps: InvestigationStep[];
}

export interface GraphData {
  nodes: any[];
  edges: any[];
  stats: {
    total_nodes: number;
    total_edges: number;
  };
}
