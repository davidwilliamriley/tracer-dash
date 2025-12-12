import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Sample burndown chart data
# In a real scenario, this would come from your project management system or database

# Define sprint parameters
sprint_start = datetime(2025, 12, 1)
sprint_end = datetime(2025, 12, 15)
total_story_points = 100

# Generate date range for the sprint
date_range = pd.date_range(start=sprint_start, end=sprint_end, freq='D')

# Ideal burndown (linear decrease from total to 0)
ideal_burndown = [total_story_points - (i * total_story_points / (len(date_range) - 1)) 
                  for i in range(len(date_range))]

# Actual burndown (simulated actual progress with some variance)
# This represents the remaining work each day
actual_burndown = [
    100,  # Day 1
    100,  # Day 2 (no progress - weekend)
    95,   # Day 3
    88,   # Day 4
    82,   # Day 5
    75,   # Day 6
    70,   # Day 7
    70,   # Day 8 (no progress - weekend)
    70,   # Day 9 (no progress - weekend)
    62,   # Day 10
    55,   # Day 11
    45,   # Day 12
    35,   # Day 13
    25,   # Day 14
    15,   # Day 15 (projected)
]

# Create DataFrame for easier manipulation
df = pd.DataFrame({
    'Date': date_range,
    'Ideal': ideal_burndown,
    'Actual': actual_burndown
})

# Create the burndown chart
fig = go.Figure()

# Add ideal burndown line
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Ideal'],
    mode='lines',
    name='Ideal Burndown',
    line=dict(color='lightblue', width=2, dash='dash'),
    hovertemplate='<b>Ideal</b><br>Date: %{x|%b %d}<br>Story Points: %{y:.1f}<extra></extra>'
))

# Add actual burndown line
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Actual'],
    mode='lines+markers',
    name='Actual Burndown',
    line=dict(color='darkblue', width=3),
    marker=dict(size=8, color='darkblue'),
    hovertemplate='<b>Actual</b><br>Date: %{x|%b %d}<br>Story Points: %{y:.1f}<extra></extra>'
))

# Add a horizontal line at y=0
fig.add_hline(y=0, line_dash="solid", line_color="gray", opacity=0.5)

# Update layout
fig.update_layout(
    title={
        'text': 'Sprint Burndown Chart',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#333'}
    },
    xaxis_title='Date',
    yaxis_title='Story Points Remaining',
    xaxis=dict(
        tickformat='%b %d',
        showgrid=True,
        gridcolor='lightgray'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        range=[-5, total_story_points + 10]
    ),
    hovermode='x unified',
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    height=600,
    margin=dict(l=50, r=50, t=100, b=50)
)

# Display the chart
fig.show()

# Optional: Save to HTML file
# fig.write_html("burndown_chart.html")

# Print summary statistics
print("\n=== Burndown Chart Summary ===")
print(f"Sprint Duration: {sprint_start.strftime('%Y-%m-%d')} to {sprint_end.strftime('%Y-%m-%d')}")
print(f"Total Story Points: {total_story_points}")
print(f"Story Points Remaining: {actual_burndown[-1]}")
print(f"Story Points Completed: {total_story_points - actual_burndown[-1]}")
print(f"Completion Rate: {((total_story_points - actual_burndown[-1]) / total_story_points * 100):.1f}%")
print(f"Days Remaining: {(sprint_end - datetime.now()).days}")

if actual_burndown[-1] <= ideal_burndown[-1]:
    print("Status: ✓ On track or ahead of schedule")
else:
    print("Status: ⚠ Behind schedule")
