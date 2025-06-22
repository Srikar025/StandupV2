import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import json

# Configuration
TEAMS_CONFIG = {
    1: {"lead_name": "SATWIK RAKHELKAR"},
    2: {"lead_name": "SRIKAR GADAGOJU"},
    3: {"lead_name": "PUNEETH PEELA"},
    4: {"lead_name": "SHIVA AMBOTU"},
    5: {"lead_name": "MADAGALA NIKHIL SAI SIDDHARDHA"},
    6: {"lead_name": "Sai Karthikeyan "},
    7: {"lead_name": "sreepranav guni "},
    8: {"lead_name": "HASINI PARRE"},
    9: {"lead_name": "Chikoti Bhuvana Sri"},
    10: {"lead_name": "GANNARAM DHRUV"}
}

# CSV file paths
USERS_CSV = "users.csv"
STANDUPS_CSV = "standups.csv"
DOUBTS_CSV = "doubts.csv"

def get_team_lead_password(team_number):
    """Get tech lead password from Streamlit secrets"""
    try:
        # Access passwords from Streamlit secrets
        passwords = st.secrets.get("team_lead_passwords", {})
        return passwords.get(str(team_number))
    except Exception as e:
        st.error(f"Error accessing credentials: {e}")
        return None

def verify_tech_lead_password(team_number, password):
    """Verify tech lead password against stored credentials"""
    stored_password = get_team_lead_password(team_number)
    return stored_password == password

def init_csv_files():
    """Initialize CSV files if they don't exist"""
    
    # Users CSV
    if not os.path.exists(USERS_CSV):
        users_df = pd.DataFrame(columns=['user_id', 'name', 'team_number', 'registration_date'])
        users_df.to_csv(USERS_CSV, index=False)
    
    # Standups CSV
    if not os.path.exists(STANDUPS_CSV):
        standups_df = pd.DataFrame(columns=[
            'submission_id', 'user_id', 'name', 'team_number', 
            'date', 'yesterday_work', 'today_plan', 'blockers', 'timestamp'
        ])
        standups_df.to_csv(STANDUPS_CSV, index=False)
    
    # Doubts CSV
    if not os.path.exists(DOUBTS_CSV):
        doubts_df = pd.DataFrame(columns=[
            'doubt_id', 'user_id', 'name', 'team_number', 
            'doubt_text', 'priority', 'status', 'reply_message', 'date', 'timestamp'
        ])
        doubts_df.to_csv(DOUBTS_CSV, index=False)

def load_users():
    """Load users from CSV"""
    try:
        return pd.read_csv(USERS_CSV)
    except:
        return pd.DataFrame(columns=['user_id', 'name', 'team_number', 'registration_date'])

