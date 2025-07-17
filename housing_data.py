from playwright.sync_api import sync_playwright
import shutil
import json
chrome_path = shutil.which("google-chrome") or shutil.which("chrome") or "/opt/google/chrome/chrome"


all_data = []

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        executable_path=chrome_path
    )
    page = browser.new_page()
    page.goto("https://housing.com/in/buy/searches/P6xfqdsey6cc3d95hU2z1ye?gad_campaignid=21063166520&gclid=Cj0KCQjwss3DBhC3ARIsALdgYxMEVNxWBEBjW7T157k70Sll8LRR0ZCZfbUf0h7EMfAJKxAgkLBbUy8aAikREALw_wcB")

    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(3000)
    
    main_dev = page.locator(".css-1m1bruh")
    # print(main_dev)
    children = main_dev.locator(":scope > div")  # or parent.locator(":scope > div") for direct children only

    # Count and loop
    count = children.count()
    for i in range(count):
        print(f"Processing {i+1}/{count}")
        data = {}
        child = children.nth(i)
        
        # images
        imgs = child.locator(".a1uuj5tz._12yd1e8i")
        count_imgs = imgs.count()
        img_set = set()
        for j in range(count_imgs):
            img = imgs.nth(j)
            if img.count() > 0:
                img_set.add(img.get_attribute("src"))
        data["img"] = list(img_set)
    
        # title
        title = child.locator(".title-style")
        if title.count() > 0:
            data["title"] = title.text_content()
        
        #sub title
        sub_title = child.locator(".subtitle-style")
        if sub_title.count() > 0:
            data["sub_title"] = sub_title.text_content()
        
        # price
        price = child.locator(".slider-Wrapper.T_sliderWrapper._e21osq._tr161g._uc12yw._mkh2mm")
        if price.count() > 0:
            price = price.locator(":scope > div")
            count_price = price.count()
            price_set = []
            for j in range(count_price):
                price = price.nth(j)
                txt = price.locator(".T_configurationStyle._fc1h6o._ar1bp4._9s1txw._1gjugq9o._1rfayjp0._7l1472._r31e5h._frclma._g3exct._cs1nn1._c81fwx._bx1t02")
                if txt.count() > 0:
                    txt_w = txt.text_content()
                p = price.locator(".T_blackText._c8dlk8._7l1ulh.T_descriptionStyle._t91dk0._r31e5h._g3exct._csbfng._bx1t02")
                if p.count() > 0:
                    p_w = p.text_content()
                price_set.append({"title": txt_w, "price": p_w})
            data["price"] = price_set
        
        # description
        description = child.locator("._c81fwx._cs1nn1._g38jkm._fr1ti3._vy1wug._7ls3je._h312gs._kbqmn7od.T_dataPointStyle")
        if description.count() > 0:
            data["description"] = description.text_content()
        
        # url
        url = child.locator(".T_arrangeElementsInLine._cxftgi._0h1h6o._fcv2br._9s1txw")
        if url.count() > 0:
            url = url.locator("a")
            if url.count() > 0:
                data["url"] = url.get_attribute("href")
        
        all_data.append(data)
    browser.close()
    
with open("data.json", "w") as f:
    json.dump(all_data, f, indent=4)
