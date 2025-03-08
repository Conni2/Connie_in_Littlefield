import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 메인 페이지 설정
st.set_page_config(page_title="Littlefield Dashboard 🏭", page_icon="📊", layout="wide")

st.title("Welcome to Littlefield Dashboard 🏭")
st.markdown("""
### 🚀 Quick Access
- [Littlefield Simulation](https://op.responsive.net/lt/najafi1/entry.html)
""")

st.sidebar.title("Navigation 🗺️")
st.sidebar.write("Use the menu to navigate between pages!")

# 사이드바 메뉴 추가
page = st.sidebar.radio("Select a page 📑", [
    "🏢 Business Overview",
    "⚙️ Process Overview",
    "📦 Reorder Point & Order Quantity",
    "🤖 Machine Evaluation"
])

# 파일 업로드
st.header("📂 Upload Littlefield Data")
uploaded_file = st.file_uploader("Upload your Excel file here", type=["xls", "xlsx"])

df = None
if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Sheet JS")
    
    # 컬럼명 변경 (짧고 직관적인 변수명으로 변경)
    df.rename(columns={
        "day": "day",
        "number of jobs accepted each day (order by day)": "daily_demand",
        "daily average number of jobs waiting for kits (day/kits)": "jobs_waiting_kits",
        "utilization of station 1, averaged over each day": "utilization_station_1",
        "daily average number of kits queued for station 1": "queue_station_1",
        "utilization of station 2, averaged over each day": "utilization_station_2",
        "daily average number of kits queued for station 2": "queue_station_2",
        "utilization of station 3, averaged over each day": "utilization_station_3",
        "daily average number of kits queued for station 3": "queue_station_3",
        "daily average revenue per job contract 1": "revenue_contract_1",
        "daily average revenue per job contract 2": "revenue_contract_2",
        "daily average revenue per job contract 3": "revenue_contract_3",
        "daily average job lead time contract 1": "lead_time_contract_1",
        "daily average job lead time contract 2": "lead_time_contract_2",
        "daily average job lead time contract 3": "lead_time_contract_3",
        "number of completed jobs each day contract 1": "completed_jobs_contract_1",
        "number of completed jobs each day contract 2": "completed_jobs_contract_2",
        "number of completed jobs each day contract 3": "completed_jobs_contract_3"
    }, inplace=True)
    
    # order to kit 단위 변경 (일부 컬럼 *60 변환)
    cols_to_convert = [
        "daily_demand", "completed_jobs_contract_1",
        "completed_jobs_contract_2", "completed_jobs_contract_3"
    ]
    for col in cols_to_convert:
        df[col] = df[col] * 60
    
    # 데이터 표시
    st.subheader("📝 Processed Data Preview")
    st.dataframe(df.head())

    # 다운로드 옵션 추가
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Download Processed Data",
        data=csv,
        file_name="processed_littlefield_data.csv",
        mime="text/csv"
    )

# Machine Evaluation Page
if page == "🤖 Machine Evaluation" and df is not None:
    st.header("🤖 Machine Evaluation")
    
    s1 = st.number_input("Enter number of machines for Station 1", min_value=1, value=3, step=1)
    s2 = st.number_input("Enter number of machines for Station 2", min_value=1, value=3, step=1)
    s3 = st.number_input("Enter number of machines for Station 3", min_value=1, value=3, step=1)
    
    PT1, PT2, PT3 = 4.4, 3.2, 1.6
    
    C1, C2, C3 = s1 / PT1, s2 / PT2, s3 / PT3
    min_capacity = min(C1, C2, C3)
    
    bottleneck_stations = []
    if min_capacity == C1:
        bottleneck_stations.append("Station 1 🏭")
    if min_capacity == C2:
        bottleneck_stations.append("Station 2 🏭")
    if min_capacity == C3:
        bottleneck_stations.append("Station 3 🏭")
    
    CT = 1 / min_capacity * 24
    
    st.metric(label="⚙️ Capacity of Station 1", value=f"{C1:.2f} jobs/day")
    st.metric(label="⚙️ Capacity of Station 2", value=f"{C2:.2f} jobs/day")
    st.metric(label="⚙️ Capacity of Station 3", value=f"{C3:.2f} jobs/day")
    st.metric(label="🔴 Minimum Capacity (Bottleneck)", value=f"{min_capacity:.2f} jobs/day")
    st.metric(label="⏳ Cycle Time", value=f"{CT:.2f} hours/job")
    st.metric(label="🌟 Bottleneck Station(s)", value=", ".join(bottleneck_stations))
    
    add_machine = st.selectbox("Which station would you like to add a machine to?", ["Station 1", "Station 2", "Station 3"])
    if st.button("Add Machine 🛠️"):
        if add_machine == "Station 1":
            s1 += 1
        elif add_machine == "Station 2":
            s2 += 1
        elif add_machine == "Station 3":
            s3 += 1
        st.experimental_rerun()
