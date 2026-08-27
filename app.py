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

    if response.status_code != 200:
        st.error(f"❌ API Error: {response.status_code}")
        st.stop()

    live_data = response.json()
    matches = live_data.get("data", [])

    if not matches:
        st.warning("No matches available right now.")
        st.stop()

    st.success(f"🟢 {len(matches)} matches found")

    # Create match names for selection
    match_options = {}

    for match in matches:

        match_id = match.get("match_id")

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

        title = match.get(
            "match_desc",
            f"{first_name} vs {second_name}"
        )

        display_name = f"{first_name} vs {second_name} — {title}"

        match_options[display_name] = match_id

    # User selects a match
    selected_match = st.selectbox(
        "🏏 Select a match",
        list(match_options.keys())
    )

    selected_match_id = match_options[selected_match]

    # Find selected match
    selected_data = next(
        (
            match for match in matches
            if match.get("match_id") == selected_match_id
        ),
        None
    )

    if selected_data:

        st.divider()
        st.header("📊 Match Overview")

        first_team = selected_data.get("first_team", {})
        second_team = selected_data.get("second_team", {})

        first_name = first_team.get(
            "full_name",
            first_team.get("name", "Team 1")
        )

        second_name = second_team.get(
            "full_name",
            second_team.get("name", "Team 2")
        )

        first_score = first_team.get(
            "score",
            "Score unavailable"
        )

        second_score = second_team.get(
            "score",
            "Score unavailable"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(first_name)
            st.title(first_score)

        with col2:
            st.subheader(second_name)
            st.title(second_score)

        st.write(
            f"📍 **Venue:** "
            f"{selected_data.get('venue', 'Unknown')}"
        )

        st.write(
            f"🟢 **Status:** "
            f"{selected_data.get('status_detail', 'Unknown')}"
        )

        st.divider()

        st.header("🧠 Match Details")

        st.write(f"**Match ID:** {selected_match_id}")

        st.json(selected_data)

except Exception as e:

    st.error(f"❌ Something went wrong: {e}")
