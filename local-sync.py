import sys
import os
import csv
from progress.bar import Bar

if len(sys.argv) != 2:
    print("python local-sync.py <directory>")
    sys.exit(1)

adcodes_root = sys.argv[1]

# 代表整个中国 adcode
china_base_adcode = "100000000000"

with open("./cpca/resources/adcodes.csv", "w") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["adcode", "name", "longitude", "latitude"])
    for root, dirs, files in os.walk(adcodes_root):
        bar = Bar('Syncing', max=len(files))
        for file_name in files:
            full_path = os.path.join(root, file_name)
            with open(full_path) as csv_file:
                csv_reader = csv.reader(csv_file)
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
