import datetime
import csv
import json
import operator

MENU = '''
1. Load trading data
2. Load current stock prices
3. Manually enter a new trade
4. View trading data
5. View current portfolio
6. Save trading data
7. Quit'''

def main():
    trading_data = []
    current_prices = {}

    print("Welcome to the Trader Assistant")
    print("Programmed by Michelle Gracie")
    print('------------------------------')

    print("Please choose from the options below: ")
    print(MENU)

    choice = input(">").upper()

    while choice != '7':
        if choice == '1':
            trading_data = load_trading_data()
            trading_data.sort(key=operator.itemgetter(4))
        elif choice == '2':
            current_prices = load_stock_prices()
        elif choice == '3':
            trading_data = enter_trade(trading_data)
        elif choice == '4':
            if not trading_data:
                print("No trading data found")
            else:
                view_trading(trading_data)
        elif choice == '5':
            if not trading_data:
                print("No trading data found")
            else:
                view_portfolio(trading_data, current_prices)
        elif choice == '6':
            save_trading(trading_data)
        else:
            print()
            print("Invalid option!")
        print(MENU)
        choice = input(">>>").upper()
    print('Thanks for using the Trade Assistant')

def validate_filename(file_name, ext):
    is_file_valid = False
    while not is_file_valid:
        try:
            if file_name == '':
                print("Cannot be blank.")
                file_name = input("Enter the file name: ")
            elif file_name.split('.')[1] != ext:
                print("File type incorrect.")
                file_name = input("Enter the filename: ")
            else:
                is_file_valid = True
        except IndexError:
            print("Please enter full filename including extension")
            file_name = input("Enter filename: ")
    return file_name


def load_trading_data():
    # open the csv file supplied by the user and read the data
    temp_list = []
    file_read = False
    trade_file = input("Enter the file name: ")
    valid_trade_name = validate_filename(trade_file, 'csv')
    while not file_read:
        try:
            file_in = open(valid_trade_name, 'r', newline='')
            csv_reader = csv.reader(file_in)
            file_read = True
            temp_list = list(csv_reader)
            for item in temp_list:
                if item[1] == 'b':
                    item[1] = 'BUY'
                else:
                    item[1] = 'SELL'
                item[2] = int(item[2])
                item[3] = float(item[3])
                item[4] = datetime.datetime.strptime(item[4], '%Y-%m-%d').date()
            count_processed = len(temp_list)
            print(count_processed, " trades processed")
            file_in.close()
            return temp_list

        except FileNotFoundError:
            print("File not found.")
            trade_file = input("Enter the file name: ")
            valid_trade_name = validate_filename(trade_file,'csv')
        except ValueError:
            print("Error with file format")
            temp_list = []
            file_read = False
            trade_file = input("Enter the file name: ")
            valid_trade_name = validate_filename(trade_file, 'csv')
        except IOError:
            print("Error reading the file")
            trade_file = input("Enter the file name: ")
            valid_trade_name = validate_filename(trade_file, 'csv')

def load_stock_prices():
    stocks = {}
    stock_file = input("Enter the file name: ")
    valid_stock_name = validate_filename(stock_file, 'json')
    is_file_read = False
    while not is_file_read:
        try:
            file_in = open(valid_stock_name, 'r')
            stocks = json.load(file_in)
            is_file_read = True
            print('Loaded', len(stocks), 'stock prices')
            file_in.close()
        except FileNotFoundError:
            print("File not found")
            stock_file = input("Enter the file name: ")
            valid_stock_name = validate_filename(stock_file,'json')
        except ValueError:
            print("Error with file format")
            stock_file = input("Enter the file name: ")
            valid_stock_name = validate_filename(stock_file, 'json')
    return stocks