def save_user(user_id, name, team_number):
    """Save new user to CSV"""
    users_df = load_users()
    
    new_user = pd.DataFrame({
        'user_id': [user_id],
        'name': [name],
        'team_number': [team_number],
        'registration_date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    })
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(USERS_CSV, index=False)

def get_user_by_id(user_id):
    """Get user details by user_id"""
    users_df = load_users()
    user_data = users_df[users_df['user_id'] == user_id]
    return user_data.iloc[0] if not user_data.empty else None

def save_standup(user_data, yesterday_work, today_plan, blockers):
    """Save standup submission to CSV"""
    standups_df = pd.read_csv(STANDUPS_CSV)
    
    submission_id = len(standups_df) + 1
    
    new_standup = pd.DataFrame({
        'submission_id': [submission_id],
        'user_id': [user_data['user_id']],
        'name': [user_data['name']],
        'team_number': [user_data['team_number']],
        'date': [date.today().strftime('%Y-%m-%d')],
        'yesterday_work': [yesterday_work],
        'today_plan': [today_plan],
        'blockers': [blockers],
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    })
    
    standups_df = pd.concat([standups_df, new_standup], ignore_index=True)
    standups_df.to_csv(STANDUPS_CSV, index=False)

def save_doubt(user_data, doubt_text, priority):
    """Save doubt submission to CSV"""
    doubts_df = pd.read_csv(DOUBTS_CSV)
    
    doubt_id = len(doubts_df) + 1
    
    new_doubt = pd.DataFrame({
        'doubt_id': [doubt_id],
        'user_id': [user_data['user_id']],
        'name': [user_data['name']],
        'team_number': [user_data['team_number']],
        'doubt_text': [doubt_text],
        'priority': [priority],
        'status': ['Open'],
        'reply_message': [""],
        'date': [date.today().strftime('%Y-%m-%d')],
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    })
    
    doubts_df = pd.concat([doubts_df, new_doubt], ignore_index=True)
    doubts_df.to_csv(DOUBTS_CSV, index=False)

def update_doubt_reply(doubt_id, reply_message, lead_name):
    """Update doubt with tech lead's reply"""
    doubts_df = pd.read_csv(DOUBTS_CSV)
    
    # Find the doubt and update it
    doubt_index = doubts_df[doubts_df['doubt_id'] == doubt_id].index
    if len(doubt_index) > 0:
        doubts_df.loc[doubt_index[0], 'reply_message'] = f"[{lead_name}]: {reply_message}"
        doubts_df.loc[doubt_index[0], 'status'] = 'Replied'
        doubts_df.to_csv(DOUBTS_CSV, index=False)
        return True
    return False

def user_registration_page():
    """User registration/login page"""
    st.title("🚀 Welcome to Standup Reports")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["🔐 Developer Login", "👤 New Developer Registration", "👥 Tech Lead Login"])
    
    with tab1:
        st.subheader("Login with Existing ID")
        
        with st.form("login_form"):
            user_id = st.text_input("Developer ID", placeholder="Enter your developer ID")
            login_submitted = st.form_submit_button("Login", use_container_width=True)
            
            if login_submitted:
                if user_id:
                    user_data = get_user_by_id(user_id)
                    if user_data is not None:
                        st.session_state.user_data = user_data.to_dict()
                        st.session_state.logged_in = True
                        st.success(f"Welcome back {user_data['name']}!")
                        st.rerun()
                    else:
                        st.error("Developer ID not found! Please register first.")
                else:
                    st.error("Please enter your Developer ID.")
    
    with tab2:
        st.subheader("Register Your Details")
        
        with st.form("registration_form"):
            name = st.text_input("Full Name*", placeholder="Enter your full name")
            user_id = st.text_input("Developer ID*", placeholder="Enter your developer ID")
            team_number = st.selectbox(
                "Select Your Team*", 
                options=list(TEAMS_CONFIG.keys()),
                format_func=lambda x: f"Team {x}"
            )
            
            submitted = st.form_submit_button("Register & Continue", use_container_width=True)
            
            if submitted:
                if name and user_id:
                    # Check if user already exists
                    existing_user = get_user_by_id(user_id)
                    if existing_user is not None:
                        st.error(f"Developer ID '{user_id}' already exists! Please use the login tab.")
                    else:
                        save_user(user_id, name, team_number)
                        st.session_state.user_data = {
                            'user_id': user_id,
                            'name': name,
                            'team_number': team_number
                        }
                        st.session_state.logged_in = True
                        st.success(f"Welcome {name}! You're registered to Team {team_number}")
                        st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    with tab3:
        st.subheader("Tech Lead Direct Login")
        st.info("👥 Tech leads can login directly here with their team number and password")
        
        with st.form("lead_direct_login"):
            team_selection = st.selectbox(
                "Select Your Team", 
                options=list(TEAMS_CONFIG.keys()),
                format_func=lambda x: f"Team {x} - {TEAMS_CONFIG[x]['lead_name']}"
            )
            
            lead_password = st.text_input("Tech Lead Password", type="password", 
                                        placeholder="Enter your tech lead password")
            
            lead_login_submitted = st.form_submit_button("Login as Tech Lead", use_container_width=True)
            
            if lead_login_submitted:
                if lead_password:
                    # Verify tech lead password
                    if verify_tech_lead_password(team_selection, lead_password):
                        st.session_state.user_data = {
                            'user_id': f"LEAD_{team_selection}",
                            'name': TEAMS_CONFIG[team_selection]['lead_name'],
                            'team_number': team_selection,
                            'is_tech_lead': True
                        }
                        st.session_state.logged_in = True
                        st.session_state.lead_authenticated = True
                        st.success(f"Welcome Tech Lead {TEAMS_CONFIG[team_selection]['lead_name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid tech lead password!")
                else:
                    st.error("Please enter your tech lead password.")

def submit_standup_page():
    """Standup submission page"""
    user_data = st.session_state.user_data
    
    st.title("📝 Daily Standup Submission")
    st.markdown(f"**Developer:** {user_data['name']} | **Team:** {user_data['team_number']}")
    st.markdown("---")
    
    # Check if user already submitted today
    standups_df = pd.read_csv(STANDUPS_CSV)
    today_str = date.today().strftime('%Y-%m-%d')
    today_submission = standups_df[
        (standups_df['user_id'] == user_data['user_id']) & 
        (standups_df['date'] == today_str)
    ]
    
    if not today_submission.empty:
        st.info("✅ You have already submitted your standup for today!")
        st.subheader("Your Today's Submission:")
        
        submission = today_submission.iloc[0]
        st.write(f"**Yesterday's Work:** {submission['yesterday_work']}")
        st.write(f"**Today's Plan:** {submission['today_plan']}")
        st.write(f"**Blockers:** {submission['blockers']}")
        st.write(f"**Submitted at:** {submission['timestamp']}")
        
        if st.button("Submit Another Update"):
            st.session_state.allow_resubmit = True
            st.rerun()
    
    if today_submission.empty or st.session_state.get('allow_resubmit', False):
        with st.form("standup_form"):
            st.subheader("Submit Your Daily Standup")
            
            yesterday_work = st.text_area(
                "What did you work on yesterday? 🔄",
                placeholder="Describe the tasks you completed yesterday...",
                height=100
            )
            
            today_plan = st.text_area(
                "What will you work on today? 📋",
                placeholder="List your plans for today...",
                height=100
            )
            
            blockers = st.text_area(
                "Any blockers or impediments? 🚧",
                placeholder="Mention any challenges or blockers (leave empty if none)...",
                height=80
            )
            
            submitted = st.form_submit_button("Submit Standup", use_container_width=True)
            
            if submitted:
                if yesterday_work and today_plan:
                    save_standup(user_data, yesterday_work, today_plan, blockers)
                    st.success("✅ Standup submitted successfully!")
                    st.balloons()
                    st.session_state.allow_resubmit = False
                    st.rerun()
                else:
                    st.error("Please fill in both yesterday's work and today's plan.")

def submit_doubt_page():
    """Doubt submission page"""
    user_data = st.session_state.user_data
    
    st.title("❓ Submit Your Doubts")
    st.markdown(f"**Developer:** {user_data['name']} | **Team:** {user_data['team_number']}")
    st.markdown("---")
    
    # Show user's existing doubts and replies
    doubts_df = pd.read_csv(DOUBTS_CSV)
    user_doubts = doubts_df[doubts_df['user_id'] == user_data['user_id']]
    
    if not user_doubts.empty:
        st.subheader("📋 Your Previous Doubts")
        
        for _, doubt in user_doubts.iterrows():
            with st.expander(f"Doubt #{doubt['doubt_id']} - {doubt['priority']} Priority - {doubt['status']} (Submitted: {doubt['date']})"):
                st.write(f"**Your Question:** {doubt['doubt_text']}")
                st.write(f"**Status:** {doubt['status']}")
                st.write(f"**Submitted:** {doubt['timestamp']}")
                
                # Show tech lead's reply if any
                if pd.notna(doubt['reply_message']) and doubt['reply_message'].strip():
                    st.write(f"**Tech Lead's Reply:** {doubt['reply_message']}")
                elif doubt['status'] == 'Open':
                    st.info("⏳ Waiting for tech lead's response...")
        
        st.markdown("---")
    
    with st.form("doubt_form"):
        st.subheader("Ask Your Question")
        
        doubt_text = st.text_area(
            "Describe your doubt or question 💭",
            placeholder="Explain your question in detail...",
            height=150
        )
        
        priority = st.selectbox(
            "Priority Level 🎯",
            options=["Low", "Medium", "High"],
            help="Select the urgency of your doubt"
        )
        
        submitted = st.form_submit_button("Submit Doubt", use_container_width=True)
        
        if submitted:
            if doubt_text:
                save_doubt(user_data, doubt_text, priority)
                st.success("✅ Your doubt has been submitted successfully!")
                st.info("Your tech lead will review and respond to your question.")
            else:
                st.error("Please describe your doubt or question.")

def team_lead_dashboard():
    """Tech lead dashboard with password protection"""
    st.title("👥 Tech Lead Dashboard")
    st.markdown("---")
    
    # Check if user is already authenticated as tech lead from direct login
    if st.session_state.user_data.get('is_tech_lead', False):
        st.session_state.lead_authenticated = True
    
    # Password authentication for regular users accessing tech lead dashboard
    if 'lead_authenticated' not in st.session_state:
        st.session_state.lead_authenticated = False
    
    if not st.session_state.lead_authenticated:
        st.subheader("🔐 Tech Lead Authentication")
        st.info("💡 Regular developers need to authenticate with tech lead password to access this dashboard")
        st.warning("⚠️ Only tech leads should access this dashboard. Please contact your tech lead for credentials.")
        
        with st.form("lead_auth_form"):
            password = st.text_input("Enter Tech Lead Password", type="password")
            auth_submitted = st.form_submit_button("Login as Tech Lead")
            
            if auth_submitted:
                # Check if password matches any tech lead password
                valid_password = False
                for team_id in TEAMS_CONFIG.keys():
                    if verify_tech_lead_password(team_id, password):
                        st.session_state.lead_authenticated = True
                        st.session_state.lead_team_access = team_id
                        valid_password = True
                        break
                
                if valid_password:
                    st.success("✅ Authentication successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid password!")
        return
    
    # Authenticated tech lead dashboard
    st.success("🎉 Welcome Tech Lead!")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Standups", "❓ Doubts", "📥 Downloads", "📊 All Teams Overview"])
    
    with tab1:
        st.subheader("Standups Management")
        
        # Get the tech lead's team number
        lead_team = st.session_state.user_data.get('team_number', 1)
        
        # Team filter - default to lead's team, but allow selection of other teams
        selected_teams = st.multiselect(
            "Filter by Teams",
            options=list(TEAMS_CONFIG.keys()),
            default=[lead_team],  # Default to lead's team
            format_func=lambda x: f"Team {x}"
        )
        
        # Date filter
        date_filter = st.date_input("Filter by Date", value=date.today())
        
        # Load and filter standups
        standups_df = pd.read_csv(STANDUPS_CSV)
        
        if not standups_df.empty:
            filtered_standups = standups_df[
                (standups_df['team_number'].isin(selected_teams)) &
                (standups_df['date'] == date_filter.strftime('%Y-%m-%d'))
            ]
            
            if not filtered_standups.empty:
                st.write(f"**Showing {len(filtered_standups)} standups**")
                
                # Download button
                csv_data = filtered_standups.to_csv(index=False)
                st.download_button(
                    label="📥 Download Standups CSV",
                    data=csv_data,
                    file_name=f"standups_{date_filter.strftime('%Y-%m-%d')}.csv",
                    mime="text/csv"
                )
                
                # Display standups
                for _, standup in filtered_standups.iterrows():
                    with st.expander(f"{standup['name']} - Team {standup['team_number']} (Submitted: {standup['timestamp']})"):
                        st.write(f"**Yesterday:** {standup['yesterday_work']}")
                        st.write(f"**Today:** {standup['today_plan']}")
                        st.write(f"**Blockers:** {standup['blockers']}")
                        st.write(f"**Submission ID:** {standup['submission_id']}")
            else:
                st.info("No standups found for selected filters.")
        else:
            st.info("No standups submitted yet.")
    
    with tab2:
        st.subheader("Doubts Management")
        
        # Get the tech lead's team number
        lead_team = st.session_state.user_data.get('team_number', 1)
        lead_name = st.session_state.user_data.get('name', 'Tech Lead')
        
        # Load doubts
        doubts_df = pd.read_csv(DOUBTS_CSV)
        
        if not doubts_df.empty:
            # Status filter
            status_filter = st.selectbox("Filter by Status", ["All", "Open", "Replied", "Resolved"])
            
            # Team filter for doubts - default to lead's team, but allow selection of other teams
            selected_teams_doubts = st.multiselect(
                "Filter by Teams",
                options=list(TEAMS_CONFIG.keys()),
                default=[lead_team],  # Default to lead's team
                format_func=lambda x: f"Team {x}",
                key="doubts_team_filter"
            )
            
            filtered_doubts = doubts_df.copy()
            if status_filter != "All":
                filtered_doubts = filtered_doubts[filtered_doubts['status'] == status_filter]
            
            # Apply team filter
            filtered_doubts = filtered_doubts[filtered_doubts['team_number'].isin(selected_teams_doubts)]
            
            if not filtered_doubts.empty:
                st.write(f"**Showing {len(filtered_doubts)} doubts**")
                
                # Download button
                csv_data = filtered_doubts.to_csv(index=False)
                st.download_button(
                    label="📥 Download Doubts CSV",
                    data=csv_data,
                    file_name=f"doubts_{datetime.now().strftime('%Y-%m-%d')}.csv",
                    mime="text/csv"
                )
                
                # Display doubts
                for _, doubt in filtered_doubts.iterrows():
                    with st.expander(f"{doubt['name']} - Team {doubt['team_number']} [{doubt['priority']} Priority] (Submitted: {doubt['timestamp']})"):
                        st.write(f"**Question:** {doubt['doubt_text']}")
                        st.write(f"**Status:** {doubt['status']}")
                        st.write(f"**Date:** {doubt['date']}")
                        st.write(f"**Doubt ID:** {doubt['doubt_id']}")
                        
                        # Show existing reply if any
                        if pd.notna(doubt['reply_message']) and doubt['reply_message'].strip():
                            st.write(f"**Reply:** {doubt['reply_message']}")
                        
                        # Reply section for tech leads
                        if doubt['status'] in ['Open', 'Replied']:
                            st.markdown("---")
                            st.write("**Add/Update Reply:**")
                            
                            # Create a unique key for each doubt's reply form
                            reply_key = f"reply_form_{doubt['doubt_id']}"
                            
                            with st.form(key=reply_key):
                                reply_text = st.text_area(
                                    "Your reply message",
                                    placeholder="Enter your reply to this doubt...",
                                    height=100,
                                    key=f"reply_text_{doubt['doubt_id']}"
                                )
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.form_submit_button("Send Reply", use_container_width=True):
                                        if reply_text.strip():
                                            if update_doubt_reply(doubt['doubt_id'], reply_text, lead_name):
                                                st.success("Reply sent successfully!")
                                                st.rerun()
                                            else:
                                                st.error("Failed to send reply. Please try again.")
                                        else:
                                            st.error("Please enter a reply message.")
                                
                                with col2:
                                    if st.form_submit_button("Mark as Resolved", use_container_width=True):
                                        # Update doubt status to resolved
                                        doubts_df.loc[doubts_df['doubt_id'] == doubt['doubt_id'], 'status'] = 'Resolved'
                                        doubts_df.to_csv(DOUBTS_CSV, index=False)
                                        st.success("Doubt marked as resolved!")
                                        st.rerun()
            else:
                st.info("No doubts found for selected filter.")
        else:
            st.info("No doubts submitted yet.")
    
    with tab3:
        st.subheader("📥 Bulk Downloads")
        st.info("Download complete datasets for analysis")
        
        # Load all data
        standups_df = pd.read_csv(STANDUPS_CSV)
        doubts_df = pd.read_csv(DOUBTS_CSV)
        users_df = pd.read_csv(USERS_CSV)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**All Standups**")
            if not standups_df.empty:
                csv_data = standups_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download All Standups",
                    data=csv_data,
                    file_name=f"all_standups_{datetime.now().strftime('%Y-%m-%d')}.csv",
                    mime="text/csv",
                    key="download_all_standups"
                )
                st.write(f"Total records: {len(standups_df)}")
            else:
                st.write("No standup data available")
        
        with col2:
            st.write("**All Doubts**")
            if not doubts_df.empty:
                csv_data = doubts_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download All Doubts",
                    data=csv_data,
                    file_name=f"all_doubts_{datetime.now().strftime('%Y-%m-%d')}.csv",
                    mime="text/csv",
                    key="download_all_doubts"
                )
                st.write(f"Total records: {len(doubts_df)}")
            else:
                st.write("No doubt data available")
        
        with col3:
            st.write("**All Developers**")
            if not users_df.empty:
                csv_data = users_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download All Developers",
                    data=csv_data,
                    file_name=f"all_developers_{datetime.now().strftime('%Y-%m-%d')}.csv",
                    mime="text/csv",
                    key="download_all_developers"
                )
                st.write(f"Total records: {len(users_df)}")
            else:
                st.write("No developer data available")
        
        # Team-wise downloads
        st.markdown("---")
        st.subheader("👥 Team-wise Downloads")
        
        # Team selection for downloads
        download_team_filter = st.selectbox(
            "Select Team for Download",
            options=['All Teams'] + [f"Team {i}" for i in TEAMS_CONFIG.keys()],
            key="team_download_filter"
        )
        
        if download_team_filter != 'All Teams':
            selected_team_num = int(download_team_filter.split()[1])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**{download_team_filter} Standups**")
                if not standups_df.empty:
                    team_standups = standups_df[standups_df['team_number'] == selected_team_num]
                    if not team_standups.empty:
                        csv_data = team_standups.to_csv(index=False)
                        st.download_button(
                            label=f"📥 Download {download_team_filter} Standups",
                            data=csv_data,
                            file_name=f"team_{selected_team_num}_standups_{datetime.now().strftime('%Y-%m-%d')}.csv",
                            mime="text/csv",
                            key=f"download_team_{selected_team_num}_standups"
                        )
                        st.write(f"Total records: {len(team_standups)}")
                    else:
                        st.write(f"No standups for {download_team_filter}")
                else:
                    st.write("No standup data available")
            
            with col2:
                st.write(f"**{download_team_filter} Doubts**")
                if not doubts_df.empty:
                    team_doubts = doubts_df[doubts_df['team_number'] == selected_team_num]
                    if not team_doubts.empty:
                        csv_data = team_doubts.to_csv(index=False)
                        st.download_button(
                            label=f"📥 Download {download_team_filter} Doubts",
                            data=csv_data,
                            file_name=f"team_{selected_team_num}_doubts_{datetime.now().strftime('%Y-%m-%d')}.csv",
                            mime="text/csv",
                            key=f"download_team_{selected_team_num}_doubts"
                        )
                        st.write(f"Total records: {len(team_doubts)}")
                    else:
                        st.write(f"No doubts for {download_team_filter}")
                else:
                    st.write("No doubt data available")
        
        # Date range download for standups
        st.markdown("---")
        st.subheader("📅 Date Range Downloads")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("Start Date", value=date.today())
        with col2:
            end_date = st.date_input("End Date", value=date.today())
        with col3:
            date_team_filter = st.selectbox(
                "Select Team",
                options=['All Teams'] + [f"Team {i}" for i in TEAMS_CONFIG.keys()],
                key="date_team_filter"
            )
        
        if start_date <= end_date:
            # Filter standups by date range and optionally by team
            if not standups_df.empty:
                standups_df_copy = standups_df.copy()
                standups_df_copy['date'] = pd.to_datetime(standups_df_copy['date'])
                filtered_standups = standups_df_copy[
                    (standups_df_copy['date'] >= pd.to_datetime(start_date)) &
                    (standups_df_copy['date'] <= pd.to_datetime(end_date))
                ]
                
                # Apply team filter if specific team is selected
                if date_team_filter != 'All Teams':
                    selected_team_num = int(date_team_filter.split()[1])
                    filtered_standups = filtered_standups[filtered_standups['team_number'] == selected_team_num]
                    file_prefix = f"team_{selected_team_num}_standups"
                    button_label = f"📥 Download {date_team_filter} Standups ({start_date} to {end_date})"
                else:
                    file_prefix = "standups"
                    button_label = f"📥 Download All Standups ({start_date} to {end_date})"
                
                if not filtered_standups.empty:
                    csv_data = filtered_standups.to_csv(index=False)
                    st.download_button(
                        label=button_label,
                        data=csv_data,
                        file_name=f"{file_prefix}_{start_date}_to_{end_date}.csv",
                        mime="text/csv",
                        key="download_date_range_standups"
                    )
                    st.write(f"Records in range: {len(filtered_standups)}")
                else:
                    st.info("No standups found in selected date range and team filter")
        else:
            st.error("Start date must be before or equal to end date")
    
    with tab4:
        st.subheader("📊 All Teams Overview")
        
        # Load all data
        standups_df = pd.read_csv(STANDUPS_CSV)
        doubts_df = pd.read_csv(DOUBTS_CSV)
        users_df = pd.read_csv(USERS_CSV)
        
        # Team statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Teams", len(TEAMS_CONFIG))
        
        with col2:
            st.metric("Total Developers", len(users_df))
        
        with col3:
            today_standups = standups_df[standups_df['date'] == date.today().strftime('%Y-%m-%d')]
            st.metric("Today's Standups", len(today_standups))
        
        with col4:
            open_doubts = doubts_df[doubts_df['status'] == 'Open']
            st.metric("Open Doubts", len(open_doubts))
        
        # Team-wise breakdown
        st.subheader("Team-wise Statistics")
        team_stats = []
        
        for team_id in TEAMS_CONFIG.keys():
            team_users = users_df[users_df['team_number'] == team_id]
            team_standups_today = today_standups[today_standups['team_number'] == team_id]
            team_open_doubts = open_doubts[open_doubts['team_number'] == team_id]
            
            team_stats.append({
                'Team': f"Team {team_id}",
                'Members': len(team_users),
                'Today Standups': len(team_standups_today),
                'Open Doubts': len(team_open_doubts)
            })
        
        st.dataframe(pd.DataFrame(team_stats), use_container_width=True)
    
    # Logout button
    if st.button("🔓 Logout", key="lead_logout"):
        st.session_state.lead_authenticated = False
        st.rerun()

