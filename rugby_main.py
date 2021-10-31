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
         return render_template('fixture_stuser.html', fixturedet = fixdet, errormsg=v_error, loguser=memdet[3] + " " +memdet[3], memberid=memdet[0])

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
      print(memname)
      print(pagename)
      vclubdet = getClubDetails(dbconn)
      vteamdet = getTeamsDetails(dbconn)
      if pagename == "member_insert":
         vnextmember = getNextID(dbconn,"members","memberid")
         print("Next memberid: ",vnextmember)
         return render_template('member_admin_user.html', dbaction="INSERT",clubsdet=vclubdet,teamsdet=vteamdet,loguser=memname,vclubid=0,vteamid=0,memberid=vnextmember)
      if pagename == "member_update":
         return render_template('member_admin_user.html', dbaction="UPDATE",clubsdet=vclubdet,teamsdet=vteamdet, loguser=memname,vclubid=0,vteamid=0)
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
###########################################################################################################



### login into the database
def dbLogin():
   dbconn.initialize('root','Feds_1234','localhost','rugby_db')
   err_msg = dbconn.connect()
   ##dbconn.closeConnection()

if __name__ == '__main__':
   app.run(debug=True)