def enter_trade(trade_data):
    new_trade = []
    # get the ticker
    ticker = input("Ticker: ")
    while ticker == '':
        print("Cannot be blank.")
        ticker = input("Ticker: ")
    # get buy or sell (b or s)
    buy_or_sell = input("Buy or sell (b/s): ").lower()
    while buy_or_sell.lower() != 'b' and buy_or_sell.lower() != 's':
        # can only be b or s
        print("Please enter b or s.")
        buy_or_sell = input("Buy or sell (b/s): ").lower()
    # get the quantity
    quantity = input("Quantity of stock: ")
    is_an_integer = False
    while not is_an_integer:
        try:
            int_quantity = int(quantity)
            if int_quantity <= 0 or int_quantity % 1 != 0:
                print("Please enter a positive whole number")
                quantity = input("Quantity of stock: ")
            else:
                is_an_integer = True
        except ValueError:
            print("Please enter a positive whole number")
            quantity = input("Quantity of stock: ")
    # dollar value
    dollar_value = input("Total cost (including brokerage): ")
    is_float = False
    try:
        float(dollar_value)
        is_float = True
    except ValueError:
        is_float = False
    if is_float:
        while float(dollar_value) <= 0:
            print("Please enter a positive number")
            dollar_value = input("Total cost (including brokerage): ")
    else:
        print("Please enter a positive number")
        dollar_value = input("Total cost (including brokerage): ")
    dollar_value = float(dollar_value)
    # get the date
    date_format = '%Y-%m-%d'
    trade_date_string = input("Date (yyyy-mm-dd): ")
    try:
        date_obj = datetime.datetime.strptime(trade_date_string, date_format)
        valid_date = True
    except ValueError:
        valid_date = False
    while not valid_date:
        print("Please enter a date in yyyy-mm-dd format.")
        trade_date_string = input("Date: ")
        try:
            date_obj = datetime.datetime.strptime(trade_date_string, date_format)
            valid_date = True
        except ValueError:
            valid_date = False
    # add all entered values to the list
    new_trade.append(ticker)
    if buy_or_sell == 'b':
        new_trade.append('BUY')
    else:
        new_trade.append('SELL')
    # create the list
    new_trade.append(int_quantity)
    new_trade.append(dollar_value)
    new_trade.append(date_obj.date())
    trade_data.append(new_trade)
    return trade_data


def view_trading(trades):
    name_found = False
    ticker = input("Ticker (blank for all): ")
    # blank entered
    if ticker == '':
        data_sort = input("Sort data in reverse chronological order? (y/n): ")
        if data_sort.lower() == 'y':
            trades.sort(key=operator.itemgetter(4), reverse=True)
        elif data_sort.lower() == 'n':
            trades.sort(key=operator.itemgetter(4))
        else:
            data_sort = input("Sort data in reverse chronological order? (y/n): ")
            if data_sort.lower() == 'y':
                trades.sort(key=operator.itemgetter(4), reverse=True)
            elif data_sort.lower() == 'n':
                trades.sort(key=operator.itemgetter(4))
        for name in trades:
            print(f"{name[4]} {name[0]:<10} {name[1]:>4} {name[2]: >10} for $ {name[3]:>10.2f}")
    elif ticker != '':
        for name in trades:
            if ticker.upper() == name[0].upper():
                name_found = True
        if not name_found:
            print("No trades found for that ticker symbol")
        else:
            # ticker was found in list so get order and print it
            data_sort = input("Sort data in reverse chronological order? (y/n): ")
            if data_sort.lower() == 'y':
                trades.sort(key=operator.itemgetter(4), reverse=True)
            elif data_sort.lower() == 'n':
                trades.sort(key=operator.itemgetter(4))
            else:
                data_sort = input("Sort data in reverse chronological order? (y/n): ")
                if data_sort.lower() == 'y':
                    trades.sort(key=operator.itemgetter(4), reverse=True)
                elif data_sort.lower() == 'n':
                    trades.sort(key=operator.itemgetter(4))
            for name in trades:
                if ticker.upper() == name[0].upper():
                    print(f"{name[4]} {name[0]:<10}  {name[1]:>4} {name[2]: >10} for $ {name[3]:>10.2f}")

def view_portfolio(trades, prices):
    portfolio = {}  # to store portfolio of stocks
    for trade in trades:
        if trade[0] not in portfolio:
            portfolio[trade[0]] = trade[2]
        elif trade[0] in portfolio:
            portfolio[trade[0]] = portfolio[trade[0]] + trade[2]
    for key in portfolio:
        print(key)
        print(f'Total units: {portfolio[key]:>12.0f}')
        if key in prices:
            total_value = operator.mul(prices[key], portfolio[key])
            print(f'Total value: {total_value:>12.2f}')
        else:
            print('Current value unknown')
    # check prices - if there is a price but no units print 0 for units and value
    for key in prices:
        if key not in portfolio:
            print(key)
            print(f'Total units: {0:>12}')
            print(f'Total value: {0.0:>12.2f}')

def save_trading(trades):
    user_filename = input("Enter filename: ")
    valid_file_name = validate_filename(user_filename, 'csv')
    is_file_written = False
    while not is_file_written:
        try:
            file_out = open(valid_file_name, 'w', newline='')
            csv_writer = csv.writer(file_out)
            for trade in trades:
                csv_writer.writerow(trade)
            is_file_written = True
            print("Data written to ", valid_file_name)
            file_out.close()
        except IOError:
            print("Error opening the file")
            is_file_written = False
            user_filename = input("Enter filename: ")
            valid_filename = validate_filename(user_filename, 'csv')


main()
