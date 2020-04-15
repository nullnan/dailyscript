import os, subprocess

adb_command = r"adb logcat -s Vizpower:I"
login_flag = r"RollcallConfirmViewController:onStartRollcallConfirm"

adb_deamon = subprocess.Popen(
    args=adb_command,stdin=None,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=False
)

print("Starting ADB Deamon....")
print("Waiting for roll call.")
with adb_deamon as adb_output:
    for line in adb_output.stdout:
        if login_flag in line.decode('utf-8'):
            os.system("adb shell input tap 800 640")
            print("Roll Call!")

