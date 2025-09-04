import streamlit as st
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips,CompositeAudioClip
from datetime import datetime
import tempfile, os
from random import randint
from proglog import ProgressBarLogger

# ==============================
# Streamlit Config
# ==============================
st.set_page_config(page_title="Professional Video Editor", page_icon="🎬", layout="wide")
st.title("🎬 Merge, Subclip & Concatenate Videos")

# ==============================
# Sidebar Settings
# ==============================
st.sidebar.header("⚙️ Settings")
codec = st.sidebar.selectbox("Video Codec", ["libx264", "mpeg4", "libvpx"], index=0)
audio_codec = st.sidebar.selectbox("Audio Codec", ["aac", "libvorbis", "mp3"], index=0)


# Custom logger for Streamlit
class StreamlitLogger(ProgressBarLogger):
    def __init__(self, total_frames=None):
        super().__init__()
        self.progress_bar = st.progress(0)
        self.progress_text = st.empty()
        self.total_frames = total_frames

    def bars_callback(self, bar, attr, value, old_value=None):
        total = self.bars[bar]["total"]
        pct = int((value / total) * 100)

        if self.total_frames:
            self.progress_text.text(f"{bar.capitalize()} progress: {pct}% ({value}/{self.total_frames} frames)")
        else:
            self.progress_text.text(f"{bar} progress: {pct}%")

        self.progress_bar.progress(pct)
# ==============================
# Utility Functions
# ==============================
def save_temp_file(uploaded_file, suffix=".mp4"):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.read())
    tmp.close()
    return tmp.name

def close_and_remove(*clips):
    for clip in clips:
        try:
            clip.close()
        except:
            pass

def remove_temp_files(*paths):
    for path in paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except:
                pass

def generate_key(prefix):
    return f"{prefix}_{randint(0, 100000)}"


# ==============================
# Tabs
# ==============================
tab1, tab2, tab3,tab4 = st.tabs(["🎵 Merge Audio + Video", "✂️ Create Subclip", "🔗 Concatenate Videos","🎶 Add Background Music"])

# ==============================
# 1️⃣ Merge Audio + Video
# ==============================
with tab1:
    if "video_temp" not in st.session_state: st.session_state.video_temp = None
    if "audio_temp" not in st.session_state: st.session_state.audio_temp = None
    if "video_key" not in st.session_state: st.session_state.video_key = generate_key("video")
    if "audio_key" not in st.session_state: st.session_state.audio_key = generate_key("audio")

    merge_video_file = st.file_uploader("Upload Video", type=["mp4","mov","avi"], key=st.session_state.video_key)
    merge_audio_file = st.file_uploader("Upload Audio", type=["mp3","wav"], key=st.session_state.audio_key)

    if merge_video_file and merge_audio_file:
        st.session_state.video_temp = save_temp_file(merge_video_file, ".mp4")
        st.session_state.audio_temp = save_temp_file(merge_audio_file, ".mp3")

        video = VideoFileClip(st.session_state.video_temp)
        audio = AudioFileClip(st.session_state.audio_temp)

        col1, col2 = st.columns(2)
        col1.success(f"🎥 Video: {merge_video_file.name} | ⏱ {video.duration:.2f}s")
        col2.success(f"🎵 Audio: {merge_audio_file.name} | ⏱ {audio.duration:.2f}s")


        if st.button("▶️ Merge Now"):
            cut_audio = audio.subclipped(0, min(audio.duration, video.duration))
            output_video = video.with_audio(cut_audio)
            

            
            total_frames = int(output_video.fps * output_video.duration)
            logger = StreamlitLogger(total_frames)


            output_filename = f"Merged__{datetime.now().strftime('%H%M%S')}.mp4"
            output_video.write_videofile(output_filename, codec=codec, audio_codec=audio_codec,logger=logger)
            
            
            st.success("✅ Merge Completed!")
            st.video(output_filename)
            with open(output_filename,"rb") as f:
                st.download_button("⬇️ Download Merged Video", f, file_name=output_filename)
            close_and_remove(output_video, video, audio)

        if st.button("❌ Remove Uploaded Files"):
            close_and_remove(video, audio)
            remove_temp_files(st.session_state.video_temp, st.session_state.audio_temp)
            st.session_state.video_temp = None
            st.session_state.audio_temp = None
            st.session_state.video_key = generate_key("video")
            st.session_state.audio_key = generate_key("audio")
            st.rerun()

# ==============================
# 2️⃣ Create Subclip
# ==============================
with tab2:
    if "subclip_temp" not in st.session_state: st.session_state.subclip_temp = None
    if "subclip_key" not in st.session_state: st.session_state.subclip_key = generate_key("subclip")

    subclip_video_file = st.file_uploader("Upload Video to Trim", type=["mp4","mov","avi"], key=st.session_state.subclip_key)
    if subclip_video_file:
        if not st.session_state.subclip_temp:
            st.session_state.subclip_temp = save_temp_file(subclip_video_file, ".mp4")

        video = VideoFileClip(st.session_state.subclip_temp)
        st.success(f"🎥 Video: {subclip_video_file.name} | Duration: {video.duration:.2f}s")


        start = st.number_input("Start time (sec)", min_value=0.0, max_value=video.duration, value=0.0, key="sub_start")
        end = st.number_input("End time (sec)", min_value=0.0, max_value=video.duration, value=min(5.0, video.duration), key="sub_end")

        if st.button("✂️ Create Subclip"):
            if start < end:
                sub_clip = video.subclipped(start,end)

                total_frames = int(sub_clip.fps * sub_clip.duration)
                logger = StreamlitLogger(total_frames)

                sub_filename = f"Subclip_{int(start)}-{int(end)}_{datetime.now().strftime('%H%M%S')}.mp4"
                sub_clip.write_videofile(sub_filename, codec=codec, audio_codec=audio_codec,logger=logger)
                st.success("✅ Subclip Created!")
                st.video(sub_filename)
                with open(sub_filename,"rb") as f:
                    st.download_button("⬇️ Download Subclip", f, file_name=sub_filename)
                sub_clip.close()
            else:
                st.error("❌ End time must be greater than start time")

        if st.button("❌ Remove Uploaded Subclip Video"):
            try: video.close()
            except: pass
            remove_temp_files(st.session_state.subclip_temp)
            st.session_state.subclip_temp = None
            st.session_state.subclip_key = generate_key("subclip")
            st.rerun()

