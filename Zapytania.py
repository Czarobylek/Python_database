from Model import Department, AppUser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:PostgersSQL123@localhost/Company_2', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

def findAllUsers(session):
    users = session.query(AppUser).all()
    return users

def findUsersWithPaymentHigher(session, payment):
    users = session.query(AppUser).filter(AppUser.payment > payment)
    return users

def findUsersFromDepartment(session, department):
    users = session.query(AppUser).filter(AppUser.fk_department == department)
    return users

def findUser(session, firstName, lastName, departmentName):
    users = session.query(AppUser).filter(AppUser.fk_department == departmentName, AppUser.firstName == firstName, AppUser.lastName == lastName)
    return users

def findAllDepartments(session):
    departments = session.query(Department).all()
    return departments

def findDepartmentMenagedByUser(session, firstName, lastName):
    u = session.query(AppUser).filter(AppUser.firstName == firstName, AppUser.lastName == lastName)
    user = list(u)
    department = session.query(Department).filter(Department.fk_manager == user[0].userName)
    return [department, user[0]]

def findDepartmentWithMaxNumberOfEmployes(session):
    employesNumber = []
    d = findAllDepartments(session)
    departments = list(d)
    for department in departments:
        u = session.query(AppUser).filter(AppUser.fk_department == department.Name)
        users = list(u)
        depEmployes = len(users)
        employesNumber.append(depEmployes)
        if depEmployes == max(employesNumber):
            maxDepartment = department.Name
    return max(employesNumber), maxDepartment

def findDepartmentWithMaxSalary(session):
    payments = []
    d = findAllDepartments(session)
    departments = list(d)
    for department in departments:
        depPayment = 0
        users = session.query(AppUser).filter(AppUser.fk_department == department.Name)
        for user in users:
            depPayment = depPayment + user.payment + user.bonus
        payments.append(depPayment)
        if depPayment == max(payments):
            maxDepartment = department.Name
    return max(payments), maxDepartment


i=0
while (i == 0):
    print("Polecenia:\n1 - Znajdź wszystkich użytkowników\n2 - Znajdź użytkowników o wypłacie większej niż X")
    print("3 - Znajdź użytkowników z działu X\n4 - Znajdź użytkownika o imieniu X, nazwisku Y z działu Z")
    print("5 - Znajdź wszystkie departamenty\n6 - Znajdź departament managera o imieniu X i nazwisku Y")
    print("7 - Znajdź departament z największą liczbą użytkowników\n6 - Znajdź departament z największą sumą wypłat")
    komenda = input("Wprowadź polecenie: ")
    if komenda == "1":
        for user in findAllUsers(session):
            print ("%s : %s : %s : %s : %s : %s : %s : %s : %s" %(user.userName, user.password, user.firstName,
            user.lastName, user.description, str(user.payment), str(user.bonus), str(user.dateOfPayment),
            user.fk_department))
        i = 0
    elif komenda == "2":
        payment = int(input("Kwota: "))
        for user in findUsersWithPaymentHigher(session, payment):
            print ("%s : %s" %(user.userName, str(user.payment)))
        i = 0
    elif komenda == "3":
        department = input("Dział: ")
        for user in findUsersFromDepartment(session, department):
            print ("%s : %s" %(user.userName, str(user.fk_department)))
        i = 0
    elif komenda == "4":
        department = input("Dział: ")
        firstName = input("Imię: ")
        lastName = input("Nazwisko: ")
        for user in findUser(session, firstName, lastName, department):
            print ("%s : %s : %s : %s" %(user.userName, user.firstName, user.lastName, user.fk_department))
        i = 0
    elif komenda == "5":
        for department in findAllDepartments(session):
            print ("%s : %s : %s : %s : %s : %s : %s" %(department.Name, department.address, department.phone,
            department.email, department.WWW, department.description, department.fk_manager))
        i = 0
    elif komenda == "6":
        firstName = input("Imię: ")
        lastName = input("Nazwisko: ")
        department, user = findDepartmentMenagedByUser(session, firstName, lastName)
        for d in department:
            print ("%s : %s : %s" %(d.Name, user.firstName, user.lastName))
        i = 0
    elif komenda == "7":
        employesNumber, maxDepartment = findDepartmentWithMaxNumberOfEmployes(session)
        print("%s : %s" %(maxDepartment, employesNumber))
        i = 0
    elif komenda == "8":
        payments, maxDepartment = findDepartmentWithMaxSalary(session)
        print("%s : %s" %(maxDepartment, payments))
        i = 0
    elif komenda == "10":
        i = 1
    else:
        print ("Błędne polecenie. Podaj poprawne.")
        i = 0
