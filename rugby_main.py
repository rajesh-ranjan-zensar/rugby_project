from flask import Flask, render_template, request
from flask.wrappers import Request
from utilities.DBConnect import *
from utilities.controller import *

dbconn = MySqlDB() ## database object. this is used to perform any database operations like selecting, inserting or updating

app = Flask(__name__,static_folder='./templates/')

@app.route('/')
def homepage():
   dbLogin()
   retval = getActiveMembers_home(dbconn)
   return render_template('home.html',memname=retval)
##app.add_url_rule('/', 'hello', hello_world)

@app.route('/login',methods = ['POST', 'GET'])
def login_request():
   print(request.method)
   if request.method == 'POST':
      loguser = request.form.get("member_name")
      memdet = getMemberDetail(dbconn, loguser)
      print(memdet[0])
      print(memdet[1])
      print(memdet[2])
      if memdet[1] == 0:
         return render_template('standard_user.html',loguser=memdet[0], memberid=memdet[2])
      elif memdet[1] == 1:
         return render_template('admin_user.html',loguser=memdet[0], memberid=memdet[2])

@app.route('/standarduser',methods = ['POST', 'GET'])
def clubnews_request():
   print(request.method)
   if request.method == 'POST':
      memberid = request.form.get("memberid")
      memname = request.form.get("memname")
      pagename = request.form.get("pagename")
      print(memname)
      print(pagename)
      if pagename == "clubnews_stuser":
         memdet = getMemberDetail(dbconn, memberid)
         newsdet = getClubNews(dbconn, memberid)
         print(newsdet)
         return render_template('clubnews_stuser.html', clubnews=newsdet, loguser=memdet[0], memberid=memdet[2], clubname=memdet[3])
      if pagename == "home_stuser":
         memdet = getMemberDetail(dbconn, memberid)
         print(memdet)
         return render_template('standard_user.html', loguser=memdet[0], memberid=memdet[2])
      if pagename == "profile_stuser":
         v_teamname = ""
         v_teamid = ""
         memdet = getMemberContactDetail(dbconn, memberid)
         print(memdet)
         v_teamid = memdet[2]
         print(type(v_teamid))
         if v_teamid == None:
            v_teamname = "NA"
         else:
            v_teamname = getMemberTeamName(dbconn, v_teamid)

         return render_template('profile_stuser.html', memberid=memdet[0], 
                                                      clubname=memdet[1],
                                                      teamname=v_teamname,
                                                      MemberFirstName=memdet[3],
                                                      MemberLastName=memdet[4],
                                                      Address1=memdet[5],
                                                      Address2=memdet[6],
                                                      City=memdet[7],
                                                      Email=memdet[8],
                                                      Phone=memdet[9],
                                                      Birthdate=memdet[10]
                                                      )
      if pagename == "fixtures_stuser":
         v_error = ""
         memdet = getMemberContactDetail(dbconn, memberid)
         v_teamid = memdet[2]
         print("Team id: ", v_teamid)
         if v_teamid == None:
            v_error = memdet[3] + " not assigned to any team"
         else:
            fixdet = getTeamFixtures(dbconn, v_teamid)
            print(fixdet)
         return render_template('fixture_stuser.html', fixturedet = fixdet, errormsg=v_error, loguser=memdet[3] + " " +memdet[4], memberid=memdet[0])

