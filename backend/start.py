'''
    This programs give the expected time that how long will a free parking spot be available.
    Addtional hardware inputs can be included if the expected parking spot is still occupied after the expected time runs out
    Also another algorithmn can be included to check whether the assigned buffer time of 2 mins is sufficient or needs to be changed
'''

from datetime import datetime,timedelta
from pandas import read_csv

#fetches the current date and time in a list now where 0 index is today's date and 1 index is today's time
def fetch_now():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()
    return now

#fetches the end column from csv and then processes it in a particular format to stores it in end screening them on some parameters
datasheet=read_csv('test.csv',sep=';',engine='python')
end=datasheet.end
end=list(end)

#function screens out the desirable dates and time on the basis of some parameters from the input end column
def screener(end):
    screened_end=[]
    for i in end:
        check=i.split('T')
        check[1]=check[1].split('+')[0]
        now=fetch_now()

        if now[0]==check[0] and now[1]<check[1]: #checks if both today's date and thr date from database is same and the the current time is less that the expected check out time
            screened_end.append(check[1])

    return screened_end

screened_end=screener(end)
time_close=[]

for check in screened_end:
    now=fetch_now()

    #variables check_t and now_t are datetime object for easier calculations
    check_t=datetime.strptime(check,'%H:%M:%S')
    now_t=datetime.strptime(now[1],'%H:%M:%S')

    wait_minutes=int(timedelta.total_seconds(abs(check_t-now_t))//60)+2 #gives an addtional 2 minute buffer time to empty the expected place according to thoer booled time

    if wait_minutes<=20: #maximum wait time is set to be as 20 minutes
        time_close.append(wait_minutes)


# This section gives a formated output to make it easier to understand for them
if len(time_close)==0:
    print('No free parking spots are expected to be free within 20 minutes other than the ones already available.')

elif len(time_close)==1:
    print('A free parking lot would be free in about {} minutes'.format(time_close[0]))

else:
    print('Here are a few parking spots that would be free soon:')
    print('Closet one would be free in about {} minutes'.format(min(time_close)))
    print('Some other durations are:')
    print('Empty in: ')

    time_close.sort()
    for i in time_close:
        if i!=min(time_close):
            print('{} minutes'.format(i))
