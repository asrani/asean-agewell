# ASEAN AgeWell — Streamlit prototype

A Malaysia and Indonesia community mobility screening demonstration with synthetic records, a screening form, simulated AI measurements, manual calculations, a referral tracker, and JSON/CSV downloads.

## Run locally

Requires Python 3.10+.

```sh
cd agewell
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open http://localhost:8501. Run from this directory so the included theme configuration loads. Internet is required for installation, not normal local operation.

## Demonstration

1. Explore the 12 synthetic records on Overview: six each for Malaysia and Indonesia.
2. Open New screening, enter a unique fictional ID, and select a measurement source.
3. Choose Illustrative AI output for fixed sample values (4 metres / 6.4 seconds and 17.2 seconds for five chair rises), or Manual observations for your fictional inputs.
4. Confirm fictional-data use and save. Download the JSON summary.
5. In Referral tracker, filter records, update a status/contact date, and export CSV.

No video is processed and no machine-learning model is connected. All new screenings go to worker review; the application does not assign clinical risk or recommend treatment. Not assessed is stored as missing, never zero. Manual walking speed is distance/time.

Records are held only in Streamlit session state. They are not durable, shared between users, or restored after a new session/server restart. Export before leaving if needed. Reset restores the synthetic demonstration records. Do not enter real patient data. This is not a production health-record system and does not provide authentication, cloud sync, multilingual support, or mobile offline capture.

The optional administrative follow-up date defaults to seven days, not a clinical recommendation. No messages or referrals are sent.

## Further development

A real pilot needs ethics approval, consent, a validated assessment protocol, independent reference assessments, real pose estimation, evaluation across sites and participant groups, secure data handling, and agreed referral pathways.

Reference: https://www.who.int/publications/i/item/9789240103726

## Verification

Run `python test_app.py` for the Streamlit interaction checks (screening save, duplicate prevention, missing measurements, referral update, and page rendering). Tested with Streamlit 1.65.0 and pandas 2.3.3.

The pilot country selectors, dashboard, and exports cover Malaysia and Indonesia only. Records from other countries in an existing session are hidden, not relabelled; Reset demo records loads the updated two-country sample.
