# **Littlefield Simulation Streamlit App**

## **Overview**

This **Streamlit** application allows you to interact with the **Littlefield Simulation** model, providing an easy exploration of **EOQ (Economic Order Quantity)**, **ROP (Reorder Point)**, **machine bottleneck analysis**, and **machine addition simulations**. You can visualize key metrics and make informed decisions based on the simulation's output.

![Littlefield Simulation](https://github.com/Conni2/Connie_in_Littlefield/blob/main/1BD97CE2-65AD-4540-AE1C-0A93435F969D.jpg?raw=true)

## **Features**

### **EOQ and ROP Calculation**:

- **EOQ (Economic Order Quantity)**: Calculates the optimal order quantity that minimizes total ordering and holding costs.
- **ROP (Reorder Point)**: Computes the point at which new orders should be placed to avoid stockouts, considering lead time and daily demand.

### **Bottleneck Analysis**:

- Identifies bottlenecks across the different stations (**Station 1**, **Station 2**, **Station 3**) based on **Capacity**, **Utilization**, and **Queue Length**.
- Recommends the station(s) to prioritize for machine additions.

### **Machine Addition Simulation**:

- Simulates the impact of adding machines to specific stations and analyzes how it affects **Cycle Time**, **Utilization**, and overall system performance.
- Displays updated bottleneck stations and new system throughput after machine additions.

### **Interactive Visualization**:

- Dynamic graphs displaying:
  - **Daily Demand**
  - **Queue Length** for each station
  - **Utilization** for each station
  - **Revenue** per contract
  - **Lead Time** for each contract
  
- Easily track the progress and decision impact on the system.

## **Data**

The app relies on historical simulation data, including:

- **Daily Demand** for each day in the simulation period
- **Queue Length** at each station
- **Utilization** metrics for each station
- **Revenue** and **Lead Time** data for different contracts

You can upload your own data or modify the app to use different datasets.
