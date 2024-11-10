import os
import sys

import requests

if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 2:
        print("Few arguments")
        sys.exit(1)

    date = args[1]
    track = args[2]

    res = requests.get(
        f"https://horse-recommendation-v2-3ltic64prq-an.a.run.app/recommendation?date={date}&race_track={track}"
    )

    if res.status_code != 200:
        print(f"Error response, code: {res.status_code}")
        sys.exit(1)

    data = res.json()

    races = "\n".join(
        [
            (
                ",".join(list(map(lambda x: str(x["horse_id"]), r["recommendation"])))
                + ("(自信あり)" if r["confidence_flag"] else "")
            )
            for r in data["race_list"]
        ]
    )

    output_file = f"outputs/{date}/{track}.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, mode="w") as f:
        f.writelines(races)
