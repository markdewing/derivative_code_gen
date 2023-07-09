# Convert text to list of lines
def make_lines(text):
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        lines.append(line)
    return lines


# Compare two source texts
def compare_src(s1, s2):
    ln1 = make_lines(s1)
    ln2 = make_lines(s2)
    for (l1, l2) in zip(ln1, ln2):
        assert l1 == l2, l1 + " versus " + l2
