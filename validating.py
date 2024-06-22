import hmac
import hashlib
from urllib.parse import unquote
from config import bot_token


def validate_init_data(init_data: str, bot_token: str):
     vals = {k: unquote(v) for k, v in [s.split('=', 1) for s in init_data.split('&')]}
     data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(vals.items()) if k != 'hash')

     secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
     h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)

     return h.hexdigest() == vals['hash'], vals

bot_token = '7159130073:AAE_7l-E7MhMoB-gIiXol6tsCeVSrFEySfM'

validate_string = 'query_id=AAG9v400AAAAAL2_jTRN4vng&user=%7B%22id%22%3A881704893%2C%22first_name%22%3A%22Gorilla%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22gorilla_bsrb%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1716209547&hash=62097dbe83d6655eb4136a96c5d68075d0ef66f49d6ad6fbd8635f2f5981bf98'


print(validate_init_data(validate_string, bot_token))

