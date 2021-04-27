from twocaptcha import TwoCaptcha

solver = TwoCaptcha("") #removed

try:
    result = solver.funcaptcha(sitekey="", #removed
                               url="https://www.roblox.com",
                               surl="https://roblox-api.arkoselabs.com"
                               )

except Exception as e:
    print(e)

else:
    print(result.get("code"))
