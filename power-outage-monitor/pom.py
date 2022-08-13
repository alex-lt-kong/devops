#!/usr/bin/python3

import datetime as dt
import os
import pandas as pd

from emailer import emailer

apc_log_path = '/var/log/apcupsd.events'  

def main() -> int:
  
  df = pd.read_csv(
    apc_log_path, delimiter='  ', engine='python', names=['Time', 'Message'], header=None
  )
  df['Time'] = df['Time'].str[:-6]
  df['Time'] =  pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S').dt.to_pydatetime()
  df = df[df['Time'] > (dt.datetime.now() - dt.timedelta(days=7))]
  df_pf = df[df['Message'] == 'Power failure.']
  df_bpe = df[df['Message'] == 'Battery power exhausted.']
  if df_pf.shape[0] == 0 and df_bpe.shape[0] == 0:
    return 0
  emailer.send_email_from_settings(
    settings_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'),
    subject='APC Power Outage Report',
    mainbody=f'power_failure_count: {df_pf.shape[0]}, battery_exhaused_count: {df_bpe.shape[0]}:\n{df}'
  )
  return 0

if __name__ == '__main__':

  main()
