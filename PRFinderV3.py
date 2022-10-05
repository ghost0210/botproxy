import datetime
import S5Crypto
import time
import socket
import start
import threading
import logging
import time
import time_calc

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)-s) %(message)s')

def prfind_e(bot,chat,time_calc,inicio,username,jdb,user_info,text):
    rango_min = str(str(text).split('-')[0]).split(' ')[1]
    rango_max = str(str(text).split('-')[1]).split(' ')[0]
    pr_range_exced = 'Se recomienda que entre rango minimo y rango máximo haya una diferencia de hasta 1000 Puertos, no más pq podría demorar días...'
    if int(rango_max) - int(rango_min) < 1001:
        ip = str(text).split(' ')[2]
        msg_start = f"🛰<b> Buscando Proxy</b>!!\n<b>🌐 IP :</b> {ip}\n<b>⏯ PUERTOS :</b> {rango_min} - {rango_max}\n\n<i>⏳ Por favor espere .....</i>"
        msg_start1 = "\n➖➖➖➖➖➖➖\n\n\n➖➖➖➖➖➖➖"
        msg_succes = f"🛰<b> Proxy Encontrado</b>!!\n<b>🌐 IP :</b> {ip}\n<b>⏯ PUERTOS :</b> {rango_min} - {rango_max}\n🥳🎉🥳🎉🥳🎉🥳🎉🥳🎉\n<b>❗️ PROXY ENCONTRADO ❗️</b>"+"\n➖➖➖➖➖➖➖\n"
        error_pr_find = f"🛰 No Hubo Éxito Buscando Proxy!!\n\n❌ IP : {ip}\n\n❌ PUERTOS : {rango_min}-{rango_max}"
        lf = msg_start+"\n➖➖➖➖➖➖➖\n"
        rg = "\n➖➖➖➖➖➖➖"
        info = "Buscando proxy...\n"
        print(info)
        try:
            getUser = user_info
            if getUser:
                getUser['rango_minimo'] = rango_min
                getUser['rango_maximo'] = rango_max
                getUser['ip'] = ip
                jdb.save_data_user(username,getUser)
                jdb.save()
        except:bot.sendMessage(chat,'✖️Error al Guardar IP y Rango de Puertos✖️')
        sms = bot.sendMessage(chat_id=chat,parse_mode="HTML",text=msg_start+msg_start1)
        time.sleep(1.5)
        bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=lf+info+rg)
        for port in range(int(rango_min),int(rango_max)):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                result = sock.connect_ex((ip,port))
                if result == 0:
                    pr_find=1
                    info = f"Puerto abierto!\nPuerto: {port}"
                    bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=msg_succes+info+rg)
                    proxy = f'{ip}:{port}'
                    proxy_new = S5Crypto.encrypt(f'{proxy}')
                    time.sleep(5)
                    time_calc.calc_time_s(inicio,proxy_new,chat,sms,bot)
                    bot.pinChatMessage(chat_id=chat, message_id=sms.message_id)
                    start.create_historial(username,proxy_new,ip,port)
                    sock.close()
                    break
                else:
                    pr_find=0
                    info = f"Error...Buscando...\nBuscando en el puerto: {str(int(port)+1)}"
                    start.porcentaje(rango_max,rango_min,port,info,bot,chat,sms,ip)
                    sock.close()
            except:
                info = f"<b>IP Inválida ❌ !!\n\nIP: </b><pre>{str(ip)}</pre>"
                bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=info)
                sock.close()
                break
        try:
            if pr_find==0:
                time_calc.calc_time_e(inicio,chat,sms,bot,error_pr_find)
            else:pass
        except Exception as ex:print(str(ex))
        return
    else:bot.sendMessage(chat_id=chat,parse_mode="HTML",text=pr_range_exced)

