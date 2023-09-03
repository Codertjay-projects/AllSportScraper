from nhl import NHL

try:
    bot = NHL(teardown=True)
    bot.land_first_page()
    bot.get_archive()
    print("Exiting")

except Exception as a:
    print(a)
