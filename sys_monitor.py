import psutil
import asyncio
#TODO: import datetime and include timestamp of when data was recorded also
import datetime
#TODO: make database to write info to
import mysql.connector


async def fetchData():
    cpuTask = asyncio.create_task(getCPU())
    ramTask = asyncio.create_task(getRAM())
    diskTask = asyncio.create_task(getDisk())
    tempTask = asyncio.create_task(getTemp())

    cpu = await cpuTask
    ram = await ramTask
    disk = await diskTask
    temp = await tempTask

    data = (cpu, ram, disk, temp)
    return data

#def insertRecord(cur, data):
#    """ Inserts the recent system information into system table """
#    cpu, ram, disk, temp, date = data[0], data[1], data[2], data[3], data[4]
#    
#    #NOTE: maybe INSERT INTO sys_stats.system(cpu_usage, cpu_temp, ram_usage, disk_usage, date) VALUES (?, ?, ?, ?, ?)", (cpu, temp, ram, disk, temp, date))
#    cur.execute("INSERT INTO sys_stats.system(cpu, temp, ram, disk, date) VALUES (?, ?, ?, ?, ?)", (cpu, temp, ram, disk, date))

def connectDB():
    conn = mysql.connector.connect(
        user='alec',
        password='USER_PASSWORD',
        host='localhost',
        database='sys_stats')
      
    print('connected!')
    conn.close()
    return


def getTime():
    """ Gets current time """
    date = 0 #get current date
    return date

async def getCPU():
    """ Get usage of the CPU """
    usage = psutil.cpu_percent(4)
    print(f'CPU usage: {usage}%')
    return usage

async def getRAM():
    """ Get system RAM usage """
    usage = psutil.virtual_memory()[2]
    print(f'RAM used: {usage}%')
    return usage

async def getDisk():
    """ Gets amount of storage in use """
    usage = psutil.disk_usage('/')
    print(f'Disk usage: {usage.percent}%')
    return usage.percent

async def getTemp():
    """ Gets system CPU temperature """
    try:
        temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        degree = u'\N{DEGREE SIGN}'
        print(f'Temperatures are: {temp}{degree}C')
        return temp
    except AttributeError:
        pass


async def main(): #NOTE: maybe remove async here?
    dataTask = asyncio.create_task(fetchData())
    data = await dataTask

    connectDB()
    
    #insertRecord(cursor, data)
    #insert_database(cpu, ram, disk, temp)
    
    

if __name__ == "__main__":
    asyncio.run(main())
