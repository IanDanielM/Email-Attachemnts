import os,sys
from imbox import Imbox # pip install imbox
import traceback
from connect import dropbox_connect
import dropbox
import pathlib as Path
from schedule import every, repeat, run_pending
import time
# enable less secure apps on your google account
# https://myaccount.google.com/lesssecureapps
host = "imap.123-reg.co.uk"
username = "ian@e-mps.co.uk"
password = '1$#i4N3B'
download_folder = r'C:\Users\WEIDIAN\emailattach\uploads'
if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)
def downloadFromMail():   
    mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)
    messages = mail.messages(unread=True) # defaults to inbox
    for (uid, message) in messages:
        mail.mark_seen(uid) # optional, mark message as read
        for idx, attachment in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                download_path = f"{download_folder}/{att_fn}"
                print(download_path)
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())
            except:
                print(traceback.print_exc())

    mail.logout()
    
def uploadToDropbox():
    dbx = dropbox_connect()
    rootdirx = "C:/Users/WEIDIAN/emailattach/uploads" 
    for dir, dirs, files in os.walk(rootdirx):
        for file in files:
            try:
                file_path = os.path.join(dir, file)
                print(file_path)
                dest_path = os.path.join('/E-MPS Work/Ian', file).replace("\\","/")
                print(dest_path)
                print('Uploading %s to %s' %  (file_path, dest_path))
                with open(file_path,'rb') as f:
                    dbx.files_upload(f.read(), dest_path,mode=dropbox.files.WriteMode.overwrite, mute=True)
            except Exception as err:
               print("Failed to upload %s\n%s" % (file, err))

@repeat(every(10).seconds)
def main():
    downloadFromMail()
    uploadToDropbox()
while True:
    run_pending()
    time.sleep(1)




