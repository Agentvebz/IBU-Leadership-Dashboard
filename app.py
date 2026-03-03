import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from openai import AzureOpenAI

st.set_page_config(page_title="IBU NBA/E — Executive Summary", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# ═══════ BRAND ═══════
LR, DN, BL, GR, AM, PR, TL, GY = "#D52B1E","#1A2E4A","#2563EB","#059669","#D97706","#7C3AED","#0EA5E9","#6B7280"
SBG = "#F4F5F7"
PC = [LR,BL,AM,PR,TL,"#10B981","#94A3B8"]

LOGO = "iVBORw0KGgoAAAANSUhEUgAAAEkAAAA0CAYAAADGzxXDAAAFUUlEQVR4nO2Za4hVVRTH17n3zmg+y9ScMnDUUst8lWFWNonYhzCJrAQ/Zu9oIPtQhgXpByshNcSkUowgK6KQyuhhSTWFWkJFUSlmplZGJaKWOP76sP977prjvcOYjfcOnj9c9lmPvc9e66y91t77mmXIkCFDhgwZMmTIkOEUApAASaXnUZUA8kDe0blKzsejw76YoiGndzQnSUJbekmSNIvuIf1DHTW3ikPLpdBeXffcALwK/ALsAGaIny8/QidEarnkgUuAu4Gh4uWcPKe2ACymiENqm9J9Oj2ig4CewP3AVmf46pROzumuk85uYKqcegR42ffp9HDGTwa+l9F/AEuBa4DBcWnF6gV0AzZIdzMwRPKPxLtZdMG9JwFyna76uaiYDjTLwEeBPiV0Ey3DBFgr3Y3AWZI/JN4WoNaN3e48V3WIX1WRsh84DEx38oKc0pJ/1C6VM74B6sS7QU4+BIxz4+dS7zzHR2VsS+lWBZzRT8roR0TXppeE050t3b3AMPFuBP4R/ybxWvZNQA1wH7Ad+JuQx7qUirCqW4ruS24EjgIjZFA+pReNHScjAa4U7wHRR4CZ4hVcnyHAp9L5Ws48AvShdbUcFZ1eVXDL6GMtletEF9yvRm134FsZeCtQD7wr43cCV7u+0UGjgF3SaQTGyElvujnMpFhJDwNTxa+OquiW0L2a5I/AVWV0V0rnB2AVRbwA9I3jOcfXAz9L5xbxvhQ9XvQy0d+5aJvt51ZxUEyYNcAaZ3gTsAiYQ9gzPcOxeB+YonF6At31nAe6Apukd4/4r4meLzo6/RU5d5OibKDk1ZPEaX20mEXY+xwt4RSAT4D5wFjXZzjwK/A50Eu8x6W/WPQq0WtFN4peJ3pRyoHHLDVOdkJXBMXyHvc+NU4+gJCkJxMqEsCK1Bi1asdLfgDoDZwnepPkMQo/IOS1wYTcs13y6LD1hKpaqnC02jJUHClnrZABmwlLKC9DYi67XO0E4EI9P0+ogA16BngH6C35SkKkjgHudOP3KzOflm1ER9seXxi/SIFQod7QMnkLeBC4wOnGpLoHGBQn6iY9R/Ilrs8ZiqidwGeSrwa6SN6XkHc+BB5zDuzn5vUscJfeFaN1gOb5kj5Wx+UrQpLO62Xoi++gdQ56Cnhaz38CE9W31o2zQPLDwDTnuEtpjbniR/kk8Q+qXUaxGg4C3hP/L3QsAkYTth4Az+GOOx3iILUxZzSl5NMJUROxF5egpTMceFvyZuBh8RM5KxqzC7jI9UuAKwhFoZlw59QgWQG4HdjnHD9JsjvkMICFbqzjyk3tVnYD9zWz7eq72Mz2mFmdmU00s4ZUtw1m1mRmB8zsMjO7VvxtZjbEzF40s5/M7HozO9/M9plZVws3msvM7HczO9fMpkg/Yq+ZPWFmZ5vZDDMbaGa7zay/5MvNbIKZjRe9IEmSeYrIo+VuSf8XuGiaRvFKJGI/Yc8ymXAvtD4lP0jYOI4gVL7fnGwbMA84UxG5M9X3K2AuobItoXjbAGGDeRtwOsU85rFIcy4cbwSdiKN88h4GXAwMBU4roVsHjAVGEu6uvawf4eayvkS/boRcMhroX0JeL0cPTPF7AROBL+Sg5W6uJ32fVPJchE7u+h0zKfFLXppFQyiRVCnuy0peh0hWo+flctDr7p2V2R9RPJK0ZXhZOcVNaDlZS9+2xhUdq1+jW4I9yjn1lINz0EjChd1+YKSXnfJw0RQLRaPo6rgFqDQoHm9myUFb2sqJ/xWdfb0iZ9SZ2VYzW6h/gpMO3Qt1VlDi9J/BIatg7UTF9kIZMmTIkCFDhgwZMmQ4QfwLJtOTDz+1UgUAAAAASUVORK5CYII="

AZ = {"endpoint":"https://openai-ibu-leadership-dashboard-instance.cognitiveservices.azure.com/","deployment":"gpt-4.1","api_key":"14Z24pmPY22AmDCAFJasrmOXgWzT5T7Cn8ElX516CdKQJtZzgt7LJQQJ99CBACHYHv6XJ3w3AAABACOG1yoB","api_version":"2024-12-01-preview"}

# ═══════ CSS ═══════
st.markdown(f"""<style>
.stApp {{font-family:Arial,sans-serif;background:{SBG};color:{DN};}}
.block-container {{padding-top:0!important;max-width:1500px;}}
[data-testid="stHeader"],.stDeployButton,#MainMenu,footer,div[data-testid="stToolbar"] {{display:none!important;}}

/* Force dark text on all markdown content */
.stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span, .stMarkdown li, .stMarkdown b, .stMarkdown strong {{color:{DN}!important;}}

/* ═══ WHITE TEXT ON DARK BG — must use .stMarkdown prefix for higher specificity ═══ */
/* Header */
.stMarkdown .hdr h1, .stMarkdown .hdr p, .stMarkdown .hdr div {{color:#fff!important;}}
.stMarkdown .hdr p {{color:rgba(255,255,255,.7)!important;}}
/* AI Banner */
.stMarkdown .ai-ban .lb {{color:{AM}!important;}}
.stMarkdown .ai-ban .tx, .stMarkdown .ai-ban div.tx {{color:#fff!important;}}
/* Tiles (blue & dark navy) */
.stMarkdown .tile, .stMarkdown .tile div, .stMarkdown .tile span,
.stMarkdown .tile .tv, .stMarkdown .tile .tl,
.stMarkdown .tile-dk, .stMarkdown .tile-dk div, .stMarkdown .tile-dk span {{color:#fff!important;}}
/* ES Sprint headers & value tiles */
.stMarkdown .es-hd {{color:#fff!important;}}
.stMarkdown .es-t, .stMarkdown .es-t div, .stMarkdown .es-t span,
.stMarkdown .es-t .tv, .stMarkdown .es-t .tl {{color:#fff!important;}}
/* Cost highlight badges */
.stMarkdown .cost-hl {{color:#fff!important;}}
/* Total savings bar (dark gradient bg) */
.stMarkdown .dark-bg, .stMarkdown .dark-bg div, .stMarkdown .dark-bg span {{color:#fff!important;}}

/* ═══ DARK TEXT ON LIGHT BG — specific component styles ═══ */
/* Risk card */
.stMarkdown .risk-c, .stMarkdown .risk-c div, .stMarkdown .risk-c span, .stMarkdown .risk-c b {{color:#1A2E4A!important;}}
.stMarkdown .risk-c h4 {{color:{LR}!important;}}
/* GPT response */
.stMarkdown .gpt-r, .stMarkdown .gpt-r div, .stMarkdown .gpt-r span {{color:{DN}!important;}}
/* KPI cards */
.kpi .vl {{color:{DN}!important;}}
.kpi .lb {{color:{GY}!important;}}
.kpi .sb {{color:{GY}!important;}}
/* Card */
.card h4 {{color:{DN}!important;}}
.card .sub {{color:{GY}!important;}}
/* Business Health tiles */
.bh .bv {{color:{DN}!important;}}
.bh .bl {{color:{DN}!important;}}
.bh .bs {{color:{GY}!important;}}
/* Section headers */
.sh h3 {{color:{DN}!important;}}
.sh .sb {{color:{GY}!important;}}
/* Status bars */
.sbar, .sbar span, .sbar .tx {{color:{DN}!important;}}
.stMarkdown .sbar .tg {{color:#fff!important;}}
/* Observation cards */
.obs {{color:{DN}!important;}}
/* Rows */
.irow, .irow div, .irow span {{color:{DN}!important;}}
.crow, .crow span {{color:{DN}!important;}}
/* Config tiles */
.ctile .cv {{color:inherit!important;}}
.ctile .cl {{color:{DN}!important;}}
.ctile .cs {{color:{GY}!important;}}
/* Release cards */
.rel-c, .rel-c div, .rel-c b, .rel-c span {{color:{DN}!important;}}
/* Work item bars */
.wi-bar, .wi-bar span, .wi-bar .wh, .wi-bar .wh span {{color:{DN}!important;}}
/* Cost rows */
.cost-r, .cost-r div, .cost-r span {{color:{DN}!important;}}
/* Ask banner */
.ask-ban span {{color:{LR}!important;}}
/* Ask Dashboard title */
.ask-title {{font-size:15px;font-weight:800;color:{LR};margin:10px 0 4px;text-align:center;letter-spacing:.3px;}}

.hdr {{background:linear-gradient(135deg,{LR} 0%,#9B1B14 100%);padding:20px 32px;display:flex;align-items:center;gap:20px;box-shadow:0 4px 16px rgba(213,43,30,.3);margin-bottom:0;}}
.hdr img {{height:52px;}}
.hdr h1 {{color:#fff;font-size:24px;font-weight:800;margin:0;letter-spacing:.3px;}}
.hdr p {{color:rgba(255,255,255,.7);font-size:11px;margin:3px 0 0;}}

.ask-top {{background:#fff;border:2px solid {LR};border-radius:12px;padding:10px 20px;margin:14px 0;display:flex;align-items:center;gap:12px;box-shadow:0 2px 8px rgba(213,43,30,.08);}}

.ai-ban {{background:linear-gradient(135deg,{DN},#1E3A5F);padding:18px 28px;border-radius:12px;margin-bottom:14px;border-left:6px solid {AM};box-shadow:0 2px 12px rgba(26,46,74,.15);}}
.ai-ban .lb {{color:{AM};font-weight:800;font-size:11px;text-transform:uppercase;letter-spacing:2px;margin-bottom:6px;}}
.ai-ban .tx {{color:#fff;font-size:14px;font-weight:500;line-height:1.5;}}

.sec {{background:#fff;border:1px solid #E8EAF0;border-radius:14px;padding:18px 20px;margin-bottom:14px;box-shadow:0 1px 6px rgba(0,0,0,.03);}}
.sh {{display:flex;align-items:center;gap:10px;padding-bottom:12px;margin-bottom:14px;border-bottom:2px solid {LR}15;}}
.sh .dt {{width:10px;height:10px;border-radius:50%;background:{LR};}}
.sh h3 {{font-size:15px;font-weight:800;color:{DN};margin:0;}}
.sh .sb {{font-size:9px;color:{GY};margin-left:auto;}}

.card {{background:#fff;border-radius:12px;padding:16px 18px;border:1px solid #E8EAF0;box-shadow:0 1px 4px rgba(0,0,0,.03);}}
.card h4 {{font-size:14px;font-weight:800;color:{DN};margin:0 0 4px;}}.card .sub {{font-size:9px;color:{GY};margin-bottom:10px;}}

.kpi {{background:#fff;border-radius:12px;padding:14px 16px;border:1px solid #E8EAF0;border-left:5px solid {DN};box-shadow:0 1px 4px rgba(0,0,0,.03);}}
.kpi .vl {{font-size:24px;font-weight:900;color:{DN};line-height:1.1;}}.kpi .lb {{font-size:9px;font-weight:600;color:{GY};text-transform:uppercase;letter-spacing:.5px;}}.kpi .sb {{font-size:9px;color:{GY};}}

.sbar {{display:flex;align-items:center;gap:10px;border-radius:10px;padding:8px 14px;margin-bottom:6px;border-left:5px solid;color:{DN};}}
.sbar .tg {{font-size:9px;font-weight:800;border-radius:5px;padding:3px 10px;color:#fff;}}.sbar .tx {{font-size:11px;font-weight:500;color:{DN};}}

.tile {{background:{BL};border-radius:10px;padding:12px;text-align:center;color:#fff;}}.tile .tv {{font-size:22px;font-weight:900;color:#fff;}}.tile .tl {{font-size:9px;opacity:.85;color:#fff;}}.tile-dk {{background:{DN};}}

.irow {{display:flex;align-items:center;gap:12px;padding:10px 14px;border-radius:10px;border:1px solid #F0F1F3;margin-bottom:5px;color:{DN};}}.irow:nth-child(odd) {{background:#FAFBFC;}}
.badge {{font-size:9px;font-weight:700;padding:3px 8px;border-radius:5px;white-space:nowrap;}}

.ctile {{padding:10px 12px;border-radius:10px;background:#fff;border:1px solid #E8EAF0;border-left:5px solid;}}.ctile .cv {{font-size:18px;font-weight:900;}}.ctile .cl {{font-size:10px;font-weight:700;color:{DN};}}.ctile .cs {{font-size:8px;color:{GY};}}

.cost-r {{display:flex;align-items:center;gap:10px;border-radius:10px;padding:10px 14px;margin-bottom:6px;color:{DN};}}.cost-hl {{color:#fff;border-radius:6px;padding:4px 12px;font-size:9px;font-weight:700;}}

.dark-bg {{color:#fff;}}.dark-bg div,.dark-bg span {{color:#fff;}}

.risk-c {{background:#FFF5F5;border:1px solid #FED7D7;border-left:6px solid {LR};border-radius:12px;padding:16px 18px;}}.risk-c h4 {{color:{LR};font-size:14px;margin:0 0 8px;}}

.ask-ban {{background:#FFF5F5;border:2px solid {LR};border-radius:12px;padding:14px;text-align:center;margin:14px 0;}}.ask-ban span {{font-size:15px;font-weight:700;color:{LR};}}

.bh {{background:#fff;border-radius:12px;padding:18px;text-align:center;border:1px solid #E8EAF0;box-shadow:0 1px 4px rgba(0,0,0,.03);}}.bh .bv {{font-size:28px;font-weight:900;color:{DN};}}.bh .bl {{font-size:11px;font-weight:700;color:{DN};margin-top:3px;}}.bh .bs {{font-size:9px;color:{GY};}}

.gpt-r {{background:#F0FDF4;border:1px solid #BBF7D0;border-radius:10px;padding:16px 18px;font-size:12px;color:{DN};line-height:1.7;}}

.es-hd {{background:{DN};border-radius:10px;padding:12px;text-align:center;color:#fff;font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;margin-bottom:5px;}}
.es-t {{background:{BL};border-radius:10px;padding:12px;text-align:center;color:#fff;margin-bottom:5px;}}.es-t .tv {{font-size:24px;font-weight:900;color:#fff;}}.es-t .tl {{font-size:9px;opacity:.85;color:#fff;}}

.rel-c {{padding:12px 16px;border-radius:10px;border-left:5px solid;margin-bottom:8px;background:#FAFBFC;border:1px solid #F0F1F3;color:{DN};}}

.obs {{padding:10px 14px;border-radius:10px;font-size:11px;margin-bottom:6px;border-left:5px solid;color:{DN};}}

.wi-bar {{margin-bottom:8px;}}.wi-bar .wh {{display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;color:{DN};}}.wi-bar .wt {{height:10px;background:#F3F4F6;border-radius:5px;overflow:hidden;}}.wi-bar .wf {{height:100%;border-radius:5px;}}

.crow {{display:flex;align-items:center;gap:6px;padding:5px 0;font-size:11px;border-bottom:1px solid #F3F4F6;color:{DN};}}.crow:last-child {{border-bottom:none;}}.cdot {{width:9px;height:9px;border-radius:3px;flex-shrink:0;}}

/* Tabs — dark text on non-selected, white on selected */
.stTabs [data-baseweb="tab-list"] {{gap:4px;}}
.stTabs [data-baseweb="tab"] {{background:#fff;border-radius:10px 10px 0 0;padding:10px 24px;font-weight:700;font-size:13px;border:1px solid #E8EAF0;border-bottom:none;color:{DN}!important;}}
.stTabs [data-baseweb="tab"] > div {{color:{DN}!important;}}
.stTabs [data-baseweb="tab"] > div > p {{color:{DN}!important;}}
.stTabs button[data-baseweb="tab"] {{color:{DN}!important;}}
.stTabs [aria-selected="true"] {{background:{LR}!important;color:#fff!important;border-color:{LR}!important;}}
.stTabs [aria-selected="true"] > div {{color:#fff!important;}}
.stTabs [aria-selected="true"] > div > p {{color:#fff!important;}}
.stTabs [aria-selected="true"] span {{color:#fff!important;}}

/* Plotly chart containers — rounded on all tabs */
div[data-testid="stPlotlyChart"] > div {{border-radius:12px;overflow:hidden;}}

/* Force dark text in Plotly SVG — axis, legends, ticks ONLY (not hover) */
div[data-testid="stPlotlyChart"] .xtick text, div[data-testid="stPlotlyChart"] .ytick text {{fill:{DN}!important;}}
div[data-testid="stPlotlyChart"] .legendtext {{fill:{DN}!important;}}
div[data-testid="stPlotlyChart"] .g-gtitle text {{fill:{DN}!important;}}
/* Plotly hover tooltip — keep white text on dark bg */
div[data-testid="stPlotlyChart"] .hoverlayer text {{fill:#fff!important;}}
div[data-testid="stPlotlyChart"] .hovertext text {{fill:#fff!important;}}
div[data-testid="stPlotlyChart"] .hovertext path {{stroke:#fff!important;}}

div[data-testid="stTextInput"] input {{border:2px solid {LR}!important;border-radius:10px!important;padding:10px 14px!important;font-size:12px!important;color:#fff!important;background:{DN}!important;}}
div[data-testid="stTextInput"] input:focus {{box-shadow:0 0 0 3px {LR}30!important;border-color:{LR}!important;}}
div[data-testid="stTextInput"] input::placeholder {{color:rgba(255,255,255,.45)!important;}}

/* Send / Ask button (primary) */
button[data-testid="stBaseButton-primary"] {{background:{LR}!important;color:#fff!important;border:none!important;border-radius:10px!important;font-size:13px!important;font-weight:700!important;cursor:pointer!important;height:44px!important;min-height:44px!important;letter-spacing:.3px;transition:background .2s;box-shadow:0 2px 8px rgba(213,43,30,.25)!important;}}
button[data-testid="stBaseButton-primary"]:hover {{background:#B82318!important;box-shadow:0 4px 12px rgba(213,43,30,.35)!important;}}
button[data-testid="stBaseButton-primary"]:active {{background:#9B1B14!important;}}
</style>""", unsafe_allow_html=True)

# ═══════ DATA ═══════
INITS = [dict(p=75,t="META Assessment & PLO Integration",r="META (UAE, KSA)",pr="Highest",s="In Progress",o="ML+Ops+DT"),dict(p=55,t="Agentic AI — IBU Chatbot Development",r="Global",pr="Highest",s="In Progress",o="ML Team"),dict(p=50,t="CNN/LSTM Model Optimization",r="Global",pr="High",s="In Progress",o="ML+Ops+DT"),dict(p=40,t="My Veeva Insights — Analytics",r="NA, Europe",pr="High",s="In Progress",o="Analytics"),dict(p=15,t="LATAM Phase 0 — NBE Expansion",r="LATAM",pr="Highest",s="Planning",o="ML+Ops+DT"),dict(p=10,t="Australia — Lilly 360 Launch",r="Australia",pr="High",s="Planning",o="APAC Analytics")]
MO = pd.DataFrame({"Month":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan'26"],"Incidents":[15,25,12,15,29,15,12,3,11,15,15,8,5],"Avg Days":[4.0,3.5,5.0,2.8,2.1,1.7,7.4,7.1,3.2,2.2,2.1,3.3,0]})
CATS = pd.DataFrame({"Category":["Data Error/Missing","Request for Info","Software Errors","Other","Config Error","Loopback Support","Remaining"],"Count":[122,18,17,7,6,5,5],"Pct":["67.8%","10.0%","9.4%","3.9%","3.3%","2.8%","2.8%"]})
RES = pd.DataFrame({"Month":["May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb"],"ML Ops":[62,58,72,68,55,50,52,48,30,18],"ZAIDYN DT&OC":[31,36,55,66,67,61,54,48,40,25],"Ops":[45,48,55,60,65,58,52,45,35,25]})
CO = pd.DataFrame({"Country":["France","Spain","Poland","Canada","UK","Germany","Japan_Med","Meta"],"Incidents":[39,35,25,16,15,9,9,9],"Avg Days":[2.81,2.74,3.69,1.63,3.69,2.90,4.44,0.93]})

CTX = """You are an executive AI analyst for IBU NBA/E Operations at Eli Lilly. DATA (Feb 2026):
INCIDENTS: 180 total, avg 3.2 biz days, peak May'25 (29), 68% Data Error/Missing, top: France(39), Spain(35), Poland(25).
CONFIG: 2,385 items (97% done), 58 releases (93.1%), AI/ML=29%, throughput +121% YoY, 12 markets, 4 active releases.
ES SPRINT: 31 JIRA items, ES51=13, ES52=18, 3.23% completion, 26 backlog (84%), 16 high priority, 52 days avg age, 9 markets.
INITIATIVES: META(75%), Agentic AI(55%), CNN/LSTM(50%), Veeva(40%), LATAM(15%), Australia(10%).
SAVINGS: EC2 500+hrs, Process ~600hrs, GIT ~1,500hrs = 2,600+ hrs/yr.
BUSINESS: 4.2M reach (↑18%), $8.3M cost avoidance, 0.82 utilisation."""

# ═══════ GPT ═══════
def gpt(prompt, sys=None, tok=300):
    try:
        c = AzureOpenAI(azure_endpoint=AZ["endpoint"],api_key=AZ["api_key"],api_version=AZ["api_version"])
        m = []
        if sys: m.append({"role":"system","content":sys})
        m.append({"role":"user","content":prompt})
        return c.chat.completions.create(model=AZ["deployment"],messages=m,max_tokens=tok,temperature=0.3).choices[0].message.content.strip()
    except Exception as e: return f"⚠️ {str(e)[:120]}"

@st.cache_data(ttl=3600)
def get_banner():
    return gpt(CTX+"\n\nProvide ONE sentence (max 30 words) — the most critical insight for leadership. Specific numbers. No preamble.","You are a concise executive briefing AI. One sharp sentence only.")

@st.cache_data(ttl=3600)
def get_insights():
    return gpt(CTX+"\n\nGenerate 3 insights (each max 20 words):\n1. [operational health]\n2. [delivery/growth]\n3. [risk/action]\nNo preamble.","Pharma ops analyst. Specific. No fluff.")

def ask_dashboard(q):
    return gpt(CTX+f"\n\nQuestion: {q}\n\nAnswer in 2-3 sentences. Specific numbers.","Executive dashboard AI for Lilly IBU Ops. Use only data provided.")

# ═══════ CHARTS ═══════
CHP = {"displayModeBar":False}
def ch_combo(h=260):
    fig=go.Figure()
    fig.add_trace(go.Bar(x=MO["Month"],y=MO["Incidents"],name="Incidents",marker_color=LR,text=MO["Incidents"],textposition="outside",textfont_size=9))
    fig.add_trace(go.Scatter(x=MO["Month"],y=MO["Avg Days"],name="Avg Days",mode="lines+markers+text",line=dict(color=AM,width=2.5),marker=dict(size=6),text=[f"{d:.1f}" if d>0 else "" for d in MO["Avg Days"]],textposition="top center",textfont_size=8,yaxis="y2"))
    fig.update_layout(height=h,margin=dict(l=40,r=40,t=10,b=30),yaxis=dict(showgrid=False,tickfont=dict(color=DN)),yaxis2=dict(overlaying="y",side="right",showgrid=False,range=[0,10],tickfont=dict(color=DN)),xaxis=dict(showgrid=False,tickfont=dict(color=DN)),legend=dict(orientation="h",y=-0.15,font_size=9,font_color=DN),plot_bgcolor="white",paper_bgcolor="white",font=dict(family="Arial",size=10,color=DN))
    return fig

def ch_res(h=210):
    fig=go.Figure()
    fig.add_trace(go.Bar(name="ML Ops",x=RES["Month"],y=RES["ML Ops"],marker_color=LR,text=RES["ML Ops"],textposition="outside",textfont_size=8))
    fig.add_trace(go.Bar(name="ZAIDYN DT & OC",x=RES["Month"],y=RES["ZAIDYN DT&OC"],marker_color=BL,text=RES["ZAIDYN DT&OC"],textposition="outside",textfont_size=8))
    fig.add_trace(go.Bar(name="Ops",x=RES["Month"],y=RES["Ops"],marker_color=AM,text=RES["Ops"],textposition="outside",textfont_size=8))
    fig.update_layout(barmode="group",height=h,margin=dict(l=30,r=10,t=15,b=30),yaxis=dict(showgrid=False,range=[0,100],ticksuffix="%",tickfont=dict(color=DN)),xaxis=dict(showgrid=False,tickfont=dict(color=DN)),legend=dict(orientation="h",y=-0.2,font_size=8,font_color=DN),plot_bgcolor="white",paper_bgcolor="white",font=dict(family="Arial",size=9,color=DN),bargap=0.15,bargroupgap=0.05)
    return fig

def ch_pie(h=180):
    fig=go.Figure(go.Pie(labels=CATS["Category"],values=CATS["Count"],hole=.55,marker_colors=PC,textinfo="percent",textfont_size=9))
    fig.update_layout(height=h,margin=dict(l=0,r=0,t=0,b=0),showlegend=False,plot_bgcolor="white",paper_bgcolor="white",font=dict(color=DN))
    return fig

# ═══════ HELPERS ═══════
def shdr(t,s=""): st.markdown(f'<div class="sh"><div class="dt"></div><h3>{t}</h3><span class="sb">{s}</span></div>',unsafe_allow_html=True)
def irow(n):
    pc=GR if n["p"]>=50 else AM if n["p"]>=25 else BL
    pb,pcl=("#FEE2E2","#991B1B") if n["pr"]=="Highest" else ("#DBEAFE","#1E40AF")
    sb,scl=("#FEF3C7","#92400E") if n["s"]=="In Progress" else ("#E0E7FF","#3730A3")
    return f'<div class="irow"><div style="width:55px;text-align:center"><div style="height:6px;background:#E5E7EB;border-radius:3px;overflow:hidden;margin-bottom:2px"><div style="height:100%;width:{n["p"]}%;background:{pc};border-radius:3px"></div></div><span style="font-size:12px;font-weight:700;color:{pc}">{n["p"]}%</span></div><div style="flex:1;min-width:0"><div style="font-size:12px;font-weight:600;color:#1A2E4A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{n["t"]}</div><div style="font-size:9px;color:#6B7280">{n["r"]}</div></div><span class="badge" style="background:{pb};color:{pcl}">{n["pr"]}</span><span class="badge" style="background:{sb};color:{scl}">{n["s"]}</span><span style="font-size:9px;color:#6B7280;min-width:75px">{n["o"]}</span></div>'

def ask_bar(key, show_title=False):
    """Render ask dashboard input with send button"""
    if show_title:
        st.markdown(f'<div class="ask-title">🔍 Ask Dashboard</div>',unsafe_allow_html=True)
    ic, bc = st.columns([9, 1])
    with ic:
        q = st.text_input("Ask", placeholder="e.g. Which market has highest incident volume? What's the sprint completion risk?", key=key, label_visibility="collapsed")
    with bc:
        clicked = st.button("➤ Ask", key=f"{key}_btn", type="primary", use_container_width=True)
    if q:
        with st.spinner("Analysing..."):
            a = ask_dashboard(q)
        st.markdown(f'<div class="gpt-r">{a}</div>', unsafe_allow_html=True)

def rel_card(n,m,s,d,p):
    """Render release card without f-string HTML escaping issues"""
    bc = BL if p>0 else (AM if "Doc" in s else GY)
    pct_bg = "#DCFCE7" if p>0 else "#FEF3C7"
    pct_clr = "#166534" if p>0 else "#92400E"
    bar = ""
    if p > 0:
        bar = f'<div style="height:5px;background:#E5E7EB;border-radius:3px;margin-top:6px;overflow:hidden"><div style="height:100%;width:{p}%;background:{GR};border-radius:3px"></div></div>'
    return f'<div class="rel-c" style="border-left-color:{bc}"><div style="display:flex;justify-content:space-between;align-items:center"><b style="font-size:12px;color:#1A2E4A">{n}</b><span style="font-size:10px;padding:3px 10px;border-radius:5px;background:{pct_bg};color:{pct_clr};font-weight:700">{p}%</span></div><div style="font-size:9px;color:{GY};margin-top:4px">📍 {m} · 📋 {s} · 📅 {d}</div>{bar}</div>'

# ═══════════════════════════════════════
# HEADER
# ═══════════════════════════════════════
st.markdown(f'<div class="hdr"><img src="data:image/png;base64,{LOGO}" alt="Lilly"><div><h1>IBU NBA/E Operations — Executive Summary</h1><p>AI-ML Implementation | As of Feb 2026 | JIRA · ServiceNow · H2 Resource Plan</p></div></div>',unsafe_allow_html=True)

# ═══════ ASK DASHBOARD (top bar) ═══════
ask_bar("ask_top", show_title=True)

# ═══════ AI BANNER ═══════
ban = get_banner()
st.markdown(f'<div class="ai-ban"><div class="lb">🧠 AI Insight — GPT-4.1</div><div class="tx">{ban}</div></div>',unsafe_allow_html=True)

# ═══════ TABS ═══════
t1,t2,t3,t4 = st.tabs(["📊 Summary","🔴 SNOW Incidents","🔧 ES Sprint","⚙️ Config Program"])

with t1:
    # ── INITIATIVES + PRIORITIES ──
    st.markdown('<div class="sec">',unsafe_allow_html=True)
    c1,c2 = st.columns([3,1])
    with c1:
        shdr("New Initiatives & Updates","6 active | JIRA Stories")
        for n in INITS: st.markdown(irow(n),unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="card" style="border-left:5px solid {AM};height:100%"><h4>Quarterly Priorities</h4><div style="font-size:12px;color:{DN};line-height:2;margin-top:10px"><b>1)</b> Australia: Lilly 360 Launch<br><b>2)</b> LATAM Phase 1 by Apr 2026<br><b>3)</b> GenAI Insights go-live Mar 2026<br><b>4)</b> Jaypirca AI/ML Multi-EU docs</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    # ── AI INSIGHTS (moved up) ──
    st.markdown('<div class="sec">',unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        shdr("🧠 Market Insights — AI Generated","GPT-4.1")
        ins = get_insights()
        st.markdown(f'<div class="gpt-r" style="font-size:13px;line-height:1.9;white-space:pre-line">{ins}</div>',unsafe_allow_html=True)
    with c2:
        shdr("REACH HCP/REPS — Business Health","Key metrics YTD")
        bc1,bc2,bc3 = st.columns(3)
        with bc1: st.markdown(f'<div class="bh"><div class="bv">4.2M</div><div class="bl">Total Reach</div><div class="bs">Customers ↑18% YTD</div></div>',unsafe_allow_html=True)
        with bc2: st.markdown(f'<div class="bh"><div class="bv">$8.3M</div><div class="bl">Cost Avoidance</div><div class="bs">Ops savings YTD</div></div>',unsafe_allow_html=True)
        with bc3: st.markdown(f'<div class="bh"><div class="bv">0.82</div><div class="bl">Utilisation</div><div class="bs">All workstreams</div></div>',unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="risk-c"><h4>🔴 Market Expansion — APAC [AT RISK]</h4><div style="font-size:9px;color:{GY};margin-bottom:8px">Raj Patel | Regional Lead</div><div style="font-size:11px;line-height:1.6;color:#1A2E4A"><b>Objective:</b> Enter SG, MY, TH by Q4 2025<br><b>Progress:</b> MY & TH on track. SG delayed ~6 wks<br><span style="color:{GR}">✓</span> MY pilot: SGD 1.2M<br><span style="color:{GR}">✓</span> TH partnership signed<br><span style="color:{LR}">▲</span> SG regulatory delayed<br><span style="color:{LR}">▲</span> FX headwinds<br><b>→</b> Engage MAS advisor for SG<br><b>→</b> Board approval for revised timeline</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    # ── NBA + COST + RESOURCE ──
    st.markdown('<div class="sec">',unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        shdr("NBA/E Sprint Updates","ES51 & ES52")
        for tg,tx,bg,ac in [("PROGRESS","3.23% completion, 1 completed in ES51","#DBEAFE","#93C5FD"),("RISK","26 Backlog items need sprint planning","#F3E8FF","#D8B4FE"),("PRIORITY","16 High Priority across sprints","#FEF9C3","#FCD34D"),("SCALE","9 Markets, 2 Focus Brands, 2 Epics","#DCFCE7","#86EFAC")]:
            st.markdown(f'<div class="sbar" style="background:{bg};border-color:{ac}"><span class="tg" style="background:{ac}">{tg}</span><span class="tx">{tx}</span></div>',unsafe_allow_html=True)
        tiles='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:8px">'
        for v,l,cls in [("31","JIRA Items",""),("13","ES51",""),("18","ES52","tile-dk"),("52 Days","Avg Backlog Age","tile-dk")]:
            tiles+=f'<div class="tile {cls}"><div class="tv">{v}</div><div class="tl">{l}</div></div>'
        st.markdown(tiles+'</div>',unsafe_allow_html=True)
    with c2:
        shdr("Cost Savings & Productivity","FTE Hours | IBU Ops")
        for ic,hl,c,bg in [("⚡ EC2 Automation","+90% productivity",GR,"#ECFDF5"),("⚙️ Process Improvements","+40% productivity",BL,"#EFF6FF"),("🔄 GIT Implementation","Manual→Controlled",PR,"#F5F3FF")]:
            st.markdown(f'<div class="cost-r" style="background:{bg};border:1px solid {c}22"><div style="flex:1;font-size:12px;font-weight:700;color:#1A2E4A">{ic}</div><span class="cost-hl" style="background:{c}">{hl}</span></div>',unsafe_allow_html=True)
        st.markdown(f'<div class="dark-bg" style="background:linear-gradient(135deg,{DN},#2A4366);border-radius:10px;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;margin-top:6px"><div style="font-size:10px;opacity:.8;font-weight:600">TOTAL ANNUAL SAVINGS</div><div style="font-size:24px;font-weight:900">2,600+ hrs</div></div>',unsafe_allow_html=True)
    with c3:
        shdr("Resource Utilisation","% Capacity | May'25–Feb'26")
        st.plotly_chart(ch_res(195),use_container_width=True,config=CHP)
    st.markdown('</div>',unsafe_allow_html=True)

    # ── CONFIG + SNOW CATS ──
    st.markdown('<div class="sec">',unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        shdr("Config Program Health","IBUNBE JIRA | 12 Markets")
        cfg='<div style="display:grid;grid-template-columns:1fr 1fr;gap:7px">'
        for v,l,s,c in [("2,385","Work Items","97% Done",GR),("58","Releases","54 Done (93.1%)",BL),("29%","AI/ML Share","of portfolio",PR),("+121%","Throughput ↑","Q3'24→Q3'25",GR),("1,200","Items Delivered","via sprints",DN),("4","Active Releases","In Prog/Doc",AM)]:
            cfg+=f'<div class="ctile" style="border-color:{c}"><div class="cv" style="color:{c}">{v}</div><div class="cl">{l}</div><div class="cs">{s}</div></div>'
        st.markdown(cfg+'</div>',unsafe_allow_html=True)
        st.markdown(f'<div style="padding:6px 10px;background:#F0FDF4;border-radius:8px;border:1px solid #BBF7D0;font-size:9px;color:#166534;margin-top:6px"><b>Top:</b> Mounjaro(18)·Platform(13)·Jaypirca(6) | <b>Active:</b> GenAI·Jaypirca·LATAM·MJO</div>',unsafe_allow_html=True)
    with c2:
        shdr("SNOW — Category Breakdown","180 total | 68% Data Error/Missing")
        pc1,pc2 = st.columns([2,3])
        with pc1: st.plotly_chart(ch_pie(170),use_container_width=True,config=CHP)
        with pc2:
            for _,row in CATS.iterrows():
                st.markdown(f'<div class="crow"><span style="flex:1;color:{DN}">{row["Category"]}</span><span style="font-weight:700;color:{DN}">{row["Count"]} ({row["Pct"]})</span></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    # ── ASK BANNER ──
    st.markdown('<div class="ask-ban"><span>🔴 Ask / Support — Leadership Action Required</span></div>',unsafe_allow_html=True)

    # ── INCIDENT TREND ──
    st.markdown('<div class="sec">',unsafe_allow_html=True)
    shdr("SNOW — Incident Trend","Monthly volume & avg resolution | Jan'25–Jan'26")
    st.plotly_chart(ch_combo(260),use_container_width=True,config=CHP)
    st.markdown('</div>',unsafe_allow_html=True)

# ═══════ TAB 2: SNOW ═══════
with t2:
    st.markdown('<div class="sec">',unsafe_allow_html=True)
    shdr("Incident KPIs","Jan'25–Jan'26")
    k1,k2,k3,k4=st.columns(4)
    for col,v,l,s,c in [(k1,"180","Total Incidents","Jan'25–Jan'26",LR),(k2,"3.2 days","Avg Resolution","Business days",BL),(k3,"May '25","Peak Month","29 incidents",AM),(k4,"68%","Top Category","Data Error/Missing",PR)]:
        with col: st.markdown(f'<div class="kpi" style="border-left-color:{c}"><div class="lb">{l}</div><div class="vl">{v}</div><div class="sb">{s}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="sec">',unsafe_allow_html=True)
    shdr("Monthly Volume + Resolution","Bar = Incidents | Line = Avg Days")
    st.plotly_chart(ch_combo(280),use_container_width=True,config=CHP)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="sec">',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Incidents by Country","Top 8")
        fig=go.Figure(go.Bar(y=CO["Country"],x=CO["Incidents"],orientation="h",marker_color=LR,text=CO["Incidents"],textposition="outside",textfont_size=9))
        fig.update_layout(height=240,margin=dict(l=5,r=30,t=10,b=10),xaxis=dict(showgrid=False),yaxis=dict(showgrid=False,autorange="reversed"),plot_bgcolor="white",paper_bgcolor="white",font=dict(family="Arial",size=9,color=DN))
        st.plotly_chart(fig,use_container_width=True,config=CHP)
    with c2:
        shdr("Resolution by Country","Color = speed")
        clrs=[GR if d<3 else AM if d<4 else LR for d in CO["Avg Days"]]
        fig2=go.Figure(go.Bar(y=CO["Country"],x=CO["Avg Days"],orientation="h",marker_color=clrs,text=[f"{d:.1f}" for d in CO["Avg Days"]],textposition="outside",textfont_size=9))
        fig2.update_layout(height=240,margin=dict(l=5,r=30,t=10,b=10),xaxis=dict(showgrid=False),yaxis=dict(showgrid=False,autorange="reversed"),plot_bgcolor="white",paper_bgcolor="white",font=dict(family="Arial",size=9,color=DN))
        st.plotly_chart(fig2,use_container_width=True,config=CHP)
    st.markdown('</div>',unsafe_allow_html=True)

# ═══════ TAB 3: ES SPRINT ═══════
with t3:
    st.markdown('<div class="sec">',unsafe_allow_html=True)
    shdr("ES Sprint — JIRA Dashboard","ES51 & ES52 | Feb 2026")
    td=[("SPRINT METRICS",[("31","Total JIRA Items"),("13","ES51"),("18","ES52"),("3.23%","Completion Rate")]),("STATUS TRACKING",[("1","Total Completed"),("2","Total Approved"),("26","Total Backlog"),("2","Total Cancelled")]),("ES REQUESTS",[("31","No. of ES Requests"),("31","Total Stories"),("2","Total Epics"),("9","Config Items")]),("PRIORITIZATION",[("9","Total Markets"),("2","Focus Brands"),("16","High Priority"),("52 Days","Avg Backlog Age")])]
    cols=st.columns(4)
    for i,(h,items) in enumerate(td):
        with cols[i]:
            st.markdown(f'<div class="es-hd">{h}</div>',unsafe_allow_html=True)
            for v,l in items: st.markdown(f'<div class="es-t"><div class="tv">{v}</div><div class="tl">{l}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="sec">',unsafe_allow_html=True)
    shdr("Active Initiatives","6 from JIRA Stories")
    for n in INITS: st.markdown(irow(n),unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="sec">',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Sprint Status")
        for tg,tx,bg,ac in [("PROGRESS","3.23% — 1 completed in ES51","#DBEAFE","#93C5FD"),("RISK","26 Backlog items require planning","#F3E8FF","#D8B4FE"),("PRIORITY","16 High Priority across sprints","#FEF9C3","#FCD34D"),("SCALE","9 markets, 33 JIRA items","#DCFCE7","#86EFAC")]:
            st.markdown(f'<div class="sbar" style="background:{bg};border-color:{ac}"><span class="tg" style="background:{ac}">{tg}</span><span class="tx">{tx}</span></div>',unsafe_allow_html=True)
    with c2:
        shdr("Key Observations")
        for tx,bg,c in [("Backlog: 26/31 (84%) — velocity needs acceleration","#FEF2F2",LR),("Age Risk: 52 days avg — beyond 2 sprint cycles","#FFFBEB",AM),("Scale: 9 markets, 2 brands — broad but thin","#F0FDF4",GR)]:
            st.markdown(f'<div class="obs" style="background:{bg};border-color:{c};color:#1A2E4A">{tx}</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ═══════ TAB 4: CONFIG ═══════
with t4:
    st.markdown('<div class="sec">',unsafe_allow_html=True)
    shdr("Config Program KPIs","IBUNBE JIRA | Feb 2026")
    cols=st.columns(6)
    for i,(v,l,s,c) in enumerate([("2,385","Total Work Items","Across 58 releases",DN),("97.0%","Completion Rate","2,314 done",GR),("58","Total Releases","54 done (93.1%)",BL),("29%","AI/ML Portfolio","17 of 58",PR),("+121%","Throughput ↑","Q3'24→Q3'25",GR),("12","Markets","Global",AM)]):
        with cols[i]: st.markdown(f'<div class="kpi" style="border-left-color:{c}"><div class="lb">{l}</div><div class="vl">{v}</div><div class="sb">{s}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="sec">',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Quarterly Delivery Trend","Total: 1,200 items")
        colors=["#93C5FD","#60A5FA","#3B82F6",BL,BL,LR]
        fig=go.Figure(go.Bar(x=["Q2'24","Q3'24","Q4'24","Q1'25","Q2'25","Q3'25"],y=[32,143,256,218,235,316],marker_color=colors,text=[32,143,256,218,235,316],textposition="outside",textfont_size=10))
        fig.update_layout(height=240,margin=dict(l=30,r=10,t=10,b=30),yaxis=dict(showgrid=False),xaxis=dict(showgrid=False),plot_bgcolor="white",paper_bgcolor="white",font=dict(family="Arial",size=10,color=DN))
        st.plotly_chart(fig,use_container_width=True,config=CHP)
    with c2:
        shdr("Active Releases (4)","Config JIRA IBUNBE")
        st.markdown(rel_card("GenAI Boosted Insights","IBU Global","In Progress","Mar 2026",55.6),unsafe_allow_html=True)
        st.markdown(rel_card("Jaypirca AI/ML (M5)","Multi-EU","In Documentation","May 2026",0),unsafe_allow_html=True)
        st.markdown(rel_card("MJO T2D/CWM (ES-IT)","ES/IT","In Documentation","Jun 2026",0),unsafe_allow_html=True)
        st.markdown(rel_card("LATAM Phase 1","LATAM","Backlog","Jun 2026",0),unsafe_allow_html=True)
        st.markdown(f'<div style="padding:7px 12px;background:#EFF6FF;border-radius:8px;border:1px solid #BFDBFE;font-size:10px;color:#1E40AF;margin-top:4px"><b>In Flight:</b> IBU Global — Cross-Market GenAI platform</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="sec">',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1:
        shdr("Releases by Product","58 total")
        prods=["Mounjaro","Platform/Other","Jaypirca","Verzenio","MSR/Med","Donanemab","Omvoh","Kisunla","Ebglyss"]
        pvals=[18,13,6,5,5,3,3,2,2]
        pclrs=[LR,LR,BL,BL,BL,GY,GY,GY,GY]
        fig=go.Figure(go.Bar(y=prods,x=pvals,orientation="h",marker_color=pclrs,text=pvals,textposition="outside",textfont_size=9))
        fig.update_layout(height=240,margin=dict(l=5,r=30,t=10,b=10),xaxis=dict(showgrid=False),yaxis=dict(showgrid=False,autorange="reversed"),plot_bgcolor="white",paper_bgcolor="white",font=dict(family="Arial",size=9,color=DN))
        st.plotly_chart(fig,use_container_width=True,config=CHP)
    with c2:
        shdr("Releases by Work Type","AI/ML leads at 29%")
        fig=go.Figure(go.Pie(labels=["AI/ML","BRB","CEI","MSR/Med","Other","PLO","Integration"],values=[17,13,10,7,7,2,2],hole=.45,marker_colors=PC,textinfo="label+percent",textfont_size=8))
        fig.update_layout(height=240,margin=dict(l=0,r=0,t=10,b=10),showlegend=False,plot_bgcolor="white",paper_bgcolor="white",font=dict(color=DN))
        st.plotly_chart(fig,use_container_width=True,config=CHP)
    with c3:
        shdr("Work Item Status","2,385 total")
        for s,v,p,c in [("Done",2314,"97.0%",GR),("Backlog",38,"1.6%","#94A3B8"),("Approved",23,"1.0%",BL),("In Progress",8,"0.3%",AM),("In Documentation",2,"0.1%",PR)]:
            w=max(v/2385*100,2)
            st.markdown(f'<div class="wi-bar"><div class="wh"><span style="font-weight:600;color:{DN}">{s}</span><span style="color:{GY}">{v:,} ({p})</span></div><div class="wt"><div class="wf" style="width:{w}%;background:{c}"></div></div></div>',unsafe_allow_html=True)
        mc1,mc2=st.columns(2)
        with mc1: st.markdown(f'<div class="bh" style="padding:10px"><div class="bv" style="font-size:20px;color:{GR}">41</div><div class="bs">Avg Items/Release</div></div>',unsafe_allow_html=True)
        with mc2: st.markdown(f'<div class="bh" style="padding:10px"><div class="bv" style="font-size:20px;color:{BL}">16</div><div class="bs">Multi-Market Releases</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

st.markdown(f'<div style="text-align:center;padding:16px 0;font-size:9px;color:{GY}">IBU NBA/E Operations | Eli Lilly and Company | Feb 2026 | AI Insights by Azure OpenAI GPT-4.1</div>',unsafe_allow_html=True)