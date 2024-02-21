import re
chars = ["=", "+", "-", "%", "/", "*", ";", "(", ")", "{", "}", ">", "<"]
sym={} # ключь-имя; Значение-[адресс, тип]
mem=['']*1024
data_addr=0
code_addr=100
str_const=[]

def read_file(file_name):
    file=open(file_name, "r")    
    res=[]
    for s in file:
        x=s
        for t in chars:
            x=x.replace(t," " + t + " ")
        y=my_split(x)
        
        res+=y
        # for i in y:
        #     res.append(i)
        
    return res
#Написать свой сплит, чтобы пробелы в ковычках не удалялись
def my_split(line):
    data=[]
    res=re.findall(r'(".+?"|[^ ]+)', line)
    data.extend(res)
    if '\n' in data:
        data.remove("\n")
    return data
    
def make_err_sym_not_found(a):
    return "Error: symbol not found(" + a +")"
def make_compare(a, b): # tm1, t2
    res=[]
    x=0
    try:
        x = int(a)
        res.append("ldi " + str(x)) 
    except:
        try:
            x = sym[a]
            res.append("lda " + str(x[0]))
        except:
            res.append(make_err_sym_not_found(a))
    try:
        y = int(b)
        res.append("subi " + str(y))
    except:
        try:
            y = sym[b]
            res.append("sub " + str(y[0]))
        except:
            res.append(make_err_sym_not_found(b))
    return res

def make_assign(a,b):
    res=[]
    x=0
    try:
        x = int(b)
        res.append("ldi " + str(x))
    except:
        try: 
            x = sym[b]
            res.append("lda " + str(x[0]))
        except:
            if b[0]=="\"":
                res+=make_str_const(b)
            else:
                res.append(make_err_sym_not_found(b))    
    try:
        y=sym[a]
        res.append("sta " + str(y[0]))
    except:
        res.append(make_err_sym_not_found(a))
    return res

def make_assign1(a):
    res=[] 
    try:
        y=sym[a]
        res.append("sta " + str(y[0]))
    except:
        res.append(make_err_sym_not_found(a))
    return res
    
def make_add(a, b):
    res=[]
    x=sym[a]
    try:
        x = int(a)
        res.append("ldi " + str(x))
    except:
        try:
            x = sym[a]
            res.append("lda " + str(x[0]))
        except:
            res.append(make_err_sym_not_found(a))
    try:
        y = int(b)
        res.append("addi " + str(y))
    except:
        try:
            y = sym[b]
            res.append("add " + str(y[0]))
        except:
            res.append(make_err_sym_not_found(b))
    return res

def make_sub(a,b):
    res=[]
    x=0
    try:
        x = int(a)
        res.append("ldi " + str(x)) 
    except:
        try:
            x = sym[a]
            res.append("lda " + str(x[0]))
        except:
            res.append(make_err_sym_not_found(a))
    try:
        y = int(b)
        res.append("subi " + str(y))
    except:
        try:
            y = sym[b]
            res.append("sub " + str(y[0]))
        except:
            res.append(make_err_sym_not_found(b))
    return res

def make_div(a,b):
    res=[]
    x=sym[a]
    try:
        x = int(a)
        res.append("ldi " + str(x)) 
    except:
        try:
            x = sym[a]
            res.append("lda " + str(x[0]))
        except:
            res.append(make_err_sym_not_found(a))
    try:
        y = int(b)
        res.append("divi " + str(y))
    except:
        try:
            y = sym[b]
            res.append("div " + str(y[0]))
        except:
            res.append(make_err_sym_not_found(b))
    return res
def make_mod(a,b):
    res=[]
    x=0
    try:
        x = int(a)
        res.append("ldi " + str(x)) 
    except:
        try:
            x = sym[a]
            res.append("lda " + str(x[0]))
        except:
            res.append(make_err_sym_not_found(a))
    try:
        y = int(b)
        res.append("modi " + str(y))
    except:
        try:
            y = sym[b]
            res.append("mod " + str(y[0]))
        except:
            res.append(make_err_sym_not_found(b))
    return res
def make_mul(a,b):
    res=[]
    x=0
    try:
        x = int(a)
        res.append("ldi " + str(x)) 
    except:
        try:
            x = sym[a]
            res.append("lda " + str(x[0]))
        except:
            res.append(make_err_sym_not_found(a))
    try:
        y = int(b)
        res.append("muli " + str(y))
    except:
        try:
            y = sym[b]
            res.append("mul " + str(y[0]))
        except:
            res.append(make_err_sym_not_found(b))
    return res
def make_const(t):
    res=["ldi "+ t]
    return res

def is_op(token):
    if chars.count(token)>0:
        return True
    else:
        return False

