
import streamlit as st
import yt_dlp
import os
import tempfile
import subprocess
from io import BytesIO
from pathlib import Path
import time

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YT Downloader Pro",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS — Dark, polished UI
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FF4B4B, #FF8F4B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }

    .sub-header {
        color: #9ca3af;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    .stTextInput > div > div > input {
        background-color: #1f2937;
        color: #f3f4f6;
        border: 1px solid #374151;
        border-radius: 8px;
    }

    .stSelectbox > div > div > div {
        background-color: #1f2937;
        color: #f3f4f6;
        border: 1px solid #374151;
        border-radius: 8px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #FF4B4B, #FF8F4B) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        height: 2.8em !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.4);
    }

    .info-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
    }

    .error-card {
        background-color: #3d1f1f;
        border-left: 4px solid #ef4444;
        border-radius: 6px;
        padding: 1rem;
        color: #fca5a5;
    }

    .success-card {
        background-color: #1f3d2a;
        border-left: 4px solid #22c55e;
        border-radius: 6px;
        padding: 1rem;
        color: #86efac;
    }

    .warning-card {
        background-color: #3d3a1f;
        border-left: 4px solid #eab308;
        border-radius: 6px;
        padding: 1rem;
        color: #fde047;
        font-size: 0.85rem;
    }

    .metric-box {
        background-color: #1f2937;
        border-radius: 8px;
        padding: 0.8rem;
        text-align: center;
    }

    .metric-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f3f4f6;
    }

    .metric-label {
        font-size: 0.75rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def check_ffmpeg():
    """Check if ffmpeg is installed and available in PATH."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False

@st.cache_data(ttl=300, show_spinner=False)
def get_video_info(url):
    """Fetch video metadata without downloading."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        # Anti-403 measures for info extraction too
        'extractor_args': {
            'youtube': {
                'player_js_version': 'actual',
                'player_client': 'web_safari',
            }
        },
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.youtube.com/',
        },
        'geo_bypass': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'uploader': info.get('uploader', info.get('channel', 'Unknown')),
                'duration': info.get('duration') or 0,
                'thumbnail': info.get('thumbnail', ''),
                'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
                'view_count': info.get('view_count') or 0,
                'like_count': info.get('like_count') or 0,
                'upload_date': info.get('upload_date', ''),
                'formats': info.get('formats', []),
                'ext': info.get('ext', 'mp4'),
                'filesize_approx': info.get('filesize_approx') or 0,
            }
    except Exception as e:
        return {'error': str(e)}

def format_duration(seconds):
    if not seconds:
        return "N/A"
    mins, secs = divmod(int(seconds), 60)
    hrs, mins = divmod(mins, 60)
    if hrs:
        return f"{hrs}:{mins:02d}:{secs:02d}"
    return f"{mins}:{secs:02d}"

def format_size(bytes_val):
    if not bytes_val:
        return "Unknown"
    bytes_val = float(bytes_val)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} TB"

def format_count(num):
    """Safely format large numbers (views, likes)."""
    if not num:
        return "0"
    num = float(num)
    if num >= 1e9:
        return f"{num/1e9:.1f}B"
    if num >= 1e6:
        return f"{num/1e6:.1f}M"
    if num >= 1e3:
        return f"{num/1e3:.1f}K"
    return f"{int(num)}"

def get_format_string(quality, mode, ffmpeg_available):
    """
    Build yt-dlp format string based on quality, mode, and ffmpeg availability.
    If ffmpeg is missing, we use pre-merged formats to avoid the merge error.
    """
    if mode == "Audio Only":
        if ffmpeg_available:
            return "bestaudio/best"
        else:
            return "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio"

    height_map = {
        "Best": None,
        "4K (2160p)": 2160,
        "1440p": 1440,
        "1080p": 1080,
        "720p": 720,
        "480p": 480,
        "360p": 360,
    }
    height = height_map.get(quality)

    if ffmpeg_available:
        if height:
            return f"bestvideo[height<={height}][vcodec!*=av01]+bestaudio[acodec!*=opus]/bestvideo[height<={height}]+bestaudio/best[height<={height}]"
        else:
            return "bestvideo[vcodec!*=av01]+bestaudio[acodec!*=opus]/bestvideo+bestaudio/best"
    else:
        if height:
            return f"best[height<={height}][ext=mp4]/best[height<={height}][ext=webm]/best[height<={height}]"
        else:
            return "best[ext=mp4]/best[ext=webm]/best"

