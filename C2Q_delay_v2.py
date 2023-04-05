
from PyLTSpice import SimCommander
import re

LTC = SimCommander("characterization_NVFF_delay.asc")
delays = []
counter = 0
# timings = [round(x / 2 + 10, 2) for x in range(0, 580)]
# timings2 = [round(x / 2 + 9.99999, 5) for x in range(0, 580)]

timings = [round(x*100 + 10, 2) for x in range(0, 99)]
timings2 = [round(x*100 + 9.99999, 5) for x in range(0, 99)]

print('=============================================')
print('TIMINGS')
print('=============================================')
for num in timings:
    print(num)
for num in timings2:
    print(num)

counter1 = 0
for i in timings:
    # Modify the data time
    with open('C:\\Users\\Law Jia Yu\\Documents\\EEEY4\\FYP\\Simulations\\new simulations\\NVDL_proposed\\designs\\45nm\\PWL files\\characterization of delay\\tb1\\D.txt', 'r+') as f:
        lines = f.readlines()
        lines[0] = '0u 0\n' 
        f.seek(0)
        lines[1] = str(timings2[counter1]) + 'u 0\n' 
        f.seek(1)
        counter1 = counter1 + 1
        lines[2] = str(i) + 'u 1.1\n'
        f.seek(2)
        f.writelines(lines)

    LTC.run()
    LTC.wait_completion()                             # Waits for the LTSpice simulations to complete

    print("Total Simulations: {}".format(LTC.runno))
    print("Successful Simulations: {}".format(LTC.okSim))
    print("Failed Simulations: {}".format(LTC.failSim))


    # Read the delay info
    counter = counter + 1
    filename = 'characterization_NVFF_delay_' + str(counter) + '.log'
    print('opening file:', filename)
    with open(filename, 'r', encoding='latin-1') as f:
        for line in f:
            if line.startswith('c2q_delay'):
                linetxt = line.strip()
                # the pattern for the line, i.e. 'c2q_delay: time - 30u=1.23296e-008 at 3.00123e-005'
                pattern = r'=([\d.]+(?:e[+-]\d+)?)\s+at'
                match = re.search(pattern, linetxt)
                if match:
                    number = float(match.group(1))
                    print(number)
                    delays.append(number)
                else:
                    print('No match found')
                break
        else:
            print("No line starting with 'c2q_delay' found in the file.")

print('=============================================')
print('DELAYS')
print('=============================================')
for num in delays:
    print(num)



