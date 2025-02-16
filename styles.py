
def get_status_color(value: str):
    if value in ["PASS", True]:
        return "color: lime"

    if value in ["FAIL", False]:
        return "color: red"

    return ""
