from datetime import datetime, timedelta


def jinja_days_ago(date):
    if date is None:
        return "Never"
    today = datetime.now().date()
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').date()
    diff = (today - date).days

    if diff == 0:
        return "Today"
    elif diff == 1:
        return "Yesterday"
    else:
        return f"{diff} days ago"


def jinja_question_boxes(current_box):
    icons = []
    for i in range(1, 7):
        if i == current_box:
            if i == 6:
                icons.append(
                    "<i class='question-button-icon bi bi-mortarboard-fill text-success'></i>")
            else:
                icons.append(
                    f"<i class='question-button-icon bi bi-{i}-square-fill text-success'></i>")
        else:
            if i == 6:
                icons.append(
                    "<i class='question-button-icon bi bi-mortarboard text-secondary'></i>")
            else:
                icons.append(
                    f"<i class='question-button-icon bi bi-{i}-square text-secondary'></i>")
    return " ".join(icons)


def jinja_answer_boxes(current_box):
    icons = []
    for i in range(1, 7):
        if i == current_box:
            if i == 6:
                icons.append(
                    "<i class='question-button-icon bi bi-mortarboard-fill text-success'></i>")
            else:
                icons.append(
                    f"<i class='question-button-icon bi bi-{i}-square-fill text-success'></i>")
        elif i == current_box + 1:
            if i == 6:
                icons.append(
                    "<i class='question-button-icon bi bi-mortarboard-fill text-info'></i>")
            else:
                icons.append(
                    f"<i class='question-button-icon bi bi-{i}-square-fill text-info'></i>")
        else:
            if i == 6:
                icons.append(
                    "<i class='question-button-icon bi bi-mortarboard text-secondary'></i>")
            elif i == 1:
                if current_box == 1:
                    icons.append(
                        "<i class='question-button-icon bi bi-1-square-fill text-success'></i>")
                else:
                    icons.append(
                        "<i class='question-button-icon bi bi-1-square-fill text-dark'></i>")
            else:
                icons.append(
                    f"<i class='question-button-icon bi bi-{i}-square text-secondary'></i>")
    return " ".join(icons)
