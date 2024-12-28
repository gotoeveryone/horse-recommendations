import os
import sys

import requests

AREAS = {
    "ohi": "大井",
    "funabashi": "船橋",
    "urawa": "浦和",
    "kawasaki": "川崎",
}

if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 2:
        print("Few arguments")
        sys.exit(1)

    date = args[1]
    area = args[2]  # ohi/funabashi/urawa/kawasaki

    if area not in AREAS:
        print(f"Invalid area, area: {area}")
        sys.exit(1)

    res = requests.get("https://keiba.rakuten.co.jp/api/aiPrediction")

    if res.status_code != 200:
        print(f"Error response, code: {res.status_code}")
        sys.exit(1)

    recommendations = list(
        filter(lambda x: x["date"] == date, res.json()["data"]["recommendations"])
    )
    if not recommendations:
        print("Data not found")
        sys.exit(1)

    recommendation = recommendations[0]
    racecourses = list(
        filter(lambda x: x["name"] == AREAS[area], recommendation["racecourses"])
    )
    if not racecourses:
        print("Data not found")
        sys.exit(1)

    racecourse = racecourses[0]

    races = "\n".join(
        [
            (
                ",".join(
                    list(
                        map(
                            lambda x: str(x["number"]),
                            filter(lambda h: h["rank"] is not None, r["horses"]),
                        )
                    )
                )
                + ("(推奨)" if r["recommended_flag"] else "")
            )
            for r in racecourse["races"]
        ]
    )

    output_file = f"outputs/{date}/nankan_{AREAS[area]}.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, mode="w") as f:
        f.writelines(races)
