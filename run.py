from prise_sys import *
from product_sys import *
from main import *
from log_sys import *

if __name__ == '__main__':
    print('http://192.168.0.15:8361/start')
    app.run(debug=True, host='192.168.0.15', port=8361)


