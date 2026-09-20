import { CaseDetail, GraphData } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function fetchCases(): Promise<CaseDetail[]> {
  const res = await fetch(`${API_BASE_URL}/cases`, { cache: 'no-store' });
  if (!res.ok) throw new Error("Failed to fetch cases");
  return res.json();
}

export async function fetchCaseById(id: string): Promise<CaseDetail> {
  const res = await fetch(`${API_BASE_URL}/cases/${id}`, { cache: 'no-store' });
  if (!res.ok) throw new Error("Failed to fetch case details");
  return res.json();
}

export async function createCase(title: string, claim_statement: string, mode: string = "STANDARD"): Promise<CaseDetail> {
  const res = await fetch(`${API_BASE_URL}/cases`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, claim_statement, mode }),
  });
  if (!res.ok) throw new Error("Failed to create case");
  return res.json();
}

export async function fetchCaseGraph(id: string): Promise<GraphData> {
  const res = await fetch(`${API_BASE_URL}/cases/${id}/graph`, { cache: 'no-store' });
  if (!res.ok) throw new Error("Failed to fetch case graph");
  return res.json();
}

export async function submitChallenge(id: string, challenge_question: string): Promise<CaseDetail> {
  const res = await fetch(`${API_BASE_URL}/cases/${id}/challenge`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ challenge_question }),
  });
  if (!res.ok) throw new Error("Failed to submit challenge");
  return res.json();
}

export async function triggerRedTeam(id: string): Promise<CaseDetail> {
  const res = await fetch(`${API_BASE_URL}/cases/${id}/red-team`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ target: "TRY_TO_DISPROVE" }),
  });
  if (!res.ok) throw new Error("Failed to activate red team mode");
  return res.json();
}

export async function loadOneClickDemo(): Promise<CaseDetail> {
  const res = await fetch(`${API_BASE_URL}/demo/load`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to load demo investigation");
  return res.json();
}

export async function triggerExternalSearch(id: string): Promise<CaseDetail> {
  const res = await fetch(`${API_BASE_URL}/cases/${id}/search`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to execute external web search");
  return res.json();
}