def build_ydl_opts(format_string, output_path, progress_hook, ffmpeg_available, mode):
    """Build yt-dlp options dict with full anti-403 protection."""
    ydl_opts = {
        'format': format_string,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'noplaylist': True,
        'retries': 10,
        'fragment_retries': 10,
        'continue_dl': True,
        'quiet': True,
        'no_warnings': False,

        # ─── ANTI-403 FIXES ───
        'extractor_args': {
            'youtube': {
                'player_js_version': 'actual',
                'player_client': 'web_safari',
            }
        },
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.youtube.com/',
        },
        'geo_bypass': True,
    }

    if ffmpeg_available and mode == "Audio Only":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        ydl_opts['merge_output_format'] = None
    elif ffmpeg_available and mode != "Audio Only":
        ydl_opts['merge_output_format'] = 'mp4'

    return ydl_opts

# ─────────────────────────────────────────────────────────────
# UI HEADER
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🎬 YT Downloader Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by yt-dlp • Supports 1800+ sites • Unlimited & Free</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR INFO
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ System Status")
    ffmpeg_ok = check_ffmpeg()
    if ffmpeg_ok:
        st.success("✅ FFmpeg detected — High quality merging enabled")
    else:
        st.warning("⚠️ FFmpeg missing — Using pre-merged formats (lower quality fallback)")
        st.info("Add `packages.txt` with `ffmpeg` to your repo to fix this.")

    st.markdown("---")
    st.markdown("### 📋 Required Files")
    st.code("""requirements.txt:
streamlit
yt-dlp

packages.txt:
ffmpeg""", language="text")

    st.markdown("---")
    st.markdown("### 🛡️ Legal Note")
    st.caption("Only download content you own or have rights to. Respect copyright laws.")

    st.markdown("---")
    st.markdown("### 🔒 Anti-Bot Status")
    st.caption("Anti-403 measures active: player_js_version=actual + Safari client + realistic headers")

