import os
import time
import subprocess
from playsound import playsound
from pathlib import Path
import smtplib

# Function that closes Blender and shutdowns the PC
def shutdown():
    try:
        # Attempt to close Blender
        subprocess.call(["taskkill", "/F", "/IM", "blender.exe"])
        print("Blender closed")
        time.sleep(5)
        # Attempt to shut down the PC
        subprocess.call(["shutdown", "/s", "/t", "0"])
        print("Shutting down...")

    except Exception:
        print(f"An error occured: {Exception}")

#Function that sends the notification email once the render is finished
def send_email(filepath):
    sender_email = "sender@gmail.com"
    receiver_email = "receiver@gmail.com"
    app_password = "enter app password here"

    email_content = f"Subject: RENDER FINISHED\n\nThe rendered image is saved in {filepath}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, email_content)
    print ("Notification mail sent!\n")

print("POST-RENDER SHUTDOWN\n")
filepath = input("Enter the expected complete filepath of the rendered image: ")

while True:
    if os.path.exists(filepath):  # Runs when True is returned
        print("\nRender is complete!")
        playsound(str(Path(__file__).parent / 'homecoming.mp3'))

        send_email(filepath)

        # 30 second countdown before shutdown
        for remaining in range(30, 0, -1):
            print(f"\rShutting down in {remaining} seconds... ", end="", flush=True)
            time.sleep(1)
        break

    else:
        print("\nRendering is still ongoing")
        # 2.5 minute countdown
        for remaining in range(150, 0, -1):
            # Divide "remaining" to minutes and seconds
            minutes, seconds = divmod(remaining, 60)

            # Time formatting
            if minutes > 0:
                time_format = f"{minutes}m {seconds}s"
            else:
                time_format = f"{seconds}s"

            print(f"\rRe-checking in {time_format}...", end="", flush=True)
            time.sleep(1)

shutdown() #Initiate the shutdown of Blender and the PC