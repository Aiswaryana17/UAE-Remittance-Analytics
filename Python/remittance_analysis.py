import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ═══════════════════════════════════════════════
# UAE REMITTANCE ANALYTICS — PYTHON ANALYSIS
# Exchange House Business Intelligence
# Analyst: Aiswarya NA | 2024
# ═══════════════════════════════════════════════

os.makedirs("charts", exist_ok=True)

# ── Load Data ──────────────────────────────────
df = pd.read_csv("data/transactions.csv")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M')
success = df[df['status'] == 'SUCCESS']

print(f"Total Transactions : {len(df):,}")
print(f"Successful         : {len(success):,}")
print(f"Failed             : {len(df) - len(success):,}")
print(f"Total Volume       : AED {success['amount_aed'].sum():,.0f}")
print(f"Total Revenue      : AED {success['fee_aed'].sum():,.0f}")

# ── Chart 1 — Volume by Corridor ───────────────
corridor = success.groupby('corridor')['amount_aed'].sum().sort_values()
plt.figure(figsize=(10, 5))
colors = ['#1D9E75' if v == corridor.max() else '#A8D9C8' for v in corridor.values]
bars = plt.barh(corridor.index, corridor.values, color=colors)
plt.title('Total Remittance Volume by Corridor (AED)',
          fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Total Volume (AED)', fontsize=11)
for bar, val in zip(bars, corridor.values):
    plt.text(val + 5000, bar.get_y() + bar.get_height()/2,
             f'AED {val:,.0f}', va='center', fontsize=9)
plt.gca().spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('charts/01_volume_by_corridor.png', dpi=150)
plt.close()
print("\n✅ Chart 1 saved — Volume by Corridor")

# ── Chart 2 — Monthly Volume Trend ─────────────
monthly = success.groupby('month')['amount_aed'].sum()
months_str = [str(m) for m in monthly.index]
plt.figure(figsize=(12, 5))
plt.plot(months_str, monthly.values,
         marker='o', color='#185FA5', linewidth=2.5, markersize=6)
plt.fill_between(range(len(monthly)), monthly.values,
                 alpha=0.1, color='#185FA5')
for i, val in enumerate(monthly.values):
    plt.text(i, val + 3000, f'AED {val/1000:.0f}K',
             ha='center', fontsize=8, color='#185FA5')
plt.title('Monthly Remittance Volume Trend — 2024',
          fontsize=13, fontweight='bold', pad=15)
plt.ylabel('Volume (AED)', fontsize=11)
plt.xticks(range(len(months_str)), months_str, rotation=45, fontsize=9)
plt.gca().spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('charts/02_monthly_trend.png', dpi=150)
plt.close()
print("✅ Chart 2 saved — Monthly Trend")

# ── Chart 3 — Agent Failure Rate ───────────────
agent = df.groupby('agent_name').apply(
    lambda x: round((x['status'] == 'FAILED').sum() / len(x) * 100, 2)
).sort_values(ascending=False).reset_index()
agent.columns = ['agent_name', 'failure_rate']
bar_colors = ['#E05C5C' if v > 10 else '#4CAF82' for v in agent['failure_rate']]
plt.figure(figsize=(10, 5))
bars = plt.bar(agent['agent_name'], agent['failure_rate'],
               color=bar_colors, width=0.5)
plt.axhline(10, color='gray', linestyle='--',
            linewidth=1, label='10% Risk Threshold')
for bar, val in zip(bars, agent['failure_rate']):
    plt.text(bar.get_x() + bar.get_width()/2, val + 0.2,
             f'{val}%', ha='center', fontsize=9)
plt.title('Agent Transaction Failure Rate (%)',
          fontsize=13, fontweight='bold', pad=15)
plt.ylabel('Failure Rate (%)', fontsize=11)
plt.xticks(rotation=30, ha='right', fontsize=9)
over = mpatches.Patch(color='#E05C5C', label='Above 10% — High Risk')
under = mpatches.Patch(color='#4CAF82', label='Below 10% — Acceptable')
plt.legend(handles=[over, under], fontsize=9)
plt.gca().spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('charts/03_agent_failure_rate.png', dpi=150)
plt.close()
print("✅ Chart 3 saved — Agent Failure Rate")

# ── Chart 4 — Revenue by Corridor ──────────────
revenue = success.groupby('corridor')['fee_aed'].sum().sort_values(ascending=False)
plt.figure(figsize=(8, 8))
wedge_colors = ['#1D9E75','#185FA5','#E05C5C','#F5A623',
                '#9B59B6','#1ABC9C','#E67E22','#2ECC71']
wedges, texts, autotexts = plt.pie(
    revenue.values,
    labels=revenue.index,
    autopct='%1.1f%%',
    colors=wedge_colors,
    startangle=140,
    pctdistance=0.75
)
for text in autotexts:
    text.set_fontsize(9)
plt.title('Revenue Share by Corridor (AED)',
          fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('charts/04_revenue_by_corridor.png', dpi=150)
plt.close()
print("✅ Chart 4 saved — Revenue by Corridor")

# ── Chart 5 — Payment Method ───────────────────
payment = success.groupby('payment_method')['amount_aed'].sum().sort_values(ascending=False)
plt.figure(figsize=(7, 4))
plt.bar(payment.index, payment.values,
        color=['#185FA5', '#1D9E75', '#F5A623'], width=0.4)
for i, val in enumerate(payment.values):
    plt.text(i, val + 2000, f'AED {val:,.0f}',
             ha='center', fontsize=9)
plt.title('Volume by Payment Method (AED)',
          fontsize=13, fontweight='bold', pad=15)
plt.ylabel('Total Volume (AED)', fontsize=11)
plt.gca().spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('charts/05_payment_method.png', dpi=150)
plt.close()
print("✅ Chart 5 saved — Payment Method")

print("\n✅ All done! 5 charts saved in charts/ folder")
print("\n── Key Business Insights ──")
print(f"Top corridor by volume : {corridor.idxmax()}")
print(f"Top corridor by revenue: {revenue.idxmax()}")
print(f"Highest risk agent     : {agent.iloc[0]['agent_name']} ({agent.iloc[0]['failure_rate']}% failure rate)")
print(f"Most used payment      : {payment.idxmax()}")