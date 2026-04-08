# Hospital / Doctor Appointment Management Portal


A professional, two-panel admin-style portal for managing hospital doctor appointments. It uses Flask (Python) on the backend, Tailwind CSS for styling, and vanilla JavaScript with the Fetch API for a clean, responsive experience that feels like a modern government service portal.

## Features
- Two-panel layout: left side shows all appointments; right side shows editable details
- Responsive design (desktop and mobile) with calm medical palette (blue/teal/white)
- Tailwind CSS UI: cards, table, rounded corners, shadows, gradients
- Data loaded from JSON and persisted via POST to the same JSON file
- Simple, student-friendly codebase

## Technology Stack
- Frontend: HTML + Tailwind CSS (CDN) + vanilla JavaScript (Fetch API)
- Backend: Python (Flask)
- Data Source: JSON file (appointments.json)

## Project Structure
```
app.py                  # Flask app and API endpoints
appointments.json       # Appointment data (persisted)
templates/
  └─ index.html         # Portal UI and JS logic
```
## Getting Started
1. Install Python 3 (Windows/macOS/Linux).
2. Install Flask:
   ```
   pip install flask
   ```
3. Run the development server:
   ```
   python app.py
   ```
4. Open the portal:
   - http://127.0.0.1:5900/

## UI Overview
- Left Panel: Appointment table (ID, Patient, Doctor, Status)
- Right Panel: Detail form (Patient, Doctor, Date, Time, Status) with Save / Update
- Clicking a row loads details on the right without reloading the page
- Save persists to appointments.json via a POST request and refreshes the list

## API Endpoints
- `GET /`  
  Renders the main HTML portal.

- `GET /api/appointments`  
  Returns all appointments as JSON array.

- `GET /api/appointments/<id>`  
  Returns a single appointment by ID or `{"error": "Appointment not found"}` with 404 status.

- `POST /api/appointments`  
  Accepts JSON body:
  ```json
  {
    "patient": "Ali Khan",
    "doctor": "Dr. Ahmed",
    "date": "2026-02-10",
    "time": "10:30 AM",
    "status": "Pending",
    "id": "APT001" // optional; if missing or duplicate, backend generates a new APT### ID
  }
  ```
  Behavior:
  - Validates required fields (patient, doctor, date, time, status)
  - Generates a unique `APT###` ID if needed
  - Reads `appointments.json`, appends the new record, writes back
  - Updates in-memory list for subsequent GET requests
  - Returns:
  ```json
  {
    "message": "Saved successfully",
    "id": "APT005"
  }
  ```
  with HTTP status `201`.

### Quick cURL Test
```bash
curl -X POST http://127.0.0.1:5900/api/appointments \
  -H "Content-Type: application/json" \
  -d '{"patient":"Test User","doctor":"Dr. Verify","date":"2026-02-13","time":"11:00 AM","status":"Pending"}'
``

## Data Persistence Details
- File: `appointments.json` in the project root
- The app appends new records via `POST /api/appointments`
- ID policy: If `id` is missing or already exists, backend assigns the next sequential `APT###`
- Note: Current implementation appends only; it does not replace existing records

## Frontend Behavior
- Loads table with `GET /api/appointments`
- On row click, fetches and fills the form using `GET /api/appointments/<id>`
- On Save / Update:
  - Gathers form values (including optional hidden `id`)
  - Sends a `POST /api/appointments` with JSON body
  - Shows a toast on success/error (no disruptive alerts)
  - Refreshes the table to reflect persisted data

## Styling
- Tailwind CSS via CDN (no build step required)
- Calm medical palette and professional admin feel
- Easily customizable in `templates/index.html` (Tailwind classes and small config)

## Notes & Next Steps
- This is a student-friendly baseline. Consider adding:
  - Update/PUT endpoint to edit existing records by ID
  - Filters (by status/doctor/date) and search on the list panel
  - SQLite storage for more robust persistence and queries
  - Pagination for large datasets
  - Form validation and disabled state while saving

## License
Use freely for learning and internal projects.
