import streamlit as st

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="Privacy Policy - Professional Online Video Editor",
    page_icon="images/themes.png"
)

# ==============================
# Page Title
# ==============================
st.title("Privacy Policy")

# ==============================
# Introduction
# ==============================
st.write(
    "At Professional Online Video Editor, your privacy is our top priority. "
    "This Privacy Policy explains how we collect, use, and protect your personal information "
    "when you use our online video editing tools."
)

# ==============================
# Information We Collect
# ==============================
st.header("Information We Collect")
st.write(
    "We may collect the following types of information when you use our platform:"
)
st.write("• Personal information you provide (name, email) when contacting us")
st.write("• Uploaded video and audio files for editing purposes")
st.write("• Usage data including pages visited, tools used, and session duration")

# ==============================
# How We Use Your Information
# ==============================
st.header("How We Use Your Information")
st.write(
    "We use the information collected to provide and improve our services:"
)
st.write("• Process your video and audio files for editing")
st.write("• Respond to support requests or inquiries")
st.write("• Improve our platform, fix bugs, and enhance user experience")
st.write("• Send important updates about our services (if you opt-in)")

# ==============================
# File Security and Temporary Storage
# ==============================
st.header("File Security")
st.write(
    "All uploaded video and audio files are temporarily stored on our servers "
    "for processing and are automatically deleted after the editing process is complete. "
    "We do not share your files with third parties without your consent."
)

# ==============================
# Cookies and Analytics
# ==============================
st.header("Cookies and Analytics")
st.write(
    "Our platform may use cookies and analytics tools to track usage and improve performance. "
    "No personally identifiable information is collected through these tools without your consent."
)

# ==============================
# Third-Party Services
# ==============================
st.header("Third-Party Services")
st.write(
    "We may use trusted third-party services to host videos, handle emails, "
    "or provide analytics. These third parties are bound by strict privacy obligations."
)

# ==============================
# Your Rights
# ==============================
st.header("Your Rights")
st.write(
    "You have the right to access, update, or request deletion of your personal information. "
    "You can also opt out of marketing communications at any time."
)

# ==============================
# Changes to This Privacy Policy
# ==============================
st.header("Changes to This Privacy Policy")
st.write(
    "We may update our Privacy Policy from time to time. "
    "All changes will be posted on this page with an updated date."
)


st.write("---")
st.info("📌 If you have any questions about this Privacy Policy, please contact us at qasimsaleem317@gmail.com")
