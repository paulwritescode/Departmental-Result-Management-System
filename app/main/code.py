
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


day3()









