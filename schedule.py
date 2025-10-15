def t(h, m=0):
    return (h, m)

def to_min(tm):
    h, m = tm
    return h*60 + m

def to_time(m):
    return (m//60, m%60)

def fmt(tm):
    return f"{tm[0]:02d}:{tm[1]:02d}"


def avail_slots(s_start, s_end, appts):
    s_min = to_min(s_start)
    e_min = to_min(s_end)

    appt_min = [(to_min(s), to_min(e)) for s, e in appts]
    appt_min.sort(key=lambda x: x[0])

    free = []
    cur = s_min
    for st, en in appt_min:
        if cur < st:
            free.append((cur, st))
        cur = max(cur, en)

    if cur < e_min:
        free.append((cur, e_min))

    return [(to_time(s), to_time(e)) for s, e in free]

def shift_dur(s_start, s_end):
    return to_min(s_end) - to_min(s_start)

def used_time(appts):
    total = 0
    for s, e in appts:
        total += to_min(e) - to_min(s)
    return total


if __name__ == "__main__":
    s_start = t(9, 30)
    s_end = t(18, 0)

    appts = [
        (t(12, 0), t(13, 0)),
        (t(15, 0), t(16, 0)),
        (t(16, 0), t(17, 0)),
    ]

    free = avail_slots(s_start, s_end, appts)

    print("Shift:", fmt(s_start), "to", fmt(s_end))
    print("Appointments:")
    for s, e in appts:
        print(f"  {fmt(s)} - {fmt(e)}")

    print("\nAvailable slots:")
    for s, e in free:
        dur = to_min(e) - to_min(s)
        h, m = dur//60, dur%60
        print(f"  {fmt(s)} - {fmt(e)}  ({h}h {m}m)")

    total = shift_dur(s_start, s_end)
    used = used_time(appts)
    avail = total - used

    print(f"\nTotal shift: {total//60}h {total%60}m")
    print(f"Utilized: {used//60}h {used%60}m")
    print(f"Available: {avail//60}h {avail%60}m")
