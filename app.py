import streamlit as st
import requests

st.set_page_config(
    page_title="CricketPulse",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 CricketPulse")
st.subheader("Real-Time Cricket Intelligence")

st.write(
    "A real-time cricket platform that analyzes live matches, "
    "momentum, and match situations."
)

st.divider()

st.header("🔴 Live Matches")

try:
    api_key = st.secrets["CRICLIVE_API_KEY"]

    response = requests.get(
        "https://cricketliveapi.com/api/v1/cricket/live",
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        timeout=10
    )

    if response.status_code == 200:

        live_data = response.json()

        if live_data.get("success"):

            matches = live_data.get("data", [])

            st.success(
                f"🟢 Live data connected — {len(matches)} matches found"
            )

            for match in matches:

                first_team = match.get("first_team", {})
                second_team = match.get("second_team", {})

                first_name = first_team.get(
                    "full_name",
                    first_team.get("name", "Team 1")
                )

                second_name = second_team.get(
                    "full_name",
                    second_team.get("name", "Team 2")
                )

                first_score = first_team.get(
                    "score", "Score unavailable"
                )

                second_score = second_team.get(
                    "score", "Score unavailable"
                )

                venue = match.get(
                    "venue", "Venue unavailable"
                )

                status = match.get(
                    "status_detail",
                    match.get("short_status", "Status unavailable")
                )

                title = match.get(
                    "title",
                    f"{first_name} vs {second_name}"
                )

                with st.container(border=True):

                    st.subheader(f"🏏 {title}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"### {first_name}")
                        st.markdown(f"## {first_score}")

                    with col2:
                        st.markdown(f"### {second_name}")
                        st.markdown(f"## {second_score}")

                    st.write(f"📍 **Venue:** {venue}")
                    st.write(f"🟢 **Status:** {status}")

        else:
            st.warning("No live match data available.")

    else:
        st.error(f"❌ API Error: {response.status_code}")
        st.write(response.text)

except Exception as e:
    st.error(f"❌ Connection failed: {e}")
