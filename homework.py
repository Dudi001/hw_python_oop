import datetime as dt

#Данный класс служит для записи входных данных.
class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

#Родительский класс.
class Calculator:
    deltime = dt.timedelta(days=7)
    datenow = dt.datetime.now().date()
    
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    #Расчёт остатка.
    def day_remainder(self):
        remainder_day = self.limit - self.get_today_stats()
        return remainder_day
    
    #Сохраняет новую запись в списке.
    def add_record(self, record):
        self.records.append(record)
    
    #Количество потраченных денег за сегодня.
    def get_today_stats(self):
        cash_day = 0
        
        for i in self.records:
            if i.date == self.datenow:
                cash_day += i.amount
        return cash_day
    
    #Расчет денег\калорий за последние 7 дней.
    def get_week_stats(self):
        last_seven = self.datenow - self.deltime
        seven_stats = 0
        
        for i in self.records:
            if last_seven < i.date <= self.datenow:
                seven_stats += i.amount
        return seven_stats

#Калькулятор калорий.
class CaloriesCalculator(Calculator):
    def __str__(self):
        return f"Лимит на сегодня {self.limit}."
    
    #Вывод количества калорий.
    def get_calories_remained(self):
        remainder_day = self.day_remainder()
        
        if remainder_day > 0:
            return (f"Сегодня можно съесть что-нибудь ещё, " 
                f"но с общей калорийностью не более {remainder_day} кКал")
        else:
            return f"Хватит есть!"

#Калькулятор денег.
class CashCalculator(Calculator):
    RUB_RATE = 1.0
    EURO_RATE = 91.3222
    USD_RATE = 77.3262
    
    #Конвертация валюты и условия вывода.
    def get_today_cash_remained(self, currency='rub'):
        currencies = {'rub': (self.RUB_RATE, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
            }
        
        remainder_day = self.day_remainder()
        
        if remainder_day == 0:
            return f'Денег нет, держись.'
        #Распаковываем словарь и округляем валюту до сотых.
        rate, currency_name = currencies[currency]
        spent_by_currency = round(abs(remainder_day) / rate, 2)
        
        if remainder_day > 0:
            return (f'На сегодня осталось - {remainder_day}'
                f' {currency_name}')
        else:
             return (f'Денег нет, держись: твой долг -'
                    f' {spent_by_currency} {currency_name}')

if __name__ == '__main__':
    pass

        
        


