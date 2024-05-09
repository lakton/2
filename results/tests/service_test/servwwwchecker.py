try:
    with open("/home/sdn/Desktop/2/results/resultservice.log", "a") as file:
        if '<html>' in open('/home/sdn/Desktop/2/results/servicewww.log').read():
            file.write("\n\nWWW server DIG test : PASS")
        else:
            file.write("\nWWW server DIG test : FAIL")
except Exception as e:
    print("Error:", e)
