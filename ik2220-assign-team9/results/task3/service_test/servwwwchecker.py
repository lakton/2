try:
    with open("/var/log/resultservice.log", "a") as file:
        if '<html>' in open('/var/log/servicewww.log').read():
            file.write("\n\nWWW server DIG test : PASS")
        else:
            file.write("\nWWW server DIG test : FAIL")
except Exception as e:
    print("Error:", e)
