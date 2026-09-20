# TRUTHCHAIN — Render & Vercel Deployment Blueprint

This document provides explicit, step-by-step instructions for deploying TRUTHCHAIN to production using Render (Backend + PostgreSQL) and Vercel (Frontend).

---

## 1. Render Backend & PostgreSQL Deployment

### A. Create PostgreSQL Database on Render
1. Go to [Render Dashboard](https://dashboard.render.com/) -> **New +** -> **PostgreSQL**.
2. **Name**: `truthchain-db`
3. **Region**: Oregon (or nearest)
4. Copy the **Internal Database URL** or **External Database URL** (e.g. `postgresql://user:pass@ep-xyz.render.com/truthchain`).

### B. Deploy FastAPI Web Service on Render
1. Go to **New +** -> **Web Service**.
2. Connect your **GitHub Repository** (`truthchain`).
3. Set configuration:
   - **Name**: `truthchain-backend`
   - **Root Directory**: `backend` (or leave blank if executing from root)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set **Environment Variables**:
   - `DATABASE_URL`: `<Your Render PostgreSQL URL>`
   - `GROQ_API_KEY`: `<Your Groq Cloud API Key>`
   - `GROQ_MODEL`: `openai/gpt-oss-20b`
   - `CORS_ORIGINS`: `https://truthchain.vercel.app` (or your Vercel URL)
5. **Health Check Path**: `/health`

---

## 2. Vercel Frontend Deployment

1. Go to [Vercel Dashboard](https://vercel.com/dashboard) -> **Add New...** -> **Project**.
2. Import your **GitHub Repository** (`truthchain`).
3. Configure project settings:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
4. Set **Environment Variables**:
   - `NEXT_PUBLIC_API_URL`: `https://truthchain-backend.onrender.com/api`
5. Click **Deploy**.

---

## 3. Post-Deployment Validation Checklist

- [ ] Backend health check responds OK (`https://truthchain-backend.onrender.com/health`).
- [ ] Vercel frontend loads without CORS errors (`https://truthchain.vercel.app`).
- [ ] Clicking **"RUN LIVE INVESTIGATION"** loads the 11-file procurement demo.
- [ ] Claim decomposition executes with real Groq LLM API.
- [ ] External Web Search executes Tavily / DuckDuckGo search.
- [ ] Multimodal upload & RapidOCR process scanned files.
- [ ] PDF Investigation Report exports cleanly.
