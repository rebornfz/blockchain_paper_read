import csv

#sFileName='data/testResult_final_without_space.csv'
def open_file(sFileName):

    info = {}
    with open(sFileName,newline='',encoding='UTF-8') as csvfile:
        rows=csv.reader(csvfile)
        for row in rows:
            #print(','.join(row))
            timestamp = row[0]
            road_id = row[1]
            vehicle_id = row[2]
            if info.get(timestamp) is None:
                info[timestamp] = {}
            if info[timestamp].get(road_id) is None:
                info[timestamp][road_id] =[]
            info[timestamp][road_id].append(vehicle_id)
    return info

def check_data(info):
    count_info = {}
    timestamp = []
    road_count = []
    vehicle_all_count = []
    everange = []
    for key in info:
        timestamp.append(key)
        rc = len(info[key])
        road_count.append(rc)
        vac = 0
        for subkey in info[key]:
            vc = len(info[key][subkey])
            vac += vc
        vehicle_all_count.append(vac)
        e = vac/rc
        everange.append(e)
        count_info[key]=[rc,vac,e]
    return count_info,timestamp,road_count,vehicle_all_count,everange
def returnlimitdata(count_info):
    # 选取2500-3000一段的车辆10个连续时间段的车辆团体信息
    #select = {}
    timestamp = []
    road_count = []
    vehicle_all_count = []
    everange = []
    everange = []
    for i in range(500, 4001, 50):
        a = count_info[str(i)]
        timestamp.append(i)
        road_count.append(a[0])
        vehicle_all_count.append(a[1])
        everange.append(a[1]/a[0])
    return timestamp,road_count,vehicle_all_count,everange












