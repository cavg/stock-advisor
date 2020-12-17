#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import statistics
from datetime import datetime
from notify.osx import Osx

class Fintual(object):
  """
  docstring
  """
  def __init__(self,logging, token, session):
    # self.risky = {}
    # self.moderate = {}
    # self.conservative = {}

    # self._get_risky_norris()
    # self._get_moderate_pit()
    # self._get_conservative_clonney()

    self.token = token 
    self.session = session
    self.logging = logging

  def _get_stats(self, url, storage):
    headers = {
        'authority': 'fintual.cl',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/84.0.4147.89 Safari/537.36',
        'accept': '*/*',
        'origin': 'https://oaestay.github.io',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://oaestay.github.io/',
        'accept-language': 'es,en-US;q=0.9,en;q=0.8',
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
      res = r.json()
      for price in res["data"]:
        storage[price["attributes"]["date"]] = {'price':price["attributes"]["price"]}
      return True
    else:
      self.logging.error("Error getting info %s status_code: %d" % (url,r.status_code))
      return None

  def _get_risky_norris(self):
    self._get_stats("https://fintual.cl/api/real_assets/186/days", self.risky)

  def _get_moderate_pit(self):
    self._get_stats("https://fintual.cl/api/real_assets/187/days", self.moderate)

  def _get_conservative_clonney(self):
    self._get_stats("https://fintual.cl/api/real_assets/188/days", self.conservative)

  def get_performance(self, goalId):
    URL = 'https://fintual.cl/app/goals/%s/performance' % goalId
    headers = {
      'accept':'application/json',
      'accept-language':'es,en-US;q=0.9,en;q=0.8',
      'authority':'fintual.cl',
      'content-type':'application/json',
      'referer':'https://fintual.cl/app/goals/%s' % goalId,
      'sec-fetch-dest':'empty',
      'sec-fetch-mode':'cors',
      'sec-fetch-site':'same-origin',
      'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
      'x-csrf-token':self.token
    }
    cookies = {
      '_fintual_session_cookie':self.session
    }
    r = requests.get(URL, headers=headers, cookies=cookies)
    data = {}
    
    if r.status_code == 200:
      res = r.json()
      fintuality = res["data"]["attributes"]["performance"][1]
      if fintuality['identifier'] != "fintual":
        self.logging.error("Error getting data from your goals")
        exit(1)
      for entry in fintuality["data"]:
        d = datetime.fromtimestamp(entry["date"]/1000)
        format_date = "%Y-%m-%d"
        price = int(round(entry["value"],0))
        data[d.strftime(format_date)] = price
      dates = list(data.keys())
      values = {data[key] for key in data}
      minimum, maximum = min(values), max(values)
      return data, dates, values, minimum, maximum, int(round(statistics.mean(values),0))
    else:
      self.logging.error("Error getting goal %s status_code: %d" % (goalId,r.status_code))
      Osx.notify('Stock Error', 'Token invalido', "Status code %d" % r.status_code)
      exit(1)

  def get_opportunities(self, data, dates, threshold):
    opportunities_high = {}
    opportunities_low = {}
    i = len(dates)-1
    while i > 0:
      diff = data[dates[i]] - data[dates[i-1]]
      if diff < threshold*-1:
        opportunities_low[dates[i]] = {'precio':data[dates[i]], 'diff':diff}
      if diff > threshold:
        opportunities_high[dates[i]] = {'precio':data[dates[i]], 'diff':diff}
      i = i - 1
    return opportunities_high, opportunities_low

if __name__ == "__main__":
    f = Fintual()
    # data, dates, values, minimum, maximum, media, rango = f.get_myown_performance(4339160822)
    # print("min:%s  max:%s media:%s rango:%s" % (minimum, maximum, media, rango))
    # f.get_opportunities(data, dates, -2000)

    data, dates, values, minimum, maximum, media, rango = f.get_myown_performance(1399180520)
    print("min:%s  max:%s media:%s rango:%s" % (minimum, maximum, media, rango))
    f.get_opportunities(data, dates, -30000)

    
    