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
# DEMO DATA
# Used only when CricLive API is unavailable
# ==========================================

demo_matches = [
    {
        "match_id": 129585,
        "title": "Pakistan tour of England 2026 - 2nd Test",
        "first_team": {
            "name": "ENG",
            "full_name": "England",
            "score": "248/9 (55.6 ov)"
        },
        "second_team": {
            "name": "PAK",
            "full_name": "Pakistan",
            "score": ""
        },
        "venue": "Lord's, London",
        "status_detail": "Day 1: Stumps"
    },

    {
        "match_id": 163017,
        "title": "India tour of Sri Lanka 2026 - 2nd Test",
        "first_team": {
            "name": "IND",
            "full_name": "India",
            "score": "503/9 (137.6 ov)"
        },
        "second_team": {
            "name": "SL",
            "full_name": "Sri Lanka",
            "score": "290/10 (89.4 ov) & 429/9 (153.6 ov)"
        },
        "venue": "Sinhalese Sports Club, Colombo",
        "status_detail": "Match drawn"
    },

    {
        "match_id": 155410,
        "title": "European T20 Premier League 2026 - 3rd Match",
        "first_team": {
            "name": "GC",
            "full_name": "Glasgow Cosmics",
            "score": "115/10 (19.6 ov)"
        },
        "second_team": {
            "name": "ECR",
            "full_name": "Edinburgh Castle Rockers",
            "score": "116/3 (11.3 ov)"
        },
        "venue": "Sportpark Duivesteijn, Voorburg",
        "status_detail": "Edinburgh Castle Rockers won by 7 wkts"
    },

    {
        "match_id": 155409,
        "title": "European T20 Premier League 2026 - 2nd Match",
        "first_team": {
            "name": "BW",
            "full_name": "Belfast Wolves",
            "score": "184/7 (19.6 ov)"
        },
        "second_team": {
            "name": "DG",
            "full_name": "Dublin Guardians",
            "score": "132/9 (19.6 ov)"
        },
        "venue": "Sportpark Duivesteijn, Voorburg",
        "status_detail": "Belfast Wolves won by 52 runs"
    },

    {
        "match_id": 154486,
        "title": "Caribbean Premier League 2026 - 18th Match",
        "first_team": {
            "name": "SKNP",
            "full_name": "St Kitts and Nevis Patriots",
            "score": ""
        },
        "second_team": {
            "name": "JK",
            "full_name": "Jamaica Kingsmen",
            "score": ""
        },
        "venue": "Warner Park, Basseterre, St Kitts",
        "status_detail": "Match starts at Aug 28, 23:00 GMT"
    },

    {
        "match_id": 154485,
        "title": "Caribbean Premier League 2026 - 17th Match",
        "first_team": {
            "name": "SLK",
            "full_name": "Saint Lucia Kings",
            "score": "211/4 (19.6 ov)"
        },
        "second_team": {
            "name": "TKR",
            "full_name": "Trinbago Knight Riders",
            "score": "175/6 (19.6 ov)"
        },
        "venue": "Queen's Park Oval, Port of Spain, Trinidad",
        "status_detail": "Saint Lucia Kings won by 36 runs"
    }
]


# ==========================================
# TRY REAL API
# ==========================================

@st.cache_data(ttl=60)
def get_live_matches(api_key):

    response = requests.get(
        "https://cricketliveapi.com/api/v1/cricket/live",
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        timeout=10
    )

    if response.status_code != 200:
        return None

    data = response.json()

    return data.get("data", [])


# ==========================================
# GET MATCH DATA
# ==========================================

try:

    api_key = st.secrets["CRICLIVE_API_KEY"]

    real_matches = get_live_matches(api_key)

except Exception:

    real_matches = None


# ==========================================
# DECIDE WHICH DATA TO SHOW
# ==========================================

if real_matches:

    matches = real_matches

    st.success(
        f"🟢 Live data connected — {len(matches)} matches found"
    )

else:

    matches = demo_matches

    st.info(
        "🔵 Showing the latest available match snapshot. "
        "Live API data will return automatically when CricLive is available."
    )


# ==========================================
# LIVE MATCHES
# ==========================================

st.header("🔴 Live Matches")


# ==========================================
# MATCH CARDS
# ==========================================

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


    # ======================================
    # CARD
    # ======================================

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
        # CLICKABLE MATCH
        # ==================================

        if st.button(
            "📊 View Match",
            key=f"match_{match_id}"
        ):

            st.session_state["selected_match"] = match

            st.session_state["selected_match_id"] = match_id


# ==========================================
# MATCH CENTER
# ==========================================

if "selected_match" in st.session_state:

    selected = st.session_state["selected_match"]

    st.divider()

    st.header("🏏 Match Center")

    st.subheader(
        selected.get(
            "title",
            "Selected Match"
        )
    )

    st.write(
        f"📍 **Venue:** {selected.get('venue', 'Unknown')}"
    )

    st.write(
        f"🟢 **Status:** {selected.get('status_detail', 'Unknown')}"
    )

    st.divider()

    first_team = selected.get(
        "first_team",
        {}
    )

    second_team = selected.get(
        "second_team",
        {}
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"### {first_team.get('full_name', first_team.get('name', 'Team 1'))}"
        )

        st.markdown(
            f"# {first_team.get('score', 'N/A')}"
        )

    with col2:

        st.markdown(
            f"### {second_team.get('full_name', second_team.get('name', 'Team 2'))}"
        )

        st.markdown(
            f"# {second_team.get('score', 'N/A')}"
        )

    st.divider()

    st.subheader("📊 Detailed Match Analysis")

    st.info(
        "Scorecard, batsmen, bowlers, commentary and "
        "momentum analysis will appear here."
    )
