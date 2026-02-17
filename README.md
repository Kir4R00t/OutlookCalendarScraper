# Outlook calendar scraper
Synchronize a Microsoft Outlook / Teams university calendar with Google Calendar using a self-hosted, Dockerized service.

This project was created to solve a real-world limitation: university Outlook calendars (published via Microsoft 365 / Teams) often cannot be directly subscribed to in Google Calendar due to permission or authentication restrictions.

## Architecture
```
  Outlook / Teams Calendar
            │
            ▼
     Selenium Scraper
            │
            ▼
    Event Parser (Python)
            │
            ▼
      ICS Generator
            │
            ▼
      Web Endpoint
            │
            ▼
 Google Calendar (Subscribe via URL)

```

## Tech stack
- Python + Selenium
- Docker
- Flask
- VPS (running debian)
- Google Calendar (ICS subscription)

## Now working on ...
- ICS Generator
- Containerization
- Setting up the Web Endpoint
- Finishing up the docs (deployment guide, setting up envs etc.)
