import streamlit as st
import requests


# ==========================================
# PAGE CONFIG
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
# API FUNCTION
# Cached for 60 seconds to reduce API calls
# ==========================================

@st.cache_data(ttl=60)
def get_live_matches(api_key):

    url = "https://cricketliveapi.com/api/v1/cricket/live"

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        timeout=10
    )

    return response.status_code, response.json()


# ==========================================
# LIVE MATCHES
# ==========================================

st.header("🔴 Live Matches")


try:

    api_key = st.secrets["CRICLIVE_API_KEY"]

    status_code, data = get_live_matches(api_key)

    # --------------------------------------
    # API ERROR
    # --------------------------------------

    if status_code == 429:

        st.warning(
            "⚠️ CricLive API limit has been reached. "
            "The app is waiting for the API limit to reset."
        )

        # If we already selected a match earlier,
        # still show it from session state.
        if "selected_match" not in st.session_state:
            st.info(
                "The CricketPulse interface is working correctly. "
                "Live data will return when the API becomes available again."
            )

    elif status_code != 200:

        st.error(f"❌ API Error: {status_code}")

    else:

        matches = data.get("data", [])

        # --------------------------------------
        # NO LIVE MATCHES
        # --------------------------------------

        if not matches:

            st.warning("No live matches available right now.")

        else:

            st.success(
                f"🟢 Live data updated — {len(matches)} matches found"
            )

            # ----------------------------------
            # DISPLAY MATCHES
            # ----------------------------------

            for match in matches:

                match_id = match.get("match_id")

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

                first_score = first_team.get(
                    "score",
                    "Score unavailable"
                )

                second_score = second_team.get(
                    "score",
                    "Score unavailable"
                )

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

                # ----------------------------------
                # MATCH CARD
                # ----------------------------------

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

                    # ----------------------------------
                    # CLICKABLE MATCH
                    # ----------------------------------

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


except KeyError:

    st.error(
        "❌ CRICLIVE_API_KEY is missing from Streamlit Secrets."
    )

except requests.exceptions.RequestException as e:

    st.error(
        f"❌ Could not connect to CricLive API: {e}"
    )

except Exception as e:

    st.error(
        f"❌ Something went wrong: {e}"
    )


# ==========================================
# SELECTED MATCH
# ==========================================

if "selected_match" in st.session_state:

    selected = st.session_state["selected_match"]

    st.divider()

    st.header("🏏 Match Center")

    # --------------------------------------
    # MATCH INFORMATION
    # --------------------------------------

    st.subheader(
        selected.get(
            "title",
            "Selected Match"
        )
    )

    venue = selected.get(
        "venue",
        "Venue unavailable"
    )

    status = selected.get(
        "status_detail",
        selected.get(
            "short_status",
            "Status unavailable"
        )
    )

    st.write(
        f"📍 **Venue:** {venue}"
    )

    st.write(
        f"🟢 **Status:** {status}"
    )

    st.divider()

    # --------------------------------------
    # TEAMS
    # --------------------------------------

    first_team = selected.get(
        "first_team",
        {}
    )

    second_team = selected.get(
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

        st.markdown(
            f"### {first_name}"
        )

        st.markdown(
            f"# {first_score}"
        )

    with col2:

        st.markdown(
            f"### {second_name}"
        )

        st.markdown(
            f"# {second_score}"
        )

    st.divider()

    # --------------------------------------
    # MATCH ID
    # --------------------------------------

    match_id = selected.get(
        "match_id"
    )

    st.caption(
        f"Match ID: {match_id}"
    )

    # --------------------------------------
    # AVAILABLE DATA
    # --------------------------------------

    st.subheader("📊 Match Information")

    format_type = selected.get(
        "format",
        "Not available"
    )

    match_type = selected.get(
        "match_type",
        "Not available"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Format:** {format_type}"
        )

    with col2:

        st.write(
            f"**Type:** {match_type}"
        )

    # --------------------------------------
    # FUTURE SCORECARD AREA
    # --------------------------------------

    st.divider()

    st.subheader(
        "🏏 Detailed Scorecard"
    )

    st.info(
        "The detailed scorecard will show "
        "batters, runs, balls, fours, sixes, "
        "strike rate, bowlers, wickets and economy."
    )
