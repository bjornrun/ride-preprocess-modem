from pathlib import Path
import natsort
import re
import json
import datetime
import math
import csv

def _preprocess_modem_data(src_path: str, dst_path: str) -> int:
    pathlist = Path(src_path).glob('**/*.csv')
    list1 = []
    list2 = []
    for path in pathlist:
        path_in_str = str(path)
        list1.append(path_in_str)

    list2 = natsort.natsorted(list1)

    with open(dst_path, 'w', newline='') as file_out:
        csv_out = csv.writer(file_out)
        csv_out.writerow(["year", "month", "day", "hour", "minute", "second", "COPS", "CESQ", "CSQ", "CEREG", "C5REG",
                          "GTRAT", "GTECELLLOCK", "GTSRVSTATUS", "GTCCINFOE", "GTCCINFO service", "GTCCINFO neighbor", "PCC", "SCC1", "SCC2"])

        row = 0

        for path in list2:
            timestamp_str = re.findall(r'\d+', path)
            try:
                year = timestamp_str[0]
                month = timestamp_str[1]
                day = timestamp_str[2]
                hour = timestamp_str[3]
                minutes = timestamp_str[4]
                seconds = timestamp_str[5]
            except IndexError:
                pass
            else:
                with open(path) as f:
                    lines = f.read().splitlines()
                    if len(lines) > 1:
                        try:
                            i = [i for i, s in enumerate(lines) if '+COPS: ' in s][0]
                            if len(lines[i]) > 12:
                                COPS = lines[i].split('+COPS: ')[1]
                        except Exception:
                            COPS = ""
                        try:
                            i = [i for i, s in enumerate(lines) if '+CSQ: ' in s][0]
                            CSQ = lines[i].split('+CSQ: ')[1]
                        except Exception:
                            CSQ = ""
                        try:
                            i = [i for i, s in enumerate(lines) if '+CESQ: ' in s][0]
                            CESQ =  lines[i].split('+CESQ: ')[1]
                        except Exception:
                            CESQ = ""
                        try:
                            i = [i for i, s in enumerate(lines) if '+CEREG: ' in s][0]
                            CEREG = lines[i].split('+CEREG: ')[1]
                        except Exception:
                            CEREG = ""
                        try:
                            i = [i for i, s in enumerate(lines) if '+C5GREG: ' in s][0]
                            C5GREG = lines[i].split('+C5GREG: ')[1]
                        except Exception:
                            C5GREG = ""
                        try:
                            i = [i for i, s in enumerate(lines) if '+GTRAT: ' in s][0]
                            GTRAT = lines[i].split('+GTRAT: ')[1]
                        except Exception:
                            GTRAT = ""
                        try:
                            i = [i for i, s in enumerate(lines) if '+GTCELLLOCK: ' in s][0]
                            GTCELLLOCK = int(lines[i].split('+GTCELLLOCK: ')[1])
                        except Exception:
                            GTCELLLOCK = 0
                        try:
                            i = [i for i, s in enumerate(lines) if '+GTSRVSTATUS: ' in s][0]
                            GTSRVSTATUS = lines[i].split('+GTSRVSTATUS: ')[1]
                        except Exception:
                            GTSRVSTATUS = ""
                        try:
                            i = [i for i, s in enumerate(lines) if '+GTCCINFOE: ' in s][0]
                            GTCCINFOE = lines[i].split('+GTCCINFOE: ')[1]
                        except Exception:
                            GTCCINFOE = ""
                        try:
                            i = [i for i, s in enumerate(lines) if '+GTCCINFO: ' in s][0]
                            GTCCINFO_service = lines[i+1] + ' ' + lines[i+2]
                            neighbors = ""
                            j = i + 4
                            while j < len(lines):
                                if ':' in lines[j]:
                                    break
                                neighbors += lines[j] + " "
                                j += 1
                            GTCCINFO_neighbors = lines[i+3] + ' ' + neighbors
                        except Exception:
                            GTCCINFO_service = ""
                            GTCCINFO_neighbors = ""
                        try:
                            i = [i for i, s in enumerate(lines) if 'PCC: ' in s][0]
                            PCC = lines[i].split('PCC: ')[1]
                        except Exception:
                            PCC = ""
                        try:
                            i = [i for i, s in enumerate(lines) if 'SCC1: ' in s][0]
                            SCC1 = lines[i].split('SCC1: ')[1]
                        except Exception:
                            SCC1 = ""
                        try:
                            i = [i for i, s in enumerate(lines) if 'SCC2: ' in s][0]
                            SCC2 = lines[i].split('SCC2: ')[1]
                        except Exception:
                            SCC2 = ""
                        csv_out.writerow(
                            [year, month, day, hour, minutes, seconds, COPS, CESQ, CSQ, CEREG, C5GREG, GTRAT, GTCELLLOCK,
                             GTSRVSTATUS, GTCCINFOE, GTCCINFO_service, GTCCINFO_neighbors, PCC, SCC1, SCC2])

                        row += 1
    return row


if __name__ == '__main__':
    print("Num positions: ", _preprocess_modem_data("/mnt/smb/modem", "/mnt/modem.csv"))
