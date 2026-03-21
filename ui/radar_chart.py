import plotly.graph_objects as go


def radar_chart(report):

    categories = [
        "ATS Score",
        "Semantic Fit",
        "Experience"
    ]

    values = [
        report["final_score"] / 100,
        report["semantic_fit"],
        report["experience_alignment"]
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False
    )

    return fig