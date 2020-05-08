import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
birddata = pd.read_csv("bird_tracking.csv")

#==========================================================================

#plot the birds' trajectories
bird_names = pd.unique(birddata.bird_name)
plt.figure(figsize = (7,7))
for names in bird_names:
    #return boolean list of len(birddata), true if Eric, false otherwise
    ix = birddata.bird_name == names
    x, y = birddata.longitude[ix], birddata.latitude[ix]
    plt.plot(x,y,".", label = names)
plt.xlabel("Longitude")
plt.ylabel("latitude")
plt.legend(loc = "lower right")
plt.savefig("3birdtrajectories.pdf")

#==========================================================================

#plot histogram of eric's speed
eric_index = birddata.bird_name == 'Eric'
speed = birddata.speed_2d[eric_index]

#check if any of the members of speed are non-numeric values with np.isnan(speed).any()
ind = np.isnan(speed)
#operand before ind means flip the true / false values, as we want to plot only numeric values
plt.hist(speed[~ind])
plt.savefig("eric_hist.pdf")

#==========================================================================
#plot normalised histogram (sum of area under curve = 1), bins used only from 0 - 30
plt.hist(speed[~ind], bins=np.linspace(0,30,20), normed=True)
plt.xlabel("2D speed (m/s)")
plt.ylabel("Frequency")
plt.savefig("eric_hist_normalized.pdf")


#==========================================================================

#add datetime column, plot elapsed time
import datetime

#check the format of the date_time column of the birddata, turns out it is like
#2013-08-15 00:18:08+00 we can see that the last 3 digit of the data is not required
#as the UTC is +00 or no shift needed
birddata.date_time.head()

#check the type for the items in the columns, turns out to be string
type(birddata.date_time[1])

#add the timestamp column to our birddata DataFrame
birddata["timestamp"] = pd.Series(timestamps, index = birddata.index)

#to find the elapsed time between 1 row of observation and the other
#use (time[x] - time[y]) / datetime.timedelta(days = 1)
#change the parameters in timedelta to change to either 
#days elapsed (days = 1) or hours elapsed (hours = 1)

times = birddata.timestamp[birddata.bird_name == 'Eric']
#get a list of elapsed_time for Eric's observations
elapsed_time = [items - times[0] for items in times]
elapsed_days = np.array(elapsed_time) / datetime.timedelta(days = 1)

#plot the number of days past for eric's observation using pandas' plot function
#which take cares of NaN values (if any) automatically
plt.plot(elapsed_days)
plt.xlabel("Observation")
plt.ylabel("Elapsed time (days)")
plt.savefig("elapsed_time.pdf")

#===================================================================

#now we want to see the average daily speed of Eric
data = birddata[birddata.bird_name == "Eric"]
next_day = 1
inds = list()
mean_speeds = list()
#enumerate is similar to dict.items(), but it is for list
for index, days in enumerate(elapsed_days):
    if days < next_day:
        inds.append(index)
    else:
        mean_speeds.append(np.mean(data.speed_2d[inds]))
        inds = list() #empty the inds list
        next_day += 1

plt.figure(figsize = (8,7))
plt.plot(mean_speeds)
plt.xlabel("Day")
plt.ylabel("Mean speed (m/s)")
plt.savefig("daily_mean_speed_eric.pdf")

#====================================================================

#plot the daily mean speed of the 3 birds
import matplotlib.pyplot as plt

#add date column to birddata
birddata["date"] = birddata["timestamp"].dt.date

grouped_birdday = birddata.groupby(["bird_name", "date"])

eric_daily_speed  = grouped_birdday.speed_2d.mean()["Eric"]
sanne_daily_speed = grouped_birdday.speed_2d.mean()["Sanne"]
nico_daily_speed  = grouped_birdday.speed_2d.mean()["Nico"]

eric_daily_speed.plot(label="Eric")
sanne_daily_speed.plot(label="Sanne")
nico_daily_speed.plot(label="Nico")
plt.legend(loc="upper left")
plt.savefig("3birds_speed.pdf")

