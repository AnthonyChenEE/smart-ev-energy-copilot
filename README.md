# ⚡ Xiaomi EV Energy Copilot — Drive the Future of Intelligent Energy

**Smart Energy Optimization for Home × EV × Grid**  
A lightweight, open-source demo inspired by Xiaomi Auto’s vision of “Human × Car × Home × AI”.  
This project demonstrates how to **optimize EV charging schedules** using linear programming, balancing **home load**, **solar PV**, and **electricity tariffs** to minimize energy costs.

> 🚗 Built with Python · Powered by Optimization · Designed for Education and Innovation

---

## 🧠 项目简介（中文说明）

**Xiaomi EV Energy Copilot（小米智能能源副驾）**  
是一个面向智能电动车与家庭能源系统的**能量优化算法演示项目**。  
项目以“小米汽车人车家全生态”为灵感，利用线性规划算法，在**家庭负荷、光伏发电与分时电价**之间实现最优能量分配，  
以达到“更低成本、更高效率、更智能”的充电策略。

- 📘 **算法核心**：基于 PuLP 的线性规划模型  
- ⚙️ **主要约束**：功率上限、SOC 动态、能量平衡、末端SOC目标  
- 💡 **输出结果**：最优充电计划、成本分析、功率与SOC曲线  
- 🧩 **可扩展性**：支持多车协同调度、时变电价、光伏预测等扩展  

> 🧠 让算法更懂能源，让能源更懂你。
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/0c639927-1ac2-42a4-a98a-62662c56c027" />

---

### 🔗 Quickstart

```bash
pip install -r requirements.txt
python src/energycopilot/simulate.py
