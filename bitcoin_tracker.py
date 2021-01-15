import os
import time
import smtplib
from selenium import webdriver
from yahoo_fin.stock_info import get_live_price
from yahoo_fin.stock_info import get_stats
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

strt_price = float(get_live_price('BTC-USD'))
print("Bitcoin price now:", strt_price)
print("Please enter the drop percentage point: ")
inp_perc = float(input())
print(inp_perc)

print("Please enter your email address: ")
send_to = str(input())

perc_calculated = strt_price - strt_price * inp_perc / 100
print("Percentage:", perc_calculated)


def check_price():
	while True:
		bitcoin_price = float(get_live_price('BTC-USD'))
		print("Bitcoin price now: " + str(bitcoin_price))
		print("Starting price: ", strt_price)
		print("---------------------------------------------")
		if (bitcoin_price < perc_calculated):
			browser = webdriver.Chrome(executable_path=r"your Chrome Driver path\chromedriver.exe")
			browser.get('https://www.binance.com/en/trade/BTC_USDT')
			browser.refresh()
			time.sleep(15)
			browser.save_screenshot('btc.png')
			browser.close()
			img = 'btc.png'

			send_mail(img)
			print('Email alert has been sent.')
			exit()
		time.sleep(60)


def send_mail(img):
	img_data = open(img, 'rb').read()
	msg = MIMEMultipart()
	msg['Subject'] = 'Bitcoin Price Dropped ' + str(inp_perc) + "%"
	msg['From'] = 'your email@gmail.com'
	msg['To'] = send_to

	text = MIMEText("Bitcoin price: " + str(get_live_price('BTC-USD')))
	stats_html = get_stats('BTC-USD').to_html()
	stats = MIMEText(stats_html, 'html')
	text2 = MIMEText("\nCheck more data and details at Binance: https://www.binance.com/en/trade/BTC_USDT")

	msg.attach(text)
	msg.attach(stats)
	msg.attach(text2)

	image = MIMEImage(img_data, name=os.path.basename(img))
	msg.attach(image)

	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login('your email@gmail.com', 'your password')
	s.sendmail('your email@gmail.com',
               send_to,
               msg.as_string())
	s.quit()


while True:
	check_price()