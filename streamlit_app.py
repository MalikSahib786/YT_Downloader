import streamlit as st
import yt_dlp
import os
import tempfile
import subprocess
from pathlib import Path
import time
import hashlib
from datetime import datetime
import base64
import urllib.request

st.set_page_config(
    page_title="Universal Downloader Pro",
    page_icon="⬇️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════════════
#  CSS — PREMIUM DARK THEME (Fixed & Polished)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --bg:       #080c12;
    --surface:  #0c1119;
    --card:     #0f1622;
    --card2:    #111a28;
    --border:   #182230;
    --border2:  #1e2d42;
    --border3:  #243650;
    --text:     #d8e8f5;
    --text2:    #8fadc8;
    --muted:    #3f5470;
    --dim:      #172030;
    --accent:   #f95f1a;
    --accent2:  #ff8944;
    --accent3:  #ffb347;
    --green:    #00e87b;
    --green2:   #00c468;
    --blue:     #3d8eff;
    --red:      #ff3b5c;
    --purple:   #9b6dff;
    --font:     'DM Sans', sans-serif;
    --display:  'Syne', sans-serif;
    --mono:     'DM Mono', monospace;
    --r-card:   18px;
    --r-input:  14px;
    --r-btn:    12px;
    --shadow:   0 20px 60px rgba(0,0,0,0.7);
    --glow-o:   0 0 32px rgba(249,95,26,0.25);
    --glow-g:   0 0 32px rgba(0,232,123,0.25);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: var(--font) !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background:
        radial-gradient(ellipse 90% 50% at 50% -5%, rgba(249,95,26,0.07) 0%, transparent 65%),
        radial-gradient(ellipse 60% 30% at 80% 80%, rgba(0,100,255,0.03) 0%, transparent 60%),
        var(--bg) !important;
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, .stDeployButton,
[data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; height: 0 !important; }

/* ── Block container ── */
.block-container {
    max-width: 780px !important;
    padding: 0 1.2rem 3rem !important;
}

/* ════════════════════════════════════════
   HEADER
════════════════════════════════════════ */
.udp-header {
    text-align: center;
    padding: 3rem 0 1.2rem;
}
.udp-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 54px; height: 54px;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(249,95,26,0.15), rgba(255,137,68,0.08));
    border: 1px solid rgba(249,95,26,0.25);
    font-size: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--glow-o), inset 0 1px 0 rgba(255,255,255,0.05);
}
.udp-wordmark {
    font-family: var(--display) !important;
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
    background: linear-gradient(135deg, #f95f1a 0%, #ff8944 50%, #ffb347 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.udp-sub {
    margin-top: 0.5rem;
    color: var(--muted);
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}
.udp-rule {
    margin: 1.5rem auto 2rem;
    height: 1px;
    max-width: 400px;
    background: linear-gradient(90deg, transparent, var(--border3) 30%, var(--border3) 70%, transparent);
}

/* ════════════════════════════════════════
   SEARCH BAR
════════════════════════════════════════ */
.search-wrap {
    position: relative;
    display: flex;
    align-items: stretch;
    background: var(--card);
    border: 1.5px solid var(--border2);
    border-radius: 16px;
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
.search-wrap:focus-within {
    border-color: rgba(249,95,26,0.45);
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), 0 0 0 3px rgba(249,95,26,0.08);
}

div[data-testid="stTextInput"] {
    flex: 1; margin: 0 !important; padding: 0 !important;
}
div[data-testid="stTextInput"] > div {
    margin: 0 !important; padding: 0 !important;
}
div[data-testid="stTextInput"] > div > div {
    border: none !important; box-shadow: none !important;
    background: transparent !important; border-radius: 0 !important;
}
div[data-testid="stTextInput"] input {
    height: 54px !important;
    background: transparent !important;
    color: var(--text) !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    font-weight: 400 !important;
    padding: 0 1.1rem !important;
    outline: none !important;
    box-shadow: none !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: var(--muted) !important;
    font-size: 0.79rem !important;
    font-family: var(--font) !important;
    font-weight: 400 !important;
}

/* Buttons inside search bar */
.sb-action button, .sb-go button {
    height: 54px !important;
    border: none !important;
    border-radius: 0 !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 0 1rem !important;
    cursor: pointer !important;
    box-shadow: none !important;
    transition: all 0.18s ease !important;
    outline: none !important;
}
.sb-action button {
    background: transparent !important;
    color: var(--muted) !important;
    border-left: 1px solid var(--border2) !important;
    min-width: 48px !important;
}
.sb-action button:hover {
    background: var(--dim) !important;
    color: var(--text2) !important;
    transform: none !important;
}
.sb-go button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important;
    min-width: 54px !important;
    font-size: 1.1rem !important;
    border-left: 1px solid rgba(249,95,26,0.3) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
.sb-go button:hover {
    background: linear-gradient(135deg, #ff6f2e, #ff9954) !important;
    transform: none !important;
}

/* Kill column gaps inside search bar */
div[data-testid="stHorizontalBlock"].searchbar-cols > div[data-testid="stColumn"] {
    padding: 0 !important; gap: 0 !important; flex-shrink: 0 !important;
}
div[data-testid="stHorizontalBlock"].searchbar-cols > div[data-testid="stColumn"]:first-child {
    flex: 1 1 auto !important;
}

/* ════════════════════════════════════════
   SHIMMER SKELETON
════════════════════════════════════════ */
@keyframes shimmerSweep {
    0%   { background-position: -500px 0; }
    100% { background-position:  500px 0; }
}
.sk-base {
    background: linear-gradient(
        90deg,
        var(--card) 0%, var(--border) 25%, #1d3050 50%, var(--border) 75%, var(--card) 100%
    );
    background-size: 1000px 100%;
    animation: shimmerSweep 1.8s ease-in-out infinite;
    border-radius: 8px;
}
.shimmer-card {
    background: var(--card);
    border: 1.5px solid var(--border2);
    border-radius: var(--r-card);
    padding: 1.4rem;
    margin: 1.4rem 0;
    box-shadow: var(--shadow);
}
.sk-row { display: flex; gap: 1.2rem; }
.sk-thumb { width: 160px; min-width: 160px; height: 90px; border-radius: 12px; }
.sk-body { flex: 1; display: flex; flex-direction: column; gap: 10px; padding-top: 2px; }
.sk-t1 { height: 18px; width: 80%; }
.sk-t2 { height: 12px; width: 48%; }
.sk-t3 { height: 24px; width: 34%; border-radius: 20px; margin-top: 4px; }
.sk-stats { display: flex; gap: 8px; margin-top: 4px; }
.sk-stat { flex: 1; height: 64px; border-radius: 10px; }
.sk-divider { height: 1px; background: var(--border); margin: 1.1rem 0; }
.sk-opts { height: 42px; border-radius: 10px; }
.sk-btn  { height: 52px; border-radius: 12px; margin-top: 10px; }

.fetch-row {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 1rem;
}
.fetch-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 8px var(--accent);
    animation: pulseDot 1.2s ease-in-out infinite;
}
@keyframes pulseDot {
    0%,100% { transform: scale(1); opacity: 1; }
    50%      { transform: scale(1.4); opacity: 0.6; }
}
.fetch-txt { font-size: 0.8rem; color: var(--text2); font-weight: 500; }
.fetch-step { color: var(--accent2); font-weight: 600; }

/* ════════════════════════════════════════
   RESULT CARD
════════════════════════════════════════ */
.result-card {
    background: var(--card);
    border: 1.5px solid var(--border2);
    border-radius: var(--r-card);
    padding: 1.4rem;
    margin: 1.4rem 0 0;
    box-shadow: var(--shadow);
    animation: riseIn 0.4s cubic-bezier(0.22,1,0.36,1) both;
}
@keyframes riseIn {
    from { opacity: 0; transform: translateY(14px) scale(0.985); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* Thumbnail */
.rc-thumb-wrap {
    width: 175px; min-width: 175px;
    border-radius: 12px; overflow: hidden;
    background: var(--dim);
    aspect-ratio: 16/9;
    position: relative;
    flex-shrink: 0;
}
.rc-thumb-wrap img {
    width: 100%; height: 100%;
    object-fit: cover; display: block;
    border-radius: 12px;
}
.rc-thumb-placeholder {
    width: 100%; height: 100%;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 6px;
    background: linear-gradient(135deg, var(--dim), var(--border));
    border-radius: 12px;
}
.rc-thumb-placeholder span:first-child { font-size: 1.8rem; opacity: 0.4; }
.rc-thumb-placeholder span:last-child  { font-size: 0.65rem; color: var(--muted); letter-spacing: .05em; }

/* Info section */
.rc-top { display: flex; gap: 1.2rem; }
.rc-info { flex: 1; min-width: 0; display: flex; flex-direction: column; }

.rc-title {
    font-family: var(--display) !important;
    font-size: 0.97rem; font-weight: 700;
    color: var(--text); line-height: 1.45;
    margin-bottom: 0.3rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.rc-uploader {
    color: var(--text2); font-size: 0.76rem;
    margin-bottom: 0.55rem;
    display: flex; align-items: center; gap: 4px;
}
.rc-uploader .sep { color: var(--border3); margin: 0 2px; }

.rc-badges { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 0.75rem; }
.badge {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px; border-radius: 20px;
    font-size: 0.64rem; font-weight: 700;
    letter-spacing: 0.07em; text-transform: uppercase;
    font-family: var(--mono) !important;
}
.b-platform { background: rgba(249,95,26,.1);  color: #f97940; border: 1px solid rgba(249,95,26,.2); }
.b-type     { background: rgba(0,232,123,.07); color: #00e87b; border: 1px solid rgba(0,232,123,.18); }
.b-subs     { background: rgba(61,142,255,.08); color: #3d8eff; border: 1px solid rgba(61,142,255,.18); }
.b-note     { background: rgba(155,109,255,.07); color: #9b6dff; border: 1px solid rgba(155,109,255,.18); }

/* Stat pills */
.rc-stats { display: flex; gap: 8px; margin-top: auto; }
.stat-pill {
    flex: 1; text-align: center;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px; padding: 0.65rem 0.3rem;
    transition: border-color .2s;
}
.stat-pill:hover { border-color: var(--border3); }
.stat-val { font-family: var(--display) !important; font-size: 1.05rem; font-weight: 800; color: var(--text); line-height: 1; }
.stat-lbl { font-size: 0.59rem; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; margin-top: 4px; font-weight: 600; }

/* Card divider */
.rc-divider { height: 1px; background: var(--border); margin: 1.2rem 0 1rem; }

/* ════════════════════════════════════════
   OPTIONS PANEL (below result card)
════════════════════════════════════════ */
.options-panel {
    background: var(--card2);
    border: 1.5px solid var(--border2);
    border-top: none;
    border-radius: 0 0 var(--r-card) var(--r-card);
    padding: 1.1rem 1.4rem 1.4rem;
    margin-top: -2px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    animation: riseIn 0.4s 0.05s cubic-bezier(0.22,1,0.36,1) both;
}

/* ════════════════════════════════════════
   SELECTBOX OVERRIDES
════════════════════════════════════════ */
div[data-testid="stSelectbox"] label {
    color: var(--muted) !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.09em !important;
    text-transform: uppercase !important;
    font-family: var(--font) !important;
    margin-bottom: 4px !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 10px !important;
    font-family: var(--font) !important;
    font-size: 0.86rem !important;
    min-height: 42px !important;
    transition: border-color .2s !important;
}
div[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--border3) !important;
}

/* ════════════════════════════════════════
   CHECKBOX
════════════════════════════════════════ */
.stCheckbox label {
    color: var(--text2) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    gap: 8px !important;
}
.stCheckbox [data-testid="stCheckbox"] > label > div:first-child {
    border: 1.5px solid var(--border3) !important;
    background: var(--surface) !important;
    border-radius: 5px !important;
}

/* ════════════════════════════════════════
   DOWNLOAD BUTTON (primary CTA)
════════════════════════════════════════ */
.udp-dl-btn button {
    width: 100% !important;
    height: 52px !important;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--r-btn) !important;
    font-family: var(--display) !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 20px rgba(249,95,26,0.35), inset 0 1px 0 rgba(255,255,255,0.12) !important;
    transition: all 0.22s cubic-bezier(0.34,1.56,.64,1) !important;
    margin-top: 0.2rem !important;
}
.udp-dl-btn button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(249,95,26,0.5), inset 0 1px 0 rgba(255,255,255,0.15) !important;
}
.udp-dl-btn button:active { transform: translateY(0) scale(0.98) !important; }

/* ════════════════════════════════════════
   SAVE FILE BUTTON (after download)
════════════════════════════════════════ */
.stDownloadButton > button {
    width: 100% !important;
    height: 56px !important;
    background: linear-gradient(135deg, var(--green) 0%, var(--green2) 100%) !important;
    color: #021a0e !important;
    border: none !important;
    border-radius: var(--r-btn) !important;
    font-family: var(--display) !important;
    font-size: 1rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 24px rgba(0,232,123,0.3), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    transition: all 0.22s cubic-bezier(0.34,1.56,.64,1) !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    padding: 0 1.5rem !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(0,232,123,0.45) !important;
}
.stDownloadButton > button:active { transform: scale(0.98) !important; }

/* ════════════════════════════════════════
   READY / ERROR / WARN CARDS
════════════════════════════════════════ */
.ready-card {
    background: linear-gradient(135deg, #021408 0%, #031b0f 100%);
    border: 1.5px solid rgba(0,232,123,0.22);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin: 0.8rem 0 0.5rem;
    box-shadow: 0 0 40px rgba(0,232,123,0.07);
    animation: readyPop 0.5s cubic-bezier(0.34,1.56,.64,1) both;
}
@keyframes readyPop {
    from { opacity: 0; transform: scale(0.94); }
    to   { opacity: 1; transform: scale(1); }
}
.ready-inner { display: flex; align-items: center; gap: 12px; }
.ready-check {
    width: 40px; height: 40px; flex-shrink: 0;
    border-radius: 50%;
    background: rgba(0,232,123,0.12);
    border: 1.5px solid rgba(0,232,123,0.25);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    box-shadow: 0 0 16px rgba(0,232,123,0.15);
}
.ready-label { font-family: var(--display) !important; font-size: 1rem; font-weight: 800; color: var(--green); }
.ready-file  { font-family: var(--mono) !important; font-size: 0.72rem; color: #4dffa0; margin-top: 2px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 440px; }
.ready-meta  { font-size: 0.7rem; color: var(--muted); margin-top: 2px; }

.err-card {
    background: linear-gradient(135deg, #120306, #0e0205);
    border: 1.5px solid rgba(255,59,92,0.2);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin: 0.8rem 0;
    animation: fadeIn .3s ease;
}
.err-title { font-size: 0.88rem; font-weight: 700; color: var(--red); margin-bottom: 5px; display: flex; align-items: center; gap: 6px; }
.err-body  { font-size: 0.79rem; color: #ff8fa0; line-height: 1.7; }

.tip-card {
    background: var(--card);
    border: 1px solid var(--border2);
    border-left: 3px solid var(--accent2);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin-top: 0.5rem;
    font-size: 0.78rem; color: var(--text2); line-height: 1.7;
}
.tip-card b { color: var(--accent2); }
.tip-card code { background: var(--dim); padding: 1px 6px; border-radius: 4px; font-family: var(--mono) !important; font-size: 0.75rem; color: var(--accent3); }

.warn-card {
    background: rgba(255,180,0,0.04);
    border: 1px solid rgba(255,180,0,0.18);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.78rem; color: #fcd34d; line-height: 1.6;
}

/* ════════════════════════════════════════
   PROGRESS BAR
════════════════════════════════════════ */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3)) !important;
    border-radius: 99px !important;
    transition: width 0.3s ease !important;
}
.stProgress > div > div {
    background: var(--border) !important;
    border-radius: 99px !important;
    height: 6px !important;
}
.stProgress > div { padding: 0 !important; }

/* Speed indicator */
.speed-bar {
    display: flex; align-items: center; gap: 10px;
    padding: 6px 0; font-size: 0.78rem;
}
.speed-val { color: var(--blue); font-weight: 700; font-family: var(--mono) !important; }
.eta-val   { color: var(--purple); font-weight: 700; font-family: var(--mono) !important; }
.speed-sep { color: var(--border3); }

/* ════════════════════════════════════════
   HISTORY
════════════════════════════════════════ */
.hist-header {
    font-size: 0.68rem; font-weight: 700;
    color: var(--muted); text-transform: uppercase; letter-spacing: .12em;
    margin: 2rem 0 0.7rem;
    display: flex; align-items: center; gap: 8px;
}
.hist-header::after {
    content: ''; flex: 1; height: 1px;
    background: var(--border);
}
.hist-item {
    display: flex; align-items: center; gap: 10px;
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 0.65rem 0.9rem;
    margin-bottom: 6px;
    transition: border-color .2s, background .2s;
    cursor: default;
}
.hist-item:hover { border-color: var(--border3); background: var(--card2); }
.hist-thumb {
    width: 48px; height: 30px;
    border-radius: 6px; object-fit: cover;
    background: var(--dim); flex-shrink: 0;
    border: 1px solid var(--border);
}
.hist-thumb-ph {
    width: 48px; height: 30px;
    border-radius: 6px; flex-shrink: 0;
    background: var(--dim); border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; color: var(--muted);
}
.hist-name { font-size: 0.78rem; color: var(--text2); font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
.hist-meta { font-size: 0.64rem; color: var(--muted); white-space: nowrap; text-align: right; }
.hist-site { font-weight: 700; color: var(--text2); }

/* ════════════════════════════════════════
   EMPTY STATE
════════════════════════════════════════ */
.empty-state {
    text-align: center;
    padding: 3rem 0 2rem;
    animation: fadeIn .5s ease;
}
.empty-icon { font-size: 3rem; opacity: 0.08; margin-bottom: 0.8rem; }
.empty-title { color: var(--muted); font-size: 0.9rem; font-weight: 600; margin-bottom: 0.4rem; }
.empty-sites { color: var(--border3); font-size: 0.72rem; line-height: 2; }
.empty-sites span { color: var(--border2); margin: 0 3px; }

/* ════════════════════════════════════════
   FOOTER
════════════════════════════════════════ */
.udp-footer {
    text-align: center;
    padding: 2rem 0 1rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
    color: var(--border3);
    font-size: 0.7rem;
    line-height: 2;
}
.udp-footer strong { color: var(--border2); }

/* ════════════════════════════════════════
   SIDEBAR
════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource(show_spinner=False)
def check_ffmpeg():
    try:
        r = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def proxy_thumbnail(url):
    """Fetch thumbnail server-side to bypass CORS/hotlink restrictions."""
    if not url:
        return None
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.google.com/',
        })
        with urllib.request.urlopen(req, timeout=6) as r:
            data = r.read()
        ext = url.split('?')[0].rsplit('.', 1)[-1].lower()
        mime = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png',
                'webp': 'image/webp', 'gif': 'image/gif'}.get(ext, 'image/jpeg')
        b64 = base64.b64encode(data).decode()
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None


def base_opts():
    return {
        'quiet': True, 'no_warnings': True,
        'extractor_args': {
            'youtube': {'player_js_version': 'actual', 'player_client': 'web_safari'},
            'instagram': {'api': ['graphql', 'web']},
        },
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
        },
        'geo_bypass': True,
    }


def fetch_info(url):
    opts = base_opts()
    opts['skip_download'] = True
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            fmts = info.get('formats', [])
            ext  = info.get('extractor', 'generic').lower()
            heights = sorted({f['height'] for f in fmts if f.get('height') and f['height'] > 0}, reverse=True)
            has_v = any(f.get('vcodec') != 'none' for f in fmts)
            has_a = any(f.get('acodec') != 'none' for f in fmts)
            has_i = any(f.get('ext') in ('jpg', 'jpeg', 'png', 'webp') for f in fmts)
            ct = ('photo'   if (has_i and not has_v) else
                  'gallery' if (not has_v and not has_a and not has_i and info.get('entries')) else 'video')

            # Fetch thumbnail server-side
            thumb_url = info.get('thumbnail', '')
            thumb_b64 = proxy_thumbnail(thumb_url)

            return {
                'title':      info.get('title', 'Unknown'),
                'uploader':   info.get('uploader', info.get('channel', info.get('uploader_id', 'Unknown'))),
                'duration':   info.get('duration') or 0,
                'thumbnail':  thumb_url,
                'thumb_b64':  thumb_b64,
                'view_count': info.get('view_count') or 0,
                'like_count': info.get('like_count') or 0,
                'filesize':   info.get('filesize_approx') or 0,
                'extractor':  ext,
                'is_youtube': 'youtube' in ext,
                'has_height_formats': bool(heights),
                'has_video':  has_v, 'has_audio': has_a, 'has_image': has_i,
                'content_type': ct,
                'entries':    info.get('entries', []),
                'heights':    heights,
                'has_subs':   bool(info.get('subtitles') or info.get('automatic_captions')),
                'success': True,
            }
    except Exception as e:
        return {'error': str(e), 'success': False}


def fmt_dur(s):
    if not s: return '—'
    m, s = divmod(int(s), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def fmt_sz(b):
    if not b: return '—'
    b = float(b)
    for u in ['B', 'KB', 'MB', 'GB']:
        if b < 1024: return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} TB"


def fmt_n(n):
    if not n: return '—'
    n = float(n)
    if n >= 1e9: return f"{n/1e9:.1f}B"
    if n >= 1e6: return f"{n/1e6:.1f}M"
    if n >= 1e3: return f"{n/1e3:.1f}K"
    return str(int(n))


def clean_name(t, mx=72):
    if not t: t = 'download'
    s = ''.join(c if c.isalnum() or c in ' ._-' else '_' for c in t).strip('._')
    if len(s) > mx:
        s = s[:mx - 7] + '_' + hashlib.md5(s.encode()).hexdigest()[:6]
    return s or 'download'


def site_name(ext):
    for k, n in [('youtube', 'YouTube'), ('instagram', 'Instagram'), ('facebook', 'Facebook'),
                 ('tiktok', 'TikTok'), ('twitter', 'Twitter/X'), ('reddit', 'Reddit'),
                 ('vimeo', 'Vimeo'), ('twitch', 'Twitch'), ('dailymotion', 'Dailymotion'),
                 ('soundcloud', 'SoundCloud')]:
        if k in ext: return n
    return ext.replace('ie', '').title() or 'Unknown'


def type_icon(ct):
    return {'video': '▶', 'photo': '◈', 'gallery': '⊞', 'audio': '♫'}.get(ct, '◉')


def get_fmt_str(quality, mode, ffmpeg_ok, info):
    ct = info.get('content_type', 'video')
    if ct == 'photo': return 'best'
    if mode == 'Audio Only':
        return 'bestaudio/best' if ffmpeg_ok else 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio'
    if not info.get('is_youtube') or not info.get('has_height_formats'):
        return 'best/bestvideo+bestaudio'
    hmap = {'Best': None, '4K (2160p)': 2160, '1440p': 1440, '1080p': 1080,
            '720p': 720, '480p': 480, '360p': 360}
    th = hmap.get(quality)
    if ffmpeg_ok:
        if th:
            return (f"bestvideo[height<={th}][vcodec!*=av01]+bestaudio[acodec!*=opus]"
                    f"/bestvideo[height<={th}]+bestaudio/best[height<={th}]")
        return 'bestvideo[vcodec!*=av01]+bestaudio[acodec!*=opus]/bestvideo+bestaudio/best'
    return f'best[height<={th}]/best' if th else 'best/bestvideo+bestaudio'


def build_opts(fmt, outdir, hook, ffmpeg_ok, mode, info, subs=False, thumb=False):
    opts = base_opts()
    opts.update({
        'format': fmt,
        'outtmpl': os.path.join(outdir, clean_name(info.get('title', 'download')) + '.%(ext)s'),
        'progress_hooks': [hook], 'noplaylist': True,
        'retries': 10, 'fragment_retries': 10, 'continue_dl': True,
    })
    ct = info.get('content_type', 'video')
    post = []
    if ct == 'photo':
        if info.get('entries'): opts['noplaylist'] = False
    elif ffmpeg_ok and mode == 'Audio Only':
        post.append({'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'})
        if thumb: post.append({'key': 'EmbedThumbnail'})
    elif ffmpeg_ok and mode != 'Audio Only' and '+' in fmt:
        opts['merge_output_format'] = 'mp4'
    if ffmpeg_ok and subs and mode != 'Audio Only':
        opts.update({'writesubtitles': True, 'writeautomaticsub': True, 'subtitleslangs': ['en', 'en-US']})
        post.append({'key': 'FFmpegSubtitlesConvertor', 'format': 'srt'})
    if post: opts['postprocessors'] = post
    return opts


def add_history(info, fname, fsize):
    if 'history' not in st.session_state: st.session_state.history = []
    st.session_state.history.insert(0, {
        'title':    info.get('title', '')[:55],
        'uploader': info.get('uploader', ''),
        'thumb_b64': info.get('thumb_b64', ''),
        'site':     site_name(info.get('extractor', 'generic')),
        'type':     info.get('content_type', 'video'),
        'fname':    fname, 'fsize': fmt_sz(fsize),
        'ts':       datetime.now().strftime('%H:%M'),
    })
    st.session_state.history = st.session_state.history[:8]


# ═══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
for k, v in {
    'last_url': '', 'video_info': None, 'is_loading': False,
    'download_error': None, 'clear_t': 0, 'history': [], 'url_val': ''
}.items():
    if k not in st.session_state: st.session_state[k] = v

ffmpeg_ok = check_ffmpeg()

# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ System")
    if ffmpeg_ok:
        st.success("✓ FFmpeg ready — full quality merging enabled")
    else:
        st.warning("⚠ FFmpeg missing — add to packages.txt")
    st.markdown("---")
    st.markdown("### 📦 Setup Files")
    st.code("requirements.txt:\nstreamlit\nyt-dlp\n\npackages.txt:\nffmpeg", language="text")
    st.markdown("---")
    if st.session_state.history:
        st.markdown("### 🕒 Recent")
        for h in st.session_state.history[:5]:
            thumb_html = f'<img class="hist-thumb" src="{h["thumb_b64"]}">' if h.get('thumb_b64') else '<div class="hist-thumb-ph">◈</div>'
            st.markdown(f"""
            <div class="hist-item">
                {thumb_html}
                <div class="hist-name">{type_icon(h['type'])} {h['title']}</div>
                <div class="hist-meta">{h['fsize']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption("⚖️ Only download content you own or have rights to use.")


# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="udp-header">
    <div class="udp-icon">⬇</div>
    <div class="udp-wordmark">Universal Downloader</div>
    <div class="udp-sub">Videos · Photos · Reels · Stories · 1800+ Sites</div>
</div>
<div class="udp-rule"></div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  SEARCH BAR
# ═══════════════════════════════════════════════════════════════════════════════
url_has_text = bool(st.session_state.url_val)

st.markdown('<div class="search-wrap searchbar-cols">', unsafe_allow_html=True)
c_input, c_action, c_go = st.columns([10, 1.1, 1.1])

with c_input:
    url_input = st.text_input(
        "", key=f"url_{st.session_state.clear_t}",
        placeholder="  Paste a URL — YouTube, TikTok, Instagram, Facebook…",
        label_visibility="collapsed"
    )
    if url_input != st.session_state.url_val:
        st.session_state.url_val = url_input

with c_action:
    st.markdown('<div class="sb-action">', unsafe_allow_html=True)
    if url_has_text:
        if st.button("✕", key="clear_btn", help="Clear"):
            st.session_state.url_val    = ''
            st.session_state.last_url   = ''
            st.session_state.video_info = None
            st.session_state.is_loading = False
            st.session_state.clear_t   += 1
            st.rerun()
    else:
        if st.button("⎘", key="paste_btn", help="Paste"):
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
    st.markdown('<div class="sb-go">', unsafe_allow_html=True)
    analyze_clicked = st.button("⌕", key="go_btn", help="Analyze")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

url = st.session_state.url_val.strip()

trigger_fetch = (
    (analyze_clicked and url and url != st.session_state.last_url) or
    (url and url != st.session_state.last_url and len(url) > 10)
)

if trigger_fetch:
    st.session_state.last_url       = url
    st.session_state.video_info     = None
    st.session_state.download_error = None
    st.session_state.is_loading     = True
    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  SHIMMER → FETCH → RESULT
# ═══════════════════════════════════════════════════════════════════════════════
SHIMMER = """
<div class="fetch-row">
    <span class="fetch-dot"></span>
    <span class="fetch-txt">Analyzing URL <span class="fetch-step">· fetching metadata…</span></span>
</div>
<div class="shimmer-card">
    <div class="sk-row">
        <div class="sk-base sk-thumb"></div>
        <div class="sk-body">
            <div class="sk-base sk-t1"></div>
            <div class="sk-base sk-t2"></div>
            <div class="sk-base sk-t3"></div>
            <div class="sk-stats">
                <div class="sk-base sk-stat"></div>
                <div class="sk-base sk-stat" style="animation-delay:.1s"></div>
                <div class="sk-base sk-stat" style="animation-delay:.2s"></div>
            </div>
        </div>
    </div>
    <div class="sk-divider"></div>
    <div class="sk-base sk-opts"></div>
    <div class="sk-base sk-btn"></div>
</div>
"""

if st.session_state.is_loading:
    slot = st.empty()
    slot.markdown(SHIMMER, unsafe_allow_html=True)
    result = fetch_info(st.session_state.last_url)
    st.session_state.video_info  = result
    st.session_state.is_loading  = False
    slot.empty()
    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  ERROR STATE
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.video_info and not st.session_state.video_info.get('success'):
    err = st.session_state.video_info.get('error', 'Unknown error')
    st.markdown(f"""
    <div class="err-card">
        <div class="err-title">✕ Failed to fetch</div>
        <div class="err-body">{err}</div>
    </div>
    """, unsafe_allow_html=True)
    el = err.lower()
    if 'authentication' in el or 'reddit' in el:
        st.markdown('<div class="tip-card"><b>Reddit</b> requires authentication. Try a direct media URL or another platform.</div>', unsafe_allow_html=True)
    elif 'no video' in el:
        st.markdown('<div class="tip-card"><b>Instagram photo</b> detected. Switch mode to <b>Photo/Gallery</b> or use a Reel URL.</div>', unsafe_allow_html=True)
    elif '403' in err:
        st.markdown('<div class="tip-card">Platform blocked this server. Try lowering quality to <b>360p</b> or run the app <b>locally</b>.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  RESULT CARD
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.video_info and st.session_state.video_info.get('success'):
    info   = st.session_state.video_info
    sname  = site_name(info['extractor'])
    ct     = info['content_type']
    ci     = type_icon(ct)
    hs     = info.get('heights', [])
    qtop   = f"· {hs[0]}p top quality" if hs else "· quality auto-adjusted"

    # Thumbnail: prefer proxied base64, fallback to direct URL, then placeholder
    thumb_b64 = info.get('thumb_b64', '')
    thumb_src = thumb_b64 or info.get('thumbnail', '')
    if thumb_src:
        thumb_html = f'<img src="{thumb_src}" alt="thumbnail" loading="lazy" onerror="this.parentElement.innerHTML=\'<div class=rc-thumb-placeholder><span>◈</span><span>No preview</span></div>\'">'
    else:
        thumb_html = '<div class="rc-thumb-placeholder"><span>◈</span><span>No preview</span></div>'

    subs_badge = '<span class="badge b-subs">CC SUBS</span>' if info.get('has_subs') else ''
    non_yt_badge = '<span class="badge b-note">◈ Auto Quality</span>' if not info.get('is_youtube') and ct == 'video' else ''

    # ── Result card ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="result-card">
        <div class="rc-top">
            <div class="rc-thumb-wrap">{thumb_html}</div>
            <div class="rc-info">
                <div class="rc-title">{info['title']}</div>
                <div class="rc-uploader">
                    <span>@{info['uploader']}</span>
                    <span class="sep">·</span>
                    <span>{fmt_dur(info['duration'])}</span>
                    <span class="sep">·</span>
                    <span>{qtop}</span>
                </div>
                <div class="rc-badges">
                    <span class="badge b-platform">{sname}</span>
                    <span class="badge b-type">{ci} {ct.title()}</span>
                    {subs_badge}{non_yt_badge}
                </div>
                <div class="rc-stats">
                    <div class="stat-pill">
                        <div class="stat-val">{fmt_sz(info['filesize'])}</div>
                        <div class="stat-lbl">Est. Size</div>
                    </div>
                    <div class="stat-pill">
                        <div class="stat-val">{fmt_n(info['view_count'])}</div>
                        <div class="stat-lbl">Views</div>
                    </div>
                    <div class="stat-pill">
                        <div class="stat-val">{fmt_n(info['like_count'])}</div>
                        <div class="stat-lbl">Likes</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Options panel ────────────────────────────────────────────────────────
    st.markdown('<div class="options-panel">', unsafe_allow_html=True)

    oc1, oc2, oc3 = st.columns([2.2, 2.2, 1.6])
    with oc1:
        mode = st.selectbox("Type", ["Auto Detect", "Video", "Audio Only", "Photo/Gallery"], index=0, key="mode_sel")
    with oc2:
        if mode == "Audio Only":       qopts = ["Best", "192kbps", "128kbps"]
        elif mode == "Photo/Gallery":  qopts = ["Best", "Original", "High", "Medium"]
        else:                          qopts = ["Best", "4K (2160p)", "1440p", "1080p", "720p", "480p", "360p"]
        quality = st.selectbox("Quality", qopts, index=0, key="qual_sel")
    with oc3:
        st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
        embed_subs  = st.checkbox("Subtitles", value=False, disabled=not ffmpeg_ok, key="subs_chk")
        embed_thumb = st.checkbox("Embed Art",  value=False, disabled=not ffmpeg_ok, key="thumb_chk")

    if not ffmpeg_ok:
        st.markdown('<div class="warn-card">⚠ FFmpeg missing — quality merging & subtitle embedding unavailable. Add <code>ffmpeg</code> to packages.txt and redeploy.</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

    st.markdown('<div class="udp-dl-btn">', unsafe_allow_html=True)
    dl_clicked = st.button("⬇  Download Now", use_container_width=True, key="dl_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close options-panel

    # ── Download logic ────────────────────────────────────────────────────────
    if dl_clicked:
        prog   = st.progress(0, text="Initialising…")
        spd    = st.empty()
        dl_err = None; file_bytes = None; file_name = None; mime = "video/mp4"

        def hook(d):
            if d['status'] == 'downloading':
                raw   = d.get('_percent_str', '0%').replace('%', '').strip()
                speed = d.get('_speed_str', '—')
                eta   = d.get('_eta_str',   '—')
                try:
                    pct = min(int(float(raw)), 99)
                    prog.progress(pct, text=f"Downloading… {pct}%")
                    spd.markdown(f"""
                    <div class="speed-bar">
                        ⚡ <span class="speed-val">{speed}</span>
                        <span class="speed-sep">·</span>
                        ⏱ ETA <span class="eta-val">{eta}</span>
                    </div>
                    """, unsafe_allow_html=True)
                except: pass
            elif d['status'] == 'finished':
                prog.progress(100, text="Post-processing…")
                spd.markdown('<div class="speed-bar" style="color:var(--green)">✓ Download complete — finalising file…</div>', unsafe_allow_html=True)

        try:
            with tempfile.TemporaryDirectory() as tmp:
                fmt  = get_fmt_str(quality, mode, ffmpeg_ok, info)
                opts = build_opts(fmt, tmp, hook, ffmpeg_ok, mode, info, embed_subs, embed_thumb)
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
                files = [f for f in os.listdir(tmp) if os.path.isfile(os.path.join(tmp, f))]
                if not files: raise Exception("Download completed but no output file was found.")
                file_name = files[0]
                fpath = os.path.join(tmp, file_name)
                ext   = file_name.rsplit('.', 1)[-1].lower()
                mime  = {'mp3': 'audio/mpeg', 'm4a': 'audio/mp4', 'webm': 'video/webm',
                         'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
                         'png': 'image/png', 'webp': 'image/webp'}.get(ext, 'video/mp4')
                fsz = os.path.getsize(fpath)
                if fsz > 500 * 1024 * 1024:
                    st.markdown('<div class="warn-card">⚠ File is over 500 MB — Streamlit Cloud may struggle. Run locally for large files.</div>', unsafe_allow_html=True)
                with open(fpath, 'rb') as f:
                    file_bytes = f.read()
        except Exception as e:
            dl_err = str(e)

        prog.empty()
        spd.empty()

        if dl_err:
            st.markdown(f"""
            <div class="err-card">
                <div class="err-title">✕ Download Failed</div>
                <div class="err-body">{dl_err}</div>
            </div>
            """, unsafe_allow_html=True)
            el = dl_err.lower()
            if '403' in dl_err or 'forbidden' in el:
                st.markdown("""
                <div class="tip-card">
                    <b>YouTube 403 — Cloud IP blocked.</b><br>
                    Try 2–3 times · switch to lower quality (360p / Audio Only) · or run locally:<br>
                    <code>pip install streamlit yt-dlp && streamlit run streamlit_app.py</code>
                </div>""", unsafe_allow_html=True)
            elif 'requested format' in el:
                st.markdown('<div class="tip-card"><b>Format unavailable.</b> Switch to <b>Best</b> quality or <b>Auto Detect</b> mode.</div>', unsafe_allow_html=True)
            elif 'ffmpeg' in el or 'merging' in el:
                st.markdown('<div class="tip-card"><b>FFmpeg not found.</b> Add <code>ffmpeg</code> to packages.txt and redeploy.</div>', unsafe_allow_html=True)
            elif 'too long' in el or 'file name' in el:
                st.markdown('<div class="tip-card"><b>Filename too long</b> — auto-truncation is active, please retry.</div>', unsafe_allow_html=True)

        elif file_bytes:
            add_history(info, file_name, len(file_bytes))
            # Truncate display name for the card
            display_name = file_name if len(file_name) <= 48 else file_name[:45] + '…'
            st.markdown(f"""
            <div class="ready-card">
                <div class="ready-inner">
                    <div class="ready-check">✓</div>
                    <div>
                        <div class="ready-label">Ready to Save!</div>
                        <div class="ready-file">{display_name}</div>
                        <div class="ready-meta">📦 {fmt_sz(len(file_bytes))} · tap the button below</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # Clean label — just show icon + size, not the full filename
            st.download_button(
                label=f"⬇  Save File  ·  {fmt_sz(len(file_bytes))}",
                data=file_bytes,
                file_name=file_name,
                mime=mime,
                use_container_width=True,
                key=f"save_{int(time.time())}"
            )


# ── Empty state ──────────────────────────────────────────────────────────────
if not url and not st.session_state.video_info:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">⬇</div>
        <div class="empty-title">Paste a URL above to get started</div>
        <div class="empty-sites">
            YouTube <span>·</span> TikTok <span>·</span> Instagram <span>·</span>
            Facebook <span>·</span> Twitter/X <span>·</span> Vimeo <span>·</span>
            Twitch <span>·</span> Reddit <span>·</span> SoundCloud <span>·</span>
            Dailymotion <span>+</span> 1800 more
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── History ──────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="hist-header">Recent Downloads</div>', unsafe_allow_html=True)
    for h in st.session_state.history:
        thumb_html = (f'<img class="hist-thumb" src="{h["thumb_b64"]}">'
                      if h.get('thumb_b64') else '<div class="hist-thumb-ph">◈</div>')
        st.markdown(f"""
        <div class="hist-item">
            {thumb_html}
            <div class="hist-name">{type_icon(h['type'])} {h['title']}</div>
            <div class="hist-meta"><span class="hist-site">{h['site']}</span> · {h['ts']} · {h['fsize']}</div>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="udp-footer">
    <strong>Universal Downloader Pro</strong><br>
    Powered by yt-dlp · Free & Open Source · No API keys · No limits<br>
    YouTube · Instagram · TikTok · Facebook · Twitter/X · Reddit · Vimeo · 1800+ sites
</div>
""", unsafe_allow_html=True)