# ==============================
# 3️⃣ Concatenate Videos
# ==============================
with tab3:
    if "concat_temp_files" not in st.session_state: st.session_state.concat_temp_files = []
    if "concat_clips" not in st.session_state: st.session_state.concat_clips = []
    if "concat_key" not in st.session_state: st.session_state.concat_key = generate_key("concat")

    concat_files = st.file_uploader("Upload Videos to Concatenate", type=["mp4","mov","avi"], accept_multiple_files=True, key=st.session_state.concat_key)

    if concat_files:
        for i,file in enumerate(concat_files):
            if i >= len(st.session_state.concat_temp_files):
                temp_path = save_temp_file(file, ".mp4")
                st.session_state.concat_temp_files.append(temp_path)
                clip = VideoFileClip(temp_path)
                st.session_state.concat_clips.append(clip)
            else:
                clip = st.session_state.concat_clips[i]

            st.info(f"📂 {file.name} | Duration: {clip.duration:.2f}s")

        if st.button("▶️ Concatenate Videos"):
            final_clip = concatenate_videoclips(st.session_state.concat_clips)

            total_frames = int(final_clip.fps * final_clip.duration)
            logger = StreamlitLogger(total_frames)
            

            final_filename = f"Concat_{datetime.now().strftime('%H%M%S')}.mp4"
            final_clip.write_videofile(final_filename, codec=codec, audio_codec=audio_codec,logger=logger)
            st.success("✅ Concatenation Completed!")
            st.video(final_filename)
            with open(final_filename,"rb") as f:
                st.download_button("⬇️ Download Concatenated Video", f, file_name=final_filename)
            close_and_remove(final_clip)

        if st.button("❌ Remove Uploaded Videos"):
            close_and_remove(*st.session_state.concat_clips)
            remove_temp_files(*st.session_state.concat_temp_files)
            st.session_state.concat_clips = []
            st.session_state.concat_temp_files = []
            st.session_state.concat_key = generate_key("concat")
            st.rerun()
# ==============================
#4️⃣ Add Background Music (Keep Original + Music)
# ==============================
with tab4:
    if "video_background_temp" not in st.session_state: st.session_state.video_background_temp = None
    if "audio_background_temp" not in st.session_state: st.session_state.audio_background_temp = None
    if "video_background_key" not in st.session_state: st.session_state.video_background_key = generate_key("video_background")
    if "audio_background_key" not in st.session_state: st.session_state.audio_background_key = generate_key("audio_background")

    merge_video_file = st.file_uploader("Upload Video", type=["mp4","mov","avi"], key=st.session_state.video_background_key)
    merge_audio_file = st.file_uploader("Upload Audio", type=["mp3","wav"], key=st.session_state.audio_background_key)

    if merge_video_file and merge_audio_file:
        st.session_state.video_temp = save_temp_file(merge_video_file, ".mp4")
        st.session_state.audio_temp = save_temp_file(merge_audio_file, ".mp3")

        video = VideoFileClip(st.session_state.video_temp)
        audio = AudioFileClip(st.session_state.audio_temp)

        col1, col2 = st.columns(2)
        col1.success(f"🎥 Video: {merge_video_file.name} | ⏱ {video.duration:.2f}s")
        col2.success(f"🎵 Audio: {merge_audio_file.name} | ⏱ {audio.duration:.2f}s")

        # ==============================
        # Volume Adjustment (Main Panel)
        # ==============================
        st.subheader("🎚 Volume Adjustment")
        original_volume = st.slider("🎙 Original Voice Volume", 0.0, 1.0, 1.0)
        music_volume = st.slider("🎵 Background Music Volume", 0.0, 1.0, 0.5)

        if st.button("▶️ Merge Now"):
            # Adjust volumes
            video_audio = video.audio.with_volume_scaled(original_volume) if video.audio else None
            cut_music = audio.subclipped(0, min(audio.duration, video.duration)).with_volume_scaled(music_volume)

            # Combine audios
            if video_audio:
                final_audio = CompositeAudioClip([video_audio, cut_music])
            else:
                final_audio = cut_music

            output_video = video.with_audio(final_audio)

            # Save final video
            total_frames = int(output_video.fps * output_video.duration)
            logger = StreamlitLogger(total_frames)
            output_filename = f"Merged__{datetime.now().strftime('%H%M%S')}.mp4"

            output_video.write_videofile(output_filename, codec=codec, audio_codec=audio_codec, logger=logger)

            st.success("✅ Merge Completed!")
            st.video(output_filename)

            with open(output_filename, "rb") as f:
                st.download_button("⬇️ Download Merged Video", f, file_name=output_filename)

            close_and_remove(output_video, video, audio)

        if st.button("❌ Remove Uploaded Files"):
            close_and_remove(video, audio)
            remove_temp_files(st.session_state.video_temp, st.session_state.audio_temp)
            st.session_state.video_background_temp = None
            st.session_state.audio_background_temp = None
            st.session_state.video_background_key = generate_key("video_background")
            st.session_state.audio_background_key = generate_key("audio_background")
            st.rerun()

