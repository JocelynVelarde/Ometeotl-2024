import reflex as rx

data = [
    {"name": "A", "value": 100},
    {"name": "B", "value": 200},
    {"name": "C", "value": 300},
    {"name": "D", "value": 400},
    {"name": "E", "value": 500},
    {"name": "F", "value": 600},
]

def funnel_simple():
    return rx.recharts.funnel_chart(
        rx.recharts.funnel(
            rx.recharts.label_list(
                position="right",
                data_key="name",
                fill="#111",
                stroke="none",
            ),
            data_key="value",
            data=data,
        ),
        width="100%",
        height=250,
    )