try:
    with open("/home/sdn/Desktop/2/results/resultservice.log", "w") as file:
        if 'ANSWER' in open('/home/sdn/Desktop/2/results/servicedns.log').read():
            file.write("\n\nDNS server DIG test : PASS")
        else:
            file.write("\nDNS server DIG test : FAIL")
except Exception as e:
    print("Error:", e)
