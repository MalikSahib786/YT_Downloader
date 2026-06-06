import streamlit as st
import yt_dlp
import os
import tempfile
import subprocess
from pathlib import Path
import time
import hashlib
from datetime import datetime

st.set_page_config(
    page_title="Universal Downloader Pro",
    page_icon="⬇️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════════════
#  CSS — PROFESSIONAL DARK THEME
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:      #06090f;
    --surface: #0b1018;
    --card:    #0e1520;
    --border:  #161f2e;
    --border2: #1c2a3d;
    --text:    #dce6f0;
    --muted:   #4a607a;
    --dim:     #1e2d40;
    --accent:  #ff5a1f;
    --accent2: #ff8c42;
    --green:   #10d97c;
    --blue:    #3b8bff;
    --red:     #ff3b5c;
    --font:    'Outfit', sans-serif;
    --mono:    'JetBrains Mono', monospace;
}

html, body, [class*="css"] {
    font-family: var(--font) !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Page background noise texture ── */
.stApp {
    background:
        radial-gradient(ellipse 80% 40% at 50% -10%, rgba(255,90,31,0.06) 0%, transparent 70%),
        var(--bg) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, .stDeployButton { visibility: hidden; display: none; }
header[data-testid="stHeader"] { background: transparent !important; }

/* ══════════════════════════════
   HEADER
══════════════════════════════ */
.udp-header {
    text-align: center;
    padding: 2.4rem 0 1rem;
}
.udp-wordmark {
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: -0.05em;
    line-height: 1;
    background: linear-gradient(135deg, #ff5a1f 0%, #ff8c42 55%, #ffb347 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.udp-sub {
    margin-top: 0.45rem;
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}
.udp-rule {
    margin: 1.2rem auto 1.8rem;
    height: 1px;
    max-width: 500px;
    background: linear-gradient(90deg, transparent 0%, var(--border2) 30%, var(--border2) 70%, transparent 100%);
}

/* ══════════════════════════════
   SEARCH BAR
══════════════════════════════ */

/* Remove ALL default Streamlit spacing around the input */
div[data-testid="stTextInput"] {
    margin: 0 !important;
    padding: 0 !important;
}
div[data-testid="stTextInput"] > div {
    margin: 0 !important;
}
div[data-testid="stTextInput"] > div > div {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

/* The actual input */
.udp-search-field input {
    height: 52px !important;
    background: var(--card) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border2) !important;
    border-right: none !important;
    border-radius: 16px 0 0 16px !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    padding: 0 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    outline: none !important;
}
.udp-search-field input:focus {
    border-color: rgba(255,90,31,0.5) !important;
    box-shadow: none !important;
}
.udp-search-field input::placeholder {
    color: var(--muted) !important;
    font-size: 0.8rem !important;
    font-family: var(--font) !important;
}

/* Side action button (paste / clear) */
.udp-side-btn button {
    height: 52px !important;
    min-width: 52px !important;
    background: var(--card) !important;
    border: 1.5px solid var(--border2) !important;
    border-left: none !important;
    border-right: none !important;
    border-radius: 0 !important;
    color: var(--muted) !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
    padding: 0 0.9rem !important;
    box-shadow: none !important;
    transition: background 0.2s, color 0.2s !important;
}
.udp-side-btn button:hover {
    background: var(--dim) !important;
    color: var(--text) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Analyze/search icon button */
.udp-go-btn button {
    height: 52px !important;
    width: 52px !important;
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    border: none !important;
    border-radius: 0 16px 16px 0 !important;
    color: white !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    padding: 0 !important;
    box-shadow: 0 0 20px rgba(255,90,31,0.3) !important;
    transition: box-shadow 0.25s, transform 0.2s !important;
}
.udp-go-btn button:hover {
    box-shadow: 0 0 30px rgba(255,90,31,0.5) !important;
    transform: scale(1.05) !important;
}
.udp-go-btn button:active {
    transform: scale(0.97) !important;
}

/* Seamless bar: remove column gaps */
div[data-testid="stHorizontalBlock"].udp-bar > div {
    padding-left: 0 !important;
    padding-right: 0 !important;
    gap: 0 !important;
}

/* ══════════════════════════════
   OPTIONS ROW
══════════════════════════════ */
.stSelectbox > div > div {
    background: var(--card) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 12px !important;
    font-family: var(--font) !important;
    font-size: 0.85rem !important;
    min-height: 42px !important;
}
div[data-testid="stSelectbox"] label {
    color: var(--muted) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ══════════════════════════════
   PRIMARY DOWNLOAD BUTTON
══════════════════════════════ */
.udp-dl-btn button {
    height: 52px !important;
    background: linear-gradient(135deg, #ff5a1f 0%, #ff8c42 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: var(--font) !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 4px 24px rgba(255,90,31,0.35) !important;
    transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}
.udp-dl-btn button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(255,90,31,0.5) !important;
}
.udp-dl-btn button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* Generic buttons */
.stButton > button {
    font-family: var(--font) !important;
}

/* ══════════════════════════════
   RESULT CARD
══════════════════════════════ */
.result-card {
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 20px;
    padding: 1.4rem;
    margin: 1.2rem 0 0.8rem;
    box-shadow: 0 16px 48px rgba(0,0,0,0.6);
    animation: slideUp 0.45s cubic-bezier(0.22,1,0.36,1) both;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(16px) scale(0.98); }
    to   { opacity: 1; transform: translateY(0)    scale(1);    }
}
.rc-top { display: flex; gap: 1.1rem; }
.rc-thumb-wrap {
    width: 170px; min-width: 170px;
    border-radius: 12px; overflow: hidden;
    background: var(--dim);
    aspect-ratio: 16/9;
}
.rc-thumb-wrap img { width:100%; height:100%; object-fit:cover; display:block; }
.rc-info { flex: 1; min-width: 0; }
.rc-title {
    font-size: 0.98rem; font-weight: 700;
    color: var(--text); line-height: 1.45;
    margin-bottom: 0.3rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.rc-uploader { color: var(--muted); font-size: 0.78rem; margin-bottom: 0.55rem; }
.rc-badges { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 0.7rem; }
.badge {
    display: inline-flex; align-items: center; gap: 3px;
    padding: 3px 9px; border-radius: 20px;
    font-size: 0.66rem; font-weight: 700;
    letter-spacing: 0.06em; text-transform: uppercase;
}
.b-platform { background:rgba(255,90,31,.1);  color:#ff7a40;  border:1px solid rgba(255,90,31,.2);  }
.b-type     { background:rgba(16,217,124,.08); color:#10d97c;  border:1px solid rgba(16,217,124,.18); }
.b-subs     { background:rgba(59,139,255,.08); color:#3b8bff;  border:1px solid rgba(59,139,255,.18); }
.rc-stats { display:flex; gap:8px; margin-top:auto; }
.stat-pill {
    flex:1; text-align:center;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px; padding: 0.6rem 0.3rem;
}
.stat-val { font-size:1.0rem; font-weight:800; color:var(--text); line-height:1; }
.stat-lbl { font-size:0.6rem; color:var(--muted); text-transform:uppercase; letter-spacing:.07em; margin-top:3px; }

/* Options bar inside result */
.options-strip {
    display: flex; align-items: center; gap: 10px;
    padding: 1rem 0 0;
    border-top: 1px solid var(--border);
    margin-top: 1rem;
}
.opt-label { color:var(--muted); font-size:0.72rem; font-weight:600; letter-spacing:.06em; text-transform:uppercase; white-space:nowrap; }

/* ══════════════════════════════
   SHIMMER SKELETON
══════════════════════════════ */
@keyframes shimmerSweep {
    0%   { background-position: -400px 0; }
    100% { background-position:  400px 0; }
}
.sk-base {
    background: linear-gradient(
        90deg,
        var(--card) 0%,
        var(--border) 20%,
        #1e3050 40%,
        var(--border) 60%,
        var(--card) 80%
    );
    background-size: 800px 100%;
    animation: shimmerSweep 1.7s ease-in-out infinite;
    border-radius: 6px;
}
.shimmer-card {
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 20px;
    padding: 1.4rem;
    margin: 1.2rem 0;
}
.sk-row { display:flex; gap:1.1rem; align-items:flex-start; }
.sk-thumb { width:170px; min-width:170px; height:96px; border-radius:12px; }
.sk-body { flex:1; }
.sk-line { height:14px; margin-bottom:10px; }
.sk-t1 { width:82%; height:18px; }
.sk-t2 { width:52%; height:12px; }
.sk-t3 { width:30%; height:20px; border-radius:20px; }
.sk-stats { display:flex; gap:8px; margin-top:12px; }
.sk-stat { flex:1; height:62px; border-radius:10px; }
.sk-opts { height:44px; border-radius:12px; margin-top:14px; }

/* Fetch indicator */
.fetch-row {
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 0.7rem;
    animation: fadeIn 0.3s ease;
}
.fetch-dot {
    width:8px; height:8px; border-radius:50%;
    background: var(--accent);
    animation: fetchPulse 1.3s ease-in-out infinite;
}
@keyframes fetchPulse {
    0%,100% { opacity:1; transform:scale(1); box-shadow:0 0 0 0 rgba(255,90,31,0.5); }
    50%      { opacity:.7; transform:scale(1.3); box-shadow:0 0 0 6px rgba(255,90,31,0); }
}
.fetch-txt { font-size:0.8rem; color:var(--muted); font-weight:500; }
.fetch-step { color:var(--accent); font-weight:600; }

/* ══════════════════════════════
   STATUS CARDS
══════════════════════════════ */
.ready-wrap {
    background: linear-gradient(135deg, #041710 0%, #061d14 100%);
    border: 1.5px solid rgba(16,217,124,.28);
    border-radius: 16px; padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    box-shadow: 0 0 32px rgba(16,217,124,.08);
    animation: readyPop 0.55s cubic-bezier(0.34,1.56,.64,1) both;
}
@keyframes readyPop {
    from { opacity:0; transform:scale(0.93); }
    to   { opacity:1; transform:scale(1);    }
}
.ready-row { display:flex; align-items:center; gap:10px; }
.ready-ico {
    width:38px; height:38px; border-radius:50%;
    background: rgba(16,217,124,.12);
    border: 1px solid rgba(16,217,124,.25);
    display:flex; align-items:center; justify-content:center;
    font-size:1.1rem; flex-shrink:0;
}
.ready-title { font-size:0.95rem; font-weight:800; color:var(--green); }
.ready-file  { font-family:var(--mono); font-size:0.77rem; color:#5efaa3; margin-top:1px; }
.ready-meta  { font-size:0.72rem; color:var(--muted); margin-top:2px; }

.err-wrap {
    background: linear-gradient(135deg, #140508, #100306);
    border: 1px solid rgba(255,59,92,.25);
    border-radius: 14px; padding: 1rem 1.1rem;
    animation: fadeIn 0.3s ease;
}
.err-title { font-size:0.85rem; font-weight:700; color:var(--red); margin-bottom:3px; }
.err-body  { font-size:0.8rem; color:#ff8fa0; line-height:1.6; }
.tip-wrap {
    background: var(--card);
    border: 1px solid var(--border2);
    border-left: 3px solid var(--accent);
    border-radius: 10px; padding: 0.85rem 1rem;
    margin-top: 0.5rem;
    font-size: 0.79rem; color:#7a9ab8; line-height:1.7;
}
.tip-wrap b { color: var(--accent2); }
.warn-wrap {
    background: #0d0a00;
    border: 1px solid rgba(255,180,0,.2);
    border-radius: 10px; padding: 0.7rem 0.9rem;
    font-size:0.78rem; color:#fcd34d; margin:0.4rem 0;
}

/* Download button (main CTA inside result) */
.stDownloadButton > button {
    width: 100% !important;
    height: 52px !important;
    background: linear-gradient(135deg, #10d97c 0%, #05b860 100%) !important;
    color: #021a0e !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: var(--font) !important;
    font-size: 1rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 24px rgba(16,217,124,.35) !important;
    transition: all 0.25s cubic-bezier(0.34,1.56,.64,1) !important;
    margin-top: 0.3rem !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(16,217,124,.5) !important;
}

/* Progress bar */
.stProgress > div > div > div { background: linear-gradient(90deg, var(--accent), var(--accent2)) !important; }
.stProgress > div > div { background: var(--border) !important; border-radius: 99px !important; }

/* History */
.hist-title { font-size:0.7rem; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:.1em; margin:1.6rem 0 0.6rem; }
.hist-item {
    display:flex; align-items:center; gap:10px;
    background: var(--card); border:1px solid var(--border);
    border-radius:12px; padding:0.6rem 0.8rem;
    margin-bottom:5px;
    transition: border-color .2s;
}
.hist-item:hover { border-color: var(--border2); }
.hist-thumb { width:46px; height:30px; border-radius:6px; object-fit:cover; background:var(--dim); flex-shrink:0; }
.hist-name  { font-size:0.78rem; color:#b0c4d8; font-weight:500; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; flex:1; }
.hist-meta  { font-size:0.65rem; color:var(--muted); white-space:nowrap; }

/* Checkbox */
.stCheckbox label { color:var(--muted) !important; font-size:0.82rem !important; }

@keyframes fadeIn { from{opacity:0} to{opacity:1} }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stMarkdown p { color:var(--muted) !important; font-size:0.8rem !important; }

/* Footer */
.udp-footer {
    text-align:center; padding:2rem 0 1rem;
    border-top:1px solid var(--border);
    margin-top:2.5rem;
    color:var(--dim);
    font-size:0.72rem; line-height:1.9;
}

/* expander */
details summary { color: var(--muted) !important; font-size: 0.8rem !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  PURE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource(show_spinner=False)
def check_ffmpeg():
    try:
        r = subprocess.run(["ffmpeg","-version"], capture_output=True, text=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def base_opts():
    return {
        'quiet': True, 'no_warnings': True,
        'extractor_args': {'youtube': {'player_js_version':'actual','player_client':'web_safari'}},
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.youtube.com/',
        },
        'geo_bypass': True,
    }


def fetch_info(url):
    opts = base_opts(); opts['skip_download'] = True
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info  = ydl.extract_info(url, download=False)
            fmts  = info.get('formats', [])
            ext   = info.get('extractor','generic').lower()
            heights = sorted({f['height'] for f in fmts if f.get('height') and f['height']>0}, reverse=True)
            has_v = any(f.get('vcodec')!='none' for f in fmts)
            has_a = any(f.get('acodec')!='none' for f in fmts)
            has_i = any(f.get('ext') in ('jpg','jpeg','png','webp') for f in fmts)
            ct = 'photo' if (has_i and not has_v) else 'gallery' if (not has_v and not has_a and not has_i and info.get('entries')) else 'video'
            return {
                'title':      info.get('title','Unknown'),
                'uploader':   info.get('uploader', info.get('channel', info.get('uploader_id','Unknown'))),
                'duration':   info.get('duration') or 0,
                'thumbnail':  info.get('thumbnail',''),
                'view_count': info.get('view_count') or 0,
                'like_count': info.get('like_count') or 0,
                'filesize':   info.get('filesize_approx') or 0,
                'extractor':  ext,
                'is_youtube': 'youtube' in ext,
                'has_height_formats': bool(heights),
                'has_video':  has_v, 'has_audio': has_a, 'has_image': has_i,
                'content_type': ct,
                'entries':    info.get('entries',[]),
                'heights':    heights,
                'has_subs':   bool(info.get('subtitles') or info.get('automatic_captions')),
                'success': True,
            }
    except Exception as e:
        return {'error': str(e), 'success': False}


def fmt_dur(s):
    if not s: return '—'
    m,s=divmod(int(s),60); h,m=divmod(m,60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def fmt_sz(b):
    if not b: return '—'
    b=float(b)
    for u in ['B','KB','MB','GB']:
        if b<1024: return f"{b:.1f} {u}"
        b/=1024
    return f"{b:.1f} TB"

def fmt_n(n):
    if not n: return '0'
    n=float(n)
    if n>=1e9: return f"{n/1e9:.1f}B"
    if n>=1e6: return f"{n/1e6:.1f}M"
    if n>=1e3: return f"{n/1e3:.1f}K"
    return str(int(n))

def clean_name(t, mx=80):
    if not t: t='download'
    s = ''.join(c if c.isalnum() or c in ' ._-' else '_' for c in t).strip('._')
    if len(s)>mx:
        s = s[:mx-7]+'_'+hashlib.md5(s.encode()).hexdigest()[:6]
    return s or 'download'

def site_name(ext):
    for k,n in [('youtube','YouTube'),('instagram','Instagram'),('facebook','Facebook'),
                ('tiktok','TikTok'),('twitter','Twitter/X'),('reddit','Reddit'),
                ('vimeo','Vimeo'),('twitch','Twitch'),('dailymotion','Dailymotion')]:
        if k in ext: return n
    return ext.replace('ie','').title()

def type_icon(ct):
    return {'video':'▶','photo':'◈','gallery':'⊞','audio':'♫'}.get(ct,'◉')

def get_fmt_str(quality, mode, ffmpeg_ok, info):
    ct = info.get('content_type','video')
    if ct=='photo': return 'best'
    if mode=='Audio Only':
        return 'bestaudio/best' if ffmpeg_ok else 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio'
    if not info.get('is_youtube') or not info.get('has_height_formats'):
        return 'best/bestvideo+bestaudio'
    hmap = {'Best':None,'4K (2160p)':2160,'1440p':1440,'1080p':1080,'720p':720,'480p':480,'360p':360}
    th = hmap.get(quality)
    if ffmpeg_ok:
        if th: return (f"bestvideo[height<={th}][vcodec!*=av01]+bestaudio[acodec!*=opus]"
                       f"/bestvideo[height<={th}]+bestaudio/best[height<={th}]")
        return 'bestvideo[vcodec!*=av01]+bestaudio[acodec!*=opus]/bestvideo+bestaudio/best'
    return f'best[height<={th}]/best' if th else 'best/bestvideo+bestaudio'

def build_opts(fmt, outdir, hook, ffmpeg_ok, mode, info, subs=False, thumb=False):
    opts = base_opts()
    opts.update({'format':fmt,
                 'outtmpl': os.path.join(outdir, clean_name(info.get('title','download'))+'.%(ext)s'),
                 'progress_hooks':[hook], 'noplaylist':True,
                 'retries':10, 'fragment_retries':10, 'continue_dl':True})
    ct = info.get('content_type','video'); post=[]
    if ct=='photo':
        if info.get('entries'): opts['noplaylist']=False
    elif ffmpeg_ok and mode=='Audio Only':
        post.append({'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192'})
        if thumb: post.append({'key':'EmbedThumbnail'})
    elif ffmpeg_ok and mode!='Audio Only' and '+' in fmt:
        opts['merge_output_format']='mp4'
    if ffmpeg_ok and subs and mode!='Audio Only':
        opts.update({'writesubtitles':True,'writeautomaticsub':True,'subtitleslangs':['en','en-US']})
        post.append({'key':'FFmpegSubtitlesConvertor','format':'srt'})
    if post: opts['postprocessors']=post
    return opts

def add_history(info, fname, fsize):
    if 'history' not in st.session_state: st.session_state.history=[]
    st.session_state.history.insert(0,{
        'title':    info.get('title','')[:55],
        'uploader': info.get('uploader',''),
        'thumb':    info.get('thumbnail',''),
        'site':     site_name(info.get('extractor','generic')),
        'type':     info.get('content_type','video'),
        'fname':    fname, 'fsize': fmt_sz(fsize),
        'ts':       datetime.now().strftime('%H:%M'),
    })
    st.session_state.history = st.session_state.history[:8]


# ═══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
for k,v in {'last_url':'','video_info':None,'is_loading':False,
            'download_error':None,'clear_t':0,'history':[],'url_val':''}.items():
    if k not in st.session_state: st.session_state[k]=v

ffmpeg_ok = check_ffmpeg()

# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### System")
    if ffmpeg_ok:
        st.success("✓ FFmpeg ready")
    else:
        st.warning("⚠ FFmpeg missing")
    st.markdown("---")
    st.markdown("### Setup Files")
    st.code("requirements.txt:\nstreamlit\nyt-dlp\n\npackages.txt:\nffmpeg", language="text")
    st.markdown("---")
    if st.session_state.history:
        st.markdown("### Recent")
        for h in st.session_state.history[:5]:
            st.markdown(f"""
            <div class="hist-item">
                {'<img class="hist-thumb" src="'+h['thumb']+'">' if h.get('thumb') else '<div class="hist-thumb"></div>'}
                <div class="hist-name">{type_icon(h['type'])} {h['title']}</div>
                <div class="hist-meta">{h['fsize']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Only download content you own or have rights to.")


# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="udp-header">
    <div class="udp-wordmark">Universal Downloader</div>
    <div class="udp-sub">Videos · Photos · Reels · Stories · 1800+ Sites</div>
</div>
<div class="udp-rule"></div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  SEARCH BAR  (paste/clear inside the bar)
# ═══════════════════════════════════════════════════════════════════════════════
url_has_text = bool(st.session_state.url_val)

# Inject CSS class on the columns block
st.markdown('<div class="udp-bar">', unsafe_allow_html=True)

# col widths: input | paste-or-clear | go-button
c_input, c_action, c_go = st.columns([10, 1.1, 1.1])

with c_input:
    st.markdown('<div class="udp-search-field">', unsafe_allow_html=True)
    url_input = st.text_input(
        "", key=f"url_{st.session_state.clear_t}",
        placeholder="  Paste a URL from YouTube, TikTok, Instagram, Facebook…",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    # sync to session
    if url_input != st.session_state.url_val:
        st.session_state.url_val = url_input

with c_action:
    st.markdown('<div class="udp-side-btn">', unsafe_allow_html=True)
    if url_has_text:
        # Clear button (X)
        if st.button("✕", key="clear_btn", help="Clear URL"):
            st.session_state.url_val   = ''
            st.session_state.last_url  = ''
            st.session_state.video_info= None
            st.session_state.is_loading= False
            st.session_state.clear_t  += 1
            st.rerun()
    else:
        # Paste button
        if st.button("⎘", key="paste_btn", help="Paste from clipboard"):
            try:
                import pyperclip
                clip = pyperclip.paste()
                if clip:
                    st.session_state.url_val = clip
                    st.rerun()
            except:
                st.toast("Use Ctrl+V to paste", icon="📋")
    st.markdown('</div>', unsafe_allow_html=True)

with c_go:
    st.markdown('<div class="udp-go-btn">', unsafe_allow_html=True)
    analyze_clicked = st.button("⌕", key="go_btn", help="Analyze URL")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

url = st.session_state.url_val.strip()

# Manual trigger via button OR auto-trigger on URL change
trigger_fetch = (analyze_clicked and url and url != st.session_state.last_url) or \
                (url and url != st.session_state.last_url and len(url) > 10)

if trigger_fetch:
    st.session_state.last_url    = url
    st.session_state.video_info  = None
    st.session_state.download_error = None
    st.session_state.is_loading  = True
    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  SHIMMER → FETCH → RESULT
# ═══════════════════════════════════════════════════════════════════════════════
SHIMMER_HTML = """
<div class="fetch-row">
    <span class="fetch-dot"></span>
    <span class="fetch-txt">Analyzing URL<span class="fetch-step"> · fetching metadata…</span></span>
</div>
<div class="shimmer-card">
    <div class="sk-row">
        <div class="sk-base sk-thumb"></div>
        <div class="sk-body" style="flex:1">
            <div class="sk-base sk-line sk-t1"></div>
            <div class="sk-base sk-line sk-t2"></div>
            <div class="sk-base sk-line sk-t3"></div>
            <div class="sk-stats">
                <div class="sk-base sk-stat"></div>
                <div class="sk-base sk-stat" style="animation-delay:.12s"></div>
                <div class="sk-base sk-stat" style="animation-delay:.24s"></div>
            </div>
        </div>
    </div>
    <div class="sk-base sk-opts" style="margin-top:14px"></div>
</div>
"""

# ── THE KEY FIX: render shimmer FIRST, then block on fetch ──
if st.session_state.is_loading:
    slot = st.empty()
    slot.markdown(SHIMMER_HTML, unsafe_allow_html=True)
    # This blocking call happens AFTER shimmer is already rendered to the browser
    result = fetch_info(st.session_state.last_url)
    st.session_state.video_info  = result
    st.session_state.is_loading  = False
    slot.empty()
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
#  ERROR STATE
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.video_info and not st.session_state.video_info.get('success'):
    err = st.session_state.video_info.get('error','Unknown error')
    st.markdown(f"""
    <div class="err-wrap">
        <div class="err-title">✕ Failed to fetch</div>
        <div class="err-body">{err}</div>
    </div>
    """, unsafe_allow_html=True)
    if 'authentication' in err.lower() or 'reddit' in err.lower():
        st.markdown('<div class="tip-wrap"><b>Reddit</b> requires authentication. Try a direct media URL or another platform.</div>', unsafe_allow_html=True)
    elif 'no video' in err.lower():
        st.markdown('<div class="tip-wrap"><b>Instagram photo post</b> detected. Switch mode to <b>Photo/Gallery</b> or use a Reel URL.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  RESULT CARD + INTEGRATED DOWNLOAD
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.video_info and st.session_state.video_info.get('success'):
    info = st.session_state.video_info
    sname = site_name(info['extractor'])
    ct    = info['content_type']
    ci    = type_icon(ct)
    hs    = info.get('heights', [])
    qtop  = f" · {hs[0]}p top quality" if hs else ""

    subs_badge = '<span class="badge b-subs">CC</span>' if info.get('has_subs') else ''
    non_yt_note = ('<div style="color:var(--muted);font-size:0.7rem;margin-top:3px">Quality auto-adjusted for this platform</div>'
                   if not info.get('is_youtube') and ct=='video' and info.get('has_video') else '')

    # ── Main result card ──────────────────────────────────────────────────────
    thumb_html = (f'<img src="{info["thumbnail"]}" style="width:100%;height:100%;object-fit:cover;border-radius:12px">'
                  if info.get('thumbnail') else '')

    st.markdown(f"""
    <div class="result-card">
        <div class="rc-top">
            <div class="rc-thumb-wrap">{thumb_html}</div>
            <div class="rc-info">
                <div class="rc-title">{info['title']}</div>
                <div class="rc-uploader">@{info['uploader']} &nbsp;·&nbsp; {fmt_dur(info['duration'])}{qtop}</div>
                <div class="rc-badges">
                    <span class="badge b-platform">{sname}</span>
                    <span class="badge b-type">{ci} {ct.title()}</span>
                    {subs_badge}
                </div>
                {non_yt_note}
                <div class="rc-stats">
                    <div class="stat-pill"><div class="stat-val">{fmt_sz(info['filesize'])}</div><div class="stat-lbl">Est. Size</div></div>
                    <div class="stat-pill"><div class="stat-val">{fmt_n(info['view_count'])}</div><div class="stat-lbl">Views</div></div>
                    <div class="stat-pill"><div class="stat-val">{fmt_n(info['like_count'])}</div><div class="stat-lbl">Likes</div></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Options + Download (integrated below the card) ────────────────────────
    st.markdown('<div style="background:var(--card);border:1px solid var(--border2);border-radius:16px;padding:1rem 1.2rem;margin-top:-0.4rem">', unsafe_allow_html=True)

    oc1, oc2, oc3 = st.columns([2, 2, 2])
    with oc1:
        mode = st.selectbox("Type", ["Auto Detect","Video","Audio Only","Photo/Gallery"], index=0, key="mode_sel")
    with oc2:
        if mode=="Audio Only":    qopts = ["Best","192kbps","128kbps"]
        elif mode=="Photo/Gallery": qopts = ["Best","Original","High","Medium"]
        else:                     qopts = ["Best","4K (2160p)","1440p","1080p","720p","480p","360p"]
        quality = st.selectbox("Quality", qopts, index=0, key="qual_sel")
    with oc3:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        embed_subs  = st.checkbox("Subtitles", value=False, disabled=not ffmpeg_ok, key="subs_chk")
        embed_thumb = st.checkbox("Embed Art",  value=False, disabled=not ffmpeg_ok, key="thumb_chk")

    if not ffmpeg_ok:
        st.markdown('<div class="warn-wrap" style="margin:0.3rem 0 0.6rem">⚠ FFmpeg missing — quality merging and subtitle embedding unavailable.</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="udp-dl-btn">', unsafe_allow_html=True)
    dl_clicked = st.button("⬇  Download Now", use_container_width=True, key="dl_btn")
    st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Download logic ────────────────────────────────────────────────────────
    if dl_clicked:
        prog = st.progress(0, text="Initialising…")
        spd  = st.empty()
        dl_err = None; file_bytes = None; file_name = None; mime = "video/mp4"

        def hook(d):
            if d['status']=='downloading':
                raw   = d.get('_percent_str','0%').replace('%','').strip()
                speed = d.get('_speed_str','—')
                eta   = d.get('_eta_str','—')
                try:
                    pct = min(int(float(raw)), 99)
                    prog.progress(pct, text=f"Downloading… {pct}%")
                    spd.markdown(
                        f'<div style="font-size:.78rem;color:var(--muted);padding:2px 0">'
                        f'⚡ <span style="color:#3b8bff;font-weight:600">{speed}</span>'
                        f' &nbsp;·&nbsp; ⏱ <span style="color:#a78bfa;font-weight:600">{eta}</span></div>',
                        unsafe_allow_html=True)
                except: pass
            elif d['status']=='finished':
                prog.progress(100, text="Post-processing…")
                spd.markdown('<div style="font-size:.78rem;color:var(--green)">✓ Complete · finalising file…</div>',
                             unsafe_allow_html=True)

        try:
            with tempfile.TemporaryDirectory() as tmp:
                fmt  = get_fmt_str(quality, mode, ffmpeg_ok, info)
                opts = build_opts(fmt, tmp, hook, ffmpeg_ok, mode, info, embed_subs, embed_thumb)
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
                files = [f for f in os.listdir(tmp) if os.path.isfile(os.path.join(tmp,f))]
                if not files: raise Exception("Download completed but no output file was created.")
                file_name = files[0]
                fpath = os.path.join(tmp, file_name)
                ext   = file_name.rsplit('.',1)[-1].lower()
                mime  = {'mp3':'audio/mpeg','m4a':'audio/mp4','webm':'video/webm',
                         'jpg':'image/jpeg','jpeg':'image/jpeg','png':'image/png','webp':'image/webp'}.get(ext,'video/mp4')
                fsz = os.path.getsize(fpath)
                if fsz > 500*1024*1024:
                    st.markdown('<div class="warn-wrap">⚠ File >500 MB — Streamlit Cloud may struggle. Run locally for large files.</div>', unsafe_allow_html=True)
                with open(fpath,'rb') as f: file_bytes=f.read()
        except Exception as e:
            dl_err = str(e)

        prog.empty(); spd.empty()

        if dl_err:
            st.markdown(f'<div class="err-wrap"><div class="err-title">✕ Download Failed</div><div class="err-body">{dl_err}</div></div>',
                        unsafe_allow_html=True)
            el = dl_err.lower()
            if '403' in dl_err or 'forbidden' in el:
                st.markdown("""<div class="tip-wrap">
                <b>YouTube 403 — Cloud IP Blocked</b><br>
                Retry 2-3× · lower quality (360p/Audio) · or run locally:<br>
                <code>pip install streamlit yt-dlp && streamlit run streamlit_app.py</code>
                </div>""", unsafe_allow_html=True)
            elif 'requested format' in el:
                st.markdown('<div class="tip-wrap"><b>Format unavailable.</b> Switch to <b>Best</b> quality or <b>Auto Detect</b>.</div>', unsafe_allow_html=True)
            elif 'ffmpeg' in el or 'merging' in el:
                st.markdown('<div class="tip-wrap"><b>FFmpeg missing.</b> Add <code>ffmpeg</code> to packages.txt and redeploy.</div>', unsafe_allow_html=True)
            elif 'too long' in el or 'file name' in el:
                st.markdown('<div class="tip-wrap"><b>Filename too long</b> — retry, auto-truncation is active.</div>', unsafe_allow_html=True)
        elif file_bytes:
            add_history(info, file_name, len(file_bytes))
            st.markdown(f"""
            <div class="ready-wrap">
                <div class="ready-row">
                    <div class="ready-ico">✓</div>
                    <div>
                        <div class="ready-title">Ready to Save!</div>
                        <div class="ready-file">{file_name}</div>
                        <div class="ready-meta">📦 {fmt_sz(len(file_bytes))} · click the button below</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label=f"⬇  Save  {file_name}",
                data=file_bytes, file_name=file_name, mime=mime,
                use_container_width=True, key=f"save_{int(time.time())}"
            )

# ── Empty state ──────────────────────────────────────────────────────────────
if not url and not st.session_state.video_info:
    st.markdown("""
    <div style="text-align:center;padding:2.5rem 0 1rem;animation:fadeIn .5s ease">
        <div style="font-size:2.8rem;opacity:.12;margin-bottom:.7rem">⬇</div>
        <div style="color:var(--dim);font-size:.85rem;font-weight:500">Paste any URL to get started</div>
        <div style="color:var(--border2);font-size:.72rem;margin-top:.4rem">
            YouTube · TikTok · Instagram · Facebook · Twitter/X · Vimeo · 1800+ more
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── History ──────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="hist-title">Recent Downloads</div>', unsafe_allow_html=True)
    for h in st.session_state.history:
        st.markdown(f"""
        <div class="hist-item">
            {'<img class="hist-thumb" src="'+h["thumb"]+'">' if h.get("thumb") else '<div class="hist-thumb"></div>'}
            <div class="hist-name">{type_icon(h["type"])} {h["title"]}</div>
            <div class="hist-meta">{h["site"]} · {h["ts"]} · {h["fsize"]}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="udp-footer">
    <span style="color:#1c2a3d;font-weight:700;font-size:.8rem">Universal Downloader Pro</span><br>
    Powered by yt-dlp · Free & Open Source · No API keys · No limits<br>
    YouTube · Instagram · TikTok · Facebook · Twitter/X · Reddit · Vimeo · 1800+ sites
</div>
""", unsafe_allow_html=True)
