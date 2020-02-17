import logging

logging.basicConfig(
    filename="masterCatalog.log",
    filemode="a",
    format=("%(asctime)s:%(levelname)s:%(message)s"),
    level=logging.INFO
)

class Log:
  def __init__(self):
    self.log = logging.getLogger()
