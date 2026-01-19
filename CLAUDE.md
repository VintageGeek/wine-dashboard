# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Wine Collection Dashboard - an interactive web application for managing a wine cellar with 425+ wines. Deployed on Firebase Hosting with Firebase Realtime Database for state sync.

---

## Data Layer Integration

> **IMPORTANT:** The backend is migrating from Firebase/static JSON to Supabase.

**Data Layer Project:** `C:\Users\mikep\Desktop\wine-data-layer`

**Before modifying any of the following, read the interface contract:**
```
C:\Users\mikep\Desktop\wine-data-layer\docs\DASHBOARD_INTEGRATION.md
```

This applies to:
- Wine data fetching (`fetch('/wine_collection.json')`)
- Pull list sync (Firebase RTDB)
- Settings/demo mode (Firebase RTDB)
- Real-time subscriptions

**Key documents in data layer:**
| File | Purpose |
|------|---------|
| `docs/DASHBOARD_INTEGRATION.md` | API contract, migration checklist |
| `docs/DATA_MODEL.md` | Database schema |
| `docs/GOTCHAS.md` | Edge cases to handle |
| `PROGRESS.md` | Migration status |

---

## Folder Structure

```
wine-dashboard/
├── public/                  # Served by Firebase Hosting
│   ├── index.html           # Desktop/tablet UI
│   ├── mobile.html          # Mobile-optimized UI
│   └── settings.html        # Admin settings page
├── data/                    # Data files (gitignored)
│   ├── wine_collection.json # Wine catalog
│   └── pull_list.json       # Pull list state
├── scripts/                 # Development tools
│   └── server.py            # Local dev server
├── .gitignore
├── .firebaserc
├── firebase.json
└── CLAUDE.md
```

## Commands (Windows Environment)

**Important**: This project runs on Windows. Use PowerShell with `-ExecutionPolicy Bypass` for npm/npx commands.

```powershell
# Start local development server
powershell -ExecutionPolicy Bypass -Command "cd 'C:\Users\mikep\Desktop\dashboard'; python scripts/server.py"
# Serves at http://localhost:8080

# Deploy to DEV (test changes here first)
powershell -ExecutionPolicy Bypass -Command "cd 'C:\Users\mikep\Desktop\dashboard'; npx firebase-tools deploy --only hosting:dev"
# URL: https://wine-explorer-puller-dev.web.app

# Deploy to PROD (after validating on dev)
powershell -ExecutionPolicy Bypass -Command "cd 'C:\Users\mikep\Desktop\dashboard'; npx firebase-tools deploy --only hosting:prod"
# URL: https://wine-explorer-puller.web.app

# Deploy to BOTH (use sparingly)
powershell -ExecutionPolicy Bypass -Command "cd 'C:\Users\mikep\Desktop\dashboard'; npx firebase-tools deploy"
```

### Deployment Workflow (CRITICAL)
1. **ALWAYS deploy to dev first** - never go straight to prod
2. **Ask user before deploying to prod** - get explicit approval after dev is verified
3. Deploy dev: `--only hosting:dev`
4. Deploy prod: `--only hosting:prod`

### Common Deployment Errors to Avoid
- **DO NOT** deploy directly to prod without testing on dev first
- **DO NOT** use `--only hosting` without a target - always specify `:dev` or `:prod`
- **DO NOT** use bash `cd` with Windows paths (backslashes are treated as escape characters)
- **DO NOT** use plain `npx` in PowerShell without `-ExecutionPolicy Bypass` (blocked by default)
- **ALWAYS** wrap the path in single quotes when using PowerShell

## Architecture

### Frontend (Vanilla JS, No Frameworks)
- **public/index.html**: Desktop/tablet UI (2,800+ lines, all CSS/JS inline)
- **public/mobile.html**: Mobile-optimized UI with bottom navigation, card-based layout, touch gestures
- **public/settings.html**: Hidden admin page for demo mode toggle (not linked from main pages)
- Both index.html and mobile.html share the same data source and Firebase sync

### Settings Page (public/settings.html)
- URL: Not linked publicly, access directly via `/settings.html`
- Basic auth required (credentials in file - replace placeholders with actual values)
- Controls `settings/demoMode` in Firebase
- Demo mode hides all dollar amounts across both pages

### Backend
- **scripts/server.py**: Python HTTP server (port 8080)
  - Serves static files from public/
  - POST `/pull_list.json`: Persists marked wines to data/
  - CORS enabled

### Data (gitignored)
- **data/wine_collection.json**: Wine catalog (425 wines, ~38K lines)
- **data/pull_list.json**: Marked wines state (synced to Firebase Realtime Database)

### Firebase
- Project: `wine-explorer-puller`
- Database: `https://wine-explorer-puller-default-rtdb.firebaseio.com`
- Hosting (multi-site):
  - **prod**: https://wine-explorer-puller.web.app
  - **dev**: https://wine-explorer-puller-dev.web.app
- Both sites serve from `public/` and share the same database

## Key Concepts

### State Management (in-memory JavaScript)
- `wineData`: Full dataset from JSON
- `filteredWines`: Current filtered results
- `activeFilters`: Object tracking filter states (country, region, varietal, vintage, drinkWindow, wineType, search)
- `markedForRemoval`: Map<wineId, quantity> for pull list
- `locationDrillLevel`: Chart drill state (country → region → producer)

### Drink Window Logic
- Calculates status from `drink_date_min`/`drink_date_max` vs current year
- Status: "Ready Now" (green), "Hold" (blue), "Past Peak" (red)
- Vintage "1001" treated as NV (Non-Vintage)

### Design System
- Apple-inspired (SF Pro typography, Cupertino colors)
- Primary accent: #0071e3
- Wine colors: Red #9d174d, White/Gold #b45309, Rosé #db2777, Sparkling #0369a1
- CSS variables in `:root` control theming

## Data Schema

```javascript
wine: {
  id, wine_name, vintage, producer, varietal, region, country,
  type, category, quantity, valuation, location, bin,
  drink_date_min, drink_date_max,
  tasting_notes: { appearance, nose, palate, finish, overall },
  characteristics: { body, sweetness, acidity, tannin, alcohol, complexity },
  aroma_descriptors: [], flavor_descriptors: [], food_pairings: []
}
```

## Important: Keep Both Pages in Sync

When making functionality changes (filters, data handling, Firebase sync, calculations), **both index.html and mobile.html must be updated**. They share the same data and Firebase backend but have separate codebases. UI/styling changes may differ, but core logic should stay synchronized.

## Mobile vs Desktop Differences

| Feature | Desktop (index.html) | Mobile (mobile.html) |
|---------|---------------------|---------------------|
| Layout | 4-column chart grid | Horizontal scroll carousel |
| Wine list | Table with sortable columns | Card-based with touch targets |
| Filters | Slide-in right panel | Full-screen bottom sheet |
| Pull list | Slide-in right panel | Bottom sheet |
| Navigation | Header buttons | Fixed bottom nav bar |
