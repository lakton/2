try:
    with open("/home/sdn/Desktop/2/results/tests/service_test/resultservice.log", "w") as file:
        if 'ANSWER' in open('/home/sdn/Desktop/2/results/tests/service_test/servicedns.log').read():
            file.write("\n\nDNS server DIG test : PASS")
        else:
            file.write("\nDNS server DIG test : FAIL")
except Exception as e:
    print("Error:", e)
