# AI PC Builder

## Team
- Christian Calvo: kuzoto@vt.edu
- Dawson Smedt: dtsmedt@vt.edu
- Tyler Arb: wtylerarb@vt.edu
- Rachana Chengari: rachanac@vt.edu

AI PC Builder is a full-stack app that streamlines the PC build or upgrade process.

It combines:
- A local parts dataset search
- Rule-based compatibility checks
- AI-generated recommendations

## Problem It Solves

Building or upgrading a PC is hard because:
- Parts must be compatible (socket type, RAM generation, PSU sizing, form factor, etc.)
- There are many options for each component
- Users often want recommendations based on budget and use case

This project reduces that complexity by:
- Letting users select parts in a guided UI
- Running compatibility checks automatically as selections change
- Producing AI recommendations with compatibility context and budget guidance

## Project Structure

- `compatability.py`: FastAPI backend + compatibility engine + OpenAI integration
- `frontend/`: React + Vite frontend
- `pc-part-dataset/`: local JSON hardware dataset used for part lookup

## Tech Stack

- Backend: Python, FastAPI, OpenAI Python SDK, python-dotenv
- Frontend: React, TypeScript, Vite
- Data: local `pc-part-dataset` JSON files

## Prerequisites

- Python 3.10+ (3.11 recommended)
- Node.js 18+ and npm
- Local dataset directory at:
  - `pc-part-dataset/data/json`

## Dependencies

### Backend dependencies

Install from project root:

```bash
pip install fastapi uvicorn openai python-dotenv
```

### Frontend dependencies

Install in `frontend/`:

```bash
cd frontend
npm install
```

## Environment Variables

### Frontend

Create `frontend/.env` with:

```bash
VITE_OPENAI_API_KEY=your_openai_api_key_here
```

The frontend sends this key to the backend for AI recommendation calls.

### Backend (optional for server mode)

No key is strictly required in backend env for the web app flow, because the frontend sends it per request.

For CLI usage of `compatability.py` directly, set:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

## How To Run

Open two terminals from the project root (`AI-PC-Builder`).

### 1. Start backend API

```bash
uvicorn compatability:app --reload --port 8000
```

Backend runs at `http://localhost:8000`.

### 2. Start frontend

```bash
cd frontend
npm run dev
```

Frontend runs at `http://localhost:5173` (default Vite port).

## Usage

1. Open the frontend URL in your browser.
2. Select parts and set budget/use case.
3. Compatibility checks update automatically as you choose/change parts.
4. Click:
   - `Generate Build` for full build recommendations
   - `Recommend Upgrade` for upgrade-focused recommendations

## Notes

- The dataset prices are historical snapshots and may be outdated.
- Compatibility output only includes checks for components currently selected by the user.