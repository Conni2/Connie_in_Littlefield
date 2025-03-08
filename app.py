import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 대시보드 제목 설정
st.title("Littlefield Simulation Dashboard")

# 엑셀 파일 업로드
uploaded_file = st.file_uploader("Upload the 🏭Littlefield Template", type=["xlsx"])

# 파일이 업로드 되었는지 확인
if uploaded_file is not None:
    # 데이터 로드
    df = pd.read_excel(uploaded_file, sheet_name="Sheet JS")
    
    # 컬럼 이름 변경 (짧고 직관적인 이름으로)
    df.rename(columns={
        "day": "day",
        "number of jobs accepted each day (order by day)": "daily_demand",
        "daily average number of jobs waiting for kits (day/kits)": "jobs_waiting_kits",
        "utilization of station 1, averaged over each day": "utilization_station_1",
        "daily average number of kits queued for station 1": "queue_station_1",
        "utilization of station 2, averaged over each day": "utilization_station_2",
        "daily average number of kits queued for station 2": "queue_station_2",
        "utilization of station 3, averaged over each day": "utilization_station_3",
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
    
    # 수요와 완료된 작업을 위한 단위 변환
    cols_to_convert = [
        "daily_demand",
        "completed_jobs_contract_1",
        "completed_jobs_contract_2",
        "completed_jobs_contract_3"
    ]
    for col in cols_to_convert:
        df[col] = df[col] * 60
    
    # -------------------------------
    # Business Overview 페이지 (그래프들)
    # -------------------------------
    
    st.header("Business Overview")
    
    # 서브플롯 생성
    fig, ax = plt.subplots(2, 2, figsize=(15, 10))

    # 일별 수요 그래프
    ax[0, 0].plot(df["day"], df["daily_demand"], color='b', label="Daily Demand")
    ax[0, 0].set_title('Daily Demand')
    ax[0, 0].set_xlabel('Day')
    ax[0, 0].set_ylabel('Demand (kits)')
    ax[0, 0].legend()

    # 계약별 수익 그래프
    ax[0, 1].plot(df["day"], df["revenue_contract_1"], label="Contract 1", color='purple')
    ax[0, 1].plot(df["day"], df["revenue_contract_2"], label="Contract 2", color='orange')
    ax[0, 1].plot(df["day"], df["revenue_contract_3"], label="Contract 3", color='green')
    ax[0, 1].set_title('Daily Revenue per Contract')
    ax[0, 1].set_xlabel('Day')
    ax[0, 1].set_ylabel('Revenue ($)')
    ax[0, 1].legend()

    # 계약별 리드 타임 그래프
    ax[1, 0].plot(df["day"], df["lead_time_contract_1"], label="Contract 1", color='g')
    ax[1, 0].plot(df["day"], df["lead_time_contract_2"], label="Contract 2", color='b')
    ax[1, 0].plot(df["day"], df["lead_time_contract_3"], label="Contract 3", color='r')
    ax[1, 0].set_title('Job Lead Time per Contract')
    ax[1, 0].set_xlabel('Day')
    ax[1, 0].set_ylabel('Lead Time (days)')
    ax[1, 0].legend()

    # 계약별 완료된 작업 그래프
    ax[1, 1].plot(df["day"], df["completed_jobs_contract_1"], label="Contract 1", color='orange')
    ax[1, 1].plot(df["day"], df["completed_jobs_contract_2"], label="Contract 2", color='purple')
    ax[1, 1].plot(df["day"], df["completed_jobs_contract_3"], label="Contract 3", color='brown')
    ax[1, 1].set_title('Completed Jobs per Contract')
    ax[1, 1].set_xlabel('Day')
    ax[1, 1].set_ylabel('Completed Jobs')
    ax[1, 1].legend()

    # 그래프 표시
    st.pyplot(fig)
    
    # -------------------------------
    # Process Overview 페이지 (그래프들)
    # -------------------------------
    
    st.header("Process Overview")
    
    # 스테이션 필터링을 위한 버튼 추가
    selected_station = st.radio("Select Station", ["All", "Station 1", "Station 2", "Station 3"])

    # Utilization 및 Queue Length 그래프
    fig, ax = plt.subplots(2, 1, figsize=(15, 10))

    # 선택된 스테이션에 따라 Utilization 그래프 표시
    if selected_station == "All":
        ax[0].plot(df["day"], df["utilization_station_1"], label="Station 1", color='g')
        ax[0].plot(df["day"], df["utilization_station_2"], label="Station 2", color='r')
        ax[0].plot(df["day"], df["utilization_station_3"], label="Station 3", color='orange')
    elif selected_station == "Station 1":
        ax[0].plot(df["day"], df["utilization_station_1"], label="Station 1", color='g')
    elif selected_station == "Station 2":
        ax[0].plot(df["day"], df["utilization_station_2"], label="Station 2", color='r')
    elif selected_station == "Station 3":
        ax[0].plot(df["day"], df["utilization_station_3"], label="Station 3", color='orange')
    
    ax[0].set_title('Utilization of Stations')
    ax[0].set_xlabel('Day')
    ax[0].set_ylabel('Utilization')
    ax[0].legend()

    # 선택된 스테이션에 따라 Queue Length 그래프 표시
    if selected_station == "All":
        ax[1].plot(df["day"], df["queue_station_1"], label="Station 1", color='b')
        ax[1].plot(df["day"], df["queue_station_2"], label="Station 2", color='r')
        ax[1].plot(df["day"], df["queue_station_3"], label="Station 3", color='g')
    elif selected_station == "Station 1":
        ax[1].plot(df["day"], df["queue_station_1"], label="Station 1", color='b')
    elif selected_station == "Station 2":
        ax[1].plot(df["day"], df["queue_station_2"], label="Station 2", color='r')
    elif selected_station == "Station 3":
        ax[1].plot(df["day"], df["queue_station_3"], label="Station 3", color='g')

    ax[1].set_title('Queue Length per Station')
    ax[1].set_xlabel('Day')
    ax[1].set_ylabel('Queue Length (kits)')
    ax[1].legend()

    # 그래프 표시
    st.pyplot(fig)

# RP와 EOQ 결과 페이지
st.header("RP and EOQ Results")

# EOQ와 ROP 값 계산 예시 (원래 코드에서 계산한 값 사용)
EOQ = 12345.67  # 예시 값, 실제로는 계산 결과에 맞춰서 사용
ROP_0 = 1000.25  # 예시 값
ROP_conservative = 1200.45  # 예시 값
ROP_99 = 1500.85  # 예시 값

# EOQ와 ROP 값을 소수점 두 자리로 표시
st.subheader("EOQ and ROP Values")
st.write(f"🚚 **EOQ**: {EOQ:.2f} kits")
st.write(f"🔴 **ROP (SS = 0)**: {ROP_0:.2f} kits")
st.write(f"🟡 **ROP (SS = Max Daily Demand - Avg Daily Demand * L)**: {ROP_conservative:.2f} kits")
st.write(f"🟢 **ROP (SS = 99% Service Level)**: {ROP_99:.2f} kits")

# EOQ와 ROP 원값 계산 후, 60으로 나누고 소수 첫째 자리로 반올림하여 자연수로 표시
order_rounded = np.ceil(EOQ / 60)  # 주문을 60으로 나누고 올림하여 자연수로 만들기
ROP_0_rounded = np.ceil(ROP_0 / 60)
ROP_conservative_rounded = np.ceil(ROP_conservative / 60)
ROP_99_rounded = np.ceil(ROP_99 / 60)

st.subheader("Rounded Values")
st.write(f"🚚 **EOQ (rounded)**: {order_rounded} orders")
st.write(f"🔴 **ROP (SS = 0, rounded)**: {ROP_0_rounded} orders")
st.write(f"🟡 **ROP (SS = Max Daily Demand - Avg Daily Demand * L, rounded)**: {ROP_conservative_rounded} orders")
st.write(f"🟢 **ROP (SS = 99% Service Level, rounded)**: {ROP_99_rounded} orders")


# 인터벌 분석 페이지
st.header("Interval Analysis")

# 새 엑셀 파일 업로드
uploaded_interval_file = st.file_uploader("Upload your inventory interval file", type=["xlsx"])

if uploaded_interval_file is not None:
    # 새 파일을 읽어들임
    inventory_df = pd.read_excel(uploaded_interval_file, sheet_name="Sheet JS")
    
    # 파일 데이터 확인
    st.write("Data preview:", inventory_df.head())
    
    # ROP 및 Order Quantity 값 설정 (예시값)
    ROP_initial = 1440  # 초기 설정된 ROP
    OQ_initial = 7200  # 초기 Order Quantity
    lead_time = 4  # 리드타임 (고정값)

    # ROP 이하로 최초로 떨어진 날 찾기
    rop_breach_days = inventory_df[inventory_df["inventory_level"] <= ROP_initial]["day"].tolist()
    st.write(f"Days when ROP was breached: {rop_breach_days}")
    
    # Shortage 발생 구간 찾기
    inventory_df["shortage_flag"] = inventory_df["inventory_level"] == 0
    shortage_periods = []
    shortage_durations = []
    
    in_shortage = False
    shortage_start = None
    for index, row in inventory_df.iterrows():
        if row["shortage_flag"]:
            if not in_shortage:
                shortage_start = row["day"]
                in_shortage = True
        else:
            if in_shortage:
                shortage_end = inventory_df.loc[index - 1, "day"]
                shortage_periods.append((shortage_start, shortage_end))
                shortage_durations.append(shortage_end - shortage_start + 1)
                in_shortage = False
    
    # 결과 출력
    st.write(f"Shortage periods (Start Day - End Day): {shortage_periods}")
    st.write(f"Shortage durations (Number of days in shortage): {shortage_durations}")
    
    # 주문 간격(Order Interval) 계산
    order_intervals = [rop_breach_days[i] - rop_breach_days[i - 1] for i in range(1, len(rop_breach_days))]
    average_order_interval = sum(order_intervals) / len(order_intervals) if order_intervals else None
    st.write(f"Average order interval: {average_order_interval:.2f} days" if average_order_interval else "Not enough data for average order interval")

    # Shortage-Free 기간 (Shortage 종료일부터 다음 Shortage 시작일까지의 평균 간격)
    shortage_intervals = [shortage_periods[i][0] - shortage_periods[i - 1][1] for i in range(1, len(shortage_periods))]
    average_shortage_free_period = sum(shortage_intervals) / len(shortage_intervals) if shortage_intervals else None
    st.write(f"Average shortage-free period: {average_shortage_free_period:.2f} days" if average_shortage_free_period else "Not enough data for shortage-free period")
    
    # k 값 계산
    k = (average_shortage_free_period / average_order_interval) if (average_shortage_free_period and average_order_interval) else 1
    st.write(f"k value: {k:.2f}")
    
    # 최적 Order Quantity (OQ) 계산
    OQ_optimized = max(EOQ, OQ_initial) * k
    st.write(f"Optimized Order Quantity: {OQ_optimized:.2f}")
    
    # 인터벌 시각화 (예시로 Shortage 기간 시각화)
    plt.figure(figsize=(10, 6))
    plt.plot(inventory_df["day"], inventory_df["inventory_level"], label="Inventory Level", color='b')
    plt.axhline(y=ROP_initial, color='r', linestyle='--', label="ROP Threshold")
    plt.title("Inventory Level with ROP Threshold")
    plt.xlabel("Day")
    plt.ylabel("Inventory Level (kits)")
    plt.legend()
    st.pyplot(plt)



# 병목 분석 및 시뮬레이션 페이지
st.header("Bottleneck Analysis and Simulation")

# 메인 대시보드에서 업로드된 파일을 st.session_state로 저장했는지 확인
if 'df' not in st.session_state:
    st.warning("Please upload the main data file on the main dashboard page first.")
else:
    # 기존 메인 대시보드에서 업로드된 데이터 사용
    df = st.session_state.df

    # 기본적으로 병목을 찾아서 시뮬레이션을 위한 설정
    st.subheader("Machine Allocation and Bottleneck Detection")
    
    # 기본 데이터 확인
    st.write("Data preview:", df.head())

    # 각 스테이션에 대한 처리 시간 (예시 값, 원본 데이터에 맞게 수정)
    PT1 = 4.4  # Station 1 처리 시간 (시간/작업)
    PT2 = 3.2  # Station 2 처리 시간 (시간/작업)
    PT3 = 1.6  # Station 3 처리 시간 (시간/작업)

    # 기본 기계 개수 입력
    s1 = st.number_input("Enter the number of machines for Station 1", min_value=1, value=1)
    s2 = st.number_input("Enter the number of machines for Station 2", min_value=1, value=1)
    s3 = st.number_input("Enter the number of machines for Station 3", min_value=1, value=1)

    # 각 스테이션의 처리 능력 계산 (Capacity = 기계 수 / 처리 시간)
    C1 = s1 / PT1  # Station 1의 처리 능력
    C2 = s2 / PT2  # Station 2의 처리 능력
    C3 = s3 / PT3  # Station 3의 처리 능력

    # 병목 찾기 (가장 낮은 처리 능력)
    min_capacity = min(C1, C2, C3)

    # 병목이 발생하는 스테이션 찾기
    bottleneck_stations = []
    if min_capacity == C1:
        bottleneck_stations.append("Station 1")
    if min_capacity == C2:
        bottleneck_stations.append("Station 2")
    if min_capacity == C3:
        bottleneck_stations.append("Station 3")

    # 시뮬레이션: Cycle Time 계산 (Cycle Time = 1 / 처리 능력)
    CT = 1 / min_capacity * 24  # Cycle Time (시간/작업)

    st.write(f"Capacity of Station 1: {C1:.2f} jobs/day")
    st.write(f"Capacity of Station 2: {C2:.2f} jobs/day")
    st.write(f"Capacity of Station 3: {C3:.2f} jobs/day")
    st.write(f"Minimum Capacity (Bottleneck): {min_capacity:.2f} jobs/day")
    st.write(f"Cycle Time (CT): {CT:.2f} hours/job")
    st.write(f"🌟 Bottleneck Station(s): {', '.join(bottleneck_stations)}")

    # 병목 해결을 위한 기계 추가 버튼
    st.subheader("Machine Addition Recommendation")

    if len(bottleneck_stations) > 1:
        st.write("Multiple bottlenecks detected. Consider adding machines to the stations with high utilization and queue length.")
        
        # 병목이 여러 개인 경우, 대기열 길이와 사용률을 기준으로 개선해야 할 스테이션을 결정
        queue_lengths = {
            "Station 1": df["queue_station_1"].mean(),
            "Station 2": df["queue_station_2"].mean(),
            "Station 3": df["queue_station_3"].mean()
        }

        utilization = {
            "Station 1": df["utilization_station_1"].mean(),
            "Station 2": df["utilization_station_2"].mean(),
            "Station 3": df["utilization_station_3"].mean()
        }

        # 병목이 발생한 스테이션에 대해 대기열 길이와 사용률 출력
        st.write("Queue Length and Utilization for Bottleneck Stations:")
        for station in bottleneck_stations:
            st.write(f"{station} - Queue Length: {queue_lengths[station]:.2f} kits")
            st.write(f"{station} - Utilization: {utilization[station]:.2f}")
        
        # 대기열 길이가 긴 스테이션 우선
        bottleneck_by_queue = max(queue_lengths, key=queue_lengths.get)
        st.write(f"Priority based on Queue Length: {bottleneck_by_queue}")

        # Utilization 우선 (대기열 길이가 같다면)
        if all(queue_lengths[station] == queue_lengths[bottleneck_by_queue] for station in bottleneck_stations):
            bottleneck_by_utilization = min(utilization, key=utilization.get)
            st.write(f"Priority based on Utilization: {bottleneck_by_utilization}")
        else:
            bottleneck_by_utilization = bottleneck_by_queue  # 대기열 기준 우선
            st.write(f"Priority based on Queue Length: {bottleneck_by_utilization}")

    else:
        st.write(f"Single bottleneck detected: {', '.join(bottleneck_stations)} 🛠️")

    # 병목 해소를 위한 추가 기계 선택 (입력 받기)
    add_machine = st.radio("Which station would you like to add a machine to?", ["None", "Station 1", "Station 2", "Station 3"])
    
    if add_machine == "Station 1":
        s1 += 1
    elif add_machine == "Station 2":
        s2 += 1
    elif add_machine == "Station 3":
        s3 += 1
    elif add_machine == "None":
        st.write("No machines added.")

    # 각 스테이션의 새로운 처리 능력 계산
    C1 = s1 / PT1
    C2 = s2 / PT2
    C3 = s3 / PT3

    # 새로운 병목 계산
    min_capacity = min(C1, C2, C3)
    bottleneck_stations = []
    if min_capacity == C1:
        bottleneck_stations.append("Station 1")
    if min_capacity == C2:
        bottleneck_stations.append("Station 2")
    if min_capacity == C3:
        bottleneck_stations.append("Station 3")

    # 새로운 Cycle Time 계산
    CT = 1 / min_capacity * 24  # Cycle Time (시간/작업)

    st.write(f"Capacity of Station 1 after addition: {C1:.2f} jobs/day")
    st.write(f"Capacity of Station 2 after addition: {C2:.2f} jobs/day")
    st.write(f"Capacity of Station 3 after addition: {C3:.2f} jobs/day")
    st.write(f"Minimum Capacity (Bottleneck after addition): {min_capacity:.2f} jobs/day")
    st.write(f"Cycle Time (CT) after addition: {CT:.2f} hours/job")
    st.write(f"🌟 Bottleneck Station(s) after machine addition: {', '.join(bottleneck_stations)}")
