def main():
    infile = r"app_2.log"
    log = []
    passed = {}
    failed = set()

    with open(infile, "r") as f:
        for line in f:
            if "BIG" in line:
                start = line.find(">") + 3
                tmp = line[start:-3].split(";")
                log.append(tmp)
                if tmp[2] in passed:
                    passed[tmp[2]] += 1
                else:
                    passed.update({tmp[2]: 1})

    for line in log:
        if line[2] in passed and line[-1] == "DD":
            passed.pop(line[2])
            failed.add(line[2])

    print(f"___________________Failed test {len(failed)} devices___________________")
    for item in failed:
        print(f"Device {item} was removed")
    print(f"___________________Success test {len(passed)} devices___________________")
    for name, amount in passed.items():
        print(f"Device {name} sent {amount} statuses")


if __name__ == "__main__":
    main()
