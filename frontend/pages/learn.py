"""Learn page for the Streamlit frontend."""

from __future__ import annotations

import streamlit as st

from frontend.client import ApiClient, FrontendApiError
from frontend.ui import render_error, render_loading_state, render_section_heading, render_status


def render() -> None:
    """Render the learn page."""
    st.title("Learn")
    st.caption("Look up educational content from the backend repository-backed content layer.")

    object_name = st.text_input("Object or topic", value="mars")
    if not st.button("Load learning content"):
        return

    client = ApiClient()
    try:
        content = None

        def load_data() -> None:
            nonlocal content
            content = client.get_learn(object_name)

        render_loading_state(load_data)
        render_status("Educational content loaded successfully.", kind="success")
        render_section_heading("Educational content")
        st.markdown(f"## {content.get('title', 'Untitled')}")
        st.caption(f"Category: {content.get('category_name', 'General')} | Slug: {content.get('slug', 'N/A')}")
        if content.get("excerpt"):
            st.write(content.get("excerpt"))
        if content.get("body"):
            st.write(content.get("body"))
        if content.get("source_url"):
            st.link_button("Open source", content.get("source_url"))
    except FrontendApiError as exc:
        render_error(str(exc))


if __name__ == "__main__":
    render()
