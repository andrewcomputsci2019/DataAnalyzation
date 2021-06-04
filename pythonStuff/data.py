import csv
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("hello world")
    postgres_Put_Time = []
    dynamoDB_Put_Time = []
    postgres_Get_Time = []
    dynamoDB_Get_Time = []
    with open("results.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count==0:
                line_count +=1
                continue
            else:
                print(row[0]+',' + row[1] + ',' + row[2] + ',' + row[3])
                postgres_Put_Time.append(np.float64(row[0])/(10.0**6)) 
                dynamoDB_Put_Time.append(np.float64(row[1])/(10.0**6))
                postgres_Get_Time.append(np.float64(row[2])/(10.0**6))
                dynamoDB_Get_Time.append(np.float64(row[3])/(10.0**6))
                line_count+=1
        figure,axis = plt.subplots(2,2,figsize=(15,15))
        axis[0,0].hist(postgres_Get_Time,bins='auto',align='mid')
        axis[0,0].set_title("Postgres Get Time")
        axis[0,0].set_xlabel("Time In Millisecond")
        axis[0,0].set_ylabel("Frequency")
        axis[0,1].hist(dynamoDB_Get_Time,bins='auto',facecolor='red',align='mid')
        axis[0,1].set_xlabel("Time in Millisecond")
        axis[0,1].set_ylabel("Frequency")
        axis[0,1].set_title("DynamoDB Get time")
        axis[1,0].hist(postgres_Put_Time,bins='auto',align='mid')
        axis[1,0].set_title('Postgres Put Time')
        axis[1,0].set_xlabel("Time in Millisecond")
        axis[1,0].set_ylabel("Frequency")
        axis[1,1].hist(dynamoDB_Put_Time,bins='auto',facecolor='red',align='mid')
        axis[1,1].set_title('DynamoDB Put Time')
        axis[1,1].set_xlabel("Time in Millisecond")
        axis[1,1].set_ylabel("Frequency")
        figure.savefig('mygraph.png',dpi=200)

        




if __name__ == '__main__':
    main()