from pprint import pprint as pp 

elves = [0]

with open("input.txt","r") as f:
    for rawln in f:
        ln = rawln.strip()
        if len(ln) > 0:
            elves[-1] = elves[-1] + int(ln)
        else:
            elves.append(0)

pp(elves)

maxind = 0
maxval = 0
for i,e in enumerate(elves):
    if e > maxval:
        maxval = e
        maxind = i
        
print(f"Elf {maxind} has {maxval} calories")

elvlist = sorted([(cal,i) for (i,cal) in enumerate(elves)], reverse=True)
pp(elvlist)
print(f"Top 3: {elvlist[0][0] + elvlist[1][0] + elvlist[2][0]}")
