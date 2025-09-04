import streamlit as st
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from datetime import datetime
import streamlit_logger as sl
import utility_functions as uf

# ==============================
# Streamlit Config
# ==============================
st.set_page_config(
    page_title="Professional Online Video Editor - Merge, Trim & Add Music", 
    page_icon="images/themes.png"
)
st.title("Professional Online Video Editor - Merge, Split & Add Music to Videos")
st.divider()

# ==============================
# Sidebar Settings
# ==============================
st.sidebar.header("⚙️ Video Editing Settings")
codec = st.sidebar.selectbox("Video Codec", ["libx264", "mpeg4", "libvpx"], index=0)
audio_codec = st.sidebar.selectbox("Audio Codec", ["aac", "libvorbis", "mp3"], index=0)

# ==============================
# Utility Functions
# ==============================
def cleanup_files(*files, new_keys={}):
    """Close clips, remove temp files, reset session_state keys, clear caches, and rerun UI"""
    for f in files:
        try:
            if f:
                f.close()
        except Exception:
            pass
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
# Tool Selection
# ==============================
option = st.radio(
    "Select Functionality",
    [
        "🎵 Merge Audio with Video Online",
        "✂️ Trim & Create Video Subclips",
        "🔗 Concatenate Multiple Videos Easily",
        "🎶 Add Background Music to Videos"
    ]
)

# ==============================
# Session Keys Configuration
# ==============================
tool_keys = {
    "🎵 Merge Audio with Video Online": {
        "video": "video_temp_merge",
        "audio": "audio_temp_merge",
        "output": "merge_output_filename",
        "video_key": "video_key_merge",
        "audio_key": "audio_key_merge"
    },
    "✂️ Trim & Create Video Subclips": {
        "video": "subclip_temp",
        "output": "subclip_output_filename",
        "key": "subclip_key"
    },
    "🔗 Concatenate Multiple Videos Easily": {
        "clips": "concat_clips",
        "files": "concat_temp_files",
        "output": "concat_output_filename",
        "key": "concat_key"
    },
    "🎶 Add Background Music to Videos": {
        "video": "video_temp_bg",
        "audio": "audio_temp_bg",
        "output": "bg_output_filename",
        "video_key": "video_key_bg",
        "audio_key": "audio_key_bg"
    }
}

# Initialize missing session_state keys
for key in tool_keys[option].values():
    if key not in st.session_state:
        if "clips" in key or "files" in key:
            st.session_state[key] = []
        elif "key" in key:
            st.session_state[key] = uf.generate_key(key)
        else:
            st.session_state[key] = None

# ==============================
# Function: Remove Uploaded Files Button
# ==============================
def remove_uploaded_files():
    keys = tool_keys[option]
    if option == "🔗 Concatenate Multiple Videos Easily":
        cleanup_files(
            *st.session_state.get(keys["clips"], []),
            *st.session_state.get(keys["files"], []),
            st.session_state.get(keys["output"]),
            new_keys={
                keys["clips"]: [],
                keys["files"]: [],
                keys["output"]: None,
                keys["key"]: uf.generate_key(keys["key"])
            }
        )
    else:
        cleanup_files(
            st.session_state.get(keys.get("video")),
            st.session_state.get(keys.get("audio")),
            st.session_state.get(keys.get("output")),
            new_keys={
                keys.get("video"): None,
                keys.get("audio"): None,
                keys.get("output"): None,
                keys.get("video_key"): uf.generate_key(keys.get("video_key")) if keys.get("video_key") else None,
                keys.get("audio_key"): uf.generate_key(keys.get("audio_key")) if keys.get("audio_key") else None,
                keys.get("key"): uf.generate_key(keys.get("key")) if keys.get("key") else None
            }
        )

# ==============================
# Tool Implementations
# ==============================

# ---------- Merge Audio ----------
if option == "🎵 Merge Audio with Video Online":
    merge_video_file = st.file_uploader("Upload Video", type=["mp4","mov","avi"], key=st.session_state.video_key_merge)
    merge_audio_file = st.file_uploader("Upload Audio", type=["mp3","wav"], key=st.session_state.audio_key_merge)

    if merge_video_file and merge_audio_file:
        st.session_state.video_temp = uf.save_temp_file(merge_video_file, ".mp4")
        st.session_state.audio_temp = uf.save_temp_file(merge_audio_file, ".mp3")
        video, audio = load_clips(st.session_state.video_temp, st.session_state.audio_temp)

        col1, col2 = st.columns(2)
        col1.success(f"🎥 Video: {merge_video_file.name} | ⏱ {video.duration:.2f}s")
        col2.success(f"🎵 Audio: {merge_audio_file.name} | ⏱ {audio.duration:.2f}s")

        if st.button("▶️ Merge Now"):
            cut_audio = audio.subclipped(0, min(audio.duration, video.duration))
            output_video = video.with_audio(cut_audio)
            output_filename = f"Merged__{datetime.now().strftime('%H%M%S')}.mp4"
            st.session_state.merge_output_filename = output_filename
            total_frames = int(output_video.fps * output_video.duration)
            output_video.write_videofile(output_filename, codec=codec, audio_codec=audio_codec, logger=sl.StreamlitLogger(total_frames))
            st.success("✅ Merge Completed!")
            st.video(output_filename)
            with open(output_filename, "rb") as f:
                st.download_button("⬇️ Download Merged Video", f, file_name=output_filename)
            uf.close_and_remove(output_video, video, audio)

    if st.button("❌ Remove Uploaded Files"):
        remove_uploaded_files()


