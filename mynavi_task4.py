import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd

# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    if "chrome" in driver_path:
          options = ChromeOptions()
    else:
      options = Options()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    if "chrome" in driver_path:
        return Chrome(executable_path=os.getcwd() + "/" + driver_path,options=options)
    else:
        return Firefox(executable_path=os.getcwd()  + "/" + driver_path,options=options)


def searchWords():
    inputWord = ""
    checkStart = ""
    checkStop = ""
    searchWords = []

    while checkStart.upper() != "Y" or checkStart.upper() != "Q":
        checkStart = input("検索ツールを起動しますか。続ける場合：Y、中止する場合：Qと入力してください：")
        if checkStart.upper() == "Q":
            exit()
        elif checkStart.upper() == "Y":
            break

    while True:
        inputWord = input("検索ワードを入力してください。：")
        searchWords.append(inputWord)
        checkStop = input("入力を続けますか。起動する場合：Y、中止する場合：Qと入力してください：")
        if checkStop.upper() == "Q":
            break

    return searchWords

# main処理
def main():
    temp_keyword = []
    temp_keyword = searchWords()
    # temp_keyword = ["高収入", "テレワーク", "愛知"]
    for search_keyword in temp_keyword:

        # driverを起動
        if os.name == 'nt': #Windows
            driver = set_driver("chromedriver.exe", False)
        elif os.name == 'posix': #Mac
            driver = set_driver("chromedriver", False)
        # Webサイトを開く
        driver.get("https://tenshoku.mynavi.jp/")
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')

        # 検索窓に入力
        driver.find_element_by_class_name(
            "topSearch__text").send_keys(search_keyword)
        # 検索ボタンクリック
        driver.find_element_by_class_name("topSearch__button").click()

        while True:
            try:
                # ページ終了まで繰り返し取得
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # driver.execute_script("window.scrollTo(520, 500);")
              # driver.execute_script("arguments[0].click();", element)
                # # 検索結果の一番上の会社名を取得
                name_list = driver.find_elements_by_class_name("cassetteRecruit__name")

            # 空のDataFrame作成
                df = pd.DataFrame()

            # 1ページ分繰り返し
                print(len(name_list))
                for name in name_list:
                    print(name.text)
                    # DataFrameに対して辞書形式でデータを追加する
                    df = df.append(
                        {"会社名": name.text, 
                            "項目B": "",
                            "項目C": ""}, 
                            ignore_index=True)
            #     driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div/nav[2]/ul/li[]/a").location_once_scrolled_into_view
            #     driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div/nav[2]/ul/li[*]/a").click()
                # driver.find_element_by_xpath("//a[@class='iconFont--arrowLeft']").location_once_scrolled_into_view
                # driver.find_element_by_xpath("//a[@class='iconFont--arrowLeft']").click
                url = driver.find_element_by_class_name("iconFont--arrowLeft").get_attribute("href")
                driver.get(url) 
            except:
                break


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
     main()