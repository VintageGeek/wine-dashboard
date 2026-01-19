# Wine Dashboard

Web dashboard for viewing and managing a wine collection. Displays inventory, valuations, tasting notes, and pull lists.

## Live

- **Production**: https://wine-explorer-puller.web.app
- **Dev**: https://wine-explorer-puller-dev.web.app

## Features

- **Wine Inventory**: Browse 425+ wines with filtering and sorting
- **Charts**: Visualize collection by country, vintage, varietal, drink window
- **Pull List**: Mark wines to pull from cellar, copy list to clipboard
- **Demo Mode**: Hide valuations for screen sharing
- **Mobile Optimized**: Dedicated mobile UI with touch gestures
- **Secure**: Supabase Auth with TOTP MFA required

## Pages

| Page | Purpose |
|------|---------|
| `index.html` | Desktop wine browser |
| `mobile.html` | Mobile-optimized browser |
| `settings.html` | Demo mode, CT sync trigger |
| `login.html` | Authentication with MFA |

## Tech Stack

- **Frontend**: Vanilla HTML/CSS/JS (no framework)
- **Backend**: Supabase (PostgreSQL + Auth)
- **Hosting**: Firebase Hosting
- **Data Source**: [wine-data-layer](https://github.com/VintageGeek/wine-data-layer)

## Setup

1. Clone:
```bash
git clone https://github.com/VintageGeek/wine-dashboard.git
cd wine-dashboard
```

2. Configure Supabase keys in each HTML file (already configured for prod)

3. Deploy:
```bash
npx firebase deploy --only hosting:dev   # Dev
npx firebase deploy --only hosting:prod  # Production
```

## Authentication

All pages require Supabase Auth with TOTP MFA:
1. Email/password login
2. TOTP code from authenticator app
3. Session persists in browser

## Data Flow

```
Supabase (v_wines_full view)
         ↓
   Dashboard Pages
         ↓
   pull_list_items (write back)
   app_settings (demo mode)
```

## Related

- **Data Layer**: [wine-data-layer](https://github.com/VintageGeek/wine-data-layer)