@app.route('/savestuserprofile',methods = ['POST', 'GET'])
def save_user_profile():
   print(request.method)
   if request.method == 'POST':
      v_memberid = request.form.get("memberid")
      v_firstname = request.form.get("MemberFirstName")
      v_clubname = request.form.get("clubname")
      v_lastname = request.form.get("MemberLastName")
      v_address1 = request.form.get("Address1")
      v_address2 = request.form.get("Address2")
      v_city = request.form.get("City")
      v_email = request.form.get("Email")
      v_phone = request.form.get("Phone")
      v_dob = request.form.get("Birthdate")
      print("Member id - ",v_memberid)
      print("First name - ",v_firstname)
      print("Last name - ",v_lastname)
      print("address1 - ",v_address1)
      print("clubname - ",v_clubname)
      updateMemberContact(dbconn,v_memberid, v_firstname,v_lastname,v_address1,v_address2,v_city,v_email,v_phone,v_dob)
      memdet = getMemberContactDetail(dbconn, v_memberid)
      print(memdet)
      v_teamid = memdet[2]
      print(type(v_teamid))
      if v_teamid == None:
         v_teamname = "NA"
      else:
         v_teamname = getMemberTeamName(dbconn, v_teamid)

      return render_template('profile_stuser.html', memberid=memdet[0], 
                                                      clubname=memdet[1],
                                                      teamname=v_teamname,
                                                      MemberFirstName=memdet[3],
                                                      MemberLastName=memdet[4],
                                                      Address1=memdet[5],
                                                      Address2=memdet[6],
                                                      City=memdet[7],
                                                      Email=memdet[8],
                                                      Phone=memdet[9],
                                                      Birthdate=memdet[10]
                                                      )



