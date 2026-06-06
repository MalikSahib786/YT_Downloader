import streamlit as st
import yt_dlp
from pathlib import Path
import tempfile
import os

st.set_page_config(page_title="YT Downloader", layout="centered")

st.title("🎬 Unlimited Free Video Downloader")
st.caption("Powered by yt-dlp — supports YouTube, TikTok, Instagram, Twitter, and 1800+ sites")

# URL Input
url = st.text_input("Paste video URL:", placeholder="https://youtube.com/watch?v=...")

# Format Selection
col1, col2 = st.columns(2)
with col1:
    quality = st.selectbox("Quality:", [
        "Best Available",
        "1080p",
        "720p", 
        "480p",
        "Audio Only (MP3)"
    ])
with col2:
    format_type = st.selectbox("Format:", ["MP4", "MP3", "WEBM"])

# Progress tracking
progress_bar = st.progress(0)
status_text = st.empty()

def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%','')
        try:
            progress_bar.progress(int(float(p))/100)
        except:
            pass
        status_text.text(f"Downloading: {d.get('_speed_str', 'N/A')}")

if st.button("Download", type="primary") and url:
    with st.spinner("Fetching video info..."):
        try:
            # Get info first
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                
            st.image(info['thumbnail'], width=300)
            st.write(f"**Title:** {info['title']}")
            st.write(f"**Channel:** {info['uploader']}")
            st.write(f"**Duration:** {info['duration']} seconds")
            
            # Map quality to format string
            format_map = {
                "Best Available": "bestvideo+bestaudio/best",
                "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
                "Audio Only (MP3)": "bestaudio/best"
            }
            
            selected_format = format_map[quality]
            
            # Setup download options
            ydl_opts = {
                'format': selected_format,
                'outtmpl': '%(title)s.%(ext)s',
                'progress_hooks': [progress_hook],
                'merge_output_format': 'mp4' if format_type == 'MP4' else None,
            }
            
            # Add audio postprocessor if MP3
            if quality == "Audio Only (MP3)":
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            # Download to temp directory
            with tempfile.TemporaryDirectory() as tmpdir:
                ydl_opts['outtmpl'] = os.path.join(tmpdir, '%(title)s.%(ext)s')
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Find downloaded file
                files = os.listdir(tmpdir)
                if files:
                    file_path = os.path.join(tmpdir, files[0])
                    with open(file_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ Download File",
                            data=f,
                            file_name=files[0],
                            mime="video/mp4"
                        )
                    st.success("Ready! Click above to download.")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
