import streamlit as st
import yt_dlp
import os
import tempfile
import subprocess
from io import BytesIO
from pathlib import Path
import time
import hashlib
import json
from datetime import datetime

# PAGE CONFIG
st.set_page_config(
    page_title="Universal Downloader Pro",
    page_icon="⬇️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── App Shell ── */
    .app-header { text-align: center; padding: 2rem 0 0.5rem; }
    .app-logo {
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(135deg, #f97316 0%, #ef4444 40%, #ec4899 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -0.04em; line-height: 1;
    }
    .app-tagline {
        color: #6b7280; font-size: 0.82rem; font-weight: 400;
        letter-spacing: 0.08em; text-transform: uppercase; margin-top: 0.4rem;
    }
    .app-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #1e293b, #334155, #1e293b, transparent);
        margin: 1.2rem 0 1.8rem;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border: 1.5px solid #1e293b !important;
        border-radius: 14px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.93rem !important;
        transition: all 0.25s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #f97316 !important;
        box-shadow: 0 0 0 3px rgba(249,115,22,0.15) !important;
    }
    .stSelectbox > div > div > div {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border: 1.5px solid #1e293b !important;
        border-radius: 12px !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #f97316 0%, #ef4444 100%) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; height: 2.75em !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important; font-size: 0.9rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1) !important;
        box-shadow: 0 4px 20px rgba(249,115,22,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 28px rgba(249,115,22,0.45) !important;
    }
    .stButton > button:active { transform: translateY(0) scale(0.98) !important; }

    /* Secondary buttons */
    div[data-testid="column"]:nth-child(2) .stButton > button,
    div[data-testid="column"]:nth-child(3) .stButton > button {
        background: #1e293b !important;
        box-shadow: none !important;
        border: 1px solid #334155 !important;
        color: #94a3b8 !important;
    }
    div[data-testid="column"]:nth-child(2) .stButton > button:hover,
    div[data-testid="column"]:nth-child(3) .stButton > button:hover {
        background: #334155 !important;
        color: #e2e8f0 !important;
        transform: translateY(-1px) !important;
        box-shadow: none !important;
    }

    /* ── Phase Step Indicator ── */
    .phase-track {
        display: flex; align-items: center; gap: 0; margin: 1rem 0 0.6rem;
        font-size: 0.72rem; font-weight: 600; letter-spacing: 0.04em;
    }
    .phase-step {
        display: flex; align-items: center; gap: 6px;
        padding: 5px 12px; border-radius: 20px;
        color: #475569; background: #0f172a;
        border: 1px solid #1e293b;
        transition: all 0.4s ease;
        white-space: nowrap;
    }
    .phase-step.active {
        color: #f97316; border-color: rgba(249,115,22,0.4);
        background: rgba(249,115,22,0.08);
        box-shadow: 0 0 12px rgba(249,115,22,0.2);
    }
    .phase-step.done {
        color: #22c55e; border-color: rgba(34,197,94,0.4);
        background: rgba(34,197,94,0.08);
    }
    .phase-step.ready {
        color: #3b82f6; border-color: rgba(59,130,246,0.4);
        background: rgba(59,130,246,0.08);
        animation: readyPulse 2s infinite;
    }
    .phase-arrow { color: #1e293b; padding: 0 4px; font-size: 0.65rem; }
    @keyframes readyPulse {
        0%,100% { box-shadow: 0 0 8px rgba(59,130,246,0.3); }
        50% { box-shadow: 0 0 18px rgba(59,130,246,0.6); }
    }

    /* ── Live dot ── */
    .live-row {
        display: flex; align-items: center; gap: 8px;
        margin-bottom: 0.8rem;
    }
    .live-dot {
        width: 9px; height: 9px; border-radius: 50%;
        background: #f97316;
        box-shadow: 0 0 0 0 rgba(249,115,22,0.5);
        animation: sonarPing 1.4s cubic-bezier(0,0,0.2,1) infinite;
    }
    .live-text { color: #94a3b8; font-size: 0.82rem; font-weight: 500; }
    .live-step { color: #f97316; font-weight: 600; }
    @keyframes sonarPing {
        0% { box-shadow: 0 0 0 0 rgba(249,115,22,0.7); }
        70% { box-shadow: 0 0 0 10px rgba(249,115,22,0); }
        100% { box-shadow: 0 0 0 0 rgba(249,115,22,0); }
    }

    /* ── Shimmer skeleton ── */
    .shimmer-card {
        background: linear-gradient(145deg, #0d1726 0%, #0a1120 100%);
        border: 1px solid #1e293b; border-radius: 20px;
        padding: 1.6rem; margin: 0.5rem 0;
        animation: entryFade 0.3s ease-out;
    }
    .shimmer-row { display: flex; gap: 1.2rem; }
    .s-thumb {
        width: 190px; height: 110px; border-radius: 14px; flex-shrink: 0;
        background: linear-gradient(100deg, #0f172a 30%, #1e293b 50%, #0f172a 70%);
        background-size: 300% 100%;
        animation: sweep 1.8s ease-in-out infinite;
    }
    .s-body { flex: 1; padding-top: 4px; }
    .s-line {
        border-radius: 6px; margin-bottom: 10px;
        background: linear-gradient(100deg, #0f172a 30%, #1e293b 50%, #0f172a 70%);
        background-size: 300% 100%;
        animation: sweep 1.8s ease-in-out infinite;
    }
    .s-title { height: 20px; width: 80%; animation-delay: 0.05s; }
    .s-sub   { height: 13px; width: 50%; animation-delay: 0.10s; }
    .s-tags  { height: 22px; width: 38%; animation-delay: 0.15s; border-radius: 20px; }
    .s-metrics { display: flex; gap: 10px; margin-top: 14px; }
    .s-metric {
        flex: 1; height: 70px; border-radius: 12px;
        background: linear-gradient(100deg, #0f172a 30%, #1e293b 50%, #0f172a 70%);
        background-size: 300% 100%;
        animation: sweep 1.8s ease-in-out infinite;
    }
    .s-metric:nth-child(2) { animation-delay: 0.1s; }
    .s-metric:nth-child(3) { animation-delay: 0.2s; }
    @keyframes sweep {
        0% { background-position: 100% 0; }
        100% { background-position: -100% 0; }
    }
    @keyframes entryFade {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Preview Card ── */
    .preview-card {
        background: linear-gradient(145deg, #0d1726 0%, #0a1120 100%);
        border: 1px solid #1e293b; border-radius: 20px;
        padding: 1.6rem; margin: 0.5rem 0;
        box-shadow: 0 12px 40px rgba(0,0,0,0.5);
        animation: entryFade 0.45s cubic-bezier(0.22,1,0.36,1);
    }
    .video-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.05rem; font-weight: 700;
        color: #f1f5f9; line-height: 1.4; margin-bottom: 4px;
    }
    .video-meta { color: #64748b; font-size: 0.82rem; margin-bottom: 0.7rem; }

    .badge {
        display: inline-flex; align-items: center; gap: 4px;
        padding: 3px 10px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 700;
        letter-spacing: 0.05em; text-transform: uppercase;
        margin-right: 5px;
    }
    .badge-platform {
        background: rgba(249,115,22,0.12); color: #f97316;
        border: 1px solid rgba(249,115,22,0.25);
    }
    .badge-type {
        background: rgba(34,197,94,0.12); color: #22c55e;
        border: 1px solid rgba(34,197,94,0.25);
    }

    .metric-box {
        background: #0f172a; border: 1px solid #1e293b;
        border-radius: 12px; padding: 0.9rem 0.5rem;
        text-align: center; transition: all 0.2s;
    }
    .metric-box:hover { border-color: #334155; transform: translateY(-2px); }
    .metric-val {
        font-family: 'Syne', sans-serif;
        font-size: 1.15rem; font-weight: 700; color: #f1f5f9;
    }
    .metric-lbl { font-size: 0.64rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 3px; }

    /* ── Download Progress ── */
    .dl-status-card {
        background: linear-gradient(145deg, #0d1726, #0a1120);
        border: 1px solid #1e293b; border-radius: 16px;
        padding: 1.2rem 1.4rem; margin: 0.8rem 0;
        animation: entryFade 0.3s ease;
    }
    .dl-progress-label {
        display: flex; justify-content: space-between;
        font-size: 0.8rem; margin-bottom: 8px;
    }
    .dl-phase-name { color: #94a3b8; font-weight: 500; }
    .dl-percent { color: #f97316; font-weight: 700; font-family: 'Syne', sans-serif; }
    .dl-stats { color: #64748b; font-size: 0.75rem; margin-top: 5px; }
    .dl-speed { color: #3b82f6; font-weight: 600; }
    .dl-eta { color: #a78bfa; font-weight: 600; }

    /* ── Ready to Download Card ── */
    .ready-card {
        background: linear-gradient(145deg, #051c14, #041510);
        border: 1.5px solid rgba(34,197,94,0.35);
        border-radius: 16px; padding: 1.2rem 1.4rem;
        margin: 0.8rem 0;
        box-shadow: 0 0 30px rgba(34,197,94,0.1), inset 0 1px 0 rgba(34,197,94,0.1);
        animation: readyEntrance 0.6s cubic-bezier(0.22,1,0.36,1);
    }
    @keyframes readyEntrance {
        0% { opacity:0; transform: scale(0.95) translateY(10px); }
        60% { transform: scale(1.01) translateY(-2px); }
        100% { opacity:1; transform: scale(1) translateY(0); }
    }
    .ready-top { display: flex; align-items: center; gap: 10px; margin-bottom: 0.6rem; }
    .ready-icon {
        width: 36px; height: 36px; border-radius: 50%;
        background: rgba(34,197,94,0.15);
        border: 1px solid rgba(34,197,94,0.3);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem;
        animation: iconBounce 0.6s cubic-bezier(0.34,1.56,0.64,1) 0.3s both;
    }
    @keyframes iconBounce {
        from { transform: scale(0); } to { transform: scale(1); }
    }
    .ready-title { color: #22c55e; font-weight: 700; font-size: 0.95rem; font-family: 'Syne', sans-serif; }
    .ready-filename { color: #86efac; font-size: 0.82rem; font-family: monospace; }
    .ready-size { color: #64748b; font-size: 0.75rem; margin-top: 2px; }

    /* ── Error Card ── */
    .error-card {
        background: linear-gradient(145deg, #1c0a0a, #160707);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 14px; padding: 1rem 1.2rem;
        color: #fca5a5; font-size: 0.85rem; line-height: 1.6;
        animation: entryFade 0.3s ease;
    }
    .error-title { font-weight: 700; color: #ef4444; margin-bottom: 4px; font-family: 'Syne', sans-serif; }

    /* ── Tip Card ── */
    .tip-card {
        background: #0d1726; border: 1px solid #1e293b;
        border-left: 3px solid #f97316;
        border-radius: 10px; padding: 0.9rem 1.1rem;
        color: #94a3b8; font-size: 0.82rem; line-height: 1.65;
        margin-top: 0.6rem;
    }
    .tip-card b { color: #f97316; }

    /* ── Warning ── */
    .warn-card {
        background: #120f00; border: 1px solid rgba(234,179,8,0.3);
        border-radius: 10px; padding: 0.8rem 1rem;
        color: #fde68a; font-size: 0.8rem;
        margin: 0.5rem 0;
    }

    /* ── History Panel ── */
    .history-header {
        font-family: 'Syne', sans-serif;
        font-size: 0.85rem; font-weight: 700;
        color: #64748b; text-transform: uppercase;
        letter-spacing: 0.08em; margin-bottom: 0.5rem;
    }
    .history-item {
        display: flex; align-items: center; gap: 10px;
        background: #0d1726; border: 1px solid #1e293b;
        border-radius: 10px; padding: 0.65rem 0.9rem;
        margin-bottom: 6px; cursor: pointer;
        transition: all 0.2s;
    }
    .history-item:hover { border-color: #334155; background: #111f35; }
    .history-thumb {
        width: 44px; height: 30px; border-radius: 6px;
        object-fit: cover; flex-shrink: 0;
        background: #1e293b;
    }
    .history-info { flex: 1; min-width: 0; }
    .history-title { color: #cbd5e1; font-size: 0.8rem; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .history-meta { color: #475569; font-size: 0.7rem; margin-top: 1px; }
    .history-badge {
        font-size: 0.65rem; font-weight: 700; padding: 2px 7px;
        border-radius: 20px; background: rgba(249,115,22,0.1);
        color: #f97316; border: 1px solid rgba(249,115,22,0.2);
        white-space: nowrap;
    }

    /* ── Batch mode ── */
    .batch-info {
        background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2);
        border-radius: 10px; padding: 0.7rem 1rem;
        color: #93c5fd; font-size: 0.8rem; margin-bottom: 0.7rem;
    }

    /* ── Option toggles ── */
    .stCheckbox > label { color: #94a3b8 !important; font-size: 0.85rem !important; }

    /* ── Footer ── */
    .app-footer {
        text-align: center; color: #334155;
        font-size: 0.73rem; margin-top: 3rem;
        padding: 1.5rem 0; border-top: 1px solid #0f172a;
        line-height: 1.8;
    }
    .footer-accent { color: #475569; }

    code {
        background: #1e293b; padding: 2px 7px;
        border-radius: 5px; color: #fb923c;
        font-size: 0.82em; font-family: 'Courier New', monospace;
    }

    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ───────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def check_ffmpeg():
    try:
        r = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def get_base_ydl_opts():
    return {
        'quiet': True, 'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_js_version': 'actual',
                'player_client': 'web_safari',
            }
        },
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.youtube.com/',
        },
        'geo_bypass': True,
    }


def fetch_video_info(url):
    opts = get_base_ydl_opts()
    opts['skip_download'] = True
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            fmts = info.get('formats', [])
            has_height = any(f.get('height') and f.get('height') > 0 for f in fmts)
            has_video  = any(f.get('vcodec') != 'none' for f in fmts)
            has_audio  = any(f.get('acodec') != 'none' for f in fmts)
            has_image  = (any(f.get('ext') in ('jpg','jpeg','png','webp') for f in fmts)
                          or info.get('ext') in ('jpg','jpeg','png','webp'))
            extractor  = info.get('extractor', 'generic').lower()

            content_type = 'video'
            if has_image and not has_video:
                content_type = 'photo'
            elif not has_video and not has_audio and not has_image:
                if info.get('entries'):
                    content_type = 'gallery'

            # Available quality levels
            heights = sorted(set(
                f['height'] for f in fmts
                if f.get('height') and f.get('height') > 0
            ), reverse=True)

            return {
                'title': info.get('title', 'Unknown'),
                'uploader': info.get('uploader', info.get('channel',
                            info.get('uploader_id', 'Unknown'))),
                'duration': info.get('duration') or 0,
                'thumbnail': info.get('thumbnail', ''),
                'description': (info.get('description', '')[:220] + '...')
                                if info.get('description') else '',
                'view_count': info.get('view_count') or 0,
                'like_count': info.get('like_count') or 0,
                'upload_date': info.get('upload_date', ''),
                'formats': fmts,
                'ext': info.get('ext', 'mp4'),
                'filesize_approx': info.get('filesize_approx') or 0,
                'extractor': extractor,
                'is_youtube':   'youtube'   in extractor,
                'is_instagram': 'instagram' in extractor,
                'is_facebook':  'facebook'  in extractor,
                'is_tiktok':    'tiktok'    in extractor,
                'is_twitter':   'twitter'   in extractor,
                'has_height_formats': has_height,
                'has_video': has_video,
                'has_audio': has_audio,
                'has_image': has_image,
                'content_type': content_type,
                'entries': info.get('entries', []),
                'available_heights': heights,
                'has_subtitles': bool(info.get('subtitles') or info.get('automatic_captions')),
                'success': True,
            }
    except Exception as e:
        return {'error': str(e), 'success': False}


def format_duration(s):
    if not s: return "N/A"
    m, s = divmod(int(s), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def format_size(b):
    if not b: return "—"
    b = float(b)
    for u in ['B','KB','MB','GB']:
        if b < 1024: return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} TB"


def format_count(n):
    if not n: return "0"
    n = float(n)
    if n >= 1e9: return f"{n/1e9:.1f}B"
    if n >= 1e6: return f"{n/1e6:.1f}M"
    if n >= 1e3: return f"{n/1e3:.1f}K"
    return str(int(n))


def sanitize_filename(title, max_len=80):
    if not title: title = "download"
    sanitized = "".join(c if c.isalnum() or c in " ._-" else "_" for c in title).strip("._")
    if len(sanitized) > max_len:
        h = hashlib.md5(sanitized.encode()).hexdigest()[:6]
        sanitized = sanitized[:max_len - 7] + "_" + h
    return sanitized or "download"


def get_format_string(quality, mode, ffmpeg_available, info):
    content_type = info.get('content_type', 'video')
    is_youtube   = info.get('is_youtube', False)
    has_height   = info.get('has_height_formats', False)

    if content_type == 'photo':
        return "best"
    if mode == "Audio Only":
        return "bestaudio/best" if ffmpeg_available else "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio"
    if not is_youtube or not has_height:
        return "best/bestvideo+bestaudio"

    height_map = {"Best": None, "4K (2160p)": 2160, "1440p": 1440,
                  "1080p": 1080, "720p": 720, "480p": 480, "360p": 360}
    th = height_map.get(quality)
    if ffmpeg_available:
        if th:
            return (f"bestvideo[height<={th}][vcodec!*=av01]"
                    f"+bestaudio[acodec!*=opus]"
                    f"/bestvideo[height<={th}]+bestaudio"
                    f"/best[height<={th}]")
        return "bestvideo[vcodec!*=av01]+bestaudio[acodec!*=opus]/bestvideo+bestaudio/best"
    else:
        return f"best[height<={th}]/best" if th else "best/bestvideo+bestaudio"


def build_ydl_opts(format_string, output_path, progress_hook, ffmpeg_available, mode, info,
                   embed_subs=False, embed_thumb=False):
    opts = get_base_ydl_opts()
    safe = sanitize_filename(info.get('title', 'download'))
    opts.update({
        'format': format_string,
        'outtmpl': os.path.join(output_path, f'{safe}.%(ext)s'),
        'progress_hooks': [progress_hook],
        'noplaylist': True,
        'retries': 10, 'fragment_retries': 10,
        'continue_dl': True,
    })
    content_type = info.get('content_type', 'video')
    post = []

    if content_type == 'photo':
        if info.get('entries'): opts['noplaylist'] = False
    elif ffmpeg_available and mode == "Audio Only":
        post.append({'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'})
        if embed_thumb:
            post.append({'key': 'EmbedThumbnail'})
    elif ffmpeg_available and mode != "Audio Only":
        if '+' in format_string:
            opts['merge_output_format'] = 'mp4'

    if ffmpeg_available:
        if embed_subs and mode != "Audio Only":
            opts['writesubtitles'] = True
            opts['writeautomaticsub'] = True
            opts['subtitleslangs'] = ['en', 'en-US']
            post.append({'key': 'FFmpegSubtitlesConvertor', 'format': 'srt'})
        if embed_thumb and mode == "Audio Only":
            opts['writethumbnail'] = True
            post.append({'key': 'EmbedThumbnail'})

    if post:
        opts['postprocessors'] = post
    return opts


def get_site_name(extractor):
    for k, n in [('youtube','YouTube'),('instagram','Instagram'),('facebook','Facebook'),
                 ('tiktok','TikTok'),('twitter','Twitter/X'),('reddit','Reddit'),
                 ('vimeo','Vimeo'),('twitch','Twitch'),('dailymotion','Dailymotion')]:
        if k in extractor: return n
    return extractor.replace('ie','').title()


def get_type_icon(ct):
    return {'video': '▶', 'photo': '◈', 'gallery': '⊞', 'audio': '♫'}.get(ct, '◉')


def add_to_history(info, file_name, file_size):
    """Add a completed download to session history."""
    if 'download_history' not in st.session_state:
        st.session_state.download_history = []
    entry = {
        'title':     info.get('title', 'Unknown')[:60],
        'uploader':  info.get('uploader', ''),
        'thumbnail': info.get('thumbnail', ''),
        'site':      get_site_name(info.get('extractor', 'generic')),
        'type':      info.get('content_type', 'video'),
        'file_name': file_name,
        'file_size': format_size(file_size),
        'ts':        datetime.now().strftime('%H:%M'),
    }
    st.session_state.download_history.insert(0, entry)
    if len(st.session_state.download_history) > 10:
        st.session_state.download_history = st.session_state.download_history[:10]


def render_phase_bar(stage):
    """stage: fetch | preview | downloading | ready | error"""
    steps = [
        ('fetch',       '① Fetch',    stage == 'fetch'),
        ('preview',     '② Preview',  stage == 'preview'),
        ('downloading', '③ Download', stage == 'downloading'),
        ('ready',       '④ Ready',    stage == 'ready'),
    ]
    html = '<div class="phase-track">'
    for i, (key, label, _active) in enumerate(steps):
        if i > 0:
            html += '<span class="phase-arrow">›</span>'
        if key == stage:
            cls = "phase-step active" if key not in ('ready',) else "phase-step ready"
            if key == 'ready': cls = "phase-step ready"
        elif _stage_done(key, stage):
            cls = "phase-step done"
        else:
            cls = "phase-step"
        html += f'<span class="{cls}">{label}</span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def _stage_done(key, current):
    order = ['fetch', 'preview', 'downloading', 'ready']
    try:
        return order.index(key) < order.index(current)
    except ValueError:
        return False


# ─── SESSION STATE ─────────────────────────────────────────────────────────────
defaults = {
    'last_url': '', 'video_info': None,
    'is_loading': False, 'download_error': None,
    'clear_trigger': 0, 'download_history': [],
    'batch_mode': False, 'stage': 'idle',
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

ffmpeg_ok = check_ffmpeg()

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-logo">Universal Downloader</div>
    <div class="app-tagline">Videos · Photos · Reels · Stories · 1800+ Sites</div>
</div>
<div class="app-divider"></div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ System")
    if ffmpeg_ok:
        st.success("✓ FFmpeg detected — full quality merging enabled")
    else:
        st.warning("⚠ FFmpeg missing — single-file formats only")
    st.markdown("---")
    st.markdown("### 📦 Required Files")
    st.code("requirements.txt:\nstreamlit\nyt-dlp\n\npackages.txt:\nffmpeg", language="text")
    st.markdown("---")
    st.markdown("### ⚖️ Legal")
    st.caption("Only download content you own or have rights to. Respect DMCA and local copyright laws.")
    st.markdown("---")
    # History in sidebar
    if st.session_state.download_history:
        st.markdown("### 🕘 Recent Downloads")
        for h in st.session_state.download_history:
            icon = get_type_icon(h['type'])
            st.markdown(f"""
            <div class="history-item">
                <div class="history-info">
                    <div class="history-title">{icon} {h['title']}</div>
                    <div class="history-meta">{h['site']} · {h['ts']} · {h['file_size']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─── BATCH MODE TOGGLE ─────────────────────────────────────────────────────────
col_single, col_batch = st.columns([3, 1])
with col_single:
    st.markdown("<div style='padding-top:6px; color:#64748b; font-size:0.8rem;'>Single URL</div>",
                unsafe_allow_html=True)
with col_batch:
    batch_mode = st.toggle("Batch Mode", value=st.session_state.batch_mode, key="batch_toggle")
    st.session_state.batch_mode = batch_mode

# ─── URL INPUT ─────────────────────────────────────────────────────────────────
if batch_mode:
    st.markdown("""
    <div class="batch-info">
        📋 <b>Batch Mode</b> — Paste one URL per line. All will be processed sequentially with the same quality settings.
    </div>
    """, unsafe_allow_html=True)
    col_area, col_clear_b = st.columns([5, 1])
    with col_area:
        input_key = "batch_input_" + str(st.session_state.clear_trigger)
        batch_text = st.text_area(
            "", placeholder="https://youtube.com/watch?v=...\nhttps://tiktok.com/@user/video/...\nhttps://instagram.com/p/...",
            height=110, label_visibility="collapsed", key=input_key
        )
        url_list = [u.strip() for u in batch_text.splitlines() if u.strip() and len(u.strip()) > 10]
        url = url_list[0] if url_list else ""
    with col_clear_b:
        st.markdown("<div style='margin-top:36px'></div>", unsafe_allow_html=True)
        if st.button("Clear", key="clear_b"):
            st.session_state.last_url = ''
            st.session_state.video_info = None
            st.session_state.clear_trigger += 1
            st.rerun()
    if url_list:
        st.caption(f"🔗 {len(url_list)} URL{'s' if len(url_list)>1 else ''} detected")
else:
    url_list = []
    col_in, col_paste, col_clear = st.columns([6, 1, 1])
    with col_in:
        input_key = "url_input_" + str(st.session_state.clear_trigger)
        url = st.text_input("", placeholder="Paste any URL here — YouTube, TikTok, Instagram, Facebook…",
                            label_visibility="collapsed", key=input_key)
    with col_paste:
        st.markdown("<div style='margin-top:4px'></div>", unsafe_allow_html=True)
        if st.button("Paste", key="paste_btn", use_container_width=True):
            try:
                import pyperclip
                c = pyperclip.paste()
                if c: st.session_state.pasted_url = c; st.rerun()
            except:
                st.toast("Paste manually (Ctrl+V)", icon="📋")
    with col_clear:
        st.markdown("<div style='margin-top:4px'></div>", unsafe_allow_html=True)
        if st.button("Clear", key="clear_btn", use_container_width=True):
            st.session_state.last_url = ''
            st.session_state.video_info = None
            st.session_state.clear_trigger += 1
            st.session_state.stage = 'idle'
            st.rerun()
    if 'pasted_url' in st.session_state:
        url = st.session_state.pasted_url
        del st.session_state.pasted_url

# ─── MODE / QUALITY / OPTIONS ──────────────────────────────────────────────────
col_mode, col_qual, col_dl = st.columns([2, 2, 1])
with col_mode:
    mode = st.selectbox("Type:", ["Auto Detect", "Video", "Audio Only", "Photo/Gallery"], index=0)
with col_qual:
    if mode == "Audio Only":
        quality = st.selectbox("Quality:", ["Best", "192kbps", "128kbps"], index=0)
    elif mode == "Photo/Gallery":
        quality = st.selectbox("Quality:", ["Best", "Original", "High", "Medium"], index=0)
    else:
        quality = st.selectbox("Quality:", ["Best","4K (2160p)","1440p","1080p","720p","480p","360p"], index=0)
with col_dl:
    st.markdown("<br>", unsafe_allow_html=True)
    download_clicked = st.button("⬇ Download", use_container_width=True, key="dl_btn")

# Advanced options expander
with st.expander("⚙️ Advanced Options"):
    opt_col1, opt_col2, opt_col3 = st.columns(3)
    with opt_col1:
        embed_subs  = st.checkbox("Embed Subtitles (EN)", value=False, disabled=not ffmpeg_ok)
    with opt_col2:
        embed_thumb = st.checkbox("Embed Thumbnail", value=False, disabled=not ffmpeg_ok)
    with opt_col3:
        show_hist   = st.checkbox("Show History Panel", value=True)
    if not ffmpeg_ok:
        st.caption("⚠ FFmpeg required for subtitle and thumbnail embedding.")

# ─── REAL-TIME FETCH TRIGGER ───────────────────────────────────────────────────
if url and url != st.session_state.last_url and len(url) > 10:
    st.session_state.last_url       = url
    st.session_state.video_info     = None
    st.session_state.download_error = None
    st.session_state.is_loading     = True
    st.session_state.stage          = 'fetch'
    st.rerun()

if st.session_state.is_loading and url:
    with st.spinner(""):
        info = fetch_video_info(url)
        st.session_state.video_info = info
        st.session_state.is_loading = False
        st.session_state.stage = 'preview' if info.get('success') else 'error'
        st.rerun()

# ─── PHASE BAR (only when active) ─────────────────────────────────────────────
current_stage = st.session_state.stage
if current_stage not in ('idle',):
    render_phase_bar(current_stage if current_stage != 'error' else 'fetch')

# ─── SHIMMER (loading) ─────────────────────────────────────────────────────────
if st.session_state.is_loading and url:
    st.markdown("""
    <div class="live-row">
        <span class="live-dot"></span>
        <span class="live-text">Fetching metadata<span class="live-step"> · analyzing URL…</span></span>
    </div>
    <div class="shimmer-card">
        <div class="shimmer-row">
            <div class="s-thumb"></div>
            <div class="s-body">
                <div class="s-line s-title"></div>
                <div class="s-line s-sub"></div>
                <div class="s-line s-sub" style="width:35%"></div>
                <div class="s-line s-tags"></div>
                <div class="s-metrics">
                    <div class="s-metric"></div>
                    <div class="s-metric"></div>
                    <div class="s-metric"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── ERROR ─────────────────────────────────────────────────────────────────────
elif st.session_state.video_info and not st.session_state.video_info.get('success'):
    err = st.session_state.video_info.get('error', 'Unknown error')
    st.markdown(f"""
    <div class="error-card">
        <div class="error-title">✕ Fetch Failed</div>
        {err}
    </div>
    """, unsafe_allow_html=True)
    # Contextual tips
    if 'reddit' in err.lower() or 'authentication' in err.lower():
        st.markdown('<div class="tip-card"><b>Reddit requires authentication.</b> Try a direct media URL or another platform.</div>', unsafe_allow_html=True)
    elif 'no video' in err.lower():
        st.markdown('<div class="tip-card"><b>Instagram photo post detected.</b> Switch mode to <b>Photo/Gallery</b> or use a Reel URL.</div>', unsafe_allow_html=True)

# ─── PREVIEW + DOWNLOAD ────────────────────────────────────────────────────────
elif st.session_state.video_info and st.session_state.video_info.get('success'):
    info     = st.session_state.video_info
    site     = get_site_name(info.get('extractor', 'generic'))
    ct       = info.get('content_type', 'video')
    ct_icon  = get_type_icon(ct)
    heights  = info.get('available_heights', [])
    qual_str = f" · Top quality: {heights[0]}p" if heights else ""

    st.markdown("<div class='preview-card'>", unsafe_allow_html=True)
    pc1, pc2 = st.columns([1, 2])
    with pc1:
        if info.get('thumbnail'):
            st.image(info['thumbnail'], use_container_width=True)
    with pc2:
        st.markdown(f"<div class='video-title'>{info['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='video-meta'>@{info['uploader']}  ·  {format_duration(info['duration'])}{qual_str}</div>",
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin:0.5rem 0 0.7rem">
            <span class="badge badge-platform">{site}</span>
            <span class="badge badge-type">{ct_icon} {ct.title()}</span>
            {"<span class='badge' style='background:rgba(168,85,247,0.1);color:#c084fc;border:1px solid rgba(168,85,247,0.25)'>CC Subtitles</span>" if info.get('has_subtitles') else ""}
        </div>
        """, unsafe_allow_html=True)
        if not info.get('is_youtube') and ct == 'video' and info.get('has_video'):
            st.markdown('<span style="color:#64748b; font-size:0.75rem">ℹ Quality selection auto-adjusted for this platform</span>',
                        unsafe_allow_html=True)
        mc = st.columns(3)
        for col, val, lbl in zip(mc,
            [format_size(info.get('filesize_approx')), format_count(info.get('view_count')), format_count(info.get('like_count'))],
            ['Est. Size', 'Views', 'Likes']):
            col.markdown(f'<div class="metric-box"><div class="metric-val">{val}</div><div class="metric-lbl">{lbl}</div></div>',
                         unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if not ffmpeg_ok and mode in ("Auto Detect", "Video") and ct == 'video':
        st.markdown('<div class="warn-card">⚠ FFmpeg not detected — single-file format, no quality merging.</div>',
                    unsafe_allow_html=True)

    # ── DOWNLOAD ────────────────────────────────────────────────────────────────
    urls_to_process = url_list if batch_mode and url_list else [url]

    if download_clicked:
        st.session_state.stage = 'downloading'
        render_phase_bar('downloading')

        all_results = []

        for i, dl_url in enumerate(urls_to_process):
            if batch_mode and len(urls_to_process) > 1:
                st.markdown(f"<div style='color:#64748b;font-size:0.8rem;margin:.4rem 0'>Processing {i+1}/{len(urls_to_process)} · <code>{dl_url[:60]}…</code></div>",
                            unsafe_allow_html=True)
                dl_info = fetch_video_info(dl_url) if dl_url != url else info
                if not dl_info.get('success'):
                    st.markdown(f'<div class="error-card"><b>Skip</b> — {dl_info.get("error","Fetch failed")}</div>',
                                unsafe_allow_html=True)
                    continue
            else:
                dl_info = info

            # ── Progress UI ────────────────────────────────────────────────────
            prog_bar    = st.progress(0)
            speed_slot  = st.empty()
            dl_error    = None
            file_bytes  = None
            file_name   = None
            mime_type   = "video/mp4"
            last_pct    = [0]

            def progress_hook(d):
                if d['status'] == 'downloading':
                    raw   = d.get('_percent_str', '0%').replace('%','').strip()
                    speed = d.get('_speed_str', '—')
                    eta   = d.get('_eta_str', '—')
                    try:
                        pct = min(int(float(raw)), 99)
                        last_pct[0] = pct
                        prog_bar.progress(pct, text=f"Downloading… {pct}%")
                        speed_slot.markdown(
                            f'<div class="dl-stats">⚡ Speed: <span class="dl-speed">{speed}</span> &nbsp;·&nbsp; ⏱ ETA: <span class="dl-eta">{eta}</span></div>',
                            unsafe_allow_html=True)
                    except: pass
                elif d['status'] == 'finished':
                    prog_bar.progress(100, text="Finalising…")
                    speed_slot.markdown(
                        '<div class="dl-stats">✓ <span style="color:#22c55e">Download complete · post-processing…</span></div>',
                        unsafe_allow_html=True)

            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    fmt  = get_format_string(quality, mode, ffmpeg_ok, dl_info)
                    opts = build_ydl_opts(fmt, tmpdir, progress_hook, ffmpeg_ok,
                                          mode, dl_info, embed_subs, embed_thumb)
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        ydl.download([dl_url])

                    files = [f for f in os.listdir(tmpdir) if os.path.isfile(os.path.join(tmpdir, f))]
                    if not files: raise Exception("Download completed but no output file found.")
                    file_name = files[0]
                    file_path = os.path.join(tmpdir, file_name)

                    ext = file_name.rsplit('.',1)[-1].lower()
                    mime_map = {'mp3':'audio/mpeg','webm':'video/webm','m4a':'audio/mp4',
                                'jpg':'image/jpeg','jpeg':'image/jpeg','png':'image/png',
                                'webp':'image/webp','mp4':'video/mp4'}
                    mime_type = mime_map.get(ext, 'video/mp4')

                    fsize = os.path.getsize(file_path)
                    if fsize > 500 * 1024 * 1024:
                        st.markdown('<div class="warn-card">⚠ File >500 MB — Streamlit Cloud may struggle. Consider running locally.</div>',
                                    unsafe_allow_html=True)

                    with open(file_path, 'rb') as f:
                        file_bytes = f.read()
            except Exception as e:
                dl_error = str(e)

            prog_bar.empty()
            speed_slot.empty()

            if dl_error:
                st.markdown(f'<div class="error-card"><div class="error-title">✕ Download Failed</div>{dl_error}</div>',
                            unsafe_allow_html=True)
                # Contextual help
                err_l = dl_error.lower()
                if "403" in dl_error or "forbidden" in err_l:
                    st.markdown("""<div class="tip-card">
                    <b>YouTube 403 — Cloud IP Blocked</b><br>
                    YouTube blocks AWS/GCP IPs used by Streamlit Cloud.<br><br>
                    <b>Fixes:</b><br>
                    1. Retry 2-3 times (transient blocks)<br>
                    2. Switch to <b>360p</b> or <b>Audio Only</b><br>
                    3. Run locally: <code>streamlit run streamlit_app.py</code><br>
                    4. Non-YouTube sites (TikTok, Instagram, Facebook) work fine on cloud.
                    </div>""", unsafe_allow_html=True)
                elif "too long" in err_l or "file name" in err_l:
                    st.markdown('<div class="tip-card"><b>Filename too long</b> — auto-truncation should handle this. Try again.</div>',
                                unsafe_allow_html=True)
                elif "requested format" in err_l:
                    st.markdown('<div class="tip-card"><b>Format unavailable.</b> Try switching to <b>Best</b> quality or <b>Auto Detect</b> mode.</div>',
                                unsafe_allow_html=True)
                elif "ffmpeg" in err_l or "merging" in err_l:
                    st.markdown('<div class="tip-card"><b>FFmpeg missing.</b> Add <code>ffmpeg</code> to packages.txt and redeploy.</div>',
                                unsafe_allow_html=True)
            elif file_bytes:
                st.session_state.stage = 'ready'
                add_to_history(dl_info, file_name, len(file_bytes))

                # ── Ready Card ──────────────────────────────────────────────────
                st.markdown(f"""
                <div class="ready-card">
                    <div class="ready-top">
                        <div class="ready-icon">✓</div>
                        <div>
                            <div class="ready-title">Ready to Download!</div>
                            <div class="ready-filename">{file_name}</div>
                        </div>
                    </div>
                    <div class="ready-size">📦 {format_size(len(file_bytes))} · Click the button below to save</div>
                </div>
                """, unsafe_allow_html=True)
                render_phase_bar('ready')

                st.download_button(
                    label=f"⬇  Save  {file_name}",
                    data=file_bytes,
                    file_name=file_name,
                    mime=mime_type,
                    use_container_width=True,
                    key=f"save_{int(time.time())}_{i}",
                )
                st.caption("File is served from memory and will be cleared on page refresh.")

# ─── HISTORY PANEL (main area) ────────────────────────────────────────────────
if show_hist and st.session_state.download_history:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='history-header'>🕘 Download History (this session)</div>", unsafe_allow_html=True)
    for h in st.session_state.download_history:
        icon = get_type_icon(h['type'])
        cols = st.columns([1, 4, 1])
        with cols[0]:
            if h.get('thumbnail'):
                st.image(h['thumbnail'], use_container_width=True)
        with cols[1]:
            st.markdown(f"""
            <div style="padding-top:4px">
                <div style="color:#cbd5e1;font-size:0.83rem;font-weight:500">{icon} {h['title']}</div>
                <div style="color:#475569;font-size:0.72rem">@{h['uploader']} · {h['site']} · {h['ts']}</div>
            </div>
            """, unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f"""
            <div style="text-align:right;padding-top:8px">
                <span style="color:#64748b;font-size:0.72rem">{h['file_size']}</span>
            </div>
            """, unsafe_allow_html=True)

# ─── EMPTY STATE ───────────────────────────────────────────────────────────────
if not url and current_stage == 'idle':
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0; color: #1e293b;">
        <div style="font-size:3rem; margin-bottom:0.5rem; opacity:0.4">⬇</div>
        <div style="color:#334155; font-size:0.85rem">Paste a URL above to get started</div>
        <div style="color:#1e293b; font-size:0.75rem; margin-top:0.4rem">
            YouTube · TikTok · Instagram · Facebook · Twitter/X · Vimeo · 1800+ more
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <div style="color:#334155; font-weight:600; font-family:'Syne',sans-serif; font-size:0.85rem; margin-bottom:0.3rem">
        Universal Downloader Pro
    </div>
    <div class="footer-accent">Powered by yt-dlp · Free & Open Source · No API keys · No limits</div>
    <div style="color:#1e293b; margin-top:0.3rem">
        YouTube · Instagram · TikTok · Facebook · Twitter/X · Reddit · Vimeo · 1800+ sites
    </div>
</div>
""", unsafe_allow_html=True)
