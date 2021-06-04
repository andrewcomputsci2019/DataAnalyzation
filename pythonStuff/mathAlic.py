import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean
from scipy import stats as st
import csv
Postgres_Put_Time = []
DynamoDB_Put_TIme = []
Postgres_Get_Time = [] 
DynamoDB_Get_Time = []
## First Function to be called
def readData():
    with open("results.csv") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        line_count = 0
        for rows in csv_reader:
            if line_count == 0:
                line_count+=1
                continue
            else:
                Postgres_Put_Time.append(np.float64(rows[0])/10**6)
                DynamoDB_Put_TIme.append(np.float64(rows[1])/10**6)
                Postgres_Get_Time.append(np.float64(rows[2])/10**6)
                DynamoDB_Get_Time.append(np.float64(rows[3])/10**6)
## to be run after readData
def doMath_T_Test_Put():
    Put_TimeSd = np.sqrt(((np.std(Postgres_Put_Time)**2)/200.0)+(np.std(DynamoDB_Put_TIme)**2)/200.0)
    t = (np.average(Postgres_Put_Time)-np.average(DynamoDB_Put_TIme))/Put_TimeSd
    pvalt = st.t.cdf(t,df=199)* 2.0
    pval = st.ttest_ind(Postgres_Put_Time,DynamoDB_Put_TIme,alternative='less')
    print("std: " + str(Put_TimeSd))
    print("stat value: " + str(t))
    print("pval: "+ str (pvalt))
    print("not my test: " + str(pval[1]))
    rv = st.t(df=199,loc=0,scale=1)
    x = np.linspace(rv.ppf(0.00001),rv.ppf(0.99999),1000)
    plt.figure(dpi=200,figsize=[15,15])
    y = rv.pdf(x)
    plt.plot(x,y,label='T-Distribution')
    xs= np.linspace(rv.ppf(0.00001),rv.ppf(pval[1]),1000)
    plt.fill_between(xs,rv.pdf(xs),color='r',label='Pval')
    plt.xlabel("Number of standard deviation from mean")
    plt.ylabel("Probity density")
    plt.title("Postgres-DynamoDb Put time in millseconds T-Distribution")
    plt.legend(loc='upper left', title='Legend')
    plt.savefig("graph1.png")
    
def doMath_T_Test_Get():
    pval = st.ttest_ind(Postgres_Get_Time,DynamoDB_Get_Time,alternative='less')
    print(str(pval[1]))
    rv = st.t(df=199,loc=0,scale=1)
    x = np.linspace(rv.ppf(0.00001),rv.ppf(0.99999),1000)
    y = rv.pdf(x)
    fig,axis = plt.subplots(1,figsize=(15,15))
    axis.plot(x,y,color='b',label='T-Distribution')
    xs = np.linspace(rv.ppf(pval[1]),rv.ppf(0.00001),100)
    axis.fill_between(xs,rv.pdf(xs),color='r',label='Pval')
    axis.set_xlabel('distance from mean in stanerd deviation')
    axis.set_ylabel('Probability density')
    axis.set_title('Postgres-DynamoDB Get time')
    axis.legend(loc='upper left',title='Legend')
    fig.savefig('graph2.png',dpi=200)
    

def doMath_T_Interval_PutTime():
    global pm 
    pm = np.array([+1,-1])
    print(str(np.std(DynamoDB_Put_TIme)))
    meanDelta = (np.average(Postgres_Put_Time)-np.average(DynamoDB_Put_TIme))
    posInterval,negInterval = meanDelta+pm*st.t.ppf(.995,199)*np.sqrt(np.std(Postgres_Put_Time)**2/200+np.std(DynamoDB_Put_TIme)**2/200)
    print("interval: (" +str(posInterval)+"," + str(negInterval)+")")

def doMath_T_Interval_GetTime():
    meanDelta = (np.average(Postgres_Get_Time)-np.average(DynamoDB_Get_Time))
    postInterval,negInterval = meanDelta+pm*st.t.ppf(.995,199)*np.sqrt(np.std(Postgres_Get_Time)**2/200+np.std(DynamoDB_Get_Time)**2/200)
    print("interval: (" + str(postInterval)+ "," + str(negInterval)+")")

readData()
##doMath_T_Test_Put()
##doMath_T_Test_Get()
doMath_T_Interval_PutTime()
doMath_T_Interval_GetTime()
pval = st.ttest_ind(Postgres_Put_Time,DynamoDB_Put_TIme,alternative='less')
print("not my test: " + str(pval[1]))

pval = st.ttest_ind(Postgres_Get_Time,DynamoDB_Get_Time,alternative='less')
print(str(pval[1]))


