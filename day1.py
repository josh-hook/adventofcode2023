import helpers


def _parse_line_part_1(line: str) -> int:
    """Parse a lines value"""
    # Scan for first number
    for i in range(len(line)):
        first = line[i]
        if first.isdigit():
            # Scan for last number
            for j in range(len(line)-1, i, -1):
                last = line[j]
                if last.isdigit():
                    return int(first+last)

            return int(first+first)

    raise Exception(f"line missing number: {line}")


def _build_tries() -> tuple[dict, dict]:
    alphabet = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    def _to_trie(reverse: bool = False) -> dict:
        trie = dict()
        for k, v in alphabet.items():
            if reverse:
                k = reversed(k)

            current = trie
            for c in k:
                if c in current:
                    current = current[c]
                else:
                    current[c] = dict()
                    current = current[c]

            current[None] = v
        return trie

    return _to_trie(), _to_trie(True)


def _find_first_number(line: str, trie: dict) -> tuple[int, int]:
    current = trie
    i = 0
    start = None
    while True:
        if None in current:
            return current[None], start
        if i >= len(line):
            return None, None

        c = line[i]
        if c in current:
            current = current[c]
            if start is None:
                start = i
        elif start is not None:
            # backtrack
            i = start
            start = None
            current = trie

        i += 1


def _parse_line_part_2(line: str) -> int:
    """Parse a lines value"""
    # Scan for first number

    trie, revtrie = _build_tries()
    first, first_idx = _find_first_number(line, trie)
    last, _ = _find_first_number(line[:first_idx:-1], revtrie)
    if last is None:
        last = first
    return (first*10) + last


@helpers.timed
def main():
    """main

    Part 2 solution runs in 0.0107089s once tries are built, but
    0.0267643s if including trie build time.
    """
    lines, part = helpers.load_input()

    sum = 0
    for line in lines:
        line = line.rstrip()
        if part == "1":
            sum += _parse_line_part_1(line)
        elif part == "2":
            sum += _parse_line_part_2(line)

    print(sum)


if __name__ == "__main__":
    main()
