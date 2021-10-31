import mysql.connector
from mysql.connector import Error

## Funciton to get active members
def getActiveMembers_home(DBHandler):
    retVal = {}
    
    vSQLQuery = "select memberid,concat(memberfirstname,' ',memberlastname) from members where membershipstatus=1"
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    for v_rec in DBHandler.cursor:
        retVal[v_rec[0]] = v_rec[1]
  
    print(type(retVal))
    print(retVal)
    return retVal

## Get Member details
def getMemberDetail(DBHandler, memberid):
    vSQLQuery = "select concat(memberfirstname,' ',memberlastname), adminaccess, memberid, clubname from members m,clubs c where c.clubid = m.clubid and memberid='" + memberid +"'"
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    """ for v_rec in DBHandler.cursor:
        retVal = v_rec[1] """
    retVal = DBHandler.cursor.fetchone()
    print(type(retVal))
    print(retVal)
    return retVal

## Get the club news
def getClubNews(DBHandler, memberid):
    noofRecords = 3
    vSQLQuery = "select c.newsheader, c.news, c.newsdate, c.newsbyline from members m,clubnews c "
    vSQLQuery += "where m.clubid = c.clubid and m.memberid=" + memberid 
    vSQLQuery += " order by c.newsdate desc limit " + str(noofRecords)
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    """ for v_rec in DBHandler.cursor:
        retVal = v_rec[1] """
    retVal = DBHandler.cursor.fetchall()
    print(type(retVal))
    print(retVal)
    return retVal

## Get the member contact details
def getMemberContactDetail(DBHandler, memberid):
    vSQLQuery = "select MemberID, c.clubname, teamid,MemberFirstName,MemberLastName, Address1, Address2, City, "
    vSQLQuery += "m.Email, Phone, Birthdate from members m ,clubs c "
    vSQLQuery += "where  m.clubid = c.clubid and m.memberid=" + memberid
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    retVal = DBHandler.cursor.fetchone()
    return retVal

## Get the member team name
def getMemberTeamName(DBHandler, p_teamid):
    v_teamname = ""
    vSQLQuery = "select teamname from teams where teamid =" + str(p_teamid)
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    for v_rec in DBHandler.cursor:
        v_teamname = v_rec[0]
    return v_teamname

## this will update the member conctact detail
def updateMemberContact(DBHandler, memberid, p_firstname, p_lastname,p_add1, p_add2, p_city,p_email,p_phone, p_dob):
    vSQLQuery = "UPDATE members SET "
    vSQLQuery += "MemberFirstName='"+ p_firstname +"', "
    vSQLQuery += "MemberLastName='"+ p_lastname +"', "
    vSQLQuery += "Address1='"+ p_add1 +"', "
    vSQLQuery += "Address2='"+ p_add2 +"', "
    vSQLQuery += "City='"+ p_city +"', "
    vSQLQuery += "Email='"+ p_email +"', "
    vSQLQuery += "Phone='"+ p_phone +"', "
    vSQLQuery += "Birthdate='"+ p_dob +"' where memberid=" + memberid

    DBHandler.cursor.execute(vSQLQuery)
    DBHandler.DBcon.commit()
    print(DBHandler.cursor.rowcount, "record(s) affected")

## get the team fixtures
def getTeamFixtures(DBHandler, p_teamid):
    vSQLQuery = "select FixtureDate, "
    vSQLQuery+= "hometeam, "
    vSQLQuery+= "(select teamname from teams where teamid = f.hometeam) hteamname, "
    vSQLQuery+= "homescore, "
    vSQLQuery+= "awayteam,  "
    vSQLQuery+= "(select teamname from teams where teamid = f.awayteam) ateamname, "
    vSQLQuery+= "awayscore "
    vSQLQuery+= "from fixtures f where " + str(p_teamid) + " in (f.hometeam, f.awayteam)"
    DBHandler.cursor.execute(vSQLQuery)
    retVal = DBHandler.cursor.fetchall()
    return retVal

################################################ ADMIN MEMBER FUNCTIONS #################################################
### This fuction an be used to get the maximum id for any table. This will be used to autogenerate the ID when doing the insert on any table
def getNextID(DBHandler, p_tablename, p_fieldname_pk):
    vSQLQuery = "select max(" + p_fieldname_pk + ")  + 1 from " + p_tablename
    DBHandler.cursor.execute(vSQLQuery)
    for v_rec in DBHandler.cursor:
            retVal = v_rec[0]
    return retVal

## Get the club details. if club id is given, will give one club with id, else will return all the clubs
def getClubDetails(DBHandler, p_club_id=0):
    retVal ={}
    if p_club_id == 0: 
        vSQLQuery = "select clubid,clubname from clubs"
    else:
        vSQLQuery = "select clubid,clubname from clubs where clubid="+str(p_club_id)
    try:
        print(vSQLQuery)
        DBHandler.cursor.execute(vSQLQuery)
        for v_rec in DBHandler.cursor:
            retVal[v_rec[0]] = v_rec[1]
        return retVal
    except Error as e:
        print("Error while getting club details", e)
        v_err = "Failed to find clubs: " + str(e)
        return v_err

