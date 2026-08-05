"""
Uni-Connect - Main Application Entry Point
A Streamlit-based platform for Lost & Found and Notes Exchange


Description: Campus utility platform using in-memory Python data structures
"""
import streamlit as st
from database.users_db import signup_user, login_user
from ui.dashboard_ui import render_dashboard
from ui.lost_found_ui import render_lost_found
from ui.notes_ui import render_notes_exchange
from utils.validators import validate_name, validate_email, validate_password


def load_custom_css():
    """Inject custom CSS for the app."""
    st.markdown("""
    <style>

    /* Sidebar */
    section[data-testid="stSidebar"]{
        background:#F3EEFF;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] *{
        color:#4C1D95;
    }

    /* Input fields */
    .stTextInput input{
        background:white;
        border:2px solid #D8B4FE;
        border-radius:10px;
    }

    /* Buttons */
    .stButton>button,
    div[data-testid="stForm"] button{
        background:linear-gradient(135deg,#7C3AED,#9333EA);
        color:white !important;
        border:none;
        border-radius:10px;
        font-weight:600;
    }

    .stButton>button:hover,
    div[data-testid="stForm"] button:hover{
        background:#6D28D9;
        color:white !important;
    }

    /* Login / Signup Tabs */
    button[data-baseweb="tab"]{
        color:#6D28D9 !important;
        font-weight:600;
    }

    button[data-baseweb="tab"][aria-selected="true"]{
        color:#7C3AED !important;
        border-bottom:3px solid #7C3AED !important;
    }

    button[data-baseweb="tab"]:hover{
        color:#9333EA !important;
    }

    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with navigation and user info"""
    with st.sidebar:
        # Logo and Title
        st.markdown("""
            <div style='text-align: center; padding: 1rem 0; color:#4C1D95;'>
                <h1 style='font-size: 2.5rem; margin: 0;'>🎓</h1>
                <h2 style='margin: 0.5rem 0; font-size: 1.5rem;'>Uni-Connect</h2>
                <p style='margin: 0; opacity: 0.8; font-size: 0.9rem;'>Connect • Share • Succeed</p>
            </div>
            <hr style='border:1px solid #D8B4FE; margin:1rem 0;'>
        """, unsafe_allow_html=True)

        # User session state
        if 'user' not in st.session_state:
            st.session_state.user = None

        # User Profile Section (when logged in)
        if st.session_state.user:

            user = st.session_state.user

            st.markdown(f"""
                <div style='background:#EDE9FE; padding:1rem;
                    border-radius:10px;
                    color:#4C1D95;
                    margin-bottom:1rem;'>
                  <h3 style='margin:0; font-size:1.2rem;'>
                     👤 {user['name']}
                  </h3>

                  <p style='margin:0.5rem 0 0 0;
                           opacity:0.8;
                           font-size:0.9rem;'>
                     Email: {user['email']}
                  </p>
                 </div>
              """, unsafe_allow_html=True)


            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.success("Logged out successfully!")
                st.rerun()


        else:
                tabs = st.tabs(["Login", "Sign Up"])
        #login tab
                with tabs[0]:
                   st.markdown(
                    "<h3 style='color:#5B21B6;'>👤 Login</h3>",
                    unsafe_allow_html=True
                   )

                   with st.form("sidebar_login_form"):
 
                          email = st.text_input("Email")
                          password = st.text_input(
                              "Password",
                          type="password"
                          )

                          login_btn = st.form_submit_button(

                                "🚀 Login",
                              use_container_width=True
                          )

                          if login_btn:
                            user = login_user(email, password)

                            if user:
                              st.session_state.user = user
                              st.success("Login successful!")
                              st.rerun()
                            else:
                              st.error("Invalid email or password.")

    #signup tab
                with tabs[1]:
                   st.markdown(
                    "<h3 style='color:#5B21B6;'>📝 Sign Up</h3>",
                    unsafe_allow_html=True
                    )

                   with st.form("sidebar_signup_form"):

                     name = st.text_input("Name")
                     email = st.text_input("Email")
                     password = st.text_input(
                        "Password",
                        type="password"
                     )

                     signup_btn = st.form_submit_button(
                        "📝 Sign Up",
                        use_container_width=True
                     )

                     if signup_btn:

                        success = signup_user(
                            name,
                            email,
                            password
                        )

                        if success:
                            st.success(
                                "Signup successful! Please login."
                            )
                        else:
                            st.error(
                                "Email already exists."
                            )
        # Navigation
        st.markdown("""
            <div style='color:#4C1D95;padding:0.5rem 0;'>
                <h3 style='margin: 0; font-size: 1.2rem;'>📍 Navigation</h3>
            </div>
          """, unsafe_allow_html=True)

        # Initialize page state if not exists
        if 'page' not in st.session_state:
            st.session_state.page = 'dashboard'

        # Navigation Buttons with custom styling
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🏠", help="Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
        
        with col2:
            if st.button("🔍", help="Lost & Found", use_container_width=True):
                st.session_state.page = 'lost_found'
                st.rerun()
        
        with col3:
            if st.button("📚", help="Notes", use_container_width=True):
                st.session_state.page = 'notes'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Full width navigation buttons
        if st.button("🏠 Dashboard", use_container_width=True, 
                     type="primary" if st.session_state.page == 'dashboard' else "secondary"):
            st.session_state.page = 'dashboard'
            st.rerun()
        
        if st.button("🔍 Lost & Found", use_container_width=True,
                     type="primary" if st.session_state.page == 'lost_found' else "secondary"):
            st.session_state.page = 'lost_found'
            st.rerun()
        
        if st.button("📚 Notes Exchange", use_container_width=True,
                     type="primary" if st.session_state.page == 'notes' else "secondary"):
            st.session_state.page = 'notes'
            st.rerun()
        
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin: 1.5rem 0;'>", unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
            <div style='text-align: center; color: #4C1D95; opacity: 0.6; 
                        font-size: 0.8rem; padding: 1rem 0;'>
                <p style='margin: 0;'>Uni-Connect v2.0</p>
                <p style='margin: 0;'>Made with ❤️ using Streamlit</p>
                <p style='margin: 0;'>© 2026 - All rights reserved</p>
            </div>
        """, unsafe_allow_html=True)

def main():
    """Main application logic"""
    
    # Load custom CSS
    load_custom_css()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    # Get current page from session state
    current_page = st.session_state.get('page', 'dashboard')
    
    # Render appropriate page
    if current_page == 'dashboard':
        render_dashboard()
    elif current_page == 'lost_found':
        render_lost_found()
    elif current_page == 'notes':
        render_notes_exchange()
    else:
        # Default to dashboard
        render_dashboard()

if __name__ == "__main__":
    main()
