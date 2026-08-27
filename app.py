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
    "match situations, and player performance."
)

# ==========================================
# API SETUP
# ==========================================

try:
    api_key = st.secrets["CRICLIVE_API_KEY"]
except Exception:
    st.error("❌ CricLive API key is missing.")
    st.stop()

headers = {
    "Authorization": f"Bearer {api_key}"
}

# ==========================================
# LIVE MATCHES
# ==========================================

st.divider()
st.header("🔴 Live Matches")

try:

    response = requests.get(
        "https://cricketliveapi.com/api/v1/cricket/live",
        headers=headers,
        timeout=10
    )

    if response.status_code != 200:
        st.error(
            f"❌ Live API Error: {response.status_code}"
        )
        st.stop()

    live_data = response.json()

    matches = live_data.get("data", [])

    if not matches:
        st.warning("No matches available right now.")
        st.stop()

    st.success(
        f"🟢 Live data updated — {len(matches)} matches found"
    )

    # ==========================================
    # MATCH CARDS
    # ==========================================

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

        # ------------------------------------------
        # MATCH CARD
        # ------------------------------------------

        with st.container(border=True):

            st.subheader(f"🏏 {title}")

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

            # --------------------------------------
            # VIEW MATCH BUTTON
            # --------------------------------------

            if st.button(
                "📊 View Match",
                key=f"view_{match_id}"
            ):

                st.session_state[
                    "selected_match_id"
                ] = match_id

                st.session_state[
                    "selected_match_title"
                ] = title


except requests.RequestException as e:

    st.error(
        f"❌ Could not connect to CricLive: {e}"
    )

except Exception as e:

    st.error(
        f"❌ Something went wrong: {e}"
    )


# ==========================================
# MATCH CENTER
# ==========================================

