if "selected_match" in st.session_state:

    selected = st.session_state["selected_match"]

    match_id = selected.get("match_id")

    st.divider()

    st.header("🏏 Match Center")

    st.subheader(
        selected.get(
            "title",
            "Selected Match"
        )
    )

    # Test the correct CricLive scorecard endpoint
    scorecard_url = (
        f"https://cricketliveapi.com/api/v1/"
        f"cricket/scorecard/{match_id}"
    )

    try:

        scorecard_response = requests.get(
            scorecard_url,
            headers={
                "Authorization": f"Bearer {api_key}"
            },
            timeout=10
        )

        if scorecard_response.status_code == 200:

            scorecard_data = scorecard_response.json()

            st.success(
                "✅ Scorecard API connected successfully!"
            )

            st.write(
                "Match ID:",
                match_id
            )

            st.write(
                "Data received successfully."
            )

            st.write(
                "Available data sections:",
                list(scorecard_data.keys())
            )

        else:

            st.error(
                f"❌ Scorecard API Error: "
                f"{scorecard_response.status_code}"
            )

    except Exception as e:

        st.error(
            f"❌ Could not connect to scorecard API: {e}"
        )
