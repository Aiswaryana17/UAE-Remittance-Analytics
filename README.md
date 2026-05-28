# UAE Remittance Transaction Analytics 🇦🇪

End-to-end data analytics project simulating a real exchange house
business intelligence use case — built specifically for the UAE financial services market.

## 🏦 Business Problem
An exchange house in Dubai processes 5,000+ remittance transactions monthly
across 8 international corridors. Management needs to understand:
- Which corridors generate the most revenue
- Which agents have unacceptable failure rates
- How transaction volume trends month by month
- How customers prefer to pay

## 🛠 Tools Used
| Tool | Purpose |
|---|---|
| SQL (SQLite) | Data extraction and KPI aggregation |
| Python (Pandas, Matplotlib) | Analysis and chart generation |
| Excel | Pivot dashboard with slicers |
| Power BI | Interactive executive dashboard |

## 📊 Key Business Insights
- **Top corridor:** India — 35% of total volume (AED 4,438,704)
- **Highest risk agent:** Rajesh Kumar — 13.95% failure rate (above 10% threshold)
- **Most used payment:** Cash — 50% of all transactions
- **Total revenue:** AED 94,206 across 4,659 successful transactions

## 📁 Project Structure
```
UAE-Remittance-Analytics/
├── data/               — Raw transaction dataset (5,000 rows)
├── sql/                — 6 SQL queries + result screenshots
├── python/             — Analysis script generating 5 charts
├── charts/             — Output visualisations
└── README.md
```

## 📈 Charts
![Volume by Corridor](charts/01_volume_by_corridor.png)
![Monthly Trend](charts/02_monthly_trend.png)
![Agent Failure Rate](charts/03_agent_failure_rate.png)
![Revenue by Corridor](charts/04_revenue_by_corridor.png)
![Payment Method](charts/05_payment_method.png)

## 💡 Business Recommendations
1. **Focus marketing on India corridor** — highest volume and revenue
2. **Retrain or review Rajesh Kumar** — 13.95% failure rate is a business risk
3. **Incentivise card and bank transfer payments** — reduces cash handling costs
4. **Investigate corridor failure rates** — 3 corridors above 10% threshold

## 🔗 Connect
- LinkedIn: linkedin.com/in/aiswarya-na
- GitHub: github.com/Aiswaryana17
- Email: aiswaryaanilan2001@gmail.com