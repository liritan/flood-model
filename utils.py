import os


def get_initial_equations_from_inputs(ui):
    return [float(ui.lineEdits[f"u{i}"].text()) for i in range(1, 16)]


def get_faks_from_inputs(ui):
    result = []
    for i in range(1, 5):
        a = float(ui.lineEdits[f"fak{i}_1"].text())
        b = float(ui.lineEdits[f"fak{i}_2"].text())
        c = float(ui.lineEdits[f"fak{i}_3"].text())
        d = float(ui.lineEdits[f"fak{i}_4"].text())
        result.append([a, b, c, d])
    return result


def get_equations_from_inputs(ui):
    result = []
    for i in range(1, 56):
        a = float(ui.lineEdits[f"f{i}_1"].text())
        b = float(ui.lineEdits[f"f{i}_2"].text())
        c = float(ui.lineEdits[f"f{i}_3"].text())
        d = float(ui.lineEdits[f"f{i}_4"].text())
        result.append([a, b, c, d])
    return result


def get_restrictions(ui):
    return [float(ui.lineEdits[f"u_restrictions{i}"].text()) for i in range(1, 16)]


lines = (
    ('g', '-'),
    ('c', '-'),
    ('r', '-'),
    ('y', '-'),
    ('m', '-'),
    ('b', '-'),
    ('teal', '-'),
    ('gray', '-'),
    ('olive', '-'),
    ('g', '--'),
    ('c', '--'),
    ('r', '--'),
    ('y', '--'),
    ('m', '--'),
    ('b', '--'),
    ('teal', '--'),
    ('gray', '--'),
    ('olive', '--'),
    ('g', '-.'),
    ('c', '-.'),
    ('r', '-.'),
    ('y', '-.'),
    ('m', '-.')
)


def clear_graphics():
    if os.path.exists("static/images/diagram.png"):
        os.remove("static/images/diagram.png")

    if os.path.exists("static/images/diagram2.png"):
        os.remove("static/images/diagram2.png")

    if os.path.exists("static/images/diagram3.png"):
        os.remove("static/images/diagram3.png")

    if os.path.exists("static/images/diagram4.png"):
        os.remove("static/images/diagram4.png")

    if os.path.exists("static/images/diagram5.png"):
        os.remove("static/images/diagram5.png")

    if os.path.exists("static/images/figure.png"):
        os.remove("static/images/figure.png")

