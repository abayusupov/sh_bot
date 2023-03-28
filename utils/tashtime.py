from datetime import datetime
import pytz


def getTimeInTashkent():
    tashtime = pytz.timezone("Asia/Tashkent")
    timeInTashkent = datetime.now(tashtime)
    currentTimeInTashkent = timeInTashkent.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(currentTimeInTashkent, '%Y-%m-%d %H:%M:%S')
