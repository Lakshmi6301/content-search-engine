# ContentSearch - Frontend (Lakshmi)

## Tech stack
- React
- Axios

## Setup
1. Open PowerShell in this folder.
2. Run `npm install`
3. Created `.env` by copying `.env.example` and adjust `REACT_APP_BACKEND_URL` if needed.
4. Run `npm start`
5. App runs at http://localhost:3000


- Backend should expose a GET `/search?q=...` endpoint returning JSON `{ results: [ { title, text, id, snippet, content } ] }`
- backend endpoint differs, update `src/api.js` or `REACT_APP_BACKEND_URL`.
- backend allows CORS from http://localhost:3000
