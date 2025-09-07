from datetime import datetime
import streamlit as st

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="About Us - Professional Online Video Editor",
    page_icon="images/themes.png"
)

# ==============================
# Page Title
# ==============================
st.title("About Us")

# ==============================
# Introduction
# ==============================
st.write(
    "Welcome to our Professional Online Video Editor – the easiest way to "
    "merge, trim, split, and add music to your videos online. Our mission is "
    "to provide a fast, reliable, and user-friendly platform for all video editing needs."
)

# ==============================
# Our Vision
# ==============================
st.header("Our Vision")
st.write(
    "We aim to empower creators, professionals, and hobbyists to edit videos "
    "efficiently without the need for complex software. Our goal is to make video editing "
    "accessible to everyone, anywhere, with just a web browser."
)

# ==============================
# Our Features
# ==============================
st.header("Key Features")
st.write("Our platform offers a range of powerful tools, including:")
st.write("• Merge multiple videos into one seamless video")
st.write("• Trim and create precise subclips")
st.write("• Concatenate videos effortlessly")
st.write("• Add background music or audio tracks")
st.write("• Supports MP4, MOV, AVI, MP3, and WAV formats")
st.write("• Fast, intuitive, and completely online – no downloads required")

# ==============================
# Why Choose Us
# ==============================
st.header("Why Choose Us")
st.write(
    "Our online video editor is designed for speed, simplicity, and professional quality. "
    "Whether you are a content creator, educator, or casual user, our platform allows you "
    "to create high-quality videos without installing heavy software. "
    "We continuously improve our tools to meet the needs of modern video creators."
)

# ==============================
# Our Commitment
# ==============================
st.header("Our Commitment")
st.write(
    "We are committed to providing a secure and reliable online platform. "
    "Your uploaded videos are processed safely, and temporary files are automatically cleaned up. "
    "We strive to make video editing online simple, efficient, and enjoyable for everyone."
)

# ==============================
# Call to Action
# ==============================
st.header("Get Started Today")
st.write(
    "Join thousands of users who trust our online video editor. "
    "Start merging, trimming, and enhancing your videos instantly with our fast and easy-to-use tools!"
)

# Footer
st.write("---")
st.info("💡 This project is open-source and community-driven. Contributions & feedback are always welcome!")