def make_str_const(t):
    global data_addr
    n=0
    p=data_addr+1
    for i in range(1, len(t)-1):
        mem[p]=t[i]
        p+=1
        n+=1
    mem[data_addr]=n
    str_const.append([data_addr, n])
    res=["ldi "+str(data_addr)]
    data_addr=p
    return res
    
def make_var(t):
    x=sym[t][0]
    res=["lda "+ str(x)]
    return res
# def make_print(a, b,sym):
def find_token(list_com, start, tok):
    i=start
    while i<len(list_com):
        if list_com[i]==tok:
            return i
        i+=1
    return -1
    
    

def translator(list_com):
    global data_addr
    res=[]
    current_type=0
    labels={}
    list_com.append("#")
    list_com.append("#")
    list_com.insert(0, "#")
    list_com.insert(0, "#")
    if_flag=False
    
    i=2
    while i<(len(list_com)-2):
        print("start while:", i)
        t=list_com[i]
        t1=list_com[i+1]
        t2=list_com[i+2]
        tm1=list_com[i-1]
        print("2:",tm1, t, t1, t2)
        j=0
        if t.isnumeric():
            res+=make_const(t)
        elif t[0]=="\"":
            res+=make_str_const(t)
        elif t=="int":
            current_type=1
        elif t == "str":
            current_type=2
            
        elif t==";":
            current_type=0
        elif t=="=":
            if t1=="=": #сравнение
                res += make_compare(tm1, t2)
            else:
                if t2==";" or t2=="#":
                    res+=make_assign(tm1, t1)   
                else:
                    k=find_token(list_com, i+1, ";")
                    print("TRANS1:", list_com[i+1:k+1])
                    res+=translator(list_com[i+1:k+1])
                    
                    res+=make_assign1(tm1)        
            
            current_type=0   
        elif t=="+":
            if t1=="=":
                res+=make_add(tm1, t2)
            else:
                res+=make_add(tm1, t1)
            current_type=0
            
        elif t=="-":
            if t1=="=":
                res+=make_sub(tm1, t2)
            else:
                res+=make_sub(tm1, t1)
            current_type=0
        elif t=="/":
            if t1=="=":
                res+=make_div(tm1, t2)
            else:
                res+=make_div(tm1, t1)
            current_type=0
        elif t=="%":
            if t1=="=":
                res+=make_mod(tm1, t2)
            else:
                res+=make_mod(tm1, t1)
            current_type=0
        elif t=="*":
            if t1=="=":
                
                res+=make_mul(tm1, t2)
            else:
                print("MUL: ", res)
                res+=make_mul(tm1, t1)
                print("MUL2: ", res)
            current_type=0
        elif t=="(":
            j=i+1
            k=1
            while k>0:
                u=list_com[j]
                if u=="(":
                    k+=1
                elif u==")":
                    k-=1
                j+=1
                if j>=len(list_com):
                    break
            sub_list_com = list_com[i + 1:j-1]    
            i-j
            res += translator(sub_list_com)
            current_type=0
        elif t=="{":
            j=i+1
            k=1
            while k>0:
                u=list_com[j]
                if u=="{":
                    k+=1
                elif u=="}":
                    k-=1
                j+=1
                if j>=len(list_com):
                    break
            sub_list_com = list_com[i + 1:j-1]    
            z=translator(sub_list_com)
            if if_flag:
                res += ["subi 0"]
                res+="jz " + str(code_addr + len(z))
                if_flag = False
            i-j
            res +=z 
            current_type=0
        elif t=="while":
            current_type=0
        elif t=="if":
            if_flag=True
            current_type=0
            # ()
            # {}
            
            # continue #должен быть if   
        # elif t=="print":
        #     # 
        #     if t1!="(":
        #         res+=make_print1(t1)
        #     else:
                 
        #         res+=make_print()
        
        # ............................................
        else:
            if t in sym:
                if is_op(t1)==False:
                    res += make_var(t) # Тут и происходит "дополнительный" lda 0 перед умножением
                    # написать функцию is_op, которая определяет является ли t1 арифметической операцией и если справа не операция, то только тогда делать make_var
                
                current_type=sym[t][1]
            else:
                sym[t]=[data_addr, current_type]
                data_addr+=1
                print("qwerty:", i)
            # current_type=0
                
        if current_type==0:        
            print("aboba1:", i)

            i=find_token(list_com, i+1, ";")+1
            print("aboba:", i)
            if i==0:
                break
        else:
            i+=1
    return res    
            
            
    
input=read_file("C:\\Users\\Kostya\\Desktop\\ITMO\\ITMO_5sem\\APC\\lab3\\test2.txt")
print(input)
print("######################")
print(translator(input))
print("end")
print(sym)


# Проверить корректность операций
# строковые константы валяются в памяти данных и не заносятся в словарь символов. Надо ли это менять?
