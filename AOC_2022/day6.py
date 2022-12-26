
test_data = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'



with open('day6_input.txt', 'r') as f:
    data = f.read()

##data = test_data


for (i, c) in enumerate(data):
    packet = data[i:i+14]
    if len(set(packet)) == 14:
        print(i+14, packet)
        break
            