# ─────────────────────────────────────────────────────────────
# MAIN INPUT AREA
# ─────────────────────────────────────────────────────────────
with st.container():
    url = st.text_input(
        "🔗 Paste Video URL:",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        mode = st.selectbox("Mode:", ["Video", "Audio Only"], index=0)
    with col2:
        if mode == "Video":
            quality = st.selectbox(
                "Quality:",
                ["Best", "4K (2160p)", "1440p", "1080p", "720p", "480p", "360p"],
                index=4
            )
        else:
            quality = st.selectbox("Quality:", ["Best", "192kbps", "128kbps"], index=0)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        download_clicked = st.button("⬇️ Download", use_container_width=True)

# ─────────────────────────────────────────────────────────────
# VIDEO PREVIEW & DOWNLOAD LOGIC
# ─────────────────────────────────────────────────────────────
if url and (download_clicked or 'info' in st.session_state):

    # Fetch info if not cached in session
    if 'info' not in st.session_state or st.session_state.get('url') != url:
        with st.spinner("🔍 Fetching video info..."):
            info = get_video_info(url)
            if 'error' in info:
                st.markdown(f'<div class="error-card">❌ Failed to fetch info: {info["error"]}</div>', unsafe_allow_html=True)
                st.stop()
            st.session_state['info'] = info
            st.session_state['url'] = url
    else:
        info = st.session_state['info']

    # ─── PREVIEW CARD ───
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)

    prev_col1, prev_col2 = st.columns([1, 2])
    with prev_col1:
        if info.get('thumbnail'):
            st.image(info['thumbnail'], use_container_width=True)
    with prev_col2:
        st.markdown(f"**{info['title']}**")
        st.markdown(f"👤 {info['uploader']}  •  ⏱ {format_duration(info['duration'])}")

        meta_cols = st.columns(3)
        with meta_cols[0]:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{format_size(info.get("filesize_approx"))}</div><div class="metric-label">Est. Size</div></div>', unsafe_allow_html=True)
        with meta_cols[1]:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{format_count(info.get("view_count"))}</div><div class="metric-label">Views</div></div>', unsafe_allow_html=True)
        with meta_cols[2]:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{format_count(info.get("like_count"))}</div><div class="metric-label">Likes</div></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # FFmpeg warning if not available
    if not ffmpeg_ok and mode == "Video":
        st.markdown(
            '<div class="warning-card">⚠️ <b>FFmpeg not detected on server.</b> '
            'Falling back to pre-merged formats. Video quality may be lower than selected. '
            'Add a <code>packages.txt</code> file with <code>ffmpeg</code> to your repo for full quality.</div>',
            unsafe_allow_html=True
        )

    # ─── DOWNLOAD EXECUTION ───
    if download_clicked:
        progress_bar = st.progress(0, text="Initializing download...")
        status_text = st.empty()

        download_error = None
        file_bytes = None
        file_name = None
        mime_type = "video/mp4"

        def progress_hook(d):
            if d['status'] == 'downloading':
                p = d.get('_percent_str', '0%').replace('%', '').strip()
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                try:
                    progress_bar.progress(min(int(float(p)), 100), text=f"⬇️ Downloading... {speed} (ETA: {eta})")
                except (ValueError, TypeError):
                    pass
                status_text.text(f"Speed: {speed} | ETA: {eta}")
            elif d['status'] == 'finished':
                progress_bar.progress(100, text="✅ Download complete! Processing...")
                status_text.text("Finalizing file...")

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                format_str = get_format_string(quality, mode, ffmpeg_ok)

                ydl_opts = build_ydl_opts(format_str, tmpdir, progress_hook, ffmpeg_ok, mode)

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # Find the downloaded file
                files = [f for f in os.listdir(tmpdir) if os.path.isfile(os.path.join(tmpdir, f))]
                if not files:
                    raise Exception("Download completed but no file found.")

                file_name = files[0]
                file_path = os.path.join(tmpdir, file_name)

                # Determine MIME type
                if file_name.endswith('.mp3'):
                    mime_type = "audio/mpeg"
                elif file_name.endswith('.webm'):
                    mime_type = "video/webm"
                elif file_name.endswith('.m4a'):
                    mime_type = "audio/mp4"
                else:
                    mime_type = "video/mp4"

                # Read file into memory (required for Streamlit download button)
                file_size = os.path.getsize(file_path)
                if file_size > 500 * 1024 * 1024:  # 500MB
                    st.warning("⚠️ File is larger than 500MB. Streamlit Cloud may struggle with large files.")

                with open(file_path, 'rb') as f:
                    file_bytes = f.read()

        except Exception as e:
            download_error = str(e)

        # Clear progress UI
        progress_bar.empty()
        status_text.empty()

        if download_error:
            st.markdown(f'<div class="error-card">❌ Download failed: {download_error}</div>', unsafe_allow_html=True)

            # Specific guidance for 403 errors
            if "403" in download_error or "forbidden" in download_error.lower():
                st.error("""
                **YouTube 403 Block Detected!**

                YouTube is blocking this cloud server's IP address. This is common on AWS/Google Cloud (Streamlit Cloud).

                **Try these fixes:**
                1. **Retry** — Sometimes it works on the 2nd or 3rd attempt
                2. **Lower the quality** — 360p/480p is less likely to be blocked than 1080p/4K
                3. **Try Audio Only mode** — Audio streams are less aggressively blocked
                4. **Use a different video** — Some videos are more restricted than others
                5. **Run locally** — This app works perfectly on your local machine where YouTube sees a residential IP

                The anti-403 measures (player_js_version=actual + Safari client) are already active in this app.
                """)
            elif "ffmpeg is not installed" in download_error.lower() or "merging" in download_error.lower():
                st.error("""
                **FFmpeg Missing Error Detected!**

                To fix this on Streamlit Cloud:
                1. Create a file named `packages.txt` in your repo root
                2. Add one line: `ffmpeg`
                3. Re-deploy the app
                """)
        elif file_bytes:
            st.markdown(
                f'<div class="success-card">✅ <b>Ready!</b> {file_name} ({format_size(len(file_bytes))})</div>',
                unsafe_allow_html=True
            )

            st.download_button(
                label="📥 Click to Download File",
                data=file_bytes,
                file_name=file_name,
                mime=mime_type,
                use_container_width=True,
                key=f"dl_{int(time.time())}"
            )

            st.caption("💡 The file is served directly from memory. No external storage used.")

st.markdown('<div class="footer">Built with Streamlit + yt-dlp • Free & Open Source</div>', unsafe_allow_html=True)