#########################################################################################################
@app.route('/adminuser',methods = ['POST', 'GET'])
def menu_navigate():
   print(request.method)
   if request.method == 'POST':
      memberid = request.form.get("memberid")
      memname = request.form.get("memname")
      pagename = request.form.get("pagename")
      action = request.form.get("action")
      print(memname)
      print("Pagename: ",pagename)
      print("Action: ",action)
      vclubdet = getClubDetails(dbconn)
      vteamdet = getTeamsDetails(dbconn)
      vgradedet = getGradeDetails(dbconn)
      if pagename == "adminhomepage" and action == "go_home":
         return render_template('admin_user.html',loguser=memname, memberid=memberid)
      if pagename == "member_insert":
         vclubdet = getClubDetails(dbconn,0,"TEAMS")
         vnextmember = getNextID(dbconn,"members","memberid")
         print("Next memberid: ",vnextmember)
         return render_template('member_admin_user.html', dbaction="INSERT",clubsdet=vclubdet,teamsdet=vteamdet,loguser=memname,vclubid=0,vteamid=0,memberid=vnextmember)
      if pagename == "member_update":
         vclubdet = getClubDetails(dbconn,0,"TEAMS")
         return render_template('member_admin_user.html', dbaction="UPDATE",clubsdet=vclubdet,teamsdet=vteamdet, loguser=memname,vclubid=0,vteamid=0)
      if pagename == "member_list":
         return render_template('member_admin_user_report.html')
      if pagename == "memberadmin" and action == "getteamname":
         vclubdet = getClubDetails(dbconn,0,"TEAMS")
         vnextmember = request.form.get("memberid")
         vdbaction = request.form.get("dbaction")
         vfname = request.form.get("textfirstname")
         vlname = request.form.get("textlastname")
         vclubname = request.form.get("drpclubname")
         vadd1 = request.form.get("textadd1")
         vadd2 = request.form.get("textadd2")
         vcity = request.form.get("textcity")
         vemail = request.form.get("textemail")
         vphone = request.form.get("textephone")
         vdob = request.form.get("textdob")
         vmemberstatus = request.form.get("drpstatus")
         vadminaccess = request.form.get("drpaccess")
         vteamdet = getTeamsDetails(dbconn,0,vclubname)
         print(vfname)
         print(vlname)
         return render_template('member_admin_user.html',
                                 dbaction=vdbaction,
                                 clubsdet=vclubdet,
                                 teamsdet=vteamdet,
                                 loguser=memname,
                                 vclubid=vclubname,
                                 vteamid=0,
                                 memberid=vnextmember,
                                 fname=vfname,
                                 lastname=vlname,
                                 address1=vadd1,
                                 address2=vadd2,
                                 cityname=vcity,
                                 emailid=vemail,
                                 phonenumber=vphone,
                                 dateofbirth=vdob,
                                 vmemstatus=vmemberstatus,
                                 vadmin=vadminaccess)

      if pagename == "admingetmemberdetail":
         dbmemberid=request.form.get("intmemberid")
         print("Getting details for member id ", dbmemberid)
         memdet = getMemberDetails(dbconn,dbmemberid,"ONE")
         print("club id ", memdet[1])
         print(memdet)
         return render_template('member_admin_user.html', dbaction="UPDATE",
                                 loguser=memname,
                                 clubsdet=vclubdet,
                                 teamsdet=vteamdet, 
                                 memberid=memdet[0], 
                                 fname=memdet[3],
                                 lastname=memdet[4],
                                 vclubid=memdet[1],
                                 vteamid=memdet[2],
                                 address1=memdet[5],
                                 address2=memdet[6],
                                 cityname=memdet[7],
                                 emailid=memdet[8],
                                 phonenumber=memdet[9],
                                 dateofbirth=memdet[10],
                                 vmemstatus=memdet[11],
                                 vadmin=memdet[12]
                                 )
      if pagename == "saveMemberDetail":
         memid = request.form.get("memberid")
         memname=request.form.get("memname")

         v_memberid = request.form.get("intmemberid")
         v_ClubID = request.form.get("drpclubname")
         v_TeamID = request.form.get("drpteamname")
         v_MemberFirstName = request.form.get("textfirstname")
         v_MemberLastName = request.form.get("textlastname")
         v_Address1 = request.form.get("textadd1")
         v_Address2 = request.form.get("textadd2")
         v_City = request.form.get("textcity")
         v_Email = request.form.get("textemail")
         v_Phone = request.form.get("textephone")
         v_Birthdate = request.form.get("textdob")
         v_MembershipStatus = request.form.get("drpstatus")
         v_AdminAccess = request.form.get("drpaccess")
         print("savintg data for memberid ",v_memberid)
         saveMemberDetails(dbconn,v_memberid,v_ClubID,v_TeamID,v_MemberFirstName,v_MemberLastName,v_Address1,v_Address2,v_City,
                           v_Email,v_Phone,v_Birthdate,v_MembershipStatus,v_AdminAccess)
         
         return render_template('member_admin_user.html', dbaction="UPDATE",clubsdet=vclubdet,teamsdet=vteamdet, loguser=memname,vclubid=0,vteamid=0)

      if pagename == "memberlist" and action == "getlist":
         v_status = request.form.get("drpstatus")
         print("pagename: ",pagename)
         print("action: ",action)
         print(v_status)
         memdet = getAllMembers(dbconn,v_status)
         return render_template('member_admin_user_report.html', memdet = memdet)
      ### for Teams
      if pagename == "team_insert":
         vnextteamid = getNextID(dbconn,"teams","teamid")
         print("Next memberid: ",vnextteamid)
         return render_template('teams_admin_user.html', action="INSERT",clubsdet=vclubdet,gradedet=vgradedet,loguser=memname,vclubid=0,vteamid=0,txtteamid=vnextteamid)
      if pagename == "team_update":
         return render_template('teams_admin_user.html', action="UPDATE",clubsdet=vclubdet,gradedet=vgradedet,loguser=memname,vclubid=0,vteamid=0)
      if pagename == "teamadmin" and action == "fetch_team_details":
         vteamid=request.form.get("txtteamid")
         print("Getting details for member id ", vteamid)
         teamdet = getTeamDet(dbconn,vteamid)
         print("club id ", teamdet[1])
         print(teamdet)
         return render_template('teams_admin_user.html', dbaction="UPDATE",
                                 loguser=memname,
                                 clubsdet=vclubdet,
                                 gradedet=vgradedet, 
                                 txtteamid=teamdet[0], 
                                 txtteamname=teamdet[2],
                                 vclubid=teamdet[1],
                                 vgradeid=teamdet[3]
                                 )
      if pagename == "teamadmin" and action == "saveteamdetail":
         memid = request.form.get("memberid")
         memname=request.form.get("memname")

         v_teamid = request.form.get("txtteamid")
         v_clubid = request.form.get("drpclubname")
         v_teamname = request.form.get("txtteamname")
         v_gradeid = request.form.get("drpgrade")
         
         print("savintg data for teamid ",v_teamid)
         saveTeamDetails(dbconn,v_teamid,v_clubid,v_teamname,v_gradeid)
         
         return render_template('teams_admin_user.html', dbaction="UPDATE",clubsdet=vclubdet,gradedet=vgradedet,loguser=memname,vclubid=0,v_gradeid=0)
      if pagename == "team_list":
         v_status = request.form.get("drpstatus")
         print("pagename: ",pagename)
         print("action: ",action)
         print(v_status)
         teamdet = getAllTeams(dbconn)
         return render_template('team_admin_user_report.html', teamdet = teamdet)
      ###### grade eligibility report
      if pagename == "grade_elig_report" and action == "load_page":
         return render_template('grade_eligiblity_report.html', gradedet=vgradedet,loguser=memname)
      if pagename == "grade_elig_report" and action == "load_criteria":
         v_gradeid = request.form.get("drpgrade")
         print("Selected gradeid ",v_gradeid)
         gradedet = getGradeCriteria(dbconn,v_gradeid)
         print("Min age: ",gradedet[0])
         print("Max age: ",gradedet[1])
         print("Grade id: ",v_gradeid)
         return render_template('grade_eligiblity_report.html', gradedet=vgradedet,
                                 loguser=memname, 
                                 grademinage = gradedet[0], 
                                 grademaxage = gradedet[1], 
                                 gradeid = v_gradeid)
      if pagename == "grade_elig_report" and action == "load_report":
         v_min_age = request.form.get("grademinage")
         v_max_age = request.form.get("grademaxage")
         v_gradeid = request.form.get("gradeid")
         v_elig_date = request.form.get("eligibledate")
         print("Min: ",v_min_age)
         print("Max: ",v_max_age)
         print("Grade id: ",v_gradeid)
         print("Date: ",v_elig_date)

         eligibledet = getEligibleGradeMember(dbconn,v_min_age,v_max_age,v_elig_date)
         return render_template('grade_eligiblity_report.html', 
                                 eligibledet = eligibledet,
                                 gradedet=vgradedet,
                                 loguser=memname, 
                                 grademinage = v_min_age, 
                                 grademaxage = v_max_age, 
                                 gradeid = v_gradeid,
                                 eligibledate=v_elig_date)
      ##### for fixture details
      if pagename == "fixture_inert":
         vnextfixid = getNextID(dbconn,"fixtures","fixtureid")
         print("Next fixtue id: ",vnextfixid)
         return render_template('fixture_admin_user.html', action="INSERT",teamsdet=vteamdet,loguser=memname,vclubid=0,vteamid=0,txtfixtureid=vnextfixid)
      if pagename == "fixture_update":
         return render_template('fixture_admin_user.html', action="UPDATE",teamsdet=vteamdet,loguser=memname,vclubid=0,vteamid=0)
      if pagename == "fixtureadmin" and action == "fetch_fixture_details":
         v_fixid = request.form.get("txtfixtureid")
         v_loguser = request.form.get("loguser")
         v_memberid = request.form.get("memberid")
         v_fixturedet = getfixtureDet(dbconn,v_fixid)
         print("Date is: ",v_fixturedet[1])
         return render_template('fixture_admin_user.html', dbaction="UPDATE",
                                 txtfixtureid=v_fixturedet[0],
                                 dtfixturedate=v_fixturedet[1],
                                 vhometeamid=v_fixturedet[2],
                                 vawayteamid=v_fixturedet[3],
                                 txthomescore=v_fixturedet[4],
                                 txtawayscore=v_fixturedet[5],
                                 teamsdet=vteamdet,loguser=v_loguser
                                 )
      if pagename == "fixtureadmin" and action == "savefixturedetail":
         memid = request.form.get("memberid")
         loguser=request.form.get("loguser")

         v_fixtureid = request.form.get("txtfixtureid")
         v_fixturedate = request.form.get("dtfixturedate")
         v_hometeam = request.form.get("drpteamnameh")
         v_awayteam = request.form.get("drpteamnamea")
         v_homescore = request.form.get("txthomescore")
         v_awayscore = request.form.get("txtawayscore")
         saveFixtureDetails(dbconn,v_fixtureid,v_fixturedate,v_hometeam, v_awayteam, v_homescore, v_awayscore)
         return render_template('fixture_admin_user.html', dbaction="UPDATE",
                                 teamsdet=vteamdet,loguser=memname,vclubid=0,vteamid=0)
      if pagename == "fixture_list":
         return render_template('fixture_admin_report.html', action="REPORT",teamsdet=vteamdet,loguser=memname,teamid=0)
      if pagename == "fixtureadmin" and action == "get_fixtures":
         v_teamid = request.form.get("drpteamname")
         print("team id: ",v_teamid)
         v_fixturedet = getTeamFixtures(dbconn,v_teamid)
         print(v_fixturedet)
         return render_template('fixture_admin_report.html', action="REPORT",teamsdet=vteamdet,loguser=memname,fixturedet=v_fixturedet, teamid=v_teamid)
      ### For clubnews 
      if pagename == "clubnews_inert":
         vnextfixid = getNextID(dbconn,"clubnews","newsid")
         print("Next fixtue id: ",vnextfixid)
         return render_template('clubnews_admin_user.html', action="INSERT",clubsdet=vclubdet,loguser=memname,vclubid=0,txtnewsid=vnextfixid)
      if pagename == "clubnews_update":
         return render_template('clubnews_admin_user.html', action="UPDATE",clubsdet=vclubdet,loguser=memname,vclubid=0)
      if pagename == "newsadmin" and action == "fetch_news_details":
         v_newsid = request.form.get("txtnewsid")
         v_loguser = request.form.get("loguser")
         v_memberid = request.form.get("memberid")
         v_newsdet = getNewsDet(dbconn,v_newsid)
         print(v_newsdet)
         print("Date is: ",v_newsdet[4])
         return render_template('clubnews_admin_user.html', dbaction="UPDATE",
                                 clubsdet=vclubdet,
                                 txtnewsid=v_newsdet[0],
                                 vclubid=v_newsdet[1],
                                 txtnewsheader=v_newsdet[2],
                                 dtnewsdate=v_newsdet[3],
                                 txtnews=v_newsdet[4],
                                 txtnewsbyline=v_newsdet[5]
                                 )
      if pagename == "newsadmin" and action == "save_news_detail":
         v_newsid = request.form.get("txtnewsid")
         v_clubid = request.form.get("drpclubname")
         v_newsheader = request.form.get("txtnewsheader")
         v_newsdate = request.form.get("dtnewsdate")
         v_news = request.form.get("txtnews")
         v_newsby = request.form.get("txtnewsbyline")
         saveNewsDetails(dbconn,v_newsid,v_clubid,v_newsheader,v_newsdate,v_news,v_newsby)
         return render_template('clubnews_admin_user.html', action="UPDATE",clubsdet=vclubdet,loguser=memname,vclubid=0)
      if pagename == "clubnews_list":
         return render_template('clubnews_admin_report.html', action="REPORT",clubsdet=vclubdet,loguser=memname,clubid=0)
      if pagename == "newsadminreport" and action == "get_clubnews":
         vclubid = request.form.get("drpclubname")
         v_clubnewsdet = getAdminClubNews(dbconn,vclubid)
         return render_template('clubnews_admin_report.html', action="REPORT",clubsdet=vclubdet,clubnews=v_clubnewsdet,loguser=memname,clubid=vclubid)



"""
def memberAction():
   print(request.method)
   if request.method == 'POST':
      memberid = request.form.get("memberid")
      memname = request.form.get("memname")

      dbmemberid=request.form.get("intmemberid")
      dbaction = request.form.get("pagename")

      vclubdet = getClubDetails(dbconn)
      vteamdet = getTeamsDetails(dbconn)
      if dbaction == "admingetmemberdetail":
         memdet = getMemberDetails(dbconn,memberid,"ONE")
         return render_template('member_admin_user.html', dbaction="UPDATE",
                                 loguser=memname,
                                 clubsdet=vclubdet,
                                 teamsdet=vteamdet, 
                                 memberid=memdet[0], 
                                 fname=memdet[3],
                                 lastname=memdet[4],
                                 vclubid=memdet[1],
                                 vteamid=memdet[2]
                                 ) 
"""
###########################################################################################################



### login into the database
def dbLogin():
   dbconn.initialize('root','Feds_1234','localhost','rugby_db')
   err_msg = dbconn.connect()
   ##dbconn.closeConnection()

if __name__ == '__main__':
   app.run(debug=True)


