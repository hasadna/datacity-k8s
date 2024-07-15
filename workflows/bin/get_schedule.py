import sys
import random


INTERVALS = {
    "monthly": "{minutes} {hours} 1 * *",
    "weekly": "{minutes} {hours} * * 1",
    "daily": "{minutes} {hours} * * *",
    "hourly": "{minutes} * * * *",
}


def main(interval):
    schedule = INTERVALS.get(interval)
    if not schedule:
        raise Exception(f"Unknown interval: {interval}")
    print(schedule.format(minutes=random.randint(0, 59), hours=random.randint(0, 23)))


if __name__ == "__main__":
    main(*sys.argv[1:])
