
import streamlit as st
import yt_dlp
import os
import tempfile
import subprocess
from io import BytesIO
from pathlib import Path
import time
import re

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
# CUSTOM CSS — Dark, polished UI + Shimmer effects
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main-header {
        font-size: 2.4rem; font-weight: 800;
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8F4B 50%, #FFD93D 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem; letter-spacing: -0.02em;
    }
    .sub-header { color: #9ca3af; font-size: 0.9rem; margin-bottom: 1.5rem; font-weight: 400; }

    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #1f2937; color: #f3f4f6;
        border: 1.5px solid #374151; border-radius: 10px;
        font-size: 0.95rem; padding: 0.6rem 1rem;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FF8F4B;
        box-shadow: 0 0 0 3px rgba(255, 143, 75, 0.15);
    }

    /* Selectbox styling */
    .stSelectbox > div > div > div {
        background-color: #1f2937; color: #f3f4f6;
        border: 1.5px solid #374151; border-radius: 10px;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8F4B 100%) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; height: 2.8em !important;
        font-weight: 700 !important; font-size: 1rem !important;
        transition: all 0.25s ease; letter-spacing: 0.01em;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 75, 75, 0.35);
    }
    .stButton > button:active { transform: translateY(0); }

    /* Cards */
    .info-card {
        background: linear-gradient(145deg, #111827 0%, #0f172a 100%);
        border: 1px solid #1f2937; border-radius: 16px;
        padding: 1.5rem; margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .error-card {
        background: linear-gradient(145deg, #3d1f1f 0%, #2d1a1a 100%);
        border-left: 4px solid #ef4444; border-radius: 10px;
        padding: 1rem 1.2rem; color: #fca5a5;
    }
    .success-card {
        background: linear-gradient(145deg, #1f3d2a 0%, #1a3322 100%);
        border-left: 4px solid #22c55e; border-radius: 10px;
        padding: 1rem 1.2rem; color: #86efac;
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

    /* Metrics */
    .metric-box {
        background: linear-gradient(145deg, #1f2937 0%, #18212f 100%);
        border-radius: 10px; padding: 0.9rem 0.5rem;
        text-align: center; border: 1px solid #374151;
        transition: transform 0.2s;
    }
    .metric-box:hover { transform: translateY(-2px); border-color: #4b5563; }
    .metric-value { font-size: 1.15rem; font-weight: 700; color: #f3f4f6; }
    .metric-label { font-size: 0.7rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 0.2rem; }

    /* Shimmer / Skeleton */
    .shimmer-container { display: flex; gap: 1rem; align-items: flex-start; }
    .shimmer-thumb {
        width: 160px; height: 90px; border-radius: 12px;
        background: linear-gradient(90deg, #1f2937 25%, #374151 50%, #1f2937 75%);
        background-size: 200% 100%; animation: shimmer 1.5s infinite;
    }
    .shimmer-text { flex: 1; }
    .shimmer-line {
        height: 16px; border-radius: 6px; margin-bottom: 10px;
        background: linear-gradient(90deg, #1f2937 25%, #374151 50%, #1f2937 75%);
        background-size: 200% 100%; animation: shimmer 1.5s infinite;
    }
    .shimmer-line.short { width: 60%; }
    .shimmer-line.medium { width: 80%; }
    .shimmer-metrics { display: flex; gap: 0.8rem; margin-top: 1rem; }
    .shimmer-metric {
        flex: 1; height: 60px; border-radius: 10px;
        background: linear-gradient(90deg, #1f2937 25%, #374151 50%, #1f2937 75%);
        background-size: 200% 100%; animation: shimmer 1.5s infinite;
    }
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    /* Live indicator */
    .live-dot {
        display: inline-block; width: 8px; height: 8px;
        background: #22c55e; border-radius: 50%;
        margin-right: 6px; animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }

    /* Quality badge */
    .quality-badge {
        display: inline-block; background: rgba(255,143,75,0.15);
        color: #FF8F4B; padding: 2px 8px; border-radius: 6px;
        font-size: 0.75rem; font-weight: 600; margin-left: 8px;
        border: 1px solid rgba(255,143,75,0.3);
    }

    .footer { text-align: center; color: #6b7280; font-size: 0.8rem; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #1f2937; }
    code { background-color: #374151; padding: 2px 6px; border-radius: 4px; color: #fbbf24; font-size: 0.85em; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
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
    """Fetch video metadata without downloading. Returns dict or error string."""
    ydl_opts = get_base_ydl_opts()
    ydl_opts['skip_download'] = True
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Analyze available formats to determine quality support
            formats = info.get('formats', [])
            has_height_formats = any(f.get('height') and f.get('height') > 0 for f in formats)
            has_video_formats = any(f.get('vcodec') != 'none' for f in formats)
            has_audio_only = not has_video_formats and any(f.get('acodec') != 'none' for f in formats)

            # Determine extractor type
            extractor = info.get('extractor', 'generic').lower()
            is_youtube = 'youtube' in extractor

            return {
                'title': info.get('title', 'Unknown'),
                'uploader': info.get('uploader', info.get('channel', info.get('uploader_id', 'Unknown'))),
                'duration': info.get('duration') or 0,
                'thumbnail': info.get('thumbnail', ''),
                'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
                'view_count': info.get('view_count') or 0,
                'like_count': info.get('like_count') or 0,
                'upload_date': info.get('upload_date', ''),
                'formats': formats,
                'ext': info.get('ext', 'mp4'),
                'filesize_approx': info.get('filesize_approx') or 0,
                'extractor': extractor,
                'is_youtube': is_youtube,
                'has_height_formats': has_height_formats,
                'has_video_formats': has_video_formats,
                'has_audio_only': has_audio_only,
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

def get_format_string(quality, mode, ffmpeg_available, info):
    """
    Smart format selection based on site capabilities.
    For non-YouTube sites (Facebook, Instagram, TikTok), always use 'best' 
    since they don't reliably support height-based quality selection.
    """
    extractor = info.get('extractor', '').lower()
    has_height = info.get('has_height_formats', False)
    is_youtube = info.get('is_youtube', False)

    # Audio mode
    if mode == "Audio Only":
        if ffmpeg_available: return "bestaudio/best"
        return "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio"

    # For non-YouTube sites OR sites without height metadata, always use best
    if not is_youtube or not has_height:
        return "best/bestvideo+bestaudio"

    # YouTube with height support
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
    """Build yt-dlp options dict."""
    ydl_opts = get_base_ydl_opts()
    ydl_opts.update({
        'format': format_string,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'noplaylist': True,
        'retries': 10, 'fragment_retries': 10,
        'continue_dl': True,
    })

    if ffmpeg_available and mode == "Audio Only":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    elif ffmpeg_available and mode != "Audio Only":
        if '+' in format_string:
            ydl_opts['merge_output_format'] = 'mp4'

    return ydl_opts

def show_shimmer():
    """Display shimmer skeleton while loading."""
    st.markdown("""
    <div class="info-card">
        <div class="shimmer-container">
            <div class="shimmer-thumb"></div>
            <div class="shimmer-text">
                <div class="shimmer-line medium"></div>
                <div class="shimmer-line short"></div>
                <div class="shimmer-metrics">
                    <div class="shimmer-metric"></div>
                    <div class="shimmer-metric"></div>
                    <div class="shimmer-metric"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_preview(info):
    """Display video preview card."""
    extractor = info.get('extractor', 'generic')
    is_youtube = info.get('is_youtube', False)
    has_height = info.get('has_height_formats', False)

    st.markdown("<div class='info-card'>", unsafe_allow_html=True)

    prev_col1, prev_col2 = st.columns([1, 2])
    with prev_col1:
        if info.get('thumbnail'):
            st.image(info['thumbnail'], use_container_width=True)
    with prev_col2:
        st.markdown(f"**{info['title']}**")
        st.markdown(f"👤 {info['uploader']}  •  ⏱ {format_duration(info['duration'])}")

        # Site badge
        site_name = extractor.replace('ie', '').title()
        st.markdown(f'<span class="quality-badge">{site_name}</span>', unsafe_allow_html=True)

        # Quality warning for non-YouTube
        if not is_youtube and not has_height and info.get('has_video_formats'):
            st.markdown('<span style="color:#9ca3af; font-size:0.8rem;">⚡ Quality selection ignored — this site offers auto quality only</span>', unsafe_allow_html=True)

        meta_cols = st.columns(3)
        with meta_cols[0]: 
            st.markdown(f'<div class="metric-box"><div class="metric-value">{format_size(info.get("filesize_approx"))}</div><div class="metric-label">Est. Size</div></div>', unsafe_allow_html=True)
        with meta_cols[1]: 
            st.markdown(f'<div class="metric-box"><div class="metric-value">{format_count(info.get("view_count"))}</div><div class="metric-label">Views</div></div>', unsafe_allow_html=True)
        with meta_cols[2]: 
            st.markdown(f'<div class="metric-box"><div class="metric-value">{format_count(info.get("like_count"))}</div><div class="metric-label">Likes</div></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────
if 'last_url' not in st.session_state:
    st.session_state.last_url = ''
if 'video_info' not in st.session_state:
    st.session_state.video_info = None
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False
if 'download_error' not in st.session_state:
    st.session_state.download_error = None

# ─────────────────────────────────────────────────────────────
# UI HEADER
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🎬 YT Downloader Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by yt-dlp • Supports 1800+ sites • Unlimited & Free</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ System Status")
    ffmpeg_ok = check_ffmpeg()
    if ffmpeg_ok: st.success("✅ FFmpeg detected")
    else: st.warning("⚠️ FFmpeg missing — add `packages.txt` with `ffmpeg`")

    st.markdown("---")
    st.markdown("### 📋 Required Files")
    st.code("""requirements.txt:
streamlit
yt-dlp

packages.txt:
ffmpeg""", language="text")

    st.markdown("---")
    st.markdown("### 🛡️ Legal Note")
    st.caption("Only download content you own or have rights to.")

# ─────────────────────────────────────────────────────────────
# MAIN INPUT — REAL-TIME FETCHING
# ─────────────────────────────────────────────────────────────
with st.container():
    url = st.text_input(
        "🔗 Paste Video URL:",
        placeholder="https://www.youtube.com/watch?v=...  (auto-fetches on paste)",
        label_visibility="collapsed",
        key="url_input"
    )

    # REAL-TIME FETCHING: Trigger when URL changes and is valid
    if url and url != st.session_state.last_url:
        st.session_state.last_url = url
        st.session_state.video_info = None
        st.session_state.download_error = None
        st.session_state.is_loading = True
        st.rerun()

    # If loading, fetch info
    if st.session_state.is_loading and url:
        with st.spinner(""):
            info = fetch_video_info(url)
            st.session_state.video_info = info
            st.session_state.is_loading = False
            st.rerun()

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        mode = st.selectbox("Mode:", ["Video", "Audio Only"], index=0)
    with col2:
        if mode == "Video":
            quality = st.selectbox(
                "Quality:",
                ["Best", "4K (2160p)", "1440p", "1080p", "720p", "480p", "360p"],
                index=4,
                key="quality_select"
            )
        else:
            quality = st.selectbox("Quality:", ["Best", "192kbps", "128kbps"], index=0)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        download_clicked = st.button("⬇️ Download", use_container_width=True)

# ─────────────────────────────────────────────────────────────
# SHIMMER / PREVIEW / ERROR DISPLAY
# ─────────────────────────────────────────────────────────────
if st.session_state.is_loading and url:
    st.markdown("<div style='margin:1rem 0;'><span class='live-dot'></span><span style='color:#9ca3af; font-size:0.9rem;'>Fetching video info...</span></div>", unsafe_allow_html=True)
    show_shimmer()

elif st.session_state.video_info and not st.session_state.video_info.get('success', False):
    error_msg = st.session_state.video_info.get('error', 'Unknown error')
    st.markdown(f'<div class="error-card">❌ Failed to fetch info: {error_msg}</div>', unsafe_allow_html=True)

    # Reddit-specific guidance
    if 'reddit' in error_msg.lower() or 'authentication' in error_msg.lower():
        st.markdown("""
        <div class="tip-card">
        <b>🔒 Reddit requires authentication</b><br>
        Reddit now blocks anonymous access. Try:<br>
        • Use a direct media URL instead of the post URL<br>
        • Or try a different platform (YouTube, TikTok, Instagram, Facebook)
        </div>
        """, unsafe_allow_html=True)

    # Instagram no video guidance
    elif 'no video' in error_msg.lower():
        st.markdown("""
        <div class="tip-card">
        <b>📷 Instagram — No video found</b><br>
        This post may be a photo carousel or the URL is a profile/link. Try:<br>
        • Use the direct Reel URL (instagram.com/reel/...)<br>
        • Ensure the post contains a video, not just images
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.video_info and st.session_state.video_info.get('success', False):
    info = st.session_state.video_info
    show_preview(info)

    # FFmpeg warning
    if not ffmpeg_ok and mode == "Video" and info.get('has_video_formats'):
        st.markdown('<div class="warning-card">⚠️ <b>FFmpeg not detected.</b> Using single-file formats (no merging needed).</div>', unsafe_allow_html=True)

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
                try: progress_bar.progress(min(int(float(p)), 100), text=f"⬇️ Downloading... {speed} (ETA: {eta})")
                except: pass
                status_text.text(f"Speed: {speed} | ETA: {eta}")
            elif d['status'] == 'finished':
                progress_bar.progress(100, text="✅ Complete! Processing...")
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
                else: mime_type = "video/mp4"

                file_size = os.path.getsize(file_path)
                if file_size > 500 * 1024 * 1024: 
                    st.warning("⚠️ File >500MB. Streamlit Cloud may struggle.")

                with open(file_path, 'rb') as f:
                    file_bytes = f.read()
        except Exception as e:
            download_error = str(e)

        progress_bar.empty()
        status_text.empty()

        if download_error:
            st.markdown(f'<div class="error-card">❌ Download failed: {download_error}</div>', unsafe_allow_html=True)

            if "403" in download_error or "forbidden" in download_error.lower():
                st.markdown("""
                <div class="tip-card">
                <b>🔒 YouTube 403 Block — Cloud IP Detected</b><br><br>
                YouTube has blocked this server's IP. This is an infrastructure limit, not a code bug.<br><br>
                <b>Free fixes:</b><br>
                1. <b>Retry 2-3 times</b> — Sometimes transient<br>
                2. <b>Lower quality</b> — Try 360p or Audio Only<br>
                3. <b>Run locally</b> — <code>pip install -r requirements.txt && streamlit run streamlit_app.py</code> (100% success on residential IP)<br><br>
                <b>Non-YouTube sites</b> (TikTok, Instagram, Facebook, Vimeo, etc.) usually work fine on cloud.
                </div>
                """, unsafe_allow_html=True)
            elif "requested format is not available" in download_error.lower():
                st.markdown("""
                <div class="tip-card">
                <b>📐 Format Not Available</b><br><br>
                The selected quality doesn't exist for this video. The app auto-detected this site and should have used "best".<br><br>
                Try:<br>
                • Switch to <b>"Best"</b> quality<br>
                • Try <b>"Audio Only"</b> mode<br>
                • Some sites only offer one quality per video
                </div>
                """, unsafe_allow_html=True)
            elif "ffmpeg" in download_error.lower() or "merging" in download_error.lower():
                st.error("Add `packages.txt` with `ffmpeg` to your repo and redeploy.")
        elif file_bytes:
            st.markdown(f'<div class="success-card">✅ <b>Ready!</b> {file_name} ({format_size(len(file_bytes))})</div>', unsafe_allow_html=True)
            st.download_button(
                label="📥 Click to Download File", data=file_bytes,
                file_name=file_name, mime=mime_type,
                use_container_width=True, key=f"dl_{int(time.time())}"
            )
            st.caption("💡 File served directly from memory.")

st.markdown('<div class="footer">Built with Streamlit + yt-dlp • Free & Open Source</div>', unsafe_allow_html=True)
