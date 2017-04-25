import requests, base64, hashlib, re

def reboot_tplink(login_user,login_pw,ip):
    
    ###
    # LOGIN
    ###

    url = "http://" + ip + "/userRpm/LoginRpm.htm?Save=Save"

    ##BUILD COOKIE
    ##
    ##The Javascript code of the Login page tells us how to build the cookie:
    ##			if(httpAutErrorArray[1] == 1)
    ##			{
    ##				password = hex_md5($("pcPassword").value);	
    ##			}			
    ##			var auth = "Basic "+ Base64Encoding(username + ":" + password);
    ##			document.cookie = "Authorization="+escape(auth)+";path=/";
    ##			location.href ="../userRpm/LoginRpm.htm?Save=Save";
    login_pw_md5 = hashlib.md5(login_pw).hexdigest()
    cookie = "Basic " + base64.b64encode(login_user + ':' + login_pw_md5) 
    cookies = {'Authorization': cookie}

    response = requests.get(url, cookies=cookies)

    #A successful response should look like this:
    #
    #<Response [200]>
    #<body><script language="javaScript">window.parent.location.href = "http://192.168.0.1/HQKATSSCQLVJQNVB/userRpm/Index.htm";
    #</script></body></html>
    #
    #we want the "HQKATSSCQLVJQNVB" part of the URL (which is different each time)
    print response.text
    print response
    
    login_string = re.findall("[A-Z]{16}",response.text)[0]



    ###
    # REBOOT
    ###

    #The router expects the following Referer header:
    referer_url = 'http://' + ip + '/' + login_string + '/userRpm/SysRebootRpm.htm'
    headers = { 'Referer' : referer_url }
    url = referer_url + '?Reboot=Reboot'

    response = requests.get(url, cookies=cookies, headers=headers)

    return response

if __name__ == "__main__":
    login_user = 'admin'
    login_pw = 'admin'
    ip = "192.168.0.1"

    response = reboot_tplink(login_user,login_pw,ip)
    print response.text
    print response
    
