def SSHRunFunc(name):
    import paramiko
    # host_name = "127.0.0.1"
    pass_word = None
    user_name = None

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect('70.31.167.140', username=user_name, password=pass_word, port=22)

    stdin, stdout, stderr = ssh_client.exec_command("python3 vrp_dummy.py %s" % name)
    #stdin,stdout,stderr = ssh_client.exec_command("ls")
    nameUsed = stdout.read().decode('ascii').strip("\n")
    print(nameUsed)
    ftp_client = ssh_client.open_sftp()
    ftp_client.get('/home/drew_mcmillen95/' + nameUsed + '.txt',
                   'D:/temp/' +nameUsed + '.txt')
    ftp_client.close()

def funcVRP():
    import pandas as pd
    import random as rand
    fake_results_raw = {"Truck":[rand.randint(1,101),rand.randint(1,101),rand.randint(1,101)], "Longitude":[rand.randint(-9000,9000)/100,rand.randint(-9000,9000)/100,rand.randint(-9000,9000)/100],"Latitude":[rand.randint(-18000,18000)/100,rand.randint(-1800,1800)/100,rand.randint(-18000,1800)/100]}
    fake_results = pd.DataFrame(fake_results_raw)
    return fake_results