# ---------- Trim & Subclip ----------
if option == "✂️ Trim & Create Video Subclips":
    subclip_video_file = st.file_uploader("Upload Video to Trim", type=["mp4","mov","avi"], key=st.session_state.subclip_key)
    if subclip_video_file:
        if not st.session_state.subclip_temp:
            st.session_state.subclip_temp = uf.save_temp_file(subclip_video_file, ".mp4")
        video, _ = load_clips(st.session_state.subclip_temp, None)
        st.success(f"🎥 Video: {subclip_video_file.name} | Duration: {video.duration:.2f}s")

        start = st.number_input("Start time (sec)", min_value=0.0, max_value=video.duration, value=0.0)
        end = st.number_input("End time (sec)", min_value=0.0, max_value=video.duration, value=min(5.0, video.duration))

        if st.button("✂️ Create Subclip"):
            if start < end:
                sub_clip = video.subclipped(start, end)
                sub_filename = f"Subclip_{int(start)}-{int(end)}_{datetime.now().strftime('%H%M%S')}.mp4"
                st.session_state.subclip_output_filename = sub_filename
                total_frames = int(sub_clip.fps * sub_clip.duration)
                sub_clip.write_videofile(sub_filename, codec=codec, audio_codec=audio_codec, logger=sl.StreamlitLogger(total_frames))
                st.success("✅ Subclip Created!")
                st.video(sub_filename)
                with open(sub_filename, "rb") as f:
                    st.download_button("⬇️ Download Subclip", f, file_name=sub_filename)
                sub_clip.close()
            else:
                st.error("❌ End time must be greater than start time")

    if st.button("❌ Remove Uploaded Subclip Video"):
        remove_uploaded_files()


# ---------- Concatenate Videos ----------
if option == "🔗 Concatenate Multiple Videos Easily":
    concat_files = st.file_uploader("Upload Videos to Concatenate", type=["mp4","mov","avi"], accept_multiple_files=True, key=st.session_state.concat_key)
    if concat_files:
        for i, file in enumerate(concat_files):
            if i >= len(st.session_state.concat_temp_files):
                temp_path = uf.save_temp_file(file, ".mp4")
                st.session_state.concat_temp_files.append(temp_path)
                clip = VideoFileClip(temp_path)
                st.session_state.concat_clips.append(clip)
            else:
                clip = st.session_state.concat_clips[i]
            st.info(f"📂 {file.name} | Duration: {clip.duration:.2f}s")

        if st.button("▶️ Concatenate Videos"):
            if st.session_state.concat_clips:
                final_clip = concatenate_videoclips(st.session_state.concat_clips)
                final_filename = f"Concat_{datetime.now().strftime('%H%M%S')}.mp4"
                st.session_state.concat_output_filename = final_filename
                total_frames = int(final_clip.fps * final_clip.duration)
                final_clip.write_videofile(final_filename, codec=codec, audio_codec=audio_codec, logger=sl.StreamlitLogger(total_frames))
                st.success("✅ Concatenation Completed!")
                st.video(final_filename)
                with open(final_filename, "rb") as f:
                    st.download_button("⬇️ Download Concatenated Video", f, file_name=final_filename)
                uf.close_and_remove(final_clip)

    if st.button("❌ Remove Uploaded Videos"):
        remove_uploaded_files()


# ---------- Add Background Music ----------
if option == "🎶 Add Background Music to Videos":
    merge_video_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"], key=st.session_state.video_key_bg)
    merge_audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav"], key=st.session_state.audio_key_bg)

    if merge_video_file and merge_audio_file:
        st.session_state.video_temp_bg = uf.save_temp_file(merge_video_file, ".mp4")
        st.session_state.audio_temp_bg = uf.save_temp_file(merge_audio_file, ".mp3")
        video, audio = load_clips(st.session_state.video_temp_bg, st.session_state.audio_temp_bg)

        col1, col2 = st.columns(2)
        col1.success(f"🎥 Video: {merge_video_file.name} | ⏱ {video.duration:.2f}s")
        col2.success(f"🎵 Audio: {merge_audio_file.name} | ⏱ {audio.duration:.2f}s")

        st.subheader("🎚 Volume Adjustment")
        original_volume = st.slider("🎙 Original Voice Volume", 0.0, 1.0, 1.0)
        music_volume = st.slider("🎵 Background Music Volume", 0.0, 1.0, 0.5)

        if st.button("▶️ Merge Now"):
            video_audio = video.audio.with_volume_scaled(original_volume) if video.audio else None
            cut_music = audio.subclipped(0, min(audio.duration, video.duration)).with_volume_scaled(music_volume)
            final_audio = CompositeAudioClip([video_audio, cut_music]) if video_audio else cut_music
            output_video = video.with_audio(final_audio)

            output_filename = f"Merged__{datetime.now().strftime('%H%M%S')}.mp4"
            st.session_state.bg_output_filename = output_filename
            total_frames = int(output_video.fps * output_video.duration)
            output_video.write_videofile(output_filename, codec=codec, audio_codec=audio_codec, logger=sl.StreamlitLogger(total_frames))
            st.success("✅ Merge Completed!")
            st.video(output_filename)
            with open(output_filename, "rb") as f:
                st.download_button("⬇️ Download Merged Video", f, file_name=output_filename)
            uf.close_and_remove(output_video, video, audio)

    if st.button("❌ Remove Uploaded Files"):
        remove_uploaded_files()
