#this file will be used for modifying the data file to a desired structure
import numpy as np
file = "./wind data (2).txt"
write_to = "./Modified_data.txt"
with open(file, 'r') as file:
    data_lines = file.readlines()
    j = 2
    angle_prev = []
    sum_array = [0.0] * 32
    modified_data = []
    i=0
    flag = 1
    print(len(data_lines[1003]))
    while i<len(data_lines):
        if(len(data_lines[i])<50):
            print(i)
            if(len(data_lines[i])<7):
                i+=1
                print(f"at i = {i}, len <5")
            else:
                if not flag:
                    print("one batch completed")
                    array = []
                    for k in range(len(sum_array)):
                        array.append(sum_array[k]/500)
                        sum_array[k]=0.0
                    print("data appended")
                    if(j != 2):
                        modified_data.append(array)
                    j=(j+1)%3
                    print(f"modified j : {j} at i = {i}")
                    i+=1
                if flag:
                    print("repeated angle considered")
                    array = []
                    for k in range(len(sum_array)):
                        sum_array[k]=0.0
                    j=(j+1)%3
                    if(len(modified_data)):
                        modified_data.pop()
                        modified_data.pop()
                    flag = 0
                    print(f"modified j : {j} at i = {i}")
                    i+=1
        else:
            if(j==0):
                data = data_lines[i].split()
                for k in range(len(sum_array)):
                    # print(data[k])
                    sum_array[k]+=float(data[k])
                i+=1
            elif(j==1):
                data = data_lines[i].split()
                for k in range(len(sum_array)):
                    sum_array[k]+=float(data[k])
                i+=1
            elif(j==2):
                print(i)
                print(data_lines[i])
                ang = data_lines[i].split()
                if(ang[0] not in angle_prev):
                    angle_prev.append(ang[0])
                    modified_data.append(ang[0])
                    i+=501
                    # print(f"changed : {data_lines[i]}, i:{i}")
                    if(len(data_lines[i])>50):
                        break
                else:
                    i+=501
                    print("repeated angle")
                    flag = 1
                    # print(f"changed : {data_lines[i]}, i:{i}")
                    
    with open(write_to, '+a') as modified_data_file :  
        k=0 
        for i in modified_data:
            if(k!=2):
                for j in i:
                    modified_data_file.write(str(j))
                    modified_data_file.write(" ")
                # print("data written")
                # file.write("\n")
                modified_data_file.write("\n")  
                k+=1
            else:
                 modified_data_file.write(str(i))
                 modified_data_file.write("\n")
                 k=0
    # print(modified_data)        

            
    