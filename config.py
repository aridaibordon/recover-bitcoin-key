from distutils.command.config import config

import os
import dotenv

dotenv.load_dotenv()

config = {
    "PUBLIC_ADDRESS": os.environ["PUBLIC_ADDRESS"],
    "PARTIAL_PRIVATE_KEY": os.environ["PARTIAL_PRIVATE_KEY"],
    "UNKNOWN_CHAR": "X",
    "CREATE_BACKUP": True,
    "PERIOD_BACKUP": int(16**4)
}