def prfind_p(user_info,bot,chat,username,time_calc):
    ini = datetime.datetime.now()
    inicio = datetime.datetime(ini.year, ini.month, ini.day, ini.hour, ini.minute, ini.second)
    try:
        getUser = user_info
        if getUser:
            ip = getUser['ip']
            rango_min = getUser['rango_minimo']
            rango_max = getUser['rango_maximo']
    except:
        rango_min = "2080"
        rango_max = "2085"
        ip = "181.225.253.188"
    msg_start = f"🛰<b> Buscando Proxy</b>!!\n<b>🌐 IP :</b> {ip}\n<b>⏯ PUERTOS :</b> {rango_min} - {rango_max}\n\n<i>⏳ Por favor espere .....</i>"
    msg_start1 = "\n➖➖➖➖➖➖➖\n\n\n➖➖➖➖➖➖➖"
    msg_succes = f"🛰<b> Proxy Encontrado</b>!!\n<b>🌐 IP :</b> {ip}\n<b>⏯ PUERTOS :</b> {rango_min} - {rango_max}\n🥳🎉🥳🎉🥳🎉🥳🎉🥳🎉\n<b>❗️ PROXY ENCONTRADO ❗️</b>"+"\n➖➖➖➖➖➖➖\n"
    error_pr_find = f"🛰 No Hubo Éxito Buscando Proxy!!\n\n❌ IP : {ip}\n\n❌ PUERTOS : {rango_min}-{rango_max}"
    lf = msg_start+"\n➖➖➖➖➖➖➖\n"
    rg = "\n➖➖➖➖➖➖➖"
    info = "Buscando proxy...\n"
    print(info)
    sms = bot.sendMessage(chat_id=chat,parse_mode="HTML",text=msg_start+msg_start1)
    time.sleep(1.5)
    bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=lf+info+rg)
    for port in range(int(rango_min),int(rango_max)):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex((str(ip),port))
            if result == 0:
                pr_find=1
                info = f"Puerto abierto!\nPuerto: {port}"
                bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=msg_succes+info+rg)
                proxy = f'{ip}:{port}'
                proxy_new = S5Crypto.encrypt(f'{proxy}')
                time.sleep(5)
                time_calc.calc_time_s(inicio,proxy_new,chat,sms,bot)
                bot.pinChatMessage(chat_id=chat, message_id=sms.message_id)
                start.create_historial(username,proxy_new,ip,port)
                sock.close()
                break
            else:
                pr_find=0
                info = f"Error...Buscando...\nBuscando en el puerto: {str(int(port)+1)}"
                start.porcentaje(rango_max,rango_min,port,info,bot,chat,sms,ip)
                sock.close()
        except:
            info = f"<b>IP Inválida ❌ !!\n\nIP: </b><pre>{str(ip)}</pre>"
            bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=info)
            sock.close()
            break
    try:
        if pr_find==0:
            time_calc.calc_time_e(inicio,chat,sms,bot,error_pr_find)
        else:pass
    except Exception as ex:print(str(ex))
    return

def pr_find(id_persona,data,sms,bot,update,pfinal,nhilos,inicio):
    #logging.info("Buscando Puertos abiertos " + str(id_persona))
    userid = update.effective_user.id
    for port in range(id_persona,pfinal,nhilos):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ip = data
            result = sock.connect_ex((str(ip),port))
            if result == 0:
                info = f"💥Puerto abierto!\n💥Puerto: {port}"
                proxy = f'{ip}:{port}'
                start.create_find(userid,proxy)
                print('🔰 '+proxy)
                userid = update.effective_user.id
                ruta = 'pr_finds'
                archivo = open(f'{ruta}/{userid}.txt')
                linea=archivo.readlines()
                aho = datetime.datetime.now()
                ahora = datetime.datetime(aho.year, aho.month, aho.day, aho.hour, aho.minute, aho.second)
                tt = ahora - inicio
                bot.editMessageText(chat_id=update.message.chat.id,parse_mode='HTML',message_id=sms.message_id,text='<b>🛰 Buscando Proxy!!</b>\n<b>🌐 IP : </b>{}\n<b>🔌 PUERTOS ABIERTOS : </b>{}\n<b>📡 ESCANEANDO PUERTOS!!</b>\n➖➖➖➖➖➖➖\n<b>🕰 TT : </b>{}\n➖➖➖➖➖➖➖'.format(ip,str(len(linea)),tt))
                sock.close()
            else:
                info = f"Error...Buscando...\nBuscando en el puerto: {str(int(port)+1)}\n"
                sock.close()
        except Exception as ex:
            print(str(ex))
            info = f"IP Inválida ❌ !!\n\nIP: {str(ip)}"
            print(info)
            sock.close()
            break
    return