def main():
    st.set_page_config(
        page_title="Standup Reports App",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize CSV files
    init_csv_files()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        user_registration_page()
        return
    
    # Sidebar navigation for logged-in users
    st.sidebar.title("🚀 Navigation")
    st.sidebar.markdown(f"**Welcome:** {st.session_state.user_data['name']}")
    st.sidebar.markdown(f"**Team:** {st.session_state.user_data['team_number']}")
    
    # Show role if tech lead
    if st.session_state.user_data.get('is_tech_lead', False):
        st.sidebar.markdown("**Role:** 👥 Tech Lead")
    
    st.sidebar.markdown("---")
    
    # Different navigation options based on role
    if st.session_state.user_data.get('is_tech_lead', False):
        page = st.sidebar.selectbox(
            "Choose a page:",
            ["👥 Tech Lead Dashboard"]
        )
    else:
        page = st.sidebar.selectbox(
            "Choose a page:",
            ["📝 Submit Standup", "❓ Submit Doubt", "👥 Tech Lead Dashboard"]
        )
    
    # Logout button
    if st.sidebar.button("🔓 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Page routing
    if page == "📝 Submit Standup":
        submit_standup_page()
    elif page == "❓ Submit Doubt":
        submit_doubt_page()
    elif page == "👥 Tech Lead Dashboard":
        team_lead_dashboard()

if __name__ == "__main__":
    main()
