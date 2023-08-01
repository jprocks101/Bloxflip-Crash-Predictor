from zenrows import ZenRowsClient
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from colorama import Fore, init, Style
import cloudscraper



def crash_scraper():
    url = "https://api.bloxflip.com/games/crash"
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    data = response.json()
    history = data["history"]
    crash_points = [points["crashPoint"] for points in history]
    return crash_points

def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def simple_linear():
    crash_data = crash_scraper()
    X = np.array(crash_data).reshape(-1, 1)
    y = np.arange(1, len(crash_data) + 1).reshape(-1, 1) 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    last_prediction = y_pred[-1][0]


    risky_prediction = np.percentile(crash_data, 75)


    safe_prediction = np.percentile(crash_data, 25)


    accuracy = mean_absolute_percentage_error(y_test, y_pred)


    print(Fore.YELLOW + "-> Prediction: {:.2f}".format(last_prediction) + Style.RESET_ALL)
    print(Fore.GREEN + "-> Safe Prediction: {:.2f}".format(safe_prediction) + Style.RESET_ALL)
    print(Fore.RED + "-> Risky Prediction: {:.2f}".format(risky_prediction) + Style.RESET_ALL)
    print(Fore.CYAN + "-> Accuracy: {:.2f}%".format(100 - accuracy) + Style.RESET_ALL)

simple_linear()

input(Fore.MAGENTA + "[-] Press Enter to exit...")
