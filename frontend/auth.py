import streamlit as st


class Auth:

    @staticmethod
    def login(token, username):

        st.session_state.logged_in = True
        st.session_state.token = token
        st.session_state.username = username

    @staticmethod
    def logout():

        st.session_state.logged_in = False
        st.session_state.token = None
        st.session_state.username = ""

    @staticmethod
    def is_authenticated():

        return st.session_state.get(
            "logged_in",
            False
        )

    @staticmethod
    def get_token():

        return st.session_state.get(
            "token",
            None
        )

    @staticmethod
    def get_username():

        return st.session_state.get(
            "username",
            ""
        )