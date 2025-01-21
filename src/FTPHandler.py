from ftplib import FTP
from dotenv import load_dotenv
import os



def ftp_to_idaq(file_to_upload):
    load_dotenv()
    remote_directory = "/idaq/source-alpha-wscada"
    ftp_server=os.getenv('ftp_server')
    ftp_username=os.getenv('ftp_username')
    ftp_password=os.getenv('ftp_password')
    try:
        # Connect to the FTP server
        ftp = FTP(ftp_server)
        ftp.login(user=ftp_username, passwd=ftp_password)
        print(f"Connected to FTP server: {ftp_server}")

        # Change to the target directory
        ftp.cwd(remote_directory)
        print(f"Changed to directory: {remote_directory}")

        # Upload the file
        with open(file_to_upload, "rb") as file:
            ftp.storbinary(f"STOR {file_to_upload.split('/')[-1]}", file)
            print(f"Uploaded file: {file_to_upload.split('/')[-1]}")

        # Close the connection
        ftp.quit()
        print("FTP connection closed.")

    except Exception as e:
        print(f"An error occurred: {e}")
