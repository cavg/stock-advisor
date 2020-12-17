from fintual.client import Fintual
from notify.osx import Osx
import os, sys, traceback
import logging
from datetime import date, timedelta
from currencies import Currency

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.ERROR, datefmt='%Y-%m-%d %H:%M:%S')

try:
  token = os.getenv('FINTUAL_TOKEN')
  session = os.getenv('FINTUAL_SESSION')

  f = Fintual(logging, token, session)

  Goals = {
    "ref-muy-arriesgada":{'id':4339160822, 'threshold':2500},
    "ref-arriesgada":{'id':3819204621, 'threshold':2000},
    "ref-moderada":{'id':2068943138, 'threshold':1500},
    "ref-conservadora":{'id':1228386490, 'threshold':1200},
    "ref-muy-conservadora":{'id':4976310882, 'threshold':600},
    "inv-muy-arriesgada":{'id':1399180520, 'threshold':30000}
  }

  data, dates, _, _, _, _ = f.get_performance(Goals['inv-muy-arriesgada']['id'])
  high,low = f.get_opportunities(data, dates, Goals['inv-muy-arriesgada']['threshold'])

  print("Subidas %s\n" % high)
  print("Bajadas %s" % low)
  yesterday = date.today() - timedelta(days=1)
  day = yesterday.strftime("%Y-%m-%d")
  currency = Currency('CLP')
  if day in high or day in low:
    if day in high:
      money = currency.get_money_format(high[day]['diff'])
      Osx.notify('Stock', 'Subieron tus inversiones', str(money))
    if day in low:
      money = currency.get_money_format(low[day]['diff'])
      Osx.notify('Stock', 'Oportunidad de invertir', str(money))
  else:
    Osx.notify('Stock', 'Sin novedades', "keep calm")
except Exception:
  print("error %s" % traceback.format_exception(*sys.exc_info()))
