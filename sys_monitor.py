import psutil
import asyncio

#TODO: make database to write info to

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
        print(f'Temperatures are: {temp}')
        return temp
    except AttributeError:
        pass


def insert_database(cpu, ram, disk, temp):
    print(f'cpu: {cpu}, ram: {ram}, disk: {disk}, temp: {temp}')
    return


async def main():
    cpuTask = asyncio.create_task(getCPU())
    ramTask = asyncio.create_task(getRAM())
    diskTask = asyncio.create_task(getDisk())
    tempTask = asyncio.create_task(getTemp())

    cpu = await cpuTask
    ram = await ramTask
    disk = await diskTask
    temp = await tempTask

    insert_database(cpu, ram, disk, temp)
    

if __name__ == "__main__":
    asyncio.run(main())
