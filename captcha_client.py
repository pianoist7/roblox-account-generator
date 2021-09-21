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

    
    # Someone managed to bypass roblox captcha by randomizing IPs and getting 1 out of 100k accounts with no captcha on creation, roblox has patched this since though
