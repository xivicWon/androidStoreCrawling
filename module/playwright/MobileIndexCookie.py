from playwright.sync_api import sync_playwright

class MobileIndexCookie() : 
        
    @staticmethod
    def getMobileIndexCookie() :
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("https://www.mobileIndex.com")
            return page.context.cookies()


    @staticmethod
    def getMobileIndexSecretCode()-> str:
        cookies = MobileIndexCookie.getMobileIndexCookie()
        secretCode = ""
        for c in cookies : 
            if c["name"] == "_secret":
                secretCode = c["value"]
                break
        return secretCode