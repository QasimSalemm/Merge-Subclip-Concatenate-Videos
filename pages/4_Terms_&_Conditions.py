import streamlit as st

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="Terms and Conditions - Professional Online Video Editor",
    page_icon="images/themes.png"
)

# ==============================
# Page Title
# ==============================
st.title("Terms and Conditions")

# ==============================
# Introduction
# ==============================
st.write(
    "Welcome to Professional Online Video Editor. By using our online video editing platform, "
    "you agree to comply with and be bound by the following terms and conditions. "
    "Please read them carefully before using our services."
)

# ==============================
# Use of Service
# ==============================
st.header("Use of Service")
st.write(
    "Our platform allows you to upload, edit, merge, trim, and add music to video files. "
    "You agree to use the service only for lawful purposes and not to upload or distribute "
    "content that violates any applicable laws or regulations."
)

# ==============================
# User Account and Responsibilities
# ==============================
st.header("User Responsibilities")
st.write(
    "While our platform does not require account registration, users are responsible for "
    "their actions and any content they upload. You agree not to misuse the platform, "
    "attempt unauthorized access, or interfere with other users’ experience."
)

# ==============================
# Intellectual Property
# ==============================
st.header("Intellectual Property")
st.write(
    "All content, design, and software provided by Professional Online Video Editor "
    "are protected by copyright and intellectual property laws. You retain ownership of your "
    "uploaded videos and audio files, but you grant us permission to process them for editing purposes."
)

# ==============================
# File Processing and Storage
# ==============================
st.header("File Processing and Storage")
st.write(
    "Uploaded video and audio files are temporarily stored for processing and automatically deleted after editing. "
    "We do not claim ownership of your files and take reasonable measures to ensure file security."
)

# ==============================
# Limitation of Liability
# ==============================
st.header("Limitation of Liability")
st.write(
    "Professional Online Video Editor is provided 'as-is' without warranties of any kind. "
    "We are not liable for any direct, indirect, or incidental damages resulting from the use of our platform, "
    "including data loss or file corruption. Users are responsible for backing up their own files."
)

# ==============================
# Changes to Terms
# ==============================
st.header("Changes to Terms")
st.write(
    "We may update these Terms and Conditions from time to time. "
    "All changes will be posted on this page with the effective date. "
    "Continued use of the platform constitutes acceptance of the updated terms."
)

# ==============================
# Governing Law
# ==============================
st.header("Governing Law")
st.write(
    "These terms are governed by and interpreted under the laws of the United States of America, "
    "or the relevant jurisdiction of the service provider, without regard to conflict of law principles."
)

# Footer
st.write("---")
st.info("📌 If you have questions about these Terms & Conditions, please contact us at qasimsaleem317@gmail.com")
