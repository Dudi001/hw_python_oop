import datetime as dt


class Record:
    DATE_FORMAT = '%d.%m.%Y'
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()

#Родительский класс.
class Calculator: 
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
        date_today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == date_today)
    
    #Расчет денег\калорий за последние 7 дней.
    def get_week_stats(self):
        date_today = dt.date.today()
        week_delta = date_today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if date_today >= record.date >= week_delta)

#Калькулятор калорий.
class CaloriesCalculator(Calculator):
    def __str__(self):
        return f"Лимит на сегодня {self.limit}."
    
    TEXT_CALORIES = ("Сегодня можно съесть что-нибудь ещё, "
                 "но с общей калорийностью не более {value} кКал") 
    TEXT_2_CALORIES = "Хватит есть!"

    #Вывод количества калорий.
    def get_calories_remained(self):
        remainder_day = self.day_remainder()
        if remainder_day > 0:
            return self.TEXT_CALORIES.format(value=remainder_day)                
        else:
            return self.TEXT_2_CALORIES

#Калькулятор денег.
class CashCalculator(Calculator):
    RUB_RATE = float(1.0)
    USD_RATE = float(60.0)
    EURO_RATE = float(70.0)
    
    CURRENCIES = {
        'rub': (RUB_RATE, 'руб'),
        'usd': (USD_RATE, 'USD'),
        'eur': (EURO_RATE, 'Euro')
    }

    #Конвертация валюты и условия вывода.
    def get_today_cash_remained(self, currency='rub'):
        remainder_day = self.day_remainder()
        if remainder_day == 0:
            return f'Денег нет, держись'
        
        #Распаковываем словарь и округляем валюту до сотых.
        rate, currency_name = self.CURRENCIES[currency]
        spent_by_currency = round(abs(remainder_day)/ rate, 2)
        
        if remainder_day > 0:
            return (f'На сегодня осталось {spent_by_currency}'
                f' {currency_name}')
        else:
             return (f'Денег нет, держись: твой долг - '
                    f'{spent_by_currency} {currency_name}')

if __name__ == '__main__':
    pass
      