# alg | acc | neum | mc | tick | struct | stream | mem | pstr | prob5 | 8bit
acc=0
dr=0
zf=0
cf=0
sf=0
mem=['0']*1024
input=['1','2','3','4','5']
const=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17']
output=[]

test_prg = ['lda 1023', 'add 1023', 'sta 100', 'mul 5', 'sta 1023', 'div 1023', 'sub 1023', 'shl 1023', 'shr 1023', 'hlt']
# test_prg = [['lda', 1023], ['add', 1023], ['sta', 100], ['mul', 5], ['sta', 1023],['div', 1023], ['sub', 1023], ['shl', 1023], ['shr', 1023]]
io_port=1023

def ld(addr):
    global input
    if addr == io_port:
        if len(input) == 0:
            return False, 0
        mem[addr] = input[0]
        input = input[1:]
    return True, mem[addr]

def ld_num(addr):
    a,b=ld(addr)
    return a, int(b)

def st(addr, val):
    mem[addr]=val

def st_num(addr, val):
    st(addr, str(val))
    

def run(org):
    running=True
    ip=org
    while running == True:
        res, c=ld(ip)
        ip+=1
        if len(c) == 0:
            continue 
        t=c.split(" ")
        cmd=t[0] 
        if len(t)>1:
            arg=int(t[1])
        else:
            arg=0

        if cmd == 'lda':
            
            res, acc = ld_num(arg)
            if (res == False):
                return
            
        elif cmd == 'ldi':
            acc=arg
        elif cmd == 'ldax':
            res, dr=ld_num(arg)
            res, acc=ld_num(dr)
        
        elif cmd == 'stax':
            res, dr = ld_num(arg)
            st_num(dr, acc)
            
        elif cmd == 'sta':
            st_num(arg, acc)
            if arg == io_port:
                output.append(mem[arg])
        elif cmd =='add':
            res, dr = ld_num(arg)
            if (res == False):
                return
            acc+=dr
        elif cmd=='addi':
            dr=arg
            acc=acc+dr
            
        elif cmd == 'sub':
            res, dr = ld_num(arg)
            if (res == False):
                return
            acc=acc-dr
            if acc==0:
                zf=1
                sf=0
                cf=0
            elif acc<0:
                zf=0
                sf=1
                cf=0
            else:
                zf=0
                sf=0
                cf=0
        elif cmd == 'subi':
            dr=arg
            acc=acc-dr
            if acc==0:
                zf=1
                sf=0
                cf=0
            elif acc<0:
                zf=0
                sf=1
                cf=0
            else:
                zf=0
                sf=0
                cf=0
                
        elif cmd == 'mul':
            res, dr = ld_num(arg)
            if(res==False):
                return
            acc*=dr
        elif cmd == 'div':
            res, dr = ld_num(arg)
            if(res==False):
                return
            acc=acc/dr
        
        elif cmd == 'divi':
            dr=arg
            acc=acc/dr
        elif cmd == 'mod':
            res, dr = ld_num(arg)
            if(res==False):
                return
            acc=acc%dr
        elif cmd == 'modi':
            dr=arg
            acc=acc%dr
        elif cmd == 'mul':
            res, dr = ld_num(arg)
            if(res==False):
                return
            acc=acc*dr
        elif cmd == 'muli':
            dr=arg
            acc=acc*dr
        elif cmd == "ldi":
            res, dr = ld_num(arg)
            if(res == False):
                return
            acc=dr

        elif cmd == "jmp":
            ip=arg
        elif cmd == "jz":
            if zf>0:
                ip=arg
        elif cmd == "js":
            if sf>0:
                ip=arg
        elif cmd=="jns":
            if sf==0:
                ip=arg
        elif cmd=="jsz":
            if sf>0 or zf>0:
                ip=arg
        
            
        elif cmd == "hlt":
            running = False
            
def load(prg, org):
    for p in prg:
        st(org, p)
        org+=1


load(test_prg, 100)
load(const, 0)
run(100)
print(output)
            