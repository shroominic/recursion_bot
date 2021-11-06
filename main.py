from rekursion_bot import RekursionBot


def main():
    rbot = RekursionBot()
    rbot.init_chrome(chromedriver_path='./chromedriver')
    # Download: https://chromedriver.chromium.org/

    rbot.open_target_page()
    rbot.click_button("I agree")
    rbot.send_keys("Recursion")
    while rbot.typo_need_to_get_fixed():
        rbot.fix_typo()


if __name__ == '__main__':
    main()
    input("Stop: ")
