import asyncio
import datetime

import psutil
from mysql.connector import connect, Error


async def fetchData():
    cpuTask = asyncio.create_task(getCPU())
    ramTask = asyncio.create_task(getRAM())
    diskTask = asyncio.create_task(getDisk())
    tempTask = asyncio.create_task(getTemp())

    cpu = await cpuTask
    ram = await ramTask
    disk = await diskTask
    temp = await tempTask

    time = getTime()

    data = (cpu, temp, ram, disk, time)
    return data

#def connectDB():
#    conn = mysql.connector.connect(
#        user='alec',
#        password='USER_PASSWORD',
#        host='localhost',
#        database='sys_stats')
      
#    print('connected!')
#    conn.close()
#    return

def connectDB(data):
    try:
        with connect(
            host='localhost',
            user='alec',
            password='USER_PASSWORD',
            database='sys_stats'
        ) as connection:
            query = "INSERT INTO system (cpu_usage, cpu_temp, ram_usage, disk_usage, date) VALUES (%s, %s, %s, %s, %s)"
            
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                connection.commit()

                cursor.close()
                connection.close()
    except Error as e:
        print(e)
 

def getTime():
    """ Gets current time """
    date = datetime.datetime.now()
    formatted = date.strftime('%Y-%m-%d %H:%M:%S')
    return formatted

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

    print(f'Data tuple: {data}')
    connectDB(data)


if __name__ == "__main__":
    asyncio.run(main())
