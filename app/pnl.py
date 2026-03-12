def calculate_pnl(entry, current, size):

    if entry == 0:
        return 0,0

    pnl = (current-entry)*size

    percent = ((current-entry)/entry)*100

    return round(pnl,2), round(percent,2)