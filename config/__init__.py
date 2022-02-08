data = []

with open('config/config.txt', 'r') as file:
    for line in file.readlines():
        data.append(line)

with open('config/config.py', 'w') as file:
    file.writelines(data)