if "selected_match_id" in st.session_state:

    selected_match_id = (
        st.session_state["selected_match_id"]
    )

    selected_title = (
        st.session_state.get(
            "selected_match_title",
            "Selected Match"
        )
    )

    st.divider()

    st.header("🏏 Match Center")

    st.subheader(selected_title)

    # ------------------------------------------
    # FETCH SCORECARD
    # ------------------------------------------

    try:

        scorecard_response = requests.get(
            f"https://cricketliveapi.com/api/v1/match/"
            f"{selected_match_id}/scorecard",
            headers=headers,
            timeout=10
        )

        if scorecard_response.status_code != 200:

            st.error(
                "❌ Could not load the match scorecard."
            )

            st.caption(
                f"API status: "
                f"{scorecard_response.status_code}"
            )

        else:

            scorecard_data = (
                scorecard_response.json()
            )

            st.success(
                "🟢 Match data loaded"
            )

            # --------------------------------------
            # BASIC MATCH INFORMATION
            # --------------------------------------

            st.subheader("📋 Match Information")

            info_col1, info_col2 = st.columns(2)

            with info_col1:

                st.write(
                    f"**Match ID:** "
                    f"{selected_match_id}"
                )

                st.write(
                    f"**Series:** "
                    f"{scorecard_data.get('series_name', '-')}"
                )

            with info_col2:

                st.write(
                    f"**Venue:** "
                    f"{scorecard_data.get('venue', '-')}"
                )

                st.write(
                    f"**Status:** "
                    f"{scorecard_data.get('status_detail', '-')}"
                )

            st.divider()

            # --------------------------------------
            # SCORECARD DATA
            # --------------------------------------

            st.subheader("🏏 Live Scorecard")

            # Different API responses may place
            # scorecard information under different keys.
            # We check the common structures safely.

            score_data = scorecard_data.get(
                "score",
                {}
            )

            current_batsmen = (
                scorecard_data.get(
                    "current_batsmen",
                    []
                )
            )

            current_bowler = (
                scorecard_data.get(
                    "current_bowler",
                    {}
                )
            )

            last_ball = (
                scorecard_data.get(
                    "last_ball",
                    None
                )
            )

            # --------------------------------------
            # SCORE
            # --------------------------------------

            if isinstance(score_data, dict):

                score_col1, score_col2, score_col3 = (
                    st.columns(3)
                )

                with score_col1:

                    st.metric(
                        "Score",
                        score_data.get(
                            "runs",
                            "-"
                        )
                    )

                with score_col2:

                    st.metric(
                        "Overs",
                        score_data.get(
                            "overs",
                            "-"
                        )
                    )

                with score_col3:

                    st.metric(
                        "Current Run Rate",
                        scorecard_data.get(
                            "crr",
                            "-"
                        )
                    )

            elif score_data:

                st.info(
                    f"Score: {score_data}"
                )

            # --------------------------------------
            # CURRENT BATSMEN
            # --------------------------------------

            st.subheader("👤 Current Batters")

            if current_batsmen:

                for batter in current_batsmen:

                    if isinstance(
                        batter,
                        dict
                    ):

                        name = batter.get(
                            "name",
                            "Unknown"
                        )

                        runs = batter.get(
                            "runs",
                            "-"
                        )

                        balls = batter.get(
                            "balls",
                            "-"
                        )

                        strike_rate = batter.get(
                            "strike_rate",
                            batter.get(
                                "sr",
                                "-"
                            )
                        )

                        st.write(
                            f"**{name}** — "
                            f"{runs} ({balls}) "
                            f"• SR: {strike_rate}"
                        )

                    else:

                        st.write(
                            f"**{batter}**"
                        )

            else:

                st.info(
                    "Current batter information "
                    "is not available for this match."
                )

            # --------------------------------------
            # CURRENT BOWLER
            # --------------------------------------

            st.subheader("🎯 Current Bowler")

            if current_bowler:

                if isinstance(
                    current_bowler,
                    dict
                ):

                    bowler_name = current_bowler.get(
                        "name",
                        "Unknown"
                    )

                    st.write(
                        f"**{bowler_name}**"
                    )

                    b1, b2, b3 = st.columns(3)

                    with b1:

                        st.metric(
                            "Overs",
                            current_bowler.get(
                                "overs",
                                "-"
                            )
                        )

                    with b2:

                        st.metric(
                            "Runs",
                            current_bowler.get(
                                "runs",
                                "-"
                            )
                        )

                    with b3:

                        st.metric(
                            "Wickets",
                            current_bowler.get(
                                "wickets",
                                "-"
                            )
                        )

                else:

                    st.write(
                        current_bowler
                    )

            else:

                st.info(
                    "Current bowler information "
                    "is not available."
                )

            # --------------------------------------
            # LAST BALL
            # --------------------------------------

            st.subheader("🔥 Last Ball")

            if last_ball:

                if isinstance(
                    last_ball,
                    dict
                ):

                    commentary = (
                        last_ball.get(
                            "commentary",
                            "No commentary"
                        )
                    )

                    st.info(
                        commentary
                    )

                    ball_col1, ball_col2, ball_col3 = (
                        st.columns(3)
                    )

                    with ball_col1:

                        st.write(
                            f"**Ball:** "
                            f"{last_ball.get('ball', '-')}"
                        )

                    with ball_col2:

                        st.write(
                            f"**Runs:** "
                            f"{last_ball.get('runs', '-')}"
                        )

                    with ball_col3:

                        st.write(
                            f"**Type:** "
                            f"{last_ball.get('type', '-')}"
                        )

                else:

                    st.info(
                        str(last_ball)
                    )

            else:

                st.info(
                    "Last-ball information "
                    "is not available."
                )

            # --------------------------------------
            # REQUIRED RUN RATE
            # --------------------------------------

            required_rate = (
                scorecard_data.get(
                    "rrr",
                    scorecard_data.get(
                        "required_run_rate",
                        None
                    )
                )
            )

            if required_rate is not None:

                st.metric(
                    "Required Run Rate",
                    required_rate
                )

    except requests.RequestException as e:

        st.error(
            f"❌ Match data connection failed: {e}"
        )

    except Exception as e:

        st.error(
            f"❌ Could not process match data: {e}"
        )
