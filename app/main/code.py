
def solution(P, S):
    total_pass = sum(P)
    res = 0
    S.sort(reverse=True)
    for i in S:
        if total_pass - i > 0:
            total_pass = total_pass - i
            res += 1
        else:
            res += 1
            return res
# Example 1
P = [1, 4, 1]
S = [1, 5, 1]
print(solution(P, S))  # Output: 2

# Example 2
P = [4, 4, 2, 4]
S = [5, 5, 2, 5]
print(solution(P, S))  # Output: 3
def day1():
    age=28
    print(f"my age is {age}")
    daysinaweek=7
    weeksinayear=54
    hoursinaday=24

    print(f"type is {type(daysinaweek*weeksinayear*hoursinaday)} and total number is{daysinaweek*hoursinaday*weeksinayear}")

    raddius=4
    print(f"the area is{raddius*raddius*22/7}")
    name='Simon'
    print(f"my name is {name}")

    # python keywords 
    # def if break return while else........
    # variable naming in python cant start with a number or a hyphen
        # thus one can start with a letter or an underscore er consider using underscore for readability
    # input functon to get user input
    age=input('what is your age ?')
    print(age)

def day2():

    suggestedloanamount=int(input("How much do you want to borrow? "))
    Period=float(input("Amount of time you will pay after (Years) you may decimals"))
    Interest=23/100
    Repayableamount=(suggestedloanamount+(suggestedloanamount*Interest*Period))
    print(Repayableamount,(suggestedloanamount*Interest*Period))

    radius=float(input('Enter the radius of your circle'))
    Area=22/7*(radius*radius)
    print ('the area of your circle is, ',Area,'.')
    print('the circumference of your circle is ,',(2*22/7*radius),'.')

    Rateperhour=float(input('Enter the salary of your employee per hour'))
    weeklysalary=Rateperhour*8*5
    Monthlysalary=weeklysalary*4
    yearlysalary=Monthlysalary*12
    print('the salary of the developer per week is',weeklysalary, ',','per month',Monthlysalary, 'and per yearis ',yearlysalary,"." )



def day3():
    # string concantenation and type conversion
    hello="Hello "
    name=input("What is your name? ")
    sentence=". Welcome to python coding. "
    sentence2="Your salary is "
    salary=120000
    age=input("Enter your age?")
    agesentence="Your age is "
   
    Yearborn=2024-int(age)
    we=()
    we=1
    i=we,3,3,6,8
    output="I am {} ,I work at {} and I am {} years old"
    company="jitu"
    hobby1="watching"
    hobby2="Computer Gaming"
    print(type(i))
    yearsentence=". You were born in the year "+str(Yearborn)+str(i)
    print(hello+name+sentence+sentence2,salary)
    print(agesentence+age+yearsentence)
    print("You are {} and you are {} years old".format(name.lower(),age))
    print(output.format(name.upper(),company.title(),age))
    print(f"My name is {name.capitalize()}, born in and my hobbies are {hobby1} and {hobby2}")


# day3()



def day4():

    # LISTS OR ARRAYS IN PYTHON
    names=['Simon',"Ann","Alison","TEST"]
    Movies=['Rick and Morty','Inside Job','Originals']
    name=input("Enete your name")
    names= names + [name]

    movie=input("enter your favourite movie")
    Movies.append(movie)
    print(Movies)
    numbers=[1,2,4,5,6]
    numbers.insert(2,3)
    print(numbers)
    print(names)
    names.remove(name)
    print(names)
    del numbers[5]
    print(numbers)

    names.pop()
    print(names)
    numbers.pop(4)
    print(numbers)

    names.clear()
    print(names)
    names.append(input("ENTER A NAME "))
    print(names)



    # TUPLES IN PYTHON
    names1=('Simon','JAmes','ANN',"DUALITY")
    # Immutable and non immutable data types
    # what the above means is that there exists data such that ince saved they cant be edited  only read
    # the following will not work  
    # { 
   
    # names2="PAULINE"}
    # names1=names1+(names2)
    numbers=(1,2,3,4,1,2,4,6,7,8,9,1,1,4)
    print(numbers.count(1))
    print(numbers.index(3))
    print(names1)
    Loans=[
        ("Simon","Muriiithi",20000,3-18-2024),
        ("ANN","Wanja",10000,31-1-2344)
    ]
    print(Loans[0][0])
    movy=[("Originals","Julie Plec",2013,35000000)]
    print(movy)
    movy.append((input("Title"),input("Director"),input("release_year"),input("Budget")))
    print(movy)
    movy.pop(0)
    print(movy)

# day4()
    
def day5():
    # Boolen values

    a=5
    b=6
    if a<b:
        print(a> b)

    # i.e an empty list ,an empty tuple empty string and integer 0 returns a False where checked for boolean
    print(bool(0))
    list=[]
    print(bool(list))
    name=""
    print(bool(name))
    print(bool(1))

    # i,e
    name1="Simon"
    if a>b:
        print(bool(name1))
    else:
        print(bool(name))

    age=(int(input("Enter age in numerals")))
    if 18<age<60:
        print("You ara ana Adult.")
    elif 18<age>60 and age<100:
        print("You are a Veteran.")
    elif age>18 and age>99 :
        print("Prove you are not a robot.")
    
    else:
        print("You are still a Minor.")
    name=input("Enter your name")
    if name:
        print("Hello ",name)
    else:
        print("Didn't get your name")


    

day5()











