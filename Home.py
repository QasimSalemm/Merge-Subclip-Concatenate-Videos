import os
from datetime import datetime
import time
import streamlit as st
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
import toml
import streamlit_logger as sl

import utility_functions as uf

# ==============================
# Streamlit Page Config
# ==============================
st.set_page_config(
    page_title="Online Video Editor - Merge, Trim, Split & Add Music to Videos",
    page_icon="images/themes.png"
)
st.title("Professional Online Video Editor: Merge, Trim & Add Music to Videos")
st.write("Easily edit your videos online with our professional video editor. Merge videos, trim clips, split segments, and add background music in just a few clicks. Supports MP4, MOV, AVI, MP3, and WAV formats.")
st.divider()



# ==============================
# Sidebar Settings
# ==============================
st.sidebar.header("⚙️ Settings")
codec = st.sidebar.selectbox("Video Codec", ["libx264", "mpeg4", "libvpx"], index=0)
audio_codec = st.sidebar.selectbox("Audio Codec", ["aac", "libvorbis", "mp3"], index=0)
st.sidebar.divider()
# ==============================
# Config & Theme
# ==============================
CONFIG_PATH = "./.streamlit/config.toml"
THEMES = {
    "Light": {"theme": {"base": "light"}},
    "Dark": {"theme": {"base": "dark", "borderColor": "mediumSlateBlue"}}
}

def get_current_theme():
    if os.path.exists(CONFIG_PATH):
        try:
            config = toml.load(CONFIG_PATH)
            base = config.get("theme", {}).get("base", "Light")
            return "Dark" if base.lower() == "dark" else "Light"
        except:
            return "Light"
    return "Light"

current_theme = get_current_theme()
theme_choice = st.sidebar.radio("Select Theme", list(THEMES.keys()),
                                index=list(THEMES.keys()).index(current_theme))

if st.sidebar.button("Apply Theme"):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        toml.dump(THEMES[theme_choice], f)
    st.sidebar.success(f"{theme_choice} theme applied!")
    time.sleep(0.5)
    st.rerun()
# ==============================
# Utility Functions
# ==============================
def cleanup_files(*files, new_keys={}):
    for f in files:
        try: f.close()
        except: pass
    uf.remove_temp_files(*files)
    for key, value in new_keys.items():
        st.session_state[key] = value
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

def load_clips(video_path=None, audio_path=None):
    video = VideoFileClip(video_path) if video_path else None
    audio = AudioFileClip(audio_path) if audio_path else None
    return video, audio

# ==============================
# Session Keys & Tools
# ==============================
TOOLS = {
    "Merge Audio with Video": {"video":"video_merge","audio":"audio_merge","output":"merge_output","video_key":"video_key_merge","audio_key":"audio_key_merge"},
    "Trim & Create Subclips": {"video":"subclip_temp","output":"subclip_output","key":"subclip_key"},
    "Concatenate Videos": {"clips":"concat_clips","files":"concat_files","output":"concat_output","key":"concat_key"},
    "Add Background Music": {"video":"video_bg","audio":"audio_bg","output":"bg_output","video_key":"video_key_bg","audio_key":"audio_key_bg"}
}

option = st.radio("Select Functionality", list(TOOLS.keys()))

# Initialize session_state keys
for key in TOOLS[option].values():
    if key not in st.session_state:
        st.session_state[key] = [] if "clips" in key or "files" in key else uf.generate_key(key) if "key" in key else None

def remove_uploaded_files():
    keys = TOOLS[option]
    if option == "Concatenate Videos":
        cleanup_files(
            *st.session_state.get(keys["clips"], []),
            *st.session_state.get(keys["files"], []),
            st.session_state.get(keys["output"]),
            new_keys={keys["clips"]: [], keys["files"]: [], keys["output"]: None, keys["key"]: uf.generate_key(keys["key"])}
        )
    else:
        cleanup_files(
            st.session_state.get(keys.get("video")),
            st.session_state.get(keys.get("audio")),
            st.session_state.get(keys.get("output")),
            new_keys={k: uf.generate_key(k) if "key" in k else None for k in keys.values()}
        )

# ==============================
# Tool Implementations
# ==============================
def merge_audio_with_video_ui():
    v_file = st.file_uploader("Upload Video", type=["mp4","mov","avi"], key=st.session_state.video_key_merge)
    a_file = st.file_uploader("Upload Audio", type=["mp3","wav"], key=st.session_state.audio_key_merge)
    if v_file and a_file:
        video_path = uf.save_temp_file(v_file, ".mp4")
        audio_path = uf.save_temp_file(a_file, ".mp3")
        video, audio = load_clips(video_path, audio_path)
        col1, col2 = st.columns(2)
        col1.success(f"🎥 {v_file.name} | {video.duration:.2f}s")
        col2.success(f"🎵 {a_file.name} | {audio.duration:.2f}s")

        if st.button("Merge Now"):
            cut_audio = audio.subclipped(0, min(audio.duration, video.duration))
            output_video = video.with_audio(cut_audio)
            filename = f"Merged__{datetime.now().strftime('%H%M%S')}.mp4"
            st.session_state.merge_output = filename
            output_video.write_videofile(filename, codec=codec, audio_codec=audio_codec, logger=sl.StreamlitLogger(int(output_video.fps*output_video.duration)))
            st.success("✅ Merge Completed!")
            st.video(filename)
            with open(filename, "rb") as f:
                st.download_button("⬇️ Download", f, file_name=filename)
            uf.close_and_remove(output_video, video, audio)

