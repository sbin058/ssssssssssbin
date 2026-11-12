# -*- coding: utf-8 -*-
"""
🚦 안전한 등하굣길 분석실

이 앱은 공공데이터포털에서 확인한 한국도로교통공단 교통사고 통계를
코드 안에 미리 정리해 두고, Streamlit과 Plotly로 시각화합니다.

중요:
- 앱 실행 중 데이터를 인터넷에서 다시 수집하지 않습니다.
- CSV 업로드도 필요하지 않습니다.
- 아래 표의 수치는 공공데이터포털의 공개 미리보기에서 직접 확인한 값입니다.
- 미리보기 일부 행만 확인된 자료는 사용 범위를 화면에 따로 표시합니다.
- 실행: streamlit run main.py
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 화면 디자인
# -----------------------------------------------------------------------------
APP_TITLE = "🚦 안전한 등하굣길 분석실"

st.set_page_config(
    page_title="안전한 등하굣길 분석실",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#101B3D"
BLUE = "#5574F7"
SKY = "#42D6E8"
RED = "#FF5C7A"
ORANGE = "#FFB454"
GREEN = "#35C99A"
PURPLE = "#9A72FF"
GRAY = "#91A0BC"
PALE = "#F3F6FF"

st.markdown(
    """
    <style>
    :root {
        --ink: #111A36;
        --muted: #71809F;
        --line: rgba(126, 149, 206, .20);
        --panel: rgba(255,255,255,.90);
    }
    .stApp {
        background:
          radial-gradient(circle at 4% 0%, rgba(85,116,247,.15), transparent 28%),
          radial-gradient(circle at 94% 8%, rgba(66,214,232,.13), transparent 25%),
          linear-gradient(135deg, #F4F7FF 0%, #EEF4FF 48%, #F8FAFF 100%);
        color: var(--ink);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101B3D 0%, #172B58 55%, #203B70 100%);
        border-right: 1px solid rgba(255,255,255,.12);
    }
    [data-testid="stSidebar"] * { color: #F3F6FF !important; }
    [data-testid="stSidebar"] [data-baseweb="radio"] label {
        border-radius: 11px; padding: 8px 10px; margin: 3px 0;
        background: rgba(255,255,255,.035);
    }
    [data-testid="stSidebar"] [data-baseweb="radio"] label:hover {
        background: rgba(95,134,255,.24);
    }
    h1, h2, h3, h4 { color: #15254C; letter-spacing: -.02em; }
    h2 { margin-top: .5rem; }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(255,255,255,.98), rgba(239,244,255,.92));
        border: 1px solid rgba(98,126,202,.20);
        border-radius: 18px; padding: 17px 18px;
        box-shadow: 0 12px 28px rgba(35,57,112,.07);
        min-height: 116px;
    }
    [data-testid="stMetricLabel"] { color: #68799C !important; font-weight: 650; }
    [data-testid="stMetricValue"] { color: #172A59 !important; font-weight: 850; }
    [data-testid="stMetricDelta"] { font-weight: 700; }
    .hero {
        position: relative; overflow: hidden;
        background: linear-gradient(112deg, #101B3D 0%, #263E87 53%, #3B61C8 100%);
        color: white; border: 1px solid rgba(255,255,255,.18);
        border-radius: 25px; padding: 29px 32px 27px 32px;
        margin: 2px 0 15px 0;
        box-shadow: 0 20px 45px rgba(33,55,121,.22);
    }
    .hero:after {
        content: ""; position: absolute; right: -45px; top: -110px;
        width: 330px; height: 330px; border-radius: 50%;
        background: radial-gradient(circle, rgba(66,214,232,.30), rgba(154,114,255,.12) 52%, transparent 70%);
    }
    .hero h1 { color: white !important; margin: 0 0 8px 0; font-size: 2.25rem; font-weight: 900; }
    .hero p { color: #E5EDFF; margin: 0; font-size: 1rem; line-height: 1.65; max-width: 880px; }
    .hero-kicker { color: #8FEAF1; font-size: .76rem; font-weight: 800; letter-spacing: .18em; margin-bottom: 7px; }
    .hero-chip {
        display: inline-block; margin: 14px 7px 0 0; padding: 6px 11px;
        color: #F7FAFF; background: rgba(255,255,255,.12);
        border: 1px solid rgba(255,255,255,.18); border-radius: 30px;
        font-size: .77rem; font-weight: 650;
    }
    .section-label {
        color: #5574F7; font-size: .72rem; font-weight: 850;
        letter-spacing: .16em; text-transform: uppercase; margin-bottom: 3px;
    }
    .glass-card {
        background: rgba(255,255,255,.82); border: 1px solid rgba(108,132,199,.20);
        border-radius: 17px; padding: 17px 19px; margin: 5px 0 14px 0;
        box-shadow: 0 10px 28px rgba(33,55,121,.055);
    }
    .insight {
        background: linear-gradient(115deg, rgba(255,255,255,.97), rgba(239,246,255,.95));
        border: 1px solid rgba(85,116,247,.18); border-left: 5px solid #5574F7;
        border-radius: 14px; padding: 15px 18px; margin: 9px 0 16px 0;
        box-shadow: 0 8px 22px rgba(35,57,112,.05); line-height: 1.8;
    }
    .small-note { color: #71809F; font-size: .86rem; }
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,.73); border: 1px solid rgba(108,132,199,.18);
        border-radius: 14px;
    }
    .stButton > button, .stDownloadButton > button {
        border: 0; border-radius: 12px; color: white; font-weight: 750;
        background: linear-gradient(100deg, #5574F7, #765EF3 60%, #9A72FF);
        box-shadow: 0 7px 17px rgba(85,116,247,.22);
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        color: white; border: 0; filter: brightness(1.06); transform: translateY(-1px);
    }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div {
        border-radius: 11px !important; border-color: rgba(98,126,202,.27) !important;
    }
    div[data-testid="stDataFrame"] { border: 1px solid rgba(98,126,202,.18); border-radius: 13px; overflow: hidden; }
    hr { border-color: rgba(98,126,202,.18); }
    @media (max-width: 700px) {
        .hero { padding: 22px 20px; }
        .hero h1 { font-size: 1.65rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# 2. 공공데이터포털에서 확인한 원자료를 코드에 직접 저장
#    (앱 실행 시 별도 업로드나 인터넷 연결 없이 바로 사용할 수 있습니다.)
# -----------------------------------------------------------------------------

# [자료 A] 한국도로교통공단_최근 5년 어린이보호구역내 어린이(12세 이하) 교통사고 통계
# 데이터셋 ID: 15118850 / 공개 미리보기 5행 전체
school_zone = pd.DataFrame(
    [
        [2021, "Y", 523, 2, 124, 419, 20],
        [2022, "Y", 514, 3, 141, 355, 33],
        [2023, "Y", 486, 2, 111, 374, 38],
        [2024, "Y", 526, 2, 120, 399, 37],
        [2025, "Y", 927, 1, 194, 726, 93],
    ],
    columns=["발생년", "어린이보호구역여부", "사고건수", "사망자수", "중상자수", "경상자수", "부상신고자수"],
)
school_zone["부상자수"] = school_zone["중상자수"] + school_zone["경상자수"] + school_zone["부상신고자수"]
school_zone["사망자수_사고100건당"] = school_zone["사망자수"] / school_zone["사고건수"] * 100

# [자료 B] 한국도로교통공단_시간대별 교통사고 통계_20251231
# 데이터셋 ID: 15087037 / 공개 미리보기 12행 전체
hourly = pd.DataFrame(
    [
        ["00시-02시", 5566, 158, 1604, 5697, 570],
        ["02시-04시", 3114, 118, 899, 3097, 349],
        ["04시-06시", 4405, 164, 1477, 3977, 423],
        ["06시-08시", 11794, 238, 3290, 11259, 1098],
        ["08시-10시", 22109, 218, 5581, 22508, 2155],
        ["10시-12시", 20675, 261, 5522, 21846, 2123],
        ["12시-14시", 22346, 245, 5725, 24471, 2358],
        ["14시-16시", 23561, 271, 5881, 25726, 2498],
        ["16시-18시", 27278, 237, 6416, 29052, 2958],
        ["18시-20시", 26247, 262, 6256, 26865, 2697],
        ["20시-22시", 16327, 219, 4283, 16623, 1714],
        ["22시-24시", 10467, 158, 2729, 10925, 1099],
    ],
    columns=["시간대", "사고건수", "사망자수", "중상자수", "경상자수", "부상신고자수"],
)
hourly["부상자수"] = hourly["중상자수"] + hourly["경상자수"] + hourly["부상신고자수"]
hourly["사망자수_사고100건당"] = hourly["사망자수"] / hourly["사고건수"] * 100
hourly["부상자수_사고100건당"] = hourly["부상자수"] / hourly["사고건수"] * 100

# 시간대 구분은 그래프에서 읽기 쉽도록 4개 구간으로 묶었습니다.
def classify_time(time_text):
    start_hour = int(time_text[:2])
    if start_hour < 6:
        return "새벽(00~06시)"
    if start_hour < 12:
        return "오전(06~12시)"
    if start_hour < 18:
        return "오후(12~18시)"
    return "저녁·밤(18~24시)"

hourly["시간구간"] = hourly["시간대"].apply(classify_time)

# [자료 C] 한국도로교통공단_월별 주야별 교통사고 통계_20251231
# 데이터셋 ID: 15070318 / 공개 미리보기 24행 전체
_day_night_rows = [
    ["01", "주", 8856, 100, 2262, 9705, 854],
    ["01", "야", 4884, 85, 1243, 5136, 472],
    ["02", "주", 8396, 94, 2030, 9058, 850],
    ["02", "야", 4620, 64, 1129, 4782, 421],
    ["03", "주", 9634, 117, 2348, 10309, 997],
    ["03", "야", 4986, 86, 1327, 4977, 523],
    ["04", "주", 11114, 115, 2873, 11760, 1125],
    ["04", "야", 5271, 62, 1337, 5423, 543],
    ["05", "주", 10924, 121, 2789, 11643, 1195],
    ["05", "야", 5420, 78, 1404, 5663, 585],
    ["06", "주", 10963, 117, 2805, 11429, 1130],
    ["06", "야", 5212, 94, 1444, 5215, 564],
    ["07", "주", 12054, 135, 2947, 12666, 1306],
    ["07", "야", 5757, 102, 1507, 5719, 577],
    ["08", "주", 11028, 146, 2776, 12053, 1168],
    ["08", "야", 5623, 113, 1512, 5625, 633],
    ["09", "주", 11538, 127, 2917, 11629, 1201],
    ["09", "야", 5892, 106, 1552, 5802, 626],
    ["10", "주", 10787, 141, 2854, 11404, 1085],
    ["10", "야", 6327, 101, 1716, 6359, 667],
    ["11", "주", 11496, 140, 3002, 11909, 1173],
    ["11", "야", 5946, 109, 1527, 6092, 615],
    ["12", "주", 10973, 117, 2812, 11297, 1106],
    ["12", "야", 6188, 79, 1550, 6391, 626],
]
day_night = pd.DataFrame(
    _day_night_rows,
    columns=["발생월", "주야", "사고건수", "사망자수", "중상자수", "경상자수", "부상신고자수"],
)
day_night["부상자수"] = day_night["중상자수"] + day_night["경상자수"] + day_night["부상신고자수"]
day_night["월"] = day_night["발생월"].astype(int)
day_night["사망자수_사고100건당"] = day_night["사망자수"] / day_night["사고건수"] * 100
day_night["부상자수_사고100건당"] = day_night["부상자수"] / day_night["사고건수"] * 100

# [자료 D] 한국도로교통공단_사고유형별 교통사고 통계_20251231
# 데이터셋 ID: 15070282 / 공개 미리보기에서 확인한 보행자 사고 4개 하위 유형만 사용
# 파일 전체는 18행이며, 아래 4행만 공개 미리보기에서 확인했으므로 전체 보행자 사고 합계로 표현하지 않습니다.
pedestrian_types = pd.DataFrame(
    [
        ["횡단중", 13777, 423, 6036, 7348, 727],
        ["차도통행중", 3459, 138, 1332, 1754, 327],
        ["길가장자리구역통행중", 1952, 22, 556, 1170, 251],
        ["보도통행중", 2052, 25, 581, 1328, 234],
    ],
    columns=["보행자 사고 하위 유형", "사고건수", "사망자수", "중상자수", "경상자수", "부상신고자수"],
)
pedestrian_types["부상자수"] = pedestrian_types["중상자수"] + pedestrian_types["경상자수"] + pedestrian_types["부상신고자수"]
pedestrian_types["사망자수_사고100건당"] = pedestrian_types["사망자수"] / pedestrian_types["사고건수"] * 100

# [자료 E] 한국도로교통공단_사고유형별 월별 교통사고 통계_20251231
# 데이터셋 ID: 15070290 / 200행 중 공개 미리보기에서 확인한 '횡단중' 월별 12행만 사용
pedestrian_crossing_month = pd.DataFrame(
    [
        [1, 1095, 37, 483, 576, 52],
        [2, 999, 30, 469, 497, 46],
        [3, 1020, 27, 423, 573, 53],
        [4, 1189, 28, 507, 656, 70],
        [5, 1111, 24, 471, 606, 61],
        [6, 1043, 33, 442, 565, 54],
        [7, 1079, 27, 474, 584, 55],
        [8, 1009, 36, 431, 554, 55],
        [9, 1243, 40, 514, 682, 86],
        [10, 1335, 47, 585, 703, 70],
        [11, 1252, 45, 594, 621, 61],
        [12, 1402, 49, 643, 731, 64],
    ],
    columns=["발생월", "사고건수", "사망자수", "중상자수", "경상자수", "부상신고자수"],
)
pedestrian_crossing_month["부상자수"] = (
    pedestrian_crossing_month["중상자수"]
    + pedestrian_crossing_month["경상자수"]
    + pedestrian_crossing_month["부상신고자수"]
)
pedestrian_crossing_month["사망자수_사고100건당"] = pedestrian_crossing_month["사망자수"] / pedestrian_crossing_month["사고건수"] * 100


# -----------------------------------------------------------------------------
# 3. 분석에 사용하는 값 계산
# -----------------------------------------------------------------------------
national_accidents = int(hourly["사고건수"].sum())
national_deaths = int(hourly["사망자수"].sum())
national_injuries = int(hourly["부상자수"].sum())

school_total_accidents = int(school_zone["사고건수"].sum())
school_total_deaths = int(school_zone["사망자수"].sum())
school_total_injuries = int(school_zone["부상자수"].sum())
latest_school = school_zone.iloc[-1]
previous_school = school_zone.iloc[-2]
school_yoy_change = (latest_school["사고건수"] / previous_school["사고건수"] - 1) * 100

crossing_accidents = int(pedestrian_crossing_month["사고건수"].sum())
day_total = int(day_night.loc[day_night["주야"] == "주", "사고건수"].sum())
night_total = int(day_night.loc[day_night["주야"] == "야", "사고건수"].sum())
day_share = day_total / (day_total + night_total) * 100
night_share = 100 - day_share

peak_hour_row = hourly.loc[hourly["사고건수"].idxmax()]
peak_fatal_rate_row = hourly.loc[hourly["사망자수_사고100건당"].idxmax()]
peak_month = (
    day_night.groupby("월", as_index=False)["사고건수"].sum().sort_values("사고건수", ascending=False).iloc[0]
)
peak_crossing_month = pedestrian_crossing_month.loc[pedestrian_crossing_month["사고건수"].idxmax()]

# 서로 다른 공개 통계의 합계를 대조해 내장 데이터의 일관성을 확인합니다.
time_total_matches = int(day_night["사고건수"].sum()) == national_accidents
crossing_total_matches = crossing_accidents == int(
    pedestrian_types.loc[pedestrian_types["보행자 사고 하위 유형"] == "횡단중", "사고건수"].iloc[0]
)


# -----------------------------------------------------------------------------
# 4. 그래프 공통 설정 및 CSV 다운로드 함수
# -----------------------------------------------------------------------------
def style_chart(fig, height=390):
    """모든 Plotly 그래프에 같은 글꼴, 여백, 배경을 적용합니다."""
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=20, r=20, t=65, b=40),
        font=dict(family="Malgun Gothic, Apple SD Gothic Neo, sans-serif", color="#24364B"),
        title_font=dict(size=18, color=NAVY),
        legend_title_text="구분",
        hoverlabel=dict(font_size=12),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#E8EEF4", zerolinecolor="#DCE5EF")
    return fig


def number(value):
    return f"{int(value):,}"


def download_csv(dataframe, file_name, button_label="CSV 다운로드", key=None):
    """앱에 내장된 실제 분석 데이터를 CSV로 저장할 수 있게 합니다."""
    st.download_button(
        label=button_label,
        data=dataframe.to_csv(index=False).encode("utf-8-sig"),
        file_name=file_name,
        mime="text/csv",
        key=key,
    )


# -----------------------------------------------------------------------------
# 5. 사용자 선택형 그래프 탐색실
# -----------------------------------------------------------------------------
EXPLORER_DATA = {
    "어린이보호구역 어린이 사고 (2021~2025)": school_zone,
    "전국 시간대별 교통사고 (2025)": hourly,
    "전국 월별 주간·야간 사고 (2025)": day_night,
    "보행자 사고 유형 미리보기 (2025)": pedestrian_types,
    "횡단 중 보행자 사고 월별 (2025)": pedestrian_crossing_month,
}


def render_chart_explorer():
    """사용자가 그래프 유형과 축 변수를 바꾸어 직접 탐색합니다."""
    st.markdown('<div class="section-label">INTERACTIVE DATA LAB</div>', unsafe_allow_html=True)
    st.header("🎛️ 그래프 탐색실")
    st.write("분석할 데이터부터 고르고 X축·Y축·색상·크기 변수를 직접 바꿔 보세요. 선택을 바꾸면 그래프가 즉시 다시 그려집니다.")

    selected_name = st.selectbox("① 분석할 데이터 선택", list(EXPLORER_DATA.keys()), key="explorer_dataset")
    df = EXPLORER_DATA[selected_name].copy()
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        st.warning("이 자료에는 그래프로 표현할 숫자형 열이 없습니다.")
        return

    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        chart_type = st.selectbox("② 그래프 종류", ["선 그래프", "막대그래프", "산점도", "히트맵"], key="explorer_chart_type")
    with col_b:
        metric = st.selectbox("③ 분석 지표(Y 또는 색상값)", numeric_cols, index=0, key="explorer_metric")
    with col_c:
        sort_order = st.selectbox("④ 정렬", ["원래 순서", "오름차순", "내림차순"], key="explorer_sort")

    st.markdown('<div class="glass-card"><b>축 및 시각화 변수 설정</b><br><span class="small-note">히트맵에서는 X축·Y축에 범주 변수를, 색상값에는 숫자 지표를 선택합니다.</span></div>', unsafe_allow_html=True)

    if chart_type == "히트맵":
        # 히트맵의 행/열은 적절한 개수의 범주값을 가진 열에서 고릅니다.
        category_cols = []
        for col in df.columns:
            if col == metric:
                continue
            nunique = df[col].nunique(dropna=True)
            if 1 < nunique <= 30:
                category_cols.append(col)
        if len(category_cols) < 2:
            st.info("이 데이터는 히트맵을 만들 범주형 변수가 2개 이상 필요합니다. 다른 데이터셋을 선택해 보세요.")
            return
        h1, h2, h3 = st.columns(3)
        with h1:
            row_var = st.selectbox("히트맵 Y축(행)", category_cols, index=0, key="explorer_heat_row")
        with h2:
            col_choices = [c for c in category_cols if c != row_var]
            col_var = st.selectbox("히트맵 X축(열)", col_choices, index=0, key="explorer_heat_col")
        with h3:
            agg = st.selectbox("셀 값 집계", ["합계", "평균", "최댓값"], key="explorer_heat_agg")
        agg_map = {"합계": "sum", "평균": "mean", "최댓값": "max"}
        work = df.copy()
        work[row_var] = work[row_var].astype(str)
        work[col_var] = work[col_var].astype(str)
        pivot = work.pivot_table(index=row_var, columns=col_var, values=metric, aggfunc=agg_map[agg], fill_value=0)
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=[str(x) for x in pivot.columns],
            y=[str(y) for y in pivot.index],
            colorscale="Turbo",
            colorbar=dict(title=metric),
            hovertemplate=f"{row_var}: %{{y}}<br>{col_var}: %{{x}}<br>{metric}: %{{z:,.1f}}<extra></extra>",
        ))
        fig.update_layout(title=f"{selected_name} · {metric} {agg}", xaxis_title=col_var, yaxis_title=row_var)
        st.plotly_chart(style_chart(fig, 500), use_container_width=True)
        st.caption("히트맵의 색이 진할수록 선택한 집계 지표의 값이 큽니다. 0은 실제 0이거나 해당 조합의 자료가 없는 경우일 수 있으므로 원본 표도 함께 확인하세요.")
        st.dataframe(pivot.reset_index(), use_container_width=True, hide_index=True)
        return

    # 선/막대/산점도는 X/Y축과 색상 구분을 모두 직접 조절할 수 있습니다.
    x_candidates = df.columns.tolist()
    d1, d2, d3, d4 = st.columns([1, 1, 1, 1])
    with d1:
        x_default = next((i for i, c in enumerate(x_candidates) if not pd.api.types.is_numeric_dtype(df[c])), 0)
        x_axis = st.selectbox("X축 변수", x_candidates, index=x_default, key="explorer_x_axis")
    with d2:
        y_default = numeric_cols.index(metric) if metric in numeric_cols else 0
        y_axis = st.selectbox("Y축 변수", numeric_cols, index=y_default, key="explorer_y_axis")
    color_options = ["구분 없음"] + [c for c in df.columns if c not in [x_axis, y_axis]]
    with d3:
        color_axis = st.selectbox("색상으로 구분", color_options, key="explorer_color_axis")
    size_options = ["사용 안 함"] + [c for c in numeric_cols if c not in [y_axis]]
    with d4:
        size_axis = st.selectbox("점 크기(산점도)", size_options, key="explorer_size_axis")

    plot_df = df.copy()
    if sort_order != "원래 순서":
        plot_df = plot_df.sort_values(x_axis, ascending=(sort_order == "오름차순"))
    color_arg = None if color_axis == "구분 없음" else color_axis

    labels = {x_axis: x_axis, y_axis: y_axis}
    if chart_type == "선 그래프":
        fig = px.line(plot_df, x=x_axis, y=y_axis, color=color_arg, markers=True, hover_data=plot_df.columns.tolist(), labels=labels)
    elif chart_type == "막대그래프":
        fig = px.bar(plot_df, x=x_axis, y=y_axis, color=color_arg, barmode="group", hover_data=plot_df.columns.tolist(), labels=labels)
    else:
        size_arg = None if size_axis == "사용 안 함" else size_axis
        fig = px.scatter(plot_df, x=x_axis, y=y_axis, color=color_arg, size=size_arg, hover_data=plot_df.columns.tolist(),
                         size_max=34, labels=labels, opacity=.82)
        fig.update_traces(marker=dict(line=dict(width=1, color="white")))
    fig.update_layout(title=f"{selected_name} · {y_axis} vs {x_axis}", xaxis_title=x_axis, yaxis_title=y_axis)
    st.plotly_chart(style_chart(fig, 500), use_container_width=True)

    if chart_type == "산점도":
        st.caption("점 하나는 원자료의 한 행입니다. 점의 위치·크기·색상은 선택한 변수의 값을 나타내며, 상관관계가 원인과 결과를 증명하지는 않습니다.")
    st.markdown("#### 선택한 데이터 원본")
    st.dataframe(df, use_container_width=True, hide_index=True)
    download_csv(df, "선택한_교통사고_데이터.csv", key="explorer_download")


# -----------------------------------------------------------------------------
# 6. 사이드바 메뉴 및 제목
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🚦 분석 메뉴")
    menu = st.radio(
        "보고 싶은 분석을 선택하세요.",
        [
            "🏠 한눈에 보기",
            "🎛️ 그래프 탐색실",
            "⏰ 시간대·주야별 분석",
            "🚶 보행자 사고 분석",
            "🏫 어린이보호구역 분석",
            "🧭 안전 개선 제안",
            "📚 데이터 출처·원본 확인",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**분석 기준**")
    st.caption("한국도로교통공단·한국도로공사 공개 통계")
    st.caption("앱 내장 데이터 · 업로드 불필요")
    st.caption("X/Y축 직접 선택 · 산점도 · 히트맵")
    st.caption("데이터 기준: 각 원본별 표기")

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-kicker">TRAFFIC SAFETY DATA LAB · PUBLIC DATA</div>
        <h1>{APP_TITLE}</h1>
        <p>교통사고 공공데이터를 여러 시각으로 탐색하고, 사고가 집중되는 시간·유형·환경을 파악해
        더 안전한 통학 환경을 고민하는 인터랙티브 분석 대시보드</p>
        <span class="hero-chip">📊 사고 통계 시각화</span>
        <span class="hero-chip">🎛️ X·Y축 직접 선택</span>
        <span class="hero-chip">🌈 산점도 · 히트맵</span>
        <span class="hero-chip">📚 공공데이터포털 기반</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("※ 지역별 좌표를 찍는 지도 앱이 아니라, 전국 단위의 집계 통계를 분석하는 앱입니다.")


# -----------------------------------------------------------------------------
# 6. 메뉴 1: 한눈에 보기
# -----------------------------------------------------------------------------
if menu == "🏠 한눈에 보기":
    st.subheader("📌 교통사고 핵심 지표")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("2025년 시간대별 사고건수 합계", number(national_accidents), help="시간대별 통계 12개 구간의 사고건수 합계")
    k2.metric("2025년 사망자수 합계", number(national_deaths), help="시간대별 통계의 사망자수 합계")
    k3.metric("2025년 부상자수 합계", number(national_injuries), help="중상자+경상자+부상신고자 합계")
    k4.metric("2025년 스쿨존 어린이 사고", number(int(latest_school["사고건수"])), help="12세 이하 어린이, 어린이보호구역 사고")

    st.info(
        "**범위 주의:** 앞의 세 지표는 2025년 전국 시간대별 교통사고 통계의 합계이고, "
        "네 번째 지표는 2025년 어린이보호구역 내 12세 이하 어린이 사고입니다. "
        "서로 다른 모집단이므로 네 수치를 서로 더하면 안 됩니다."
    )
    if time_total_matches and crossing_total_matches:
        st.success(
            "데이터 교차 확인 완료: 시간대별 합계와 월별 주·야간 합계가 모두 "
            f"{number(national_accidents)}건으로 일치하고, 횡단 중 월별 합계도 사고유형별 연간 값 "
            f"{number(crossing_accidents)}건과 일치합니다."
        )

    left, right = st.columns(2)
    with left:
        st.markdown("#### 최근 5년 스쿨존 어린이 사고")
        fig = px.line(
            school_zone,
            x="발생년",
            y="사고건수",
            markers=True,
            text="사고건수",
            hover_data=["사망자수", "중상자수", "경상자수", "부상신고자수"],
            labels={"발생년": "연도", "사고건수": "사고건수"},
        )
        fig.update_traces(line=dict(color=BLUE, width=4), marker=dict(size=10), textposition="top center")
        fig.update_xaxes(dtick=1)
        st.plotly_chart(style_chart(fig, 350), use_container_width=True)
    with right:
        st.markdown("#### 사고가 가장 많았던 시간대")
        fig = px.bar(
            hourly,
            x="시간대",
            y="사고건수",
            color="사고건수",
            color_continuous_scale=["#B8D9E8", BLUE, RED],
            text="사고건수",
            labels={"시간대": "사고 발생 시간", "사고건수": "사고건수"},
        )
        fig.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_chart(fig, 350), use_container_width=True)

    st.markdown(
        f"""
        <div class="insight">
        <b>핵심 관찰</b><br>
        • 전국 시간대별 통계에서는 <b>{peak_hour_row['시간대']}</b>에 사고가 가장 많았습니다
        ({number(peak_hour_row['사고건수'])}건).<br>
        • 어린이보호구역 내 12세 이하 어린이 사고는 2024년 {number(previous_school['사고건수'])}건에서
        2025년 {number(latest_school['사고건수'])}건으로 <b>{school_yoy_change:.1f}% 증가</b>했습니다.<br>
        • 보행자 사고 미리보기 4개 유형 중에서는 <b>횡단 중</b> 사고가 가장 큰 비중을 차지했습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# 7. 메뉴 2: 직접 조절하는 그래프 탐색실
# -----------------------------------------------------------------------------
elif menu == "🎛️ 그래프 탐색실":
    render_chart_explorer()


# -----------------------------------------------------------------------------
# 8. 메뉴 3: 시간대·주야별 분석
# -----------------------------------------------------------------------------
elif menu == "⏰ 시간대·주야별 분석":
    st.header("⏰ 언제 사고가 많이 발생할까?")
    st.write("시간대별 자료는 2시간 간격으로, 주야별 자료는 주간(06~18시)과 야간(18~06시)으로 구분됩니다.")

    peak_col1, peak_col2, peak_col3 = st.columns(3)
    peak_col1.metric("사고 최다 시간대", peak_hour_row["시간대"], f"{number(peak_hour_row['사고건수'])}건")
    peak_col2.metric("주간 사고 비중", f"{day_share:.1f}%", f"{number(day_total)}건")
    peak_col3.metric("야간 사고 비중", f"{night_share:.1f}%", f"{number(night_total)}건")

    st.markdown("#### ① 2시간 단위 사고 발생 건수")
    fig = px.bar(
        hourly,
        x="시간대",
        y="사고건수",
        color="시간구간",
        text="사고건수",
        category_orders={"시간대": hourly["시간대"].tolist()},
        color_discrete_map={
            "새벽(00~06시)": "#64748B",
            "오전(06~12시)": SKY,
            "오후(12~18시)": BLUE,
            "저녁·밤(18~24시)": ORANGE,
        },
        labels={"시간대": "사고 발생 시간대", "사고건수": "사고건수", "시간구간": "시간 구분"},
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    st.plotly_chart(style_chart(fig, 420), use_container_width=True)

    st.markdown("#### ② 사고건수와 사망자수의 관계: 산점도")
    scatter = px.scatter(
        hourly,
        x="사고건수",
        y="사망자수",
        size="중상자수",
        color="시간구간",
        text="시간대",
        hover_data={
            "사고건수": ":,",
            "사망자수": ":,",
            "중상자수": ":,",
            "사망자수_사고100건당": ":.2f",
        },
        color_discrete_map={
            "새벽(00~06시)": "#64748B",
            "오전(06~12시)": SKY,
            "오후(12~18시)": BLUE,
            "저녁·밤(18~24시)": ORANGE,
        },
        labels={"사고건수": "사고건수", "사망자수": "사망자수", "시간구간": "시간 구분"},
        size_max=34,
    )
    scatter.update_traces(textposition="top center", marker=dict(opacity=0.78, line=dict(width=1, color="white")))
    st.plotly_chart(style_chart(scatter, 430), use_container_width=True)
    st.caption("점 하나가 2시간 구간 하나를 뜻합니다. 점의 크기는 중상자수이며, 상관관계가 사고 원인을 의미하지는 않습니다.")

    st.markdown("#### ③ 월별 주간·야간 사고건수 비교")
    monthly_chart = px.bar(
        day_night,
        x="발생월",
        y="사고건수",
        color="주야",
        barmode="group",
        text="사고건수",
        color_discrete_map={"주": BLUE, "야": ORANGE},
        category_orders={"발생월": [f"{i:02d}" for i in range(1, 13)]},
        labels={"발생월": "월", "사고건수": "사고건수", "주야": "주야 구분"},
    )
    monthly_chart.update_traces(texttemplate="%{text:,}", textposition="outside")
    st.plotly_chart(style_chart(monthly_chart, 420), use_container_width=True)

    month_totals = day_night.groupby("월", as_index=False)["사고건수"].sum()
    fig = px.line(
        month_totals,
        x="월",
        y="사고건수",
        markers=True,
        text="사고건수",
        labels={"월": "월", "사고건수": "주간+야간 사고건수"},
    )
    fig.update_traces(line=dict(color=RED, width=3), textposition="top center")
    fig.update_xaxes(dtick=1)
    st.plotly_chart(style_chart(fig, 340), use_container_width=True)

    st.markdown(
        f"""
        <div class="insight">
        <b>시간대 분석 해석</b><br>
        • 사고건수는 <b>{peak_hour_row['시간대']}</b>가 가장 많았습니다.<br>
        • 사고 100건당 사망자수는 <b>{peak_fatal_rate_row['시간대']}</b>가 가장 높았습니다
        ({peak_fatal_rate_row['사망자수_사고100건당']:.2f}명/100건).<br>
        • 월별 주간·야간 합계는 <b>{int(peak_month['월'])}월</b>에 가장 많았습니다
        ({number(peak_month['사고건수'])}건).
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# 8. 메뉴 3: 보행자 사고 분석
# -----------------------------------------------------------------------------
elif menu == "🚶 보행자 사고 분석":
    st.header("🚶 보행자는 어떤 상황에서 위험할까?")
    st.write("보행자 사고 하위 유형 통계와 횡단 중 사고의 월별 흐름을 살펴봅니다.")

    st.warning(
        "사고유형별 파일은 전체 18행 중 공공데이터포털 미리보기에서 확인 가능한 보행자 하위 유형 4행만 사용했습니다. "
        "아래 4개 유형의 합계를 전체 보행자 사고 총계로 해석하면 안 됩니다."
    )

    st.markdown("#### ① 확인된 보행자 사고 유형 4개")
    fig = px.bar(
        pedestrian_types.sort_values("사고건수", ascending=True),
        x="사고건수",
        y="보행자 사고 하위 유형",
        orientation="h",
        color="사고건수",
        color_continuous_scale=["#F7D58B", ORANGE, RED],
        text="사고건수",
        hover_data=["사망자수", "중상자수", "부상자수"],
        labels={"사고건수": "사고건수", "보행자 사고 하위 유형": "사고 상황"},
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_chart(fig, 360), use_container_width=True)

    st.markdown("#### ② 횡단 중 사고의 월별 추이")
    fig = px.line(
        pedestrian_crossing_month,
        x="발생월",
        y="사고건수",
        markers=True,
        text="사고건수",
        hover_data=["사망자수", "중상자수", "경상자수", "부상신고자수"],
        labels={"발생월": "월", "사고건수": "횡단 중 사고건수"},
    )
    fig.update_traces(line=dict(color=RED, width=4), marker=dict(size=9), textposition="top center")
    fig.update_xaxes(dtick=1)
    st.plotly_chart(style_chart(fig, 390), use_container_width=True)

    st.markdown("#### ③ 횡단 중 사고: 사고건수와 사망·중상 현황")
    scatter = px.scatter(
        pedestrian_crossing_month,
        x="사고건수",
        y="사망자수",
        size="중상자수",
        color="발생월",
        text="발생월",
        hover_data=["중상자수", "경상자수", "부상신고자수"],
        labels={"사고건수": "사고건수", "사망자수": "사망자수", "발생월": "월", "중상자수": "중상자수"},
        size_max=30,
    )
    scatter.update_traces(textposition="top center", marker=dict(opacity=0.8))
    st.plotly_chart(style_chart(scatter, 390), use_container_width=True)

    st.markdown(
        f"""
        <div class="insight">
        <b>보행자 사고 분석 해석</b><br>
        • 확인된 4개 하위 유형 중 <b>횡단 중</b> 사고가 {number(13777)}건으로 가장 많았습니다.<br>
        • 횡단 중 사고는 <b>{int(peak_crossing_month['발생월'])}월</b>에 {number(peak_crossing_month['사고건수'])}건으로 가장 많았습니다.<br>
        • 따라서 횡단보도 주변 시야 확보, 보행 신호 준수, 차량의 정지선 준수와 감속을 중심으로 안전 대책을 검토할 필요가 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# 9. 메뉴 4: 어린이보호구역 분석
# -----------------------------------------------------------------------------
elif menu == "🏫 어린이보호구역 분석":
    st.header("🏫 어린이보호구역 어린이 교통사고")
    st.write("12세 이하 어린이의 어린이보호구역 사고 통계를 연도별로 비교합니다.")

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("5년 누적 사고", number(school_total_accidents))
    s2.metric("5년 누적 사망", number(school_total_deaths))
    s3.metric("5년 누적 부상", number(school_total_injuries))
    s4.metric("2025년 사고 증감", f"+{school_yoy_change:.1f}%", "2024년 대비")

    st.markdown("#### ① 연도별 사고건수")
    fig = px.line(
        school_zone,
        x="발생년",
        y="사고건수",
        markers=True,
        text="사고건수",
        labels={"발생년": "연도", "사고건수": "사고건수"},
    )
    fig.update_traces(line=dict(color=BLUE, width=4), marker=dict(size=10), textposition="top center")
    fig.update_xaxes(dtick=1)
    st.plotly_chart(style_chart(fig, 390), use_container_width=True)

    st.markdown("#### ② 연도별 부상자 구성")
    injury_long = school_zone.melt(
        id_vars=["발생년"],
        value_vars=["중상자수", "경상자수", "부상신고자수"],
        var_name="부상 정도",
        value_name="인원수",
    )
    fig = px.bar(
        injury_long,
        x="발생년",
        y="인원수",
        color="부상 정도",
        barmode="stack",
        color_discrete_map={"중상자수": RED, "경상자수": BLUE, "부상신고자수": SKY},
        labels={"발생년": "연도", "인원수": "부상자수", "부상 정도": "부상 정도"},
    )
    fig.update_xaxes(dtick=1)
    st.plotly_chart(style_chart(fig, 390), use_container_width=True)

    st.markdown("#### ③ 사고건수와 중상자수의 관계: 산점도")
    scatter = px.scatter(
        school_zone,
        x="사고건수",
        y="중상자수",
        size="부상자수",
        color="발생년",
        text="발생년",
        hover_data=["사망자수", "경상자수", "부상신고자수"],
        labels={"사고건수": "사고건수", "중상자수": "중상자수", "발생년": "연도"},
        size_max=34,
    )
    scatter.update_traces(textposition="top center", marker=dict(opacity=0.8))
    st.plotly_chart(style_chart(scatter, 390), use_container_width=True)

    st.dataframe(school_zone, use_container_width=True, hide_index=True)
    download_csv(school_zone, "어린이보호구역_어린이교통사고_2021-2025.csv", key="download_school")

    st.warning(
        "이 자료는 어린이보호구역에서 발생한 12세 이하 어린이 사고입니다. "
        "고등학생 사고 통계나 특정 학교 주변의 사고 통계로 바꾸어 해석할 수 없습니다. "
        "2025년 수치가 크게 증가했지만, 이 집계표만으로 증가 원인을 단정할 수는 없습니다."
    )


# -----------------------------------------------------------------------------
# 10. 메뉴 5: 안전 개선 제안
# -----------------------------------------------------------------------------
elif menu == "🧭 안전 개선 제안":
    st.header("🧭 데이터에서 찾은 교통안전 개선 방향")
    st.write("아래 제안은 실제 통계에서 확인된 패턴을 바탕으로 한 정책·교육 아이디어입니다.")

    st.markdown("#### 1. 통학 시간대에는 보행자와 차량 모두 주의")
    st.markdown(
        f"- 전국 시간대별 사고건수는 **{peak_hour_row['시간대']}**에 가장 많았습니다({number(peak_hour_row['사고건수'])}건).\n"
        "- 학교 주변에서는 등교·하교 시간에 차량 감속 안내, 횡단보도 앞 일시정지, 보행자 시야 확보를 강화하는 방안을 검토할 수 있습니다."
    )

    st.markdown("#### 2. 횡단보도 주변 보행자 안전 강화")
    st.markdown(
        f"- 확인한 보행자 하위 유형 4개 중 **횡단 중 사고가 {number(13777)}건**으로 가장 많았습니다.\n"
        "- 횡단보도 조명과 노면 표시 정비, 보행 신호 대기 공간 확보, 우회전 차량의 보행자 확인 교육이 필요합니다."
    )

    st.markdown("#### 3. 어린이보호구역 사고 추이 확인")
    st.markdown(
        f"- 12세 이하 어린이의 어린이보호구역 사고는 2025년 **{number(int(latest_school['사고건수']))}건**으로 전년보다 **{school_yoy_change:.1f}% 증가**했습니다.\n"
        f"- 2025년 중상자는 **{number(int(latest_school['중상자수']))}명**입니다. 보호구역 내 제한속도 준수, 불법 주정차 관리, 횡단보도 주변 시야 확보를 우선 검토할 수 있습니다."
    )

    st.markdown("#### 4. 야간·새벽 시간대의 치명도 고려")
    st.markdown(
        f"- 사고 100건당 사망자수는 **{peak_fatal_rate_row['시간대']}** 구간에서 가장 높았습니다.\n"
        "- 야간 보행 시 밝은 옷이나 반사 소재 사용, 가로등·보행로 조명 점검, 운전자의 전방 주시 교육이 도움이 될 수 있습니다."
    )

    st.markdown("#### 5. 실제 학교 주변 위험 지점을 찾으려면")
    st.info(
        "현재 내장된 통계는 전국 단위의 연도·월·시간·사고유형별 집계 자료입니다. "
        "사고 좌표, 학교 주소, 횡단보도·신호등 좌표, 도로별 차량 통행량은 포함되어 있지 않습니다. "
        "따라서 특정 학교의 위험 구간이나 최적 통학 경로를 계산했다고 볼 수 없습니다. "
        "학교 주변 지도 분석을 하려면 위치 좌표가 포함된 사고 원자료와 안전시설 위치 자료가 추가로 필요합니다."
    )


# -----------------------------------------------------------------------------
# 11. 메뉴 6: 데이터 출처·원본 확인
# -----------------------------------------------------------------------------
elif menu == "📚 데이터 출처·원본 확인":
    st.header("📚 사용한 공공데이터와 분석 기준")
    st.write("아래 수치는 앱 코드 안에 내장되어 있습니다. 앱 실행 중 공공데이터포털에 접속하지 않습니다.")

    sources = pd.DataFrame(
        [
            ["15118850", "최근 5년 어린이보호구역 내 12세 이하 어린이 교통사고 통계", "2021~2025", "공개 미리보기 5행 전체", "연도별 스쿨존 어린이 사고"],
            ["15087037", "시간대별 교통사고 통계", "2025", "공개 미리보기 12행 전체", "2시간 단위 사고·피해 현황"],
            ["15070318", "월별 주야별 교통사고 통계", "2025", "공개 미리보기 24행 전체", "월별 주간·야간 사고 비교"],
            ["15070282", "사고유형별 교통사고 통계", "2025", "전체 18행 중 미리보기 4행", "보행자 사고 하위 유형 비교"],
            ["15070290", "사고유형별 월별 교통사고 통계", "2025", "전체 200행 중 미리보기 12행", "횡단 중 사고의 월별 추이"],
            ["15045638", "한국도로공사 고속도로 교통사고통계", "2000~2024", "포털 전체 26행 / 값 미리보기 미확인", "장기 추세 후보·원본 링크 제공"],
            ["15070271", "도로종류별 월별 교통사고 통계", "2025", "전체 84행 / 값 미리보기 미확인", "도로종류별 차이 분석 후보"],
            ["15070339", "최근 5년 전국 교통사고 통계", "최근 5년", "CSV 스키마 확인 / 값 미리보기 미확인", "전국 연도별 사고·사망·부상 추이 후보"],
        ],
        columns=["데이터셋 ID", "데이터 이름", "기준 시점", "확인 범위", "앱에서 활용한 내용"],
    )
    st.dataframe(sources, use_container_width=True, hide_index=True)

    st.markdown("#### 원본 데이터포털 페이지")
    st.markdown("- [어린이보호구역 어린이 교통사고 통계 (15118850)](https://www.data.go.kr/data/15118850/fileData.do)")
    st.markdown("- [시간대별 교통사고 통계 (15087037)](https://www.data.go.kr/data/15087037/fileData.do)")
    st.markdown("- [월별 주야별 교통사고 통계 (15070318)](https://www.data.go.kr/data/15070318/fileData.do)")
    st.markdown("- [사고유형별 교통사고 통계 (15070282)](https://www.data.go.kr/data/15070282/fileData.do)")
    st.markdown("- [사고유형별 월별 교통사고 통계 (15070290)](https://www.data.go.kr/data/15070290/fileData.do)")
    st.markdown("- [고속도로 교통사고통계 2000~2024 (15045638)](https://www.data.go.kr/data/15045638/fileData.do)")
    st.markdown("- [도로종류별 월별 교통사고 통계 (15070271)](https://www.data.go.kr/data/15070271/fileData.do)")
    st.markdown("- [최근 5년 전국 교통사고 통계 (15070339)](https://www.data.go.kr/data/15070339/fileData.do)")

    st.markdown("### 🕰️ 2020년 이전 데이터: 장기 추세 데이터 발견")
    st.markdown(
        "**한국도로공사_교통사고통계 (데이터셋 ID: 15045638)**는 2000년부터 2024년까지 "
        "고속도로의 연도별 사고건수·사망자수·부상자수를 제공하는 CSV 파일입니다. "
        "포털 상세 페이지에는 전체 26행, 컬럼은 `연도`, `사고`, `사망`, `부상`으로 안내되어 있습니다."
    )
    st.markdown(
        "[공공데이터포털에서 2000~2024년 고속도로 사고 원본 CSV 확인·다운로드](https://www.data.go.kr/data/15045638/fileData.do)"
    )
    st.warning(
        "이 데이터는 2000~2024년이라는 기간과 컬럼 정의·전체 행 수는 확인했지만, "
        "이 세션에서 포털 미리보기에 실제 26개 수치 행이 표시되지 않았습니다. "
        "따라서 그래프에 임의의 연도별 수치를 만들어 넣지 않았습니다. 원본 CSV 행을 확인할 수 있게 되면 "
        "현재 전국 사고 통계와 별도의 '고속도로 장기 추세' 그래프로 추가하는 것이 정확합니다."
    )

    extra_sources = pd.DataFrame(
        [
            ["15045638", "한국도로공사", "2000~2024", "연도·사고·사망·부상", "고속도로 장기 추세 비교"],
            ["15070271", "한국도로교통공단", "2025", "도로종류·발생월·사고·사망·중상·경상·부상신고", "고속국도/일반국도 등 도로종류별 비교"],
            ["15070339", "한국도로교통공단", "최근 5년", "발생년·사고·사망·중상·경상·부상신고", "전국 연도별 추이 비교"],
        ],
        columns=["데이터셋 ID", "제공기관", "기준 기간", "확인된 주요 컬럼", "추가 분석 아이디어"],
    )
    st.dataframe(extra_sources, use_container_width=True, hide_index=True)

    st.markdown("#### 내장된 데이터 확인 및 CSV 저장")
    with st.expander("어린이보호구역 5개 연도 데이터"):
        st.dataframe(school_zone, use_container_width=True, hide_index=True)
        download_csv(school_zone, "schoolzone_child_2021_2025.csv", key="csv_school_source")
    with st.expander("시간대별 교통사고 데이터 12개 구간"):
        st.dataframe(hourly, use_container_width=True, hide_index=True)
        download_csv(hourly, "traffic_accidents_by_2hour_2025.csv", key="csv_hourly_source")
    with st.expander("월별 주야별 교통사고 데이터 24행"):
        st.dataframe(day_night, use_container_width=True, hide_index=True)
        download_csv(day_night, "traffic_accidents_day_night_by_month_2025.csv", key="csv_daynight_source")
    with st.expander("보행자 사고 하위 유형 4개: 공개 미리보기"):
        st.dataframe(pedestrian_types, use_container_width=True, hide_index=True)
        download_csv(pedestrian_types, "pedestrian_accident_types_preview_2025.csv", key="csv_pedtype_source")
    with st.expander("횡단 중 사고 월별 데이터 12행: 공개 미리보기"):
        st.dataframe(pedestrian_crossing_month, use_container_width=True, hide_index=True)
        download_csv(pedestrian_crossing_month, "pedestrian_crossing_by_month_2025.csv", key="csv_crossing_source")

    if time_total_matches and crossing_total_matches:
        st.success(
            "교차 검증 결과: 시간대별 통계 193,889건 = 월별 주·야간 통계 193,889건, "
            "횡단 중 월별 합계 13,777건 = 사고유형별 횡단 중 연간 값 13,777건입니다."
        )

    st.markdown("#### 데이터 해석 시 주의할 점")
    st.markdown(
        """
        1. 한국도로교통공단의 해당 통계는 경찰에서 조사·처리한 사고 중 인적 피해가 있는 사고를 집계한 자료입니다.
        2. 시간대별·월별 통계는 2025년 전국 집계이며, 특정 학교나 특정 동네의 통계가 아닙니다.
        3. 어린이보호구역 자료의 대상은 12세 이하 어린이입니다. 고등학생 교통사고 통계와 동일하지 않습니다.
        4. 사고유형별 통계와 사고유형별 월별 통계는 데이터포털 미리보기에서 확인 가능한 일부 행만 앱에 내장했습니다.
        5. 제공된 통계에는 사고 위치 좌표, 교통안전시설 위치, 차량 통행량이 없으므로 지도 기반 위험지역 분석이나 인과관계 분석은 할 수 없습니다.
        6. 사망자 100건당 비율은 사고건수 대비 단순 비율이며, 교통량·보행량을 보정한 개인별 사고 위험률이 아닙니다.
        7. 고속도로 2000~2024 데이터(15045638)는 포털에서 기간·컬럼·전체 행 수를 확인했지만, 실제 수치 행을 미리보기에서 읽을 수 없어 현재 그래프에는 포함하지 않았습니다.
        8. 도로종류별 월별 데이터(15070271), 최근 5년 전국 통계(15070339)는 분석 가치가 높아 원본 링크와 메타데이터를 추가했으며, 공개 페이지에서 숫자 행을 확인하지 못한 지표는 차트에 임의로 넣지 않았습니다.
        """
    )


# -----------------------------------------------------------------------------
# 12. 모든 화면 하단의 공통 안내
# -----------------------------------------------------------------------------
st.divider()
st.caption(
    "자료 제공: 한국도로교통공단·한국도로공사 · 공공데이터포털 | "
    "그래프: Plotly | 데이터 처리: pandas | "
    "본 앱은 공개 통계의 교육·탐구 목적 시각화이며, 특정 도로의 실시간 위험도나 최적 통학 경로를 보증하지 않습니다."
)
