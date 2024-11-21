import streamlit as st

def show_dashboards():
    st.title("Search Console Dashboards Integration")

    col1, col2, col3, col4, col5 = st.columns(5)

    if "dashboard" not in st.session_state:
        st.session_state.dashboard = "Google Search Console"

    with col1:
        if st.button("Google Search Console"):
            st.session_state.dashboard = "Google Search Console"
    with col2:
        if st.button("Twitter Search Console"):
            st.session_state.dashboard = "Twitter Search Console"
    with col3:
        if st.button("Bing Search Console"):
            st.session_state.dashboard = "Bing Search Console"
    with col4:
        if st.button("Yahoo Search Console"):
            st.session_state.dashboard = "Yahoo Search Console"
    with col5:
        if st.button("Last Dashboard"):
            st.session_state.dashboard = "Last Dashboard"

    dashboard_links = {
        "Google Search Console": "https://lookerstudio.google.com/embed/reporting/0B_U5RNpwhcE6QXg4SXFBVGUwMjg/page/6zXD",
        "Twitter Search Console": "https://lookerstudio.google.com/embed/reporting/52cfd9c8-a6e8-4452-a718-d97726d3117c/page/1xZU",
        "Bing Search Console": "https://lookerstudio.google.com/embed/reporting/0B_U5RNpwhcE6QXg4SXFBVGUwMjg/page/6zXD",
        "Yahoo Search Console": "https://lookerstudio.google.com/embed/reporting/52cfd9c8-a6e8-4452-a718-d97726d3117c/page/1xZU",
        "Last Dashboard": "https://lookerstudio.google.com/embed/reporting/0B_U5RNpwhcE6QXg4SXFBVGUwMjg/page/6zXD",
    }

    dashboard_title = st.session_state.dashboard
    st.markdown(f"### {dashboard_title}")
    st.components.v1.iframe(dashboard_links[dashboard_title], width=1300, height=1000)
