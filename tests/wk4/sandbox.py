def get_base(drink: str, total: int):
    for s in ["coffee", "tea", "milk", "latte", "milk tea"]:
        if s in drink:
            base_needed = [0, 0, 0]
            if "latte" in s:
                base_needed[0] += int(total / 2)
                base_needed[2] += int(total / 2)
            elif "milk tea" in s:
                base_needed[1] += int(total / 2)
                base_needed[2] += int(total / 2)
            elif "coffee" in s:
                base_needed[0] += total
            elif "tea" in s:
                base_needed[1] += total
            else:
                base_needed[2] += total
            return s, base_needed
    return "", [0, 0, 0]
