# 从 https://github.com/Vonng/adcode/tree/master/data/adcode 同步需要的数据

import requests
import json
import base64
from io import StringIO
import csv
from progress.bar import Bar

adcode_dir_url = "https://api.github.com/repos/Vonng/adcode/git/trees/55df6cf713cdac2ac5220c972edf68553d2d4afa"
# 代表整个中国 adcode
china_base_adcode = "100000000000"


def get_body(url):
    r = requests.get(url, timeout=30, headers={'user-agent': 'Mozilla/5.0'})
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text


csvs = json.loads(get_body(adcode_dir_url))["tree"]
bar = Bar('Syncing', max=len(csvs))

with open("./cpca/resources/adcodes.csv", "w") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["adcode", "name", "longitude", "latitude"])
    for csv_info in csvs:
        blobs_url = csv_info["url"]
        csv_blob = json.loads(get_body(blobs_url))
        csv_lines = str(base64.b64decode(csv_blob["content"]), encoding="utf8")
        f = StringIO(csv_lines)
        csv_reader = csv.reader(f)
        for csv_record in csv_reader:
            adcode = csv_record[0]
            standard_name = csv_record[2]
            longitude = csv_record[12]
            latitude = csv_record[13]
            # 只选取省市区三级的 adcode 并且排除代表整个中国的 adcode
            if adcode[6:] == "000000" and adcode != china_base_adcode:
                csv_writer.writerow([adcode, standard_name, longitude, latitude])
        bar.next()

bar.finish()
