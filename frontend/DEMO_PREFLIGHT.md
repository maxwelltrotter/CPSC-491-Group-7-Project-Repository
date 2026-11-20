# Sprint 5 mock frontend demo preflight

From the repository root, on the machine that will run the live demonstration:

```powershell
python -m pip install -r requirements.txt
python -m frontend --check-demo
python -m pytest frontend/tests -q
python -m frontend
```

The preflight is read-only and does not open a window. It checks that Tkinter
can be imported and that the bundled mock fixture contains the three alert IDs
used in Terry's script (`ALT-001`, `ALT-002`, `ALT-003`), with a consistent
Dashboard count. It exits nonzero if a check fails. It is not a substitute for
launching the GUI and executing the live dry-run on the presentation laptop.

Expected GUI starting state: Dashboard shows three active mock alerts. Open
Alerts to review one synthetic alert and export its in-session history. The
review does not change the source alert or Dashboard counts. Saved reviews are
lost when the app closes unless explicitly exported to JSON.

This command checks local mock data only. It does not test live traffic,
backend integration, an AWS deployment, or perimeter prevention.
