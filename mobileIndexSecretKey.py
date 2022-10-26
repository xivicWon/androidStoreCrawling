from playwright.sync_api import sync_playwright


class MobileIndexCookie() :

    @staticmethod
    def getMobileIndexCookie() :
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True )
            page = browser.new_page()
            page.goto("https://www.mobileIndex.com")
            return page.context.cookies()


    @staticmethod
    def getMobileIndexSecretCode()-> str:
        MAXTRYCOUNT = 3
        tryCount = 0
        cookies = []
        while ( len(cookies) == 0  and tryCount < MAXTRYCOUNT) :
            cookies = MobileIndexCookie.getMobileIndexCookie()
            tryCount = tryCount + 1
            print(tryCount)
        secretCode = None
        for c in cookies :
            if c["name"] == "_secret":
                secretCode = c["value"]
                break

        if secretCode is None :
            print(cookies)
        return secretCode

if __name__ == "__main__":
    
    secretCode = MobileIndexCookie.getMobileIndexSecretCode()
    if type(secretCode) == str  :
        mobileIndexSecretCodeFile = "mobileIndexSecretCode.txt"
        with open(mobileIndexSecretCodeFile, "w") as f :
            f.write(secretCode)
    