from ncaa import NCAA

try:
    bot = NCAA(teardown=True)
    bot.land_first_page()
    bot.get_archive()
    print("Exiting")

except Exception as a:
    print(a)
