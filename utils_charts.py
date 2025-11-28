import plotly.graph_objects as go

def plot_price_chart(prices):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=prices,
        mode="lines",
        name="BTC Price (USDT)"
    ))
    fig.update_layout(
        title="Real-Time BTC/USDT Price Chart",
        xaxis_title="Time",
        yaxis_title="Price (USDT)",
        template="plotly_dark"
    )
    return fig
    
