import streamlit as st
import requests

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CricketPulse",
    page_icon="🏏",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================

st.title("🏏 CricketPulse")
st.subheader("Real-Time Cricket Intelligence")

st.write(
    "A real-time cricket platform that analyzes live matches, "
    "momentum, and match situations."
)

st.divider()

# ==========================================
# API KEY
# ==========================================

try:
    api_key = st.secrets["CRICLIVE_API_KEY"]

except Exception:
    st.error(
        "❌ CRICLIVE_API_KEY is missing from Streamlit Secrets."
    )
    st.stop()

headers = {
    "Authorization": f"Bearer {api_key}"
}

# ==========================================
# LIVE MATCHES
# ==========================================

st.header("🔴 Live Matches")

try:

    response = requests.get(
        "https://cricketliveapi.com/api/v1/cricket/matches/live",
        headers=headers,
        timeout=10
    )

    # --------------------------------------
    # CHECK API STATUS
    # --------------------------------------

    if response.status_code != 200:

        st.error(
            f"❌ API Error: {response.status_code}"
        )

        st.stop()

    # --------------------------------------
    # READ RESPONSE
    # --------------------------------------

    data = response.json()

    # TEMPORARY DEBUG INFORMATION
    with st.expander("🔍 API Debug Information"):

        st.write("API Status:", response.status_code)

        st.write(
            "Response keys:",
            list(data.keys()) if isinstance(data, dict) else "Not a dictionary"
        )

        st.json(data)

    # --------------------------------------
    # GET MATCHES
    # --------------------------------------

    matches = data.get("data", [])

    if not matches:

        st.warning(
            "No matches available right now."
        )

        st.info(
            "The CricLive API is connected, "
            "but it currently returned no matches."
        )

        st.stop()

    # --------------------------------------
    # SUCCESS
    # --------------------------------------

    st.success(
        f"🟢 Live data updated — "
        f"{len(matches)} matches found"
    )

    # ======================================
    # MATCH CARDS
    # ======================================

    for match in matches:

        # ----------------------------------
        # MATCH ID
        # ----------------------------------

        match_id = match.get(
            "match_id"
        )

        # ----------------------------------
        # TEAMS
        # ----------------------------------

        first_team = match.get(
            "first_team",
            {}
        )

        second_team = match.get(
            "second_team",
            {}
        )

        first_name = first_team.get(
            "full_name",
            first_team.get(
                "name",
                "Team 1"
            )
        )

        second_name = second_team.get(
            "full_name",
            second_team.get(
                "name",
                "Team 2"
            )
        )

        # ----------------------------------
        # SCORES
        # ----------------------------------

        first_score = first_team.get(
            "score",
            "Score unavailable"
        )

        second_score = second_team.get(
            "score",
            "Score unavailable"
        )

        # ----------------------------------
        # MATCH INFORMATION
        # ----------------------------------

        title = match.get(
            "title",
            f"{first_name} vs {second_name}"
        )

        venue = match.get(
            "venue",
            "Venue unavailable"
        )

        status = match.get(
            "status_detail",
            match.get(
                "short_status",
                "Status unavailable"
            )
        )

        # ==================================
        # MATCH CARD
        # ==================================

        with st.container(border=True):

            st.subheader(
                f"🏏 {title}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    f"### {first_name}"
                )

                st.markdown(
                    f"## {first_score}"
                )

            with col2:

                st.markdown(
                    f"### {second_name}"
                )

                st.markdown(
                    f"## {second_score}"
                )

            st.write(
                f"📍 **Venue:** {venue}"
            )

            st.write(
                f"🟢 **Status:** {status}"
            )

            # ==================================
            # VIEW MATCH
            # ==================================

            if st.button(
                "📊 View Match",
                key=f"view_{match_id}"
            ):

                st.session_state[
                    "selected_match"
                ] = match

                st.session_state[
                    "selected_match_id"
                ] = match_id


# ==========================================
# API CONNECTION ERROR
# ==========================================

except requests.RequestException as e:

    st.error(
        f"❌ Could not connect to CricLive: {e}"
    )

except Exception as e:

    st.error(
        f"❌ Something went wrong: {e}"
    )


# ==========================================
# SELECTED MATCH
# ==========================================

if "selected_match" in st.session_state:

    selected = st.session_state[
        "selected_match"
    ]

    selected_match_id = st.session_state[
        "selected_match_id"
    ]

    st.divider()

    st.header("🏏 Selected Match")

    st.subheader(
        selected.get(
            "title",
            "Selected Match"
        )
    )

    st.write(
        f"**Match ID:** {selected_match_id}"
    )

    st.success(
        "✅ Match selected successfully!"
    )

    st.info(
        "Detailed match information will be "
        "connected after we verify the correct "
        "CricLive endpoint."
    )
