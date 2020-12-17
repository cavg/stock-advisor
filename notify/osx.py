import os

class Osx(object):
  """
  docstring
  """
  def __init__(self):
    pass

  @classmethod
  def notify(self, title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))