
import streamlit as st
import yt_dlp
import os
import tempfile
import subprocess
from io import BytesIO
from pathlib import Path
import time
import hashlib

# PAGE CONFIG
st.set_page_config(
    page_title="Universal Downloader Pro",
    page_icon="arrow_down",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CUSTOM CSS - Ultra Professional Dark Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .app-header {
        text-align: center; padding: 1.5rem 0 0.5rem;
    }
    .app-logo {
        font-size: 2.6rem; font-weight: 800;
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8F4B 40%, #FFD93D 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em; margin-bottom: 0.3rem;
    }
    .app-tagline {
        color: #6b7280; font-size: 0.85rem; font-weight: 400;
        letter-spacing: 0.02em;
    }
    .app-divider {
        height: 1px; background: linear-gradient(90deg, transparent, #374151, transparent);
        margin: 1rem 0 1.5rem;
    }

    .stTextInput > div > div > input {
        background-color: #1f2937; color: #f3f4f6;
        border: 1.5px solid #374151; border-radius: 12px;
        font-size: 0.95rem; padding: 0.7rem 1rem;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FF8F4B;
        box-shadow: 0 0 0 3px rgba(255, 143, 75, 0.15);
    }

    .stSelectbox > div > div > div {
        background-color: #1f2937; color: #f3f4f6;
        border: 1.5px solid #374151; border-radius: 10px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8F4B 100%) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; height: 2.8em !important;
        font-weight: 700 !important; font-size: 1rem !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.45) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    .preview-card {
        background: linear-gradient(145deg, #111827 0%, #0f172a 100%);
        border: 1px solid #1f2937; border-radius: 16px;
        padding: 1.5rem; margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        animation: fadeIn 0.4s ease-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .error-card {
        background: linear-gradient(145deg, #3d1f1f 0%, #2d1a1a 100%);
        border-left: 4px solid #ef4444; border-radius: 10px;
        padding: 1rem 1.2rem; color: #fca5a5;
        animation: fadeIn 0.3s ease-out;
    }
    .success-card {
        background: linear-gradient(145deg, #1f3d2a 0%, #1a3322 100%);
        border-left: 4px solid #22c55e; border-radius: 10px;
        padding: 1rem 1.2rem; color: #86efac;
        animation: fadeIn 0.3s ease-out;
    }
    .warning-card {
        background: linear-gradient(145deg, #3d3a1f 0%, #2d2b16 100%);
        border-left: 4px solid #eab308; border-radius: 10px;
        padding: 1rem 1.2rem; color: #fde047; font-size: 0.85rem;
    }
    .tip-card {
        background: linear-gradient(145deg, #1f2937 0%, #18212f 100%);
        border: 1px solid #374151; border-radius: 10px;
        padding: 1rem 1.2rem; margin: 0.5rem 0;
        color: #d1d5db; font-size: 0.88rem; line-height: 1.6;
    }

    .metric-box {
        background: linear-gradient(145deg, #1f2937 0%, #18212f 100%);
        border-radius: 12px; padding: 1rem 0.5rem;
        text-align: center; border: 1px solid #374151;
        transition: all 0.2s;
    }
    .metric-box:hover { transform: translateY(-2px); border-color: #4b5563; }
    .metric-value { font-size: 1.2rem; font-weight: 700; color: #f3f4f6; }
    .metric-label { font-size: 0.68rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 0.3rem; }

    .shimmer-wrapper {
        background: linear-gradient(145deg, #111827 0%, #0f172a 100%);
        border: 1px solid #1f2937; border-radius: 16px;
        padding: 1.5rem; margin: 1rem 0;
        animation: fadeIn 0.3s ease-out;
    }
    .shimmer-flex { display: flex; gap: 1.2rem; align-items: flex-start; }
    .shimmer-thumb {
        width: 180px; height: 100px; border-radius: 12px; flex-shrink: 0;
        background: linear-gradient(90deg, #1f2937 25%, #374151 50%, #1f2937 75%);
        background-size: 200% 100%; animation: shimmer 1.6s infinite;
    }
    .shimmer-body { flex: 1; }
    .shimmer-line {
        height: 14px; border-radius: 6px; margin-bottom: 12px;
        background: linear-gradient(90deg, #1f2937 25%, #374151 50%, #1f2937 75%);
        background-size: 200% 100%; animation: shimmer 1.6s infinite;
    }
    .shimmer-line.title { width: 85%; height: 18px; }
    .shimmer-line.meta { width: 50%; height: 12px; }
    .shimmer-metrics { display: flex; gap: 0.8rem; margin-top: 1.2rem; }
    .shimmer-metric {
        flex: 1; height: 65px; border-radius: 12px;
        background: linear-gradient(90deg, #1f2937 25%, #374151 50%, #1f2937 75%);
        background-size: 200% 100%; animation: shimmer 1.6s infinite;
    }
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    .live-indicator {
        display: inline-flex; align-items: center; gap: 6px;
        color: #22c55e; font-size: 0.85rem; font-weight: 500;
        margin-bottom: 0.8rem;
    }
    .live-dot {
        width: 8px; height: 8px; background: #22c55e;
        border-radius: 50%; animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(1.3); }
    }

    .site-badge {
        display: inline-flex; align-items: center; gap: 4px;
        background: rgba(255,143,75,0.12); color: #FF8F4B;
        padding: 3px 10px; border-radius: 20px;
        font-size: 0.72rem; font-weight: 600;
        border: 1px solid rgba(255,143,75,0.25);
        text-transform: uppercase; letter-spacing: 0.04em;
    }
    .type-badge {
        display: inline-flex; align-items: center; gap: 4px;
        background: rgba(34,197,94,0.12); color: #22c55e;
        padding: 3px 10px; border-radius: 20px;
        font-size: 0.72rem; font-weight: 600;
        border: 1px solid rgba(34,197,94,0.25);
        text-transform: uppercase; letter-spacing: 0.04em;
        margin-left: 6px;
    }

    .app-footer {
        text-align: center; color: #4b5563;
        font-size: 0.78rem; margin-top: 3rem;
        padding: 1.5rem 0; border-top: 1px solid #1f2937;
    }

    code { background-color: #374151; padding: 2px 6px; border-radius: 4px; color: #fbbf24; font-size: 0.85em; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def check_ffmpeg():
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except Exception:
        return False

def get_base_ydl_opts():
    opts = {
        'quiet': True, 'no_warnings': True,
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
    return opts

def fetch_video_info(url):
    ydl_opts = get_base_ydl_opts()
    ydl_opts['skip_download'] = True
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            has_height = any(f.get('height') and f.get('height') > 0 for f in formats)
            has_video = any(f.get('vcodec') != 'none' for f in formats)
            has_audio = any(f.get('acodec') != 'none' for f in formats)
            has_image = any(f.get('ext') in ('jpg', 'jpeg', 'png', 'webp') for f in formats) or info.get('ext') in ('jpg', 'jpeg', 'png', 'webp')

            extractor = info.get('extractor', 'generic').lower()
            is_youtube = 'youtube' in extractor
            is_instagram = 'instagram' in extractor
            is_facebook = 'facebook' in extractor
            is_tiktok = 'tiktok' in extractor
            is_twitter = 'twitter' in extractor

            content_type = 'video'
            if has_image and not has_video:
                content_type = 'photo'
            elif not has_video and not has_audio and not has_image:
                entries = info.get('entries', [])
                if entries:
                    content_type = 'gallery'

            return {
                'title': info.get('title', 'Unknown'),
                'uploader': info.get('uploader', info.get('channel', info.get('uploader_id', 'Unknown'))),
                'duration': info.get('duration') or 0,
                'thumbnail': info.get('thumbnail', ''),
                'description': info.get('description', '')[:250] + '...' if info.get('description') else '',
                'view_count': info.get('view_count') or 0,
                'like_count': info.get('like_count') or 0,
                'upload_date': info.get('upload_date', ''),
                'formats': formats,
                'ext': info.get('ext', 'mp4'),
                'filesize_approx': info.get('filesize_approx') or 0,
                'extractor': extractor,
                'is_youtube': is_youtube,
                'is_instagram': is_instagram,
                'is_facebook': is_facebook,
                'is_tiktok': is_tiktok,
                'is_twitter': is_twitter,
                'has_height_formats': has_height,
                'has_video': has_video,
                'has_audio': has_audio,
                'has_image': has_image,
                'content_type': content_type,
                'entries': info.get('entries', []),
                'success': True,
            }
    except Exception as e:
        return {'error': str(e), 'success': False}

def format_duration(seconds):
    if not seconds: return "N/A"
    mins, secs = divmod(int(seconds), 60)
    hrs, mins = divmod(mins, 60)
    if hrs: return f"{hrs}:{mins:02d}:{secs:02d}"
    return f"{mins}:{secs:02d}"

def format_size(bytes_val):
    if not bytes_val: return "Unknown"
    bytes_val = float(bytes_val)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024: return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} TB"

def format_count(num):
    if not num: return "0"
    num = float(num)
    if num >= 1e9: return f"{num/1e9:.1f}B"
    if num >= 1e6: return f"{num/1e6:.1f}M"
    if num >= 1e3: return f"{num/1e3:.1f}K"
    return f"{int(num)}"

def sanitize_filename(title, max_len=80):
    """Sanitize and truncate filename to prevent 'File name too long' errors."""
    if not title:
        title = "download"
    # Remove/replace invalid chars
    sanitized = "".join(c if c.isalnum() or c in " ._-" else "_" for c in title)
    sanitized = sanitized.strip("._")
    # Truncate if too long
    if len(sanitized) > max_len:
        # Create short hash for uniqueness
        short_hash = hashlib.md5(sanitized.encode()).hexdigest()[:6]
        sanitized = sanitized[:max_len-7] + "_" + short_hash
    return sanitized or "download"

def get_format_string(quality, mode, ffmpeg_available, info):
    content_type = info.get('content_type', 'video')
    is_youtube = info.get('is_youtube', False)
    has_height = info.get('has_height_formats', False)

    if content_type == 'photo':
        return "best"

    if mode == "Audio Only":
        if ffmpeg_available: return "bestaudio/best"
        return "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio"

    if not is_youtube or not has_height:
        return "best/bestvideo+bestaudio"

    height_map = {"Best": None, "4K (2160p)": 2160, "1440p": 1440, "1080p": 1080, "720p": 720, "480p": 480, "360p": 360}
    target_height = height_map.get(quality)

    if ffmpeg_available:
        if target_height:
            return f"bestvideo[height<={target_height}][vcodec!*=av01]+bestaudio[acodec!*=opus]/bestvideo[height<={target_height}]+bestaudio/best[height<={target_height}]"
        return "bestvideo[vcodec!*=av01]+bestaudio[acodec!*=opus]/bestvideo+bestaudio/best"
    else:
        if target_height:
            return f"best[height<={target_height}]/best"
        return "best/bestvideo+bestaudio"

def build_ydl_opts(format_string, output_path, progress_hook, ffmpeg_available, mode, info):
    ydl_opts = get_base_ydl_opts()

    # FIX: Use sanitized short filename to prevent "File name too long" errors
    safe_title = sanitize_filename(info.get('title', 'download'))

    ydl_opts.update({
        'format': format_string,
        'outtmpl': os.path.join(output_path, f'{safe_title}.%(ext)s'),
        'progress_hooks': [progress_hook],
        'noplaylist': True,
        'retries': 10, 'fragment_retries': 10,
        'continue_dl': True,
    })

    content_type = info.get('content_type', 'video')

    if content_type == 'photo':
        if info.get('entries'):
            ydl_opts['noplaylist'] = False
    elif ffmpeg_available and mode == "Audio Only":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    elif ffmpeg_available and mode != "Audio Only":
        if '+' in format_string:
            ydl_opts['merge_output_format'] = 'mp4'

    return ydl_opts

def get_site_name(extractor):
    mapping = {
        'youtube': 'YouTube',
        'instagram': 'Instagram',
        'facebook': 'Facebook',
        'tiktok': 'TikTok',
        'twitter': 'Twitter/X',
        'reddit': 'Reddit',
        'vimeo': 'Vimeo',
    }
    for key, name in mapping.items():
        if key in extractor:
            return name
    return extractor.replace('ie', '').title()

def get_content_icon(content_type):
    icons = {'video': 'film', 'photo': 'image', 'gallery': 'images', 'audio': 'music'}
    return icons.get(content_type, 'file')

# SESSION STATE INIT
if 'last_url' not in st.session_state:
    st.session_state.last_url = ''
if 'video_info' not in st.session_state:
    st.session_state.video_info = None
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False
if 'download_error' not in st.session_state:
    st.session_state.download_error = None
if 'clear_trigger' not in st.session_state:
    st.session_state.clear_trigger = 0

# HEADER
st.markdown("""
<div class="app-header">
    <div class="app-logo">Universal Downloader</div>
    <div class="app-tagline">Videos | Photos | Reels | Posts | Stories | 1800+ Sites</div>
</div>
<div class="app-divider"></div>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### System Status")
    ffmpeg_ok = check_ffmpeg()
    if ffmpeg_ok: st.success("FFmpeg detected")
    else: st.warning("FFmpeg missing")

    st.markdown("---")
    st.markdown("### Required Files")
    st.code("""requirements.txt:
streamlit
yt-dlp

packages.txt:
ffmpeg""", language="text")

    st.markdown("---")
    st.markdown("### Legal Note")
    st.caption("Only download content you own or have rights to.")

# INPUT BAR WITH PASTE & CLEAR BUTTONS
col_input, col_paste, col_clear = st.columns([6, 1, 1])

with col_input:
    input_key = "url_input_" + str(st.session_state.clear_trigger)
    url = st.text_input(
        "", placeholder="Paste any URL here...",
        label_visibility="collapsed", key=input_key
    )

with col_paste:
    st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)
    if st.button("Paste", help="Paste from clipboard", key="paste_btn", use_container_width=True):
        try:
            import pyperclip
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                st.session_state.pasted_url = clipboard_text
                st.rerun()
        except:
            st.toast("Paste from clipboard manually", icon="warning")

with col_clear:
    st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)
    if st.button("Clear", help="Clear URL", key="clear_btn", use_container_width=True):
        st.session_state.last_url = ''
        st.session_state.video_info = None
        st.session_state.clear_trigger += 1
        st.rerun()

if 'pasted_url' in st.session_state:
    url = st.session_state.pasted_url
    del st.session_state.pasted_url

# MODE & QUALITY SELECTION
col_mode, col_quality, col_download = st.columns([2, 2, 1])

with col_mode:
    mode = st.selectbox("Type:", ["Auto Detect", "Video", "Audio Only", "Photo/Gallery"], index=0)

with col_quality:
    if mode == "Audio Only":
        quality = st.selectbox("Quality:", ["Best", "192kbps", "128kbps"], index=0)
    elif mode == "Photo/Gallery":
        quality = st.selectbox("Quality:", ["Best", "Original", "High", "Medium"], index=0)
    else:
        quality = st.selectbox("Quality:", ["Best", "4K (2160p)", "1440p", "1080p", "720p", "480p", "360p"], index=0)

with col_download:
    st.markdown("<br>", unsafe_allow_html=True)
    download_clicked = st.button("Download", use_container_width=True, key="download_btn")

# REAL-TIME FETCHING LOGIC
if url and url != st.session_state.last_url and len(url) > 10:
    st.session_state.last_url = url
    st.session_state.video_info = None
    st.session_state.download_error = None
    st.session_state.is_loading = True
    st.rerun()

if st.session_state.is_loading and url:
    with st.spinner(""):
        info = fetch_video_info(url)
        st.session_state.video_info = info
        st.session_state.is_loading = False
        st.rerun()

# SHIMMER / PREVIEW / ERROR DISPLAY
if st.session_state.is_loading and url:
    st.markdown("""
    <div class="live-indicator">
        <span class="live-dot"></span>
        <span>Analyzing URL and fetching metadata...</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="shimmer-wrapper">
        <div class="shimmer-flex">
            <div class="shimmer-thumb"></div>
            <div class="shimmer-body">
                <div class="shimmer-line title"></div>
                <div class="shimmer-line meta"></div>
                <div class="shimmer-line meta" style="width:35%"></div>
                <div class="shimmer-metrics">
                    <div class="shimmer-metric"></div>
                    <div class="shimmer-metric"></div>
                    <div class="shimmer-metric"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.video_info and not st.session_state.video_info.get('success', False):
    error_msg = st.session_state.video_info.get('error', 'Unknown error')
    st.markdown(f'<div class="error-card">{error_msg}</div>', unsafe_allow_html=True)

    if 'reddit' in error_msg.lower() or 'authentication' in error_msg.lower():
        st.markdown("""
        <div class="tip-card">
        <b>Reddit requires authentication</b><br>
        Try a direct media URL or use another platform.
        </div>
        """, unsafe_allow_html=True)
    elif 'no video' in error_msg.lower():
        st.markdown("""
        <div class="tip-card">
        <b>Instagram - No video found</b><br>
        This may be a photo post. Try switching mode to <b>Photo/Gallery</b> or use a Reel URL.
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.video_info and st.session_state.video_info.get('success', False):
    info = st.session_state.video_info
    site_name = get_site_name(info.get('extractor', 'generic'))
    content_type = info.get('content_type', 'video')
    content_icon = get_content_icon(content_type)

    st.markdown("<div class='preview-card'>", unsafe_allow_html=True)

    prev_col1, prev_col2 = st.columns([1, 2])
    with prev_col1:
        if info.get('thumbnail'):
            st.image(info['thumbnail'], use_container_width=True)
    with prev_col2:
        st.markdown(f"**{info['title']}**")
        st.markdown(f"@{info['uploader']}  |  {format_duration(info['duration'])}")

        st.markdown(f"""
        <div style="margin: 0.5rem 0;">
            <span class="site-badge">{site_name}</span>
            <span class="type-badge">{content_icon} {content_type.title()}</span>
        </div>
        """, unsafe_allow_html=True)

        if not info.get('is_youtube') and content_type == 'video' and info.get('has_video'):
            st.markdown('<span style="color:#9ca3af; font-size:0.8rem;">Quality selection auto-adjusted for this platform</span>', unsafe_allow_html=True)

        meta_cols = st.columns(3)
        with meta_cols[0]: 
            st.markdown(f'<div class="metric-box"><div class="metric-value">{format_size(info.get("filesize_approx"))}</div><div class="metric-label">Est. Size</div></div>', unsafe_allow_html=True)
        with meta_cols[1]: 
            st.markdown(f'<div class="metric-box"><div class="metric-value">{format_count(info.get("view_count"))}</div><div class="metric-label">Views</div></div>', unsafe_allow_html=True)
        with meta_cols[2]: 
            st.markdown(f'<div class="metric-box"><div class="metric-value">{format_count(info.get("like_count"))}</div><div class="metric-label">Likes</div></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if not ffmpeg_ok and mode in ("Auto Detect", "Video") and content_type == 'video':
        st.markdown('<div class="warning-card">FFmpeg not detected. Using single-file formats (no merging needed).</div>', unsafe_allow_html=True)

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
                try: progress_bar.progress(min(int(float(p)), 100), text=f"Downloading... {speed} (ETA: {eta})")
                except: pass
                status_text.text(f"Speed: {speed} | ETA: {eta}")
            elif d['status'] == 'finished':
                progress_bar.progress(100, text="Complete! Processing...")
                status_text.text("Finalizing file...")

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                format_str = get_format_string(quality, mode, ffmpeg_ok, info)
                ydl_opts = build_ydl_opts(format_str, tmpdir, progress_hook, ffmpeg_ok, mode, info)

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                files = [f for f in os.listdir(tmpdir) if os.path.isfile(os.path.join(tmpdir, f))]
                if not files: raise Exception("Download completed but no file found.")
                file_name = files[0]
                file_path = os.path.join(tmpdir, file_name)

                if file_name.endswith('.mp3'): mime_type = "audio/mpeg"
                elif file_name.endswith('.webm'): mime_type = "video/webm"
                elif file_name.endswith('.m4a'): mime_type = "audio/mp4"
                elif file_name.endswith(('.jpg', '.jpeg')): mime_type = "image/jpeg"
                elif file_name.endswith('.png'): mime_type = "image/png"
                elif file_name.endswith('.webp'): mime_type = "image/webp"
                else: mime_type = "video/mp4"

                file_size = os.path.getsize(file_path)
                if file_size > 500 * 1024 * 1024: 
                    st.warning("File >500MB. Streamlit Cloud may struggle.")

                with open(file_path, 'rb') as f:
                    file_bytes = f.read()
        except Exception as e:
            download_error = str(e)

        progress_bar.empty()
        status_text.empty()

        if download_error:
            st.markdown(f'<div class="error-card">{download_error}</div>', unsafe_allow_html=True)

            if "too long" in download_error.lower() or "file name" in download_error.lower():
                st.markdown("""
                <div class="tip-card">
                <b>File name too long</b><br>
                The video title was too long for the filesystem. This has been fixed in the latest version with auto-truncation.
                </div>
                """, unsafe_allow_html=True)
            elif "403" in download_error or "forbidden" in download_error.lower():
                st.markdown("""
                <div class="tip-card">
                <b>YouTube 403 Block - Cloud IP Detected</b><br><br>
                YouTube has blocked this server's IP. This is an infrastructure limit.<br><br>
                <b>Free fixes:</b><br>
                1. <b>Retry 2-3 times</b> - Sometimes transient<br>
                2. <b>Lower quality</b> - Try 360p or Audio Only<br>
                3. <b>Run locally</b> - <code>pip install -r requirements.txt && streamlit run streamlit_app.py</code><br><br>
                <b>Non-YouTube sites</b> (TikTok, Instagram, Facebook, Vimeo) usually work fine on cloud.
                </div>
                """, unsafe_allow_html=True)
            elif "requested format is not available" in download_error.lower():
                st.markdown("""
                <div class="tip-card">
                <b>Format Not Available</b><br>
                The selected quality doesn't exist. Try switching to <b>"Best"</b> quality or <b>"Auto Detect"</b> mode.
                </div>
                """, unsafe_allow_html=True)
            elif "ffmpeg" in download_error.lower() or "merging" in download_error.lower():
                st.error("Add packages.txt with ffmpeg to your repo and redeploy.")
        elif file_bytes:
            st.markdown(f'<div class="success-card">Ready! {file_name} ({format_size(len(file_bytes))})</div>', unsafe_allow_html=True)
            st.download_button(
                label="Click to Download File", data=file_bytes,
                file_name=file_name, mime=mime_type,
                use_container_width=True, key=f"dl_{int(time.time())}"
            )
            st.caption("File served directly from memory.")

# FOOTER
st.markdown("""
<div class="app-footer">
    <div style="margin-bottom: 0.5rem;">
        <span style="color: #6b7280;">Universal Downloader Pro</span>
        <span style="color: #4b5563;"> | </span>
        <span style="color: #6b7280;">Powered by yt-dlp</span>
    </div>
    <div style="font-size: 0.7rem; color: #374151;">
        Supports 1800+ platforms including YouTube, Instagram, TikTok, Facebook, Twitter/X, Reddit, Vimeo and more<br>
        Free & Open Source | No API keys required | Unlimited downloads
    </div>
</div>
""", unsafe_allow_html=True)
