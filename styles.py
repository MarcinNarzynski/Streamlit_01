
def get_status_color(value: str):
    if value in ["PASS", 1]:
        return "color: lime"

    if value in ["FAIL", -1]:
        return "color: red"

    return ""
