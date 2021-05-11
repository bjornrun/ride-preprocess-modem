import datetime
import os
import sys
from pathlib import Path
import natsort
import re
import csv


def _preprocess_modem_data(src_path: str, dst_path: str) -> int:
    if os.path.exists(dst_path):
        if os.stat(dst_path).st_size > 1024 * 1024:
            print("{dst} exists with size {size}, skip calculation".format(dst=dst_path,
                                                                           size=os.stat(dst_path).st_size))
            return 0

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
                          "GTRAT", "GTECELLLOCK", "GTSRVSTATUS", "GTCCINFOE", "GTCCINFO service cell", "IsServiceCell",
                          "rat", "mcc", "mnc", "tac", "cellid", "earfcn", "physicalcellId", "band", "bandwidth",
                          "rssnr_value",
                          "rxlev", "rsrp", "rsrq",
                          "IsServiceCell1", "rat1", "mcc1", "mnc1", "tac1", "cellid1", "earfcn1", "physicalcellId1",
                          "bandwidth1", "rxlev1", "rsrp1", "rsrq1",
                          "IsServiceCell2", "rat2", "mcc2", "mnc2", "tac2", "cellid2", "earfcn2", "physicalcellId2",
                          "bandwidth2", "rxlev2", "rsrp2", "rsrq2",
                          "IsServiceCell3", "rat3", "mcc3", "mnc3", "tac3", "cellid3", "earfcn3", "physicalcellId3",
                          "bandwidth3", "rxlev3", "rsrp3", "rsrq3",
                          "IsServiceCell4", "rat4", "mcc4", "mnc4", "tac4", "cellid4", "earfcn4", "physicalcellId4",
                          "bandwidth4", "rxlev4", "rsrp4", "rsrq4",
                          "PCC", "SCC1", "SCC2", "datetime"])

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
                            GTCCINFO_service_cell = lines[i+1]
                            [IsServiceCell,rat,mcc,mnc,tac,cellid,earfcn,physicalcellId,band,bandwidth,rssnr_value,rxlev,rsrp,rsrq] = lines[i+2].split(',')
                            j = i + 4
                            [IsServiceCell_0,rat_0,mcc_0,mnc_0,tac_0,cellid_0,earfcn_0,physicalcellId_0,bandwidth_0,rxlev_0,rsrp_0,rsrq_0] = ",,,,,,,,,,,".split(',')
                            [IsServiceCell_1,rat_1,mcc_1,mnc_1,tac_1,cellid_1,earfcn_1,physicalcellId_1,bandwidth_1,rxlev_1,rsrp_1,rsrq_1] = ",,,,,,,,,,,".split(',')
                            [IsServiceCell_2,rat_2,mcc_2,mnc_2,tac_2,cellid_2,earfcn_2,physicalcellId_2,bandwidth_2,rxlev_2,rsrp_2,rsrq_2] = ",,,,,,,,,,,".split(',')
                            [IsServiceCell_3,rat_3,mcc_3,mnc_3,tac_3,cellid_3,earfcn_3,physicalcellId_3,bandwidth_3,rxlev_3,rsrp_3,rsrq_3] = ",,,,,,,,,,,".split(',')

                            if j < len(lines):
                                [IsServiceCell_0,rat_0,mcc_0,mnc_0,tac_0,cellid_0,earfcn_0,physicalcellId_0,bandwidth_0,rxlev_0,rsrp_0,rsrq_0] = lines[j].split(',')
                            if j + 1 < len(lines):
                                [IsServiceCell_1,rat_1,mcc_1,mnc_1,tac_1,cellid_1,earfcn_1,physicalcellId_1,bandwidth_1,rxlev_1,rsrp_1,rsrq_1] = lines[j + 1].split(',')
                            if j + 2 < len(lines):
                                [IsServiceCell_2,rat_2,mcc_2,mnc_2,tac_2,cellid_2,earfcn_2,physicalcellId_2,bandwidth_2,rxlev_2,rsrp_2,rsrq_2] = lines[j + 2].split(',')
                            if j + 3 < len(lines):
                                [IsServiceCell_3,rat_3,mcc_3,mnc_3,tac_3,cellid_3,earfcn_3,physicalcellId_3,bandwidth_3,rxlev_3,rsrp_3,rsrq_3] = lines[j + 3].split(',')

                        except Exception:
                            GTCCINFO_service_cell = ""
                            [IsServiceCell,rat,mcc,mnc,tac,cellid,earfcn,physicalcellId,band,bandwidth,rssnr_value,rxlev,rsrp,rsrq] = ",,,,,,,,,,,,,".split(',')
                            [IsServiceCell_0,rat_0,mcc_0,mnc_0,tac_0,cellid_0,earfcn_0,physicalcellId_0,bandwidth_0,rxlev_0,rsrp_0,rsrq_0] = ",,,,,,,,,,,".split(',')
                            [IsServiceCell_1,rat_1,mcc_1,mnc_1,tac_1,cellid_1,earfcn_1,physicalcellId_1,bandwidth_1,rxlev_1,rsrp_1,rsrq_1] = ",,,,,,,,,,,".split(',')
                            [IsServiceCell_2,rat_2,mcc_2,mnc_2,tac_2,cellid_2,earfcn_2,physicalcellId_2,bandwidth_2,rxlev_2,rsrp_2,rsrq_2] = ",,,,,,,,,,,".split(',')
                            [IsServiceCell_3,rat_3,mcc_3,mnc_3,tac_3,cellid_3,earfcn_3,physicalcellId_3,bandwidth_3,rxlev_3,rsrp_3,rsrq_3] = ",,,,,,,,,,,".split(',')
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
                            [year, month, day, hour, minutes, seconds, COPS, CESQ, CSQ, CEREG, C5GREG, GTRAT,
                             GTCELLLOCK, GTSRVSTATUS, GTCCINFOE, GTCCINFO_service_cell, IsServiceCell, rat, mcc, mnc,
                             tac, cellid, earfcn, physicalcellId,band,bandwidth,rssnr_value,rxlev,rsrp,rsrq,
                             IsServiceCell_0,rat_0,mcc_0,mnc_0,tac_0,cellid_0,earfcn_0,physicalcellId_0,bandwidth_0,rxlev_0,rsrp_0,rsrq_0,
                             IsServiceCell_1,rat_1,mcc_1,mnc_1,tac_1,cellid_1,earfcn_1,physicalcellId_1,bandwidth_1,rxlev_1,rsrp_1,rsrq_1,
                             IsServiceCell_2,rat_2,mcc_2,mnc_2,tac_2,cellid_2,earfcn_2,physicalcellId_2,bandwidth_2,rxlev_2,rsrp_2,rsrq_2,
                             IsServiceCell_3,rat_3,mcc_3,mnc_3,tac_3,cellid_3,earfcn_3,physicalcellId_3,bandwidth_3,rxlev_3,rsrp_3,rsrq_3,
                             PCC, SCC1, SCC2,
                             datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes), int(seconds))
                             ])

                        row += 1
    return row


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Num modem data: ", _preprocess_modem_data("/mnt/smb/modem", "/mnt/modem.csv"))
    else:
        print("Src:", sys.argv[1], " Dst:", sys.argv[2], " Num modem data:",
              _preprocess_modem_data(sys.argv[1], sys.argv[2]))
