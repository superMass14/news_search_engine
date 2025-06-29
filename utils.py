from datetime import datetime
def format_label(label="", values=""):
    formatted_values = ', '.join(
        list(
            map(lambda x: x[1:-1],values[1:-1].split(", "))
        )
    )
    return f"{label}:   {formatted_values}"


def format_time(date):
    time = datetime.fromisoformat(date)
    return time.strftime("%d/%m/%Y %H:%M:%S")