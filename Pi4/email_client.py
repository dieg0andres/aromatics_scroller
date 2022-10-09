


# gmail password: srlapusybarewuej for diego.a.galindo@gmail
# diegoaromatics@gmail.com $Carmen19

import imaplib
import email

SENDER = 'diego.galindo@exxonmobil.com'
FUSION = 'x'

#credentials
username ="diego.a.galindo@gmail.com"

#generated app password
app_password= "srlapusybarewuej"

# https://www.systoolsgroup.com/imap/
gmail_host= 'imap.gmail.com'

#set connection
mail = imaplib.IMAP4_SSL(gmail_host)

#login
mail.login(username, app_password)

#select inbox
mail.select("INBOX")

#select specific mails
_, selected_emails = mail.search(None, '(SUBJECT "*BZ*")')

#total number of mails from specific user
print("Total Messages from SENDER" , len(selected_emails[0].split()))

print(selected_emails)

message=''

for num in selected_emails[0].split():
    _, data = mail.fetch(num , '(RFC822)')
    _, bytes_data = data[0]

    print('num: ' + str(num))
    #convert the byte data to message
    email_message = email.message_from_bytes(bytes_data)
    print("\n===========================================")
    #access data
    print("Subject: ",email_message["subject"])
    print("To:", email_message["to"])
    print("From: ",email_message["from"])
    print("Date: ",email_message["date"])
    for part in email_message.walk():
        if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
            message = part.get_payload(decode=True)
            print("Message: \n", message.decode())
            print("==========================================\n")
            break
#    break

print(message)
