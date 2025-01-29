import os
from math import cos, sin, radians
filename1 = "./cal_coeff0.txt"
filename2 = "./cal_coeff1.txt"
filename3 = "./no_wind.txt"
filename4 = "./portmap.txt"
data_file = "./Modified_data.txt"
mapping = []
with open(filename4, 'r') as file4, open(filename3, 'r') as file3, open(filename2, 'r') as file2, open(filename1, 'r') as file1, open(data_file, 'r') as data_file:
    
    #data = sr.no, port (0/1), port no., x_dist, y_dist, x, C0, C1, C2, no_wind
            # 0     1           2           3       4    5  6   7   8       9
    #2	U01	0.0025	0.0087	0	0	0.4	1.3075
    lines4 = file4.readlines()
    lines3 = file3.readlines()
    lines2 = file2.readlines()
    lines1 = file1.readlines()
    line_data = data_file.readlines()   
    cal0 = [] # array of all coefficients of sensor 0
    for line in lines1:
        cal = line.split()
        cal0.append(cal)
    
    cal1 = []
    for line in lines2:
        cal = line.split()
        cal1.append(cal)
    
    no_wind = []
    for line in lines3:
        cal = line.split()
        no_wind.append(cal)
        
    for line in lines4:
        data = []
        datan = line.split()
        data.append(int(datan[0]))
        data.append(int(datan[4]))
        data.append(int(datan[5]))
        data.append(float(datan[2]))
        data.append(float(datan[3]))
        data.append(float(datan[6]))
        # print(data)
        if(int(datan[4])==0):
            data.append(float(cal0[int(datan[5])][0]))
            data.append(float(cal0[int(datan[5])][1]))
            data.append(float(cal0[int(datan[5])][2]))
            data.append(float(no_wind[int(datan[4])][int(datan[5])]))
        else:
            data.append(float(cal1[int(datan[5])][0]))
            data.append(float(cal1[int(datan[5])][1]))
            data.append(float(cal1[int(datan[5])][2]))
            data.append(float(no_wind[int(datan[4])][int(datan[5])]))
        mapping.append(data)
    j = 0
    dict_lift = {}
    dict_drag = {}
    dict_pressure = {}
    while((j*3)<len(line_data)):
        sensor1 = line_data[(j*3)].split()
        sensor2 = line_data[(j*3)+1].split()
        angle = float(line_data[(j*3)+2])
        j+=1
        total_lift = 0
        total_drag = 0
        prev_u = 0
        prev_l = 0
        dist_lower = []
        dist_upper = []
        pressure_lower = []
        pressure_upper = []
        for i in mapping:
            if(i[1]==0):    #other side port, first readingprev = i[5]
                voltage = float(sensor1[i[2]])-float(i[9])
                pressure = i[6]*(voltage**2) + i[7]*voltage + i[8]
                if(i[4]<=0):
                    pressure_lower.append(pressure/(0.5*1.225*(100)))
                    dist = i[5]-prev_l
                    prev_l = i[5]
                    dist_lower.append(i[5])
                    total_lift+=(pressure * dist)*cos(radians(angle))
                    total_drag+=(pressure * dist)*sin(radians(angle))
                else:
                    dist = i[5]-prev_u
                    prev_u = i[5]
                    pressure_upper.append(pressure/(0.5*1.225*(100)))
                    dist_upper.append(i[5])
                    total_lift-=(pressure * dist)*cos(radians(angle))
                    total_drag-=(pressure * dist)*sin(radians(angle))
            else:
                voltage = float(sensor2[int(i[2])])-float(i[9])
                pressure = i[6]*(voltage**2) + i[7]*voltage + i[8]
                if(i[4]<=0):
                    dist = i[5]-prev_l
                    prev_l = i[5]
                    pressure_lower.append(pressure/(0.5*1.225*(100)))
                    dist_lower.append(i[5])
                    total_lift+=(pressure * dist)*cos(radians(angle))
                    total_drag+=(pressure * dist)*sin(radians(angle))
                else:
                    dist = i[5]-prev_u
                    prev_u = i[5]
                    pressure_upper.append(pressure/(0.5*1.225*(100)))
                    dist_upper.append(i[5])
                    total_lift-=(pressure * dist)*cos(radians(angle))
                    total_drag-=(pressure * dist)*sin(radians(angle))
        pressures = {}
        for i in range(len(dist_upper)):
            pressures[dist_upper[i]] = pressure_upper[i]
        for i in range(len(dist_lower)):
            pressures[dist_lower[i]] = pressure_lower[i]
        print(len(dist_upper))
        dict_pressure[angle]=pressures
        dict_lift[angle]=total_lift/(0.5*1.225*(100)*150)
        dict_drag[angle]=total_drag/(0.5*1.225*(100)*150)
# for i in mapping:
#     print(i)
# print()
# print()
# print(dict_drag)
# print(dict_lift)
print(dict_pressure[-3.996])

import matplotlib.pyplot as plt
# Define the folder where you want to save the plots
save_folder = "pressure_plots"
os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist

for i in dict_pressure.keys():
    # Extract angles (keys) and values
    angles = list(dict_pressure[i].keys())
    values = list(dict_pressure[i].values())

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.scatter(angles, values, marker='o', color='b')

    # Add labels and title
    plt.xlabel('x-distance', fontsize=12)
    plt.ylabel('Coefficient of Pressure', fontsize=12)
    plt.title(f'Distance vs Pressure at angle: {i}', fontsize=14)

    # Add grid for better readability
    plt.grid(True)

    # Define the filename with the naming convention
    filename = os.path.join(save_folder, f'Cp_{i}.png')

    # Save the figure
    plt.savefig(filename, dpi=300, bbox_inches='tight')

    # Close the plot to free up memory
    plt.close()

print(f"Plots saved in '{save_folder}' folder.")

