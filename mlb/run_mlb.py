from mlb import MLB

try:
    bot = MLB(teardown=True)
    bot.land_first_page()
    bot.get_archive()
    print("Exiting")

except Exception as a:
    print(a)
