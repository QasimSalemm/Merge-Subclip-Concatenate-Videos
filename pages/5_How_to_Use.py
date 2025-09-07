import streamlit as st

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="How to Use - Professional Online Video Editor",
    page_icon="images/themes.png"
)

# ==============================
# Page Title
# ==============================
st.title("How to Use the Online Video Editor")

# ==============================
# Introduction
# ==============================
st.write(
    "Our Professional Online Video Editor makes it easy to edit videos online. "
    "Follow the step-by-step guide below to merge, trim, split, or add music to your videos quickly."
)

# ==============================
# Step 1: Upload Your Files
# ==============================
st.header("Step 1: Upload Your Files")
st.write(
    "Click the upload buttons to add your video and audio files. "
    "Supported formats include MP4, MOV, AVI for videos and MP3, WAV for audio."
)

# ==============================
# Step 2: Choose Your Tool
# ==============================
st.header("Step 2: Choose Your Tool")
st.write(
    "Select the functionality you want from the options provided:\n"
    "• Merge Audio with Video\n"
    "• Trim & Create Subclips\n"
    "• Concatenate Multiple Videos\n"
    "• Add Background Music"
)

# ==============================
# Step 3: Configure Settings
# ==============================
st.header("Step 3: Configure Settings")
st.write(
    "Adjust settings as needed, such as video codec, audio codec, volume levels for music, "
    "or start and end times for trimming clips. These options allow you to customize your output."
)

# ==============================
# Step 4: Process and Preview
# ==============================
st.header("Step 4: Process and Preview")
st.write(
    "Click the corresponding button to process your video. "
    "A preview of your edited video will appear once processing is complete. "
    "You can watch the video directly in the browser before downloading."
)

# ==============================
# Step 5: Download Your Video
# ==============================
st.header("Step 5: Download Your Video")
st.write(
    "Once your video is ready, click the 'Download' button to save it to your device. "
    "Each file is automatically named with a timestamp to avoid overwriting previous edits."
)

# ==============================
# Step 6: Clear Files (Optional)
# ==============================
st.header("Step 6: Clear Files (Optional)")
st.write(
    "To start fresh, use the 'Clear All' button to remove uploaded files and reset the editor. "
    "This ensures a clean workspace for your next project."
)

# Footer
st.write("---")
st.success(
    "💡 Use high-quality video and audio files for the best editing output.\n"
    "💡 Keep video durations reasonable to avoid long processing times.\n"
    "💡 Ensure audio length matches or is longer than video when adding background music.\n"
    "💡 Avoid unsupported file formats to prevent errors."
)