## Get the team names. if team id is given, will return that team name, else give all the teams
def getTeamsDetails(DBHandler, p_team_id=0):
    retVal={}
    if p_team_id == 0: 
        vSQLQuery = "select teamid,teamname from teams"
    else:
        vSQLQuery = "select teamid,teamname from teams where teamid="+str(p_team_id)
    try:
        print(vSQLQuery)
        DBHandler.cursor.execute(vSQLQuery)
        for v_rec in DBHandler.cursor:
            retVal[v_rec[0]] = v_rec[1]
        return retVal
    except Error as e:
        print("Error while getting team details", e)
        v_err = "Failed to find teams: " + str(e)
        return v_err
## Get member details. if ONE is given then member id is compulsory, otherwise ALL will return all the members
def getMemberDetails(DBHandler,p_memberid, p_fetch_all):
    v_err = ""
    if p_fetch_all == "ONE":
        vSQLQuery = "select MemberID,ClubID, TeamID, MemberFirstName, MemberLastName, Address1, Address2, City, Email, Phone, "
        vSQLQuery += "Birthdate, MembershipStatus, AdminAccess from members where memberid = " + str(p_memberid)   
    elif p_fetch_all == "ALL":
        vSQLQuery = "select MemberID,ClubID, TeamID, MemberFirstName, MemberLastName, Address1, Address2, City, Email, Phone, "
        vSQLQuery += "Birthdate, MembershipStatus, AdminAccess from members"
    print(vSQLQuery)
    try:
        DBHandler.cursor.execute(vSQLQuery)
        if  p_fetch_all == "ONE":
           retVal = DBHandler.cursor.fetchone()
        elif p_fetch_all == "ALL":
            retVal = DBHandler.cursor.fetchall()
        return retVal
    except Error as e:
            print("Error while execution", e)
            v_err = "Failed to find member: " + str(e)
            return v_err

## Save the member details in database (this will be used to add new member or to update the existing member)
def saveMemberDetails(DBHandler,
                    p_memberid,
                    p_ClubID,
                    p_TeamID,
                    p_MemberFirstName, 
                    p_MemberLastName, 
                    p_Address1, 
                    p_Address2, 
                    p_City, 
                    p_Email, 
                    p_Phone, 
                    p_Birthdate, 
                    p_MembershipStatus, 
                    p_AdminAccess):
    vSQLQuery = "select count(1) from members where memberid="+str(p_memberid)
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    for v_rec in DBHandler.cursor:
            v_cnt = v_rec[0]
    print(v_rec[0])
    v_cnt = v_rec[0]
    print("Total recoreds found: ",v_cnt)
    print(v_cnt)
    v_ClubID = p_ClubID
    v_TeamID = p_TeamID
    if v_cnt == 0:
        if p_ClubID == "0":
            v_ClubID = "null"
        print("Team id: ",p_TeamID)
        if p_TeamID == "0":
            print("inside Team id: ",p_TeamID)
            v_TeamID = "null"

        vSQLQuery = "INSERT INTO Members VALUES ("
        vSQLQuery += str(p_memberid) + "," + str(v_ClubID) + "," + str(v_TeamID) + ",'" + p_MemberFirstName + "','" + p_MemberLastName + "','" + p_Address1+ "','"
        vSQLQuery += p_Address2 + "','" + p_City + "','" + p_Email + "','" + p_Phone + "','" + p_Birthdate  + "'," + str(p_MembershipStatus) + "," + str(p_AdminAccess) +")"
        print(vSQLQuery)
        DBHandler.cursor.execute(vSQLQuery)
        DBHandler.DBcon.commit()
        print(DBHandler.cursor.rowcount, "record(s) affected")
    elif v_cnt > 0:
        vSQLQuery = "UPDATE members SET "
        vSQLQuery += "MemberFirstName='"+ p_MemberFirstName +"', "
        vSQLQuery += "MemberLastName='"+ p_MemberLastName +"', "
        vSQLQuery += "Address1='"+ p_Address1 +"', "
        vSQLQuery += "Address2='"+ p_Address2 +"', "
        vSQLQuery += "City='"+ p_City +"', "
        vSQLQuery += "Email='"+ p_Email +"', "
        vSQLQuery += "Phone='"+ p_Phone +"', "
        vSQLQuery += "Birthdate='"+ p_Birthdate + "', "
        vSQLQuery += "clubid = " + str(p_ClubID) +"," 
        vSQLQuery += "teamid = " + str(p_TeamID) +"," 
        vSQLQuery += "MembershipStatus = " + str(p_MembershipStatus) +"," 
        vSQLQuery += "AdminAccess = " + str(p_AdminAccess) + " where memberid=" + str(p_memberid)
        print(vSQLQuery)
        DBHandler.cursor.execute(vSQLQuery)
        DBHandler.DBcon.commit()
        print(DBHandler.cursor.rowcount, "record(s) affected")