def pr_find_thread(text,bot,update):
    bot = bot
    ip = str(text).split(' ')[1]
    ini = datetime.datetime.now()
    inicio = datetime.datetime(ini.year, ini.month, ini.day, ini.hour, ini.minute, ini.second)
    aire=' '
    ndpp = 0
    nhilos = 240
    pfinal = 65535
    texto1 = '<b>🛰 Buscando Proxy!!</b>\n<b>🌐 IP : </b>{}\n<b>🔌 PUERTOS ABIERTOS : </b>{}\n<b>📡 ESCANEANDO PUERTOS!!</b>\n➖➖➖➖➖➖➖\n<b>🕰 TT : </b>{}\n➖➖➖➖➖➖➖'.format(ip,ndpp,aire)
    sms = bot.sendMessage(chat_id=update.message.chat.id,parse_mode='HTML',text=texto1)

    for i in range(0,nhilos):
        i += 1
        if i != nhilos:
            t = threading.Thread(name='hilo'+str(i),target=pr_find,args=(i, ip, sms, bot, update, pfinal, nhilos, inicio))
            t.start()
        else :
            tf = threading.Thread(name='hilof',target=pr_find,args=(i, ip, sms, bot, update, pfinal, nhilos, inicio))
            tf.start()
    tf.join()
    t.join()
    aho = datetime.datetime.now()
    ahora = datetime.datetime(aho.year, aho.month, aho.day, aho.hour, aho.minute, aho.second)
    tt = ahora - inicio
    userid = update.effective_user.id
    ruta = 'pr_finds'
    archivo = open(f'{ruta}/{userid}.txt')
    linea=archivo.readlines()
    texto2 = '<b>🛰 Buscando Proxy!!</b>\n<b>🌐 IP : </b>{}\n<b>🔌 PUERTOS ABIERTOS : </b>{}\n<b>🛰 PROCESO FINALIZADO!!</b>\n➖➖➖➖➖➖➖\n<b>🕰  TT : </b>{}\n➖➖➖➖➖➖➖'.format(ip,str(len(linea)),tt)
    bot.editMessageText(chat_id=update.message.chat.id,parse_mode='HTML',message_id=sms.message_id,text=texto2)
    archivo.close()
    start.view_pr(bot,update)




















#def pr_find_thread(text,bot,update):
#    bot = bot
#    ip = str(text).split(' ')[1]
#    ini = datetime.datetime.now()
#    inicio = datetime.datetime(ini.year, ini.month, ini.day, ini.hour, ini.minute, ini.second)
#    aire=' '
#    ndpp = 0
#    pfinal = 65535
#    texto1 = '''
#<b>🛰 Buscando Proxy!!</b>
#<b>🌐 IP : </b>{}
#<b>🔌 PUERTOS ABIERTOS : </b>{}
#<b>🕰 TIEMPO TRANSCURRIDO :</b>
#➖➖➖➖➖➖➖
#{}
#➖➖➖➖➖➖➖
#    '''.format(ip,ndpp,aire)
#    sms = bot.sendMessage(chat_id=update.message.chat.id,parse_mode='HTML',text=texto1)
#    #print(sms.message_id)
#
#    t1 = threading.Thread(name='hilo1',target=pr_find,args=(0, ip, sms, bot, update, pfinal))
#    t2 = threading.Thread(name='hilo2',target=pr_find,args=(1, ip, sms, bot, update, pfinal))
#    t3 = threading.Thread(name='hilo3',target=pr_find,args=(2, ip, sms, bot, update, pfinal))
#    t4 = threading.Thread(name='hilo4',target=pr_find,args=(3, ip, sms, bot, update, pfinal))
#    t5 = threading.Thread(name='hilo5',target=pr_find,args=(4, ip, sms, bot, update, pfinal))
#    t6 = threading.Thread(name='hilo6',target=pr_find,args=(5, ip, sms, bot, update, pfinal))
#    t7 = threading.Thread(name='hilo7',target=pr_find,args=(6, ip, sms, bot, update, pfinal))
#    t8 = threading.Thread(name='hilo8',target=pr_find,args=(7, ip, sms, bot, update, pfinal))
#    t9 = threading.Thread(name='hilo9',target=pr_find,args=(8, ip, sms, bot, update, pfinal))
#    t10 = threading.Thread(name='hilo10',target=pr_find,args=(9, ip, sms, bot, update, pfinal))
#
#    time.sleep(0.2)
#    t1.start()
#    time.sleep(0.2)
#    t2.start()
#    time.sleep(0.2)
#    t3.start()
#    time.sleep(0.2)
#    t4.start()
#    time.sleep(0.2)
#    t5.start()
#    time.sleep(0.2)
#    t6.start()
#    time.sleep(0.2)
#    t7.start()
#    time.sleep(0.2)
#    t8.start()
#    time.sleep(0.2)
#    t9.start()
#    time.sleep(0.2)
#    t10.start()
#
#    t1.join()
#    t2.join()
#    t3.join()
#    t4.join()
#    t5.join()
#    t6.join()
#    t7.join()
#    t8.join()
#    t9.join()
#    t10.join()
#
#    time.sleep(0.2)
#    barra = '\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
#    print(barra)
#    time_calc.calc_time(inicio)
#    print(barra)
#    print(str(ndpp))