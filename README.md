# ⚡ Smart EV Energy Copilot — Drive the Future of Intelligent Energy  

**Smart Energy Optimization for Home × EV × Grid**  
A lightweight, open-source demo **inspired by Xiaomi Auto’s “Human × Car × Home × AI” ecosystem vision**.  
This project demonstrates how to **optimize EV charging schedules** using linear programming, balancing **home load**, **solar PV**, and **electricity tariffs** to minimize energy costs.

> 🚗 Built with Python · Powered by Optimization · Designed for Education and Innovation  
> *(Independent open-source project — inspired by Xiaomi Auto’s ecosystem vision, not affiliated with the company.)*

---

## 🧠 项目简介（中文说明）

**Smart EV Energy Copilot（智能电动车能源副驾）**  
是一个面向智能电动车与家庭能源系统的**能量优化算法演示项目**。  
项目以“小米汽车人车家全生态”理念为灵感，利用线性规划算法，在**家庭负荷、光伏发电与分时电价**之间实现最优能量分配，  
以达到“更低成本、更高效率、更智能”的充电策略。

- 📘 **算法核心**：基于 PuLP 的线性规划模型  
- ⚙️ **主要约束**：功率上限、SOC 动态、能量平衡、末端 SOC 目标  
- 💡 **输出结果**：最优充电计划、成本分析、功率与 SOC 曲线  
- 🧩 **可扩展性**：支持多车协同调度、时变电价、光伏预测等扩展  

> 🧠 让算法更懂能源，让能源更懂你。

<img width="1024" height="1024" alt="ChatGPT Image Oct 30, 2025, 12_03_04 AM" src="https://github.com/user-attachments/assets/e7d166c8-f656-4d48-8bd0-f68197dc1169" />


---

### 🔗 Quickstart

```bash
pip install -r requirements.txt
python src/energycopilot/simulate.py
