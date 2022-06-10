class Kmaps:
    def __init__(self, minterm, dontcare):
        self.minterm = minterm
        self.dontcare = dontcare

        self.minterm.sort()
        self.minterms = self.minterm + self.dontcare
        self.minterms.sort()
        self.size = 4
        self.groups = {}
        self.all_pi = set()
        # Primary grouping starts
        for mterm in self.minterms:     # count '1' in minterms and convert to binary form in str
            try:
                self.groups[bin(mterm).count('1')].append(bin(mterm)[2:].zfill(self.size))  # 7 -> 0b111  ,minterm)[2:]=111 - '0b' remove 
            except KeyError:
                self.groups[bin(mterm).count('1')] = [bin(mterm)[2:].zfill(self.size)]
        # Primary grouping ends

        #Primary group printing starts
        self.pri_grp_str = f"\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n{'='*50}\n"

        for i in sorted(self.groups.keys()):
            self.pri_grp_str += f"{i:5d}:\n"   # Prints group number
            for j in self.groups[i]:
                self.pri_grp_str += f"\t\t    {int(j,2):<20d}{j:<20}\n" # Prints minterm and its binary representation
            self.pri_grp_str += f"{'-'*50}\n"
        #Primary group printing ends
        
        self.all_pi, self.all_pi_str = self.find_PI(self.groups)
        
        self.chart, self.chart_str = self.chart_PI(self.minterm, self.dontcare, self.all_pi)



    def mul(self,x,y): # Multiply 2 minterms
        res = []
        for i in x:
            if i+"'" in y or (len(i)==2 and i[0] in y):
                return []
            else:
                res.append(i)
        for i in y:
            if i not in res:
                res.append(i)
        return res

    def multiply(self,x,y): # Multiply 2 expressions
        res = []
        for i in x:
            for j in y:
                tmp = self.mul(i,j)
                res.append(tmp) if len(tmp) != 0 else None
        return res

    def refine(self,my_list,dc_list): # Removes don't care terms from a given list and returns refined list
        res = []
        for i in my_list:
            if int(i) not in dc_list:
                res.append(i)
        return res

    def findEPI(self,x): # Function to find essential prime implicants from prime implicants chart
        res = []
        for i in x:
            if len(x[i]) == 1:
                res.append(x[i][0]) if x[i][0] not in res else None
        return res

    def findVariables(self,x): # Function to find variables in a meanterm. For example, the minterm --01 has C' and D as variables
        var_list = []
        for i in range(len(x)):
            if x[i] == '0':
                var_list.append(chr(i+65)+"'")
            elif x[i] == '1':
                var_list.append(chr(i+65))
        return var_list

    def flatten(self,x): # Flattens a list
        flattened_items = []
        for i in x:
            flattened_items.extend(x[i])
        return flattened_items

    def findminterms(self,a): #Function for finding out which minterms are merged. For example, 10-1 is obtained by merging 9(1001) and 11(1011)
        gaps = a.count('-')
        if gaps == 0:
            return [str(int(a,2))]
        x = [bin(i)[2:].zfill(gaps) for i in range(pow(2,gaps))]
        temp = []
        for i in range(pow(2,gaps)):
            temp2,ind = a[:],-1
            for j in x[0]:
                if ind != -1:
                    ind = ind+temp2[ind+1:].find('-')+1
                else:
                    ind = temp2[ind+1:].find('-')
                temp2 = temp2[:ind]+j+temp2[ind+1:]
            temp.append(str(int(temp2,2)))
            x.pop(0)
        return temp

    def compare(self,a,b): # Function for checking if 2 minterms differ by 1 bit only
        c = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                mismatch_index = i
                c += 1
                if c>1:
                    return (False,None)
        return (True,mismatch_index)

    def removeTerms(self,_chart,terms): # Removes minterms which are already covered from chart
        for i in terms:
            for j in self.findminterms(i):
                try:
                    del _chart[j]
                except KeyError:
                    pass
                

    def find_PI(self, groups):  
        # Process for creating tables and finding prime implicants starts
        all_pi = set()
        all_pi_str =""
        while True:
            tmp = groups.copy()
            groups,m,marked,should_stop = {},0,set(),True
            l = sorted(list(tmp.keys()))
            for i in range(len(l)-1):
                for j in tmp[l[i]]: # Loop which iterates through current group elements
                    for k in tmp[l[i+1]]: # Loop which iterates through next group elements
                        res = self.compare(j,k) # Compare the minterms
                        if res[0]: # If the minterms differ by 1 bit only
                            try:
                                groups[m].append(j[:res[1]]+'-'+j[res[1]+1:]) if j[:res[1]]+'-'+j[res[1]+1:] not in groups[m] else None # Put a '-' in the changing bit and add it to corresponding group
                            except KeyError:
                                groups[m] = [j[:res[1]]+'-'+j[res[1]+1:]] # If the group doesn't exist, create the group at first and then put a '-' in the changing bit and add it to the newly created group
                            should_stop = False
                            marked.add(j) # Mark element j
                            marked.add(k) # Mark element k
                m += 1
            local_unmarked = set(self.flatten(tmp)).difference(marked) # Unmarked elements of each table
            all_pi = all_pi.union(local_unmarked) # Adding Prime Implicants to global list
            all_pi_str += f"Unmarked elements(Prime Implicants) of this table: "

            #all_pi_str += f"{None}\n" if len(local_unmarked)==0 else f"{', '.join(local_unmarked)}\n" # Printing Prime Implicants of current table

            if len(local_unmarked)==0:
                all_pi_str += f"{None}\n"
            else:
                all_pi_str += f"{', '.join(local_unmarked)}\n"

            if should_stop: # If the minterms cannot be combined further
                all_pi_str += f"\n\nAll Prime Implicants: "

                #all_pi_str += f"{None}\n" if len(all_pi)==0 else f"{', '.join(all_pi)}\n" # Print all prime implicants

                if len(all_pi)==0:
                    all_pi_str += f"{None}\n"
                else:
                    all_pi_str += f"{', '.join(all_pi)}\n"

                break
            # Printing of all the next groups starts
            all_pi_str += f"\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n{'='*50}\n"
            for i in sorted(groups.keys()):
                all_pi_str += f"{i:5d}:\n" # Prints group number
                for j in groups[i]:
                    all_pi_str += f"\t\t{','.join(self.findminterms(j)):<24}{j:<24}\n" # Prints minterms and its binary representation
                all_pi_str += f"{'-'*50}\n"
            # Printing of all the next groups ends
        # Process for creating tables and finding prime implicants ends
        #print(all_pi_str)
        return all_pi, all_pi_str

    def chart_PI(self, mt, dc, all_pi):     
        chart = {}
        try:
            # Printing and processing of Prime Implicant chart starts
            sz = len(str(mt[-1])) # The number of digits of the largest minterm
            chart_str = f"\n\n\nPrime Implicants chart:\n\n    Minterms    |{' '.join((' '*(sz-len(str(i))))+str(i) for i in mt)}\n{'='*(len(mt)*(sz+1)+16)}\n"
            for i in all_pi:
                merged_minterms,y = self.findminterms(i),0
                chart_str += f"{','.join(merged_minterms):<16}|"
                for j in self.refine(merged_minterms,dc):
                    x = mt.index(int(j))*(sz+1) # The position where we should put 'X'
                    chart_str += f"{' '*abs(x-y)}{' '*(sz-1)}{'X'}"
                    y = x+sz
                    try:
                        chart[j].append(i) if i not in chart[j] else None # Add minterm in chart
                    except KeyError:
                        chart[j] = [i]
                chart_str += f"\n{'-'*(len(mt)*(sz+1)+16)}\n"
            # Printing and processing of Prime Implicant chart ends
            #print(chart_str)
        except:
            pass
        chart_str += "\n"
        return chart, chart_str
       