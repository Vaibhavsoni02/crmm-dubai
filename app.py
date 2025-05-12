import streamlit as st
import pandas as pd
import requests

st.title("Konfhub Attendee Extractor")

fetch_btn = st.button("Fetch Attendees")

if fetch_btn:
    st.info("Fetching data... Please wait.")
    all_attendees = []

    event_id = "3e6ef626-59e8-41ec-a865-9ad9576c5b06"
    bearer_token = "Bearer eyJraWQiOiJYRHQ5cGhGQ0piRzVZWmY5RHV4RTVtamcxMElFMHlYUkRxNThENW9MVFIwPSIsImFsZyI6IlJTMjU2In0.eyJjdXN0b206c2lnblVwRXZlbnRJZCI6IjNlNmVmNjI2LTU5ZTgtNDFlYy1hODY1LTlhZDk1NzZjNWIwNiIsInN1YiI6IjJkZGVmMzBiLWU3OWItNDIwZS05OWY4LThlZWUzNTk0NmEwZSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtc291dGgtMS5hbWF6b25hd3MuY29tXC9hcC1zb3V0aC0xX2FjSm8zWEdiTCIsImNvZ25pdG86dXNlcm5hbWUiOiIyZGRlZjMwYi1lNzliLTQyMGUtOTlmOC04ZWVlMzU5NDZhMGUiLCJjdXN0b206Y2xpZW50VHlwZSI6IjEiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiI5MDkwMDcyNS02ZTJiLTQ1NmUtYmJiYS1kZjg5ODdkMjUwMDgiLCJjdXN0b206ZGVzaWduYXRpb24iOiJTci4gUHJvZHVjdCBNYW5hZ2VyIiwiY3VzdG9tOnVzZXJJZCI6IjkwOTAwNzI1LTZlMmItNDU2ZS1iYmJhLWRmODk4N2QyNTAwOCIsIm9yaWdpbl9qdGkiOiJjZDZiMzIyZC1iZDYwLTQ2NWMtOGY5ZS00OTM1ZmU4MDQ3MzYiLCJjdXN0b206dXNlclR5cGUiOiIzIiwiYXVkIjoiNWpmMTByazJjMG11ZnRvdHAxaXUydWN1cDAiLCJldmVudF9pZCI6ImViNmZmMzQ1LTVmZDMtNDIwOS1hMDQzLTMyNjVhNGZmNDYwMSIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNzQ3MDc0NTk3LCJuYW1lIjoiVmFpYmhhdiBTb25pIiwiY3VzdG9tOmRpYWxDb2RlIjoiOTEiLCJleHAiOjE3NDcwNzgxOTcsImlhdCI6MTc0NzA3NDU5NywiY3VzdG9tOnByb2ZpbGVQaWN0dXJlIjoiaHR0cHM6XC9cL21lZGlhLmtvbmZodWIuY29tXC9kZWZhdWx0LXByb2ZpbGUucG5nIiwianRpIjoiNGY2MGMxMjYtZDFmYi00MTQ0LWJiOGYtNmEyMjc2MDMzMTQ3IiwiZW1haWwiOiJ2YWliaGF2QG9wdGlibGFjay5jb20ifQ.lF5wkq_fCHPgZ6Kkp02fhJnBOENQSOx3Mw_acCzSHYkwiszDG4cBscjrPkSSbMED7BjaTNGVgnM0yHajZGGXlkHgQQu5NdHlFiNzI9oVvS10DVsW4F00fAcyanIfvuu2Gs1m7SEUuqGryT96WVnmbj6ir56A998SEclOjx7DqL0vxN89QP3oQ7mRNmOtLULdlQI_QXQIxzWTM5wlLYcmpRqqOAIORzwsPcb7ezC0l-vGsf_j6UQg4Bi2rH8oDb9pHiQlvXA21xFLCE2dJr418rzguKQW5sIPfaY_8Y7xfeqOKVP132bjI6NJSwen8-ltQfcELQQSRznZLDLGgkMvQQ"

    headers = {
        "accept": "application/json",
        "authorization": bearer_token
    }

    for offset in range(10000, 20000, 50):
        url = f"https://api.konfhub.com/attendee-app/event/{event_id}/att-app/attendees"
        params = {
            "limit": 50,
            "offset": offset,
            "include_count_metrics": "true"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            attendees = response.json().get("attendees", [])
            all_attendees.extend(attendees)
        else:
            st.error(f"Failed at offset {offset}: {response.status_code}")
            break

    if all_attendees:
        df = pd.DataFrame(all_attendees)
        st.success(f"Fetched {len(df)} attendees.")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download as CSV", csv, "attendees.csv", "text/csv")
    else:
        st.warning("No attendees found.")