def trim_video_ui():
    video_file = st.file_uploader("Upload Video to Trim", type=["mp4","mov","avi"], key=st.session_state.subclip_key)
    if video_file:
        video_path = uf.save_temp_file(video_file, ".mp4")
        video, _ = load_clips(video_path, None)
        st.success(f"🎥 {video_file.name} | {video.duration:.2f}s")
        start = st.number_input("Start time (sec)", 0.0, video.duration, 0.0)
        end = st.number_input("End time (sec)", 0.0, video.duration, min(5.0, video.duration))

        if st.button("Create Subclip"):
            if start < end:
                sub_clip = video.subclipped(start, end)
                filename = f"Subclip_{int(start)}-{int(end)}_{datetime.now().strftime('%H%M%S')}.mp4"
                st.session_state.subclip_output = filename
                sub_clip.write_videofile(filename, codec=codec, audio_codec=audio_codec, logger=sl.StreamlitLogger(int(sub_clip.fps*sub_clip.duration)))
                st.success("✅ Subclip Created!")
                st.video(filename)
                with open(filename, "rb") as f:
                    st.download_button("Download", f, file_name=filename)
                sub_clip.close()
            else:
                st.error("End time must be greater than start time")

def concatenate_videos_ui():
    files = st.file_uploader("Upload Videos to Concatenate", type=["mp4","mov","avi"], accept_multiple_files=True, key=st.session_state.concat_key)
    if files:
        clips = []
        for f in files:
            temp_path = uf.save_temp_file(f, ".mp4")
            clip = VideoFileClip(temp_path)
            clips.append(clip)
            st.info(f"📂 {f.name} | Duration: {clip.duration:.2f}s")
        if st.button("Concatenate Videos"):
            final_clip = concatenate_videoclips(clips)
            filename = f"Concat_{datetime.now().strftime('%H%M%S')}.mp4"
            st.session_state.concat_output = filename
            final_clip.write_videofile(filename, codec=codec, audio_codec=audio_codec, logger=sl.StreamlitLogger(int(final_clip.fps*final_clip.duration)))
            st.success("✅ Concatenation Completed!")
            st.video(filename)
            with open(filename, "rb") as f:
                st.download_button("Download", f, file_name=filename)
            uf.close_and_remove(final_clip, *clips)

def add_background_music_ui():
    video_file = st.file_uploader("Upload Video", type=["mp4","mov","avi"], key=st.session_state.video_key_bg)
    audio_file = st.file_uploader("Upload Audio", type=["mp3","wav"], key=st.session_state.audio_key_bg)
    if video_file and audio_file:
        video_path = uf.save_temp_file(video_file, ".mp4")
        audio_path = uf.save_temp_file(audio_file, ".mp3")
        video, audio = load_clips(video_path, audio_path)
        st.success(f"🎥 {video_file.name} | 🎵 {audio_file.name} | {video.duration:.2f}s")
        orig_vol = st.slider("Original Voice Volume", 0.0, 1.0, 1.0)
        music_vol = st.slider("Background Music Volume", 0.0, 1.0, 0.5)

        if st.button("Merge Now"):
            video_audio = video.audio.with_volume_scaled(orig_vol) if video.audio else None
            cut_music = audio.subclipped(0, min(audio.duration, video.duration)).with_volume_scaled(music_vol)
            final_audio = CompositeAudioClip([video_audio, cut_music]) if video_audio else cut_music
            output_video = video.with_audio(final_audio)
            filename = f"Merged__{datetime.now().strftime('%H%M%S')}.mp4"
            st.session_state.bg_output = filename
            output_video.write_videofile(filename, codec=codec, audio_codec=audio_codec, logger=sl.StreamlitLogger(int(output_video.fps*output_video.duration)))
            st.success("✅ Merge Completed!")
            st.video(filename)
            with open(filename, "rb") as f:
                st.download_button("Download", f, file_name=filename)
            uf.close_and_remove(output_video, video, audio)

# ==============================
# Tool Dispatcher
# ==============================
tool_dispatch = {
    "Merge Audio with Video": merge_audio_with_video_ui,
    "Trim & Create Subclips": trim_video_ui,
    "Concatenate Videos": concatenate_videos_ui,
    "Add Background Music": add_background_music_ui
}

tool_dispatch[option]()

# ==============================
# Remove Uploaded Files Button
# ==============================
if st.button("Clear All"):
    remove_uploaded_files()

# Footer
st.write("---")
# Copyright (centered)
year = datetime.now().year
_, col, _ = st.columns([4, 2.5, 4])  # empty, center, empty
with col:
    st.caption(f"© {year} All rights reserved.")