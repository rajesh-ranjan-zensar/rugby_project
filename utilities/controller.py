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
    print(vSQLQuery)
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

## Get the grade details. 
def getGradeDetails(DBHandler, p_grade_id=0):
    retVal={}
    if p_grade_id == 0: 
        vSQLQuery = "select gradeid,concat(gradename , ' (From Age ' , grademinimumage, ' To ',grademaximumage,' Years)') from grades"
    else:
        vSQLQuery = "select gradeid,concat(gradename , ' (From Age ' , grademinimumage, ' To ',grademaximumage,' Years)') from grades where gradeid=" + str(p_grade_id)
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

## Get list of all active/inactive members
def getAllMembers(DBHandler,p_status):
    vSQLQuery = "select m.memberid,c.clubname, t.teamname, "
    vSQLQuery += "memberfirstname, memberlastname, address1, address2, city, m.email, m.phone, m.birthdate, "
    vSQLQuery += "if(m.membershipstatus=1,'Active','Inactive'), "
    vSQLQuery += "if(m.adminaccess=1,'Admin User','Standard User') "
    vSQLQuery += "from members m left  join clubs c on (m.clubid = c.clubid) "
    vSQLQuery += "left  join teams t on (m.teamid = t.teamid and c.clubid = t.clubid) "
    vSQLQuery += "where m.membershipstatus=" + str(p_status)

    DBHandler.cursor.execute(vSQLQuery)
    retVal = DBHandler.cursor.fetchall()
    return retVal

## Get team details for team admin page
def getTeamDet(DBHandler,p_team_id):
    vSQLQuery = "select teamid,clubid, teamname,teamgrade from teams where teamid = " + str(p_team_id)
    DBHandler.cursor.execute(vSQLQuery)
    retVal = DBHandler.cursor.fetchone()
    return retVal


def saveTeamDetails(DBHandler,
                    p_teamid,
                    p_clubid,
                    p_teamname,
                    p_teamgrade
                    ):
    vSQLQuery = "select count(1) from teams where teamid="+str(p_teamid)
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    for v_rec in DBHandler.cursor:
            v_cnt = v_rec[0]
    print(v_rec[0])
    v_cnt = v_rec[0]
    print("Total recoreds found: ",v_cnt)
    v_ClubID = p_clubid
    v_gradeid = p_teamgrade
    if v_cnt == 0:
        if v_ClubID == "0":
            v_ClubID = "null"
        if v_gradeid == "0":
            v_gradeid = "null"

        vSQLQuery = "INSERT INTO teams VALUES ("
        vSQLQuery += str(p_teamid) + "," + str(v_ClubID) + ",'" + str(p_teamname) + "'," + str(v_gradeid)  +")"
        print(vSQLQuery)
        DBHandler.cursor.execute(vSQLQuery)
        DBHandler.DBcon.commit()
        print(DBHandler.cursor.rowcount, "record(s) affected")
    elif v_cnt > 0:
        vSQLQuery = "UPDATE teams SET "
        vSQLQuery += "clubid='"+ str(v_ClubID) +"', "
        vSQLQuery += "teamname='"+ str(p_teamname) +"', "
        vSQLQuery += "teamgrade='"+ str(v_gradeid) + "' where teamid=" + str(p_teamid)
        print(vSQLQuery)
        DBHandler.cursor.execute(vSQLQuery)
        DBHandler.DBcon.commit()
        print(DBHandler.cursor.rowcount, "record(s) affected")
### Get all teams
def getAllTeams(DBHandler):
    vSQLQuery = """select t.teamid,c.clubname,t.teamname, g.gradename 
                from teams t 
                    left join clubs c on (t.clubid = c.clubid) 
                    left join grades g on (t.teamgrade = g.gradeid)"""
    DBHandler.cursor.execute(vSQLQuery)
    retVal = DBHandler.cursor.fetchall()
    return retVal

##### Get grade eligibility criteria
def getGradeCriteria(DBHandler, p_gradeid):
    vSQLQuery = "select GradeMinimumAge, GradeMaximumAge from grades where gradeid=" + str(p_gradeid)
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    retVal = DBHandler.cursor.fetchone()
    return retVal

##### Get list of eligible members for grade
def getEligibleGradeMember(DBHandler, p_min_age,p_max_age, p_elig_date):

    vSQLQuery = "select MemberFirstName, MemberLastName, birthdate, age "
    vSQLQuery += "from (select m.MemberFirstName, "
    vSQLQuery += "m.MemberLastName, "
    vSQLQuery += "m.birthdate, "
    vSQLQuery += "DATE_FORMAT('" + str(p_elig_date) +"', '%Y') - DATE_FORMAT(birthdate, '%Y') - (DATE_FORMAT('" + str(p_elig_date) +"', '00-%m-%d') < DATE_FORMAT(birthdate, '00-%m-%d')) AS age "
    vSQLQuery += "from members m) as elgible_member "
    vSQLQuery +=  "where age between " + str(p_min_age) + " and " + str(p_max_age)
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    retVal = DBHandler.cursor.fetchall()
    return retVal

### Get Fixture details
def getfixtureDet(DBHandler,p_fix_id):
    vSQLQuery = "select fixtureid, fixturedate, hometeam,awayteam, homescore,awayscore from fixtures where fixtureid=" + str(p_fix_id)
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    retVal = DBHandler.cursor.fetchone()
    return retVal

## Save fixture details
def saveFixtureDetails(DBHandler,
                    p_fixid,
                    p_fixdate,
                    p_hometeam,
                    p_awayteam,
                    p_homescore,
                    p_awayscore
                    ):
    vSQLQuery = "select count(1) from fixtures where fixtureid="+str(p_fixid)
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    for v_rec in DBHandler.cursor:
            v_cnt = v_rec[0]
    print(v_rec[0])
    v_cnt = v_rec[0]
    print("Total recoreds found: ",v_cnt)
    

    v_hometeam = p_hometeam
    v_awayteam = p_awayteam
    v_homescore = p_homescore
    v_awayscore = p_awayscore
    if v_hometeam == "0":
        v_hometeam = "null"
    if v_awayteam == "0":
        v_awayteam = "null"

    if v_homescore == "":
        v_homescore = "0"
    if v_awayscore == "":
        v_awayscore = "0"
    if v_cnt == 0:
        vSQLQuery = "INSERT INTO fixtures VALUES ("
        vSQLQuery += str(p_fixid) + ",'" + str(p_fixdate) + "'," + str(v_hometeam) + "," + str(v_awayteam) + ","  + str(v_homescore) + "," + str(v_awayscore) + ")"
        print(vSQLQuery)
        DBHandler.cursor.execute(vSQLQuery)
        DBHandler.DBcon.commit()
        print(DBHandler.cursor.rowcount, "record(s) affected")
    elif v_cnt > 0:
        vSQLQuery = "UPDATE fixtures SET "
        vSQLQuery += "fixtureid='"+ str(p_fixid) +"', "
        vSQLQuery += "fixturedate='"+ str(p_fixdate) +"', "
        vSQLQuery += "hometeam='"+ str(p_hometeam) + "', "
        vSQLQuery += "awayteam='"+ str(p_awayteam) + "', "
        vSQLQuery += "homescore='"+ str(v_homescore) + "', "
        vSQLQuery += "awayscore='"+ str(v_awayscore) + "' where fixtureid=" + str(p_fixid)
        print(vSQLQuery)
        DBHandler.cursor.execute(vSQLQuery)
        DBHandler.DBcon.commit()
        print(DBHandler.cursor.rowcount, "record(s) affected")


### Get News details
def getNewsDet(DBHandler,p_news_id):
    vSQLQuery = "select newsid, clubid,newsheader, newsdate,news,newsbyline from clubnews where newsid = " + str(p_news_id)
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    retVal = DBHandler.cursor.fetchone()
    return retVal

## Save News details
def saveNewsDetails(DBHandler,
                    p_newsid,
                    p_clubid,
                    p_newsheader,
                    p_newsdate,
                    p_news,
                    p_newsbyline
                    ):
    vSQLQuery = "select count(1) from clubnews where newsid="+str(p_newsid)
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    for v_rec in DBHandler.cursor:
            v_cnt = v_rec[0]
    print(v_rec[0])
    v_cnt = v_rec[0]
    print("Total recoreds found: ",v_cnt)
    

    v_clubid = p_clubid

    if v_clubid == "0":
        v_clubid = "null"
    
    if v_cnt == 0:
        vSQLQuery = "INSERT INTO clubnews VALUES ("
        vSQLQuery += str(p_newsid) + "," + str(p_clubid) + ',"' + str(p_newsheader) + '","' + str(p_newsbyline) + '","'  + str(p_newsdate) + '","' + str(p_news.strip()) + '")'
        print(vSQLQuery)
        DBHandler.cursor.execute(vSQLQuery)
        DBHandler.DBcon.commit()
        print(DBHandler.cursor.rowcount, "record(s) affected")
    elif v_cnt > 0:
        vSQLQuery = "UPDATE clubnews SET "
        vSQLQuery += "NewsID='"+ str(p_newsid) +"', "
        vSQLQuery += "ClubID='"+ str(p_clubid) +"', "
        vSQLQuery += 'NewsHeader="'+ str(p_newsheader) + '", '
        vSQLQuery += "NewsByline='"+ str(p_newsbyline) + "', "
        vSQLQuery += "NewsDate='"+ str(p_newsdate) + "', "
        vSQLQuery += 'News="'+ str(p_news) + '" where newsid=' + str(p_newsid)
        print(vSQLQuery)
        DBHandler.cursor.execute(vSQLQuery)
        DBHandler.DBcon.commit()
        print(DBHandler.cursor.rowcount, "record(s) affected")

## Get all club news as per selected club in admin mode
def getAdminClubNews(DBHandler, p_clubid):
    vSQLQuery = "select c.newsheader, c.news, c.newsdate, c.newsbyline from clubnews c where clubid =" + str(p_clubid)
    print(vSQLQuery)
    DBHandler.cursor.execute(vSQLQuery)
    retVal = DBHandler.cursor.fetchall()
    return retVal