from datetime import datetime


def create_backup(last_hex) -> None:
    """
    Create a backup with the last character.

    """
    with open("log.txt", "a") as f:
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        f.write(f"{timestamp: <20} {last_hex}\n")


def load_backup() -> int:
    """
    Return last backup in log.txt.

    """
    try:
        with open("log.txt", "r") as f:
            for line in f.readlines():
                pass

            return int(line.split()[-1], 16)

    except:
        print("No backup found!")
        return 0
