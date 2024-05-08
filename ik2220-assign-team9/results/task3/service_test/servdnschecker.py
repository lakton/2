try:
    with open("/var/log/resultservice.log", "w") as file:
        if 'ANSWER' in open('/var/log/servicedns.log').read():
            file.write("\n\nDNS server DIG test : PASS")
        else:
            file.write("\nDNS server DIG test : FAIL")
except Exception as e:
    print("Error:", e)
