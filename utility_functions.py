from random import randint
import tempfile
import streamlit as st

def save_temp_file(uploaded_file, suffix=".mp4"):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.read())
    tmp.close()
    return tmp.name

def close_and_remove(*clips):
    for clip in clips:
        try:
            if clip:
                clip.close()
        except Exception:
            pass


def remove_temp_files(*files):
    import os
    for file in files:
        try:
            if file and os.path.exists(file):
                os.remove(file)
        except Exception:
            pass


def generate_key(prefix):
    return f"{prefix}_{randint(0, 100000)}"
