chars = ["=", "+", "%", "/", "*", ";", "(", ")", "{", "}", ">", "<"]

def read_file(file_name):
    file=open("C:\\Users\\Kostya\\Desktop\\ITMO\\ITMO_5sem\\APC\\lab3\\language.txt", "r")    
    res=[]
    for s in file:
        x=s
        for t in chars:
            x=x.replace(t," " + t + " ")
        y=x.split()
        
        res+=y
        # for i in y:
        #     res.append(i)
        
    return res
def make_err_sym_not_found(a):
    return "Error: symbol not found(" + a +")"
def make_compare(a, b, sym):
    res=[]
    x=sym[a]
    try:
        x = int(a)
        res.append("ldi " + str(x)) #добавить в машинный
    except:
        try:
            x = sym[a]
            res.append("lda " + str(x[0]))
        except:
            res.append(make_err_sym_not_found(a))
    try:
        x = int(b)
        res.append("subi " + str(x))
    except:
        try:
            x = sym[b]
            res.append("sub " + str(x[0]))
        except:
            res.append(make_err_sym_not_found(b))
    return res

def make_assign(a,b,sym):
    try:
        x = int(b)
        res.append("ldi " + str(x))
    except:
        try: 
            x = sym[b]
            res.append("lda " + str(x[0]))
        except:
            res.append(make_err_sym_not_found(b))    
    try:
        y=sym[a]
        res.append("sta " + str(x[0]))
    except:
        res.append(make_err_sym_not_found(a))
    return res
    
def make_add(a, b, sym):
    try:
        x = int(a)
        res.append("ldi " + str(x)) #добавить в машинный
    except:
        try:
            x = sym[a]
            res.append("lda " + str(x[0]))
        except:
            res.append(make_err_sym_not_found(a))
    try:
        x = int(b)
        res.append("addi " + str(x))
    except:
        try:
            x = sym[b]
            res.append("add " + str(x[0]))
        except:
            res.append(make_err_sym_not_found(b))
    return res
        

def translator(list_com, code_start, data_start):
    res=[]
    sym={} # ключь-имя; Значение-[адресс, тип]
    current_type=0
    data_addr=data_start
    code_addr=code_start
    labels={}
    list_com.append("#")
    list_com.append("#")
    list_com.insert(0, "#")
    list_com.insert(0, "#")
    
    for i in range(2, len(list_com)-2):
        t=list_com[i]
        t1=list_com[i+1]
        t2=list_com[i+2]
        tm1=list_com[i-1]
        
        if t=="int":
            current_type=1
            continue #todo
        elif t == "string":
            current_type=2
            continue
        elif t==";":
            continue #todo
        elif t=="=":
            if t1=="=": #сравнение
                res += make_compare(tm1, t2, sym)
            else:
                res+=make_assign(tm1, t2, sym)       
        elif t=="+":
            if t1=="=":
                res+=make_add(tm1, t2,sym)
        # ............................................
        else:
            sym[t]=[data_addr, current_type]
            data_addr+=1
            
    
res=read_file("language.txt")
print(res)
translator(res)