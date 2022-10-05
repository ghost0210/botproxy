import socket
import S5Crypto
import os
import time
from JDatabase import JsonDatabase

def create_historial(username,proxy_new,ip,port):
    ruta = 'historial'
    archivo = f'{ruta}/{username}.txt'
    try:
        if not os.path.exists(ruta):os.makedirs(ruta)
        if not os.path.exists(ruta):open(archivo, 'w')
        write='PROXY : '+str(proxy_new)
        write+=' -- IP : '+str(ip)
        write+=' -- PUERTO : '+str(port)+'\n'
        with open(archivo, 'a') as db :db.write(write)
    except Exception as ex:print(str(ex))

def create_find(userid,proxy):
    proxy_new = S5Crypto.encrypt(f'{proxy}')
    ruta = 'pr_finds'
    archivo = f'{ruta}/{userid}.txt'
    try:
        if not os.path.exists(ruta):os.makedirs(ruta)
        if not os.path.exists(ruta):open(archivo, 'w')
        write='PROXY : '+str(proxy_new)
        write+='  IP+PUERTO : '+str(proxy)+'\n'
        with open(archivo, 'a') as db :db.write(write)
    except Exception as ex:print(str(ex))

def view_db(chat,username,bot):
    ruta = 'historial'
    archivo = f'{ruta}/{username}.txt'
    try:
        with open(archivo, 'rb') as db, open("PR-FinderV2-Cuadrado.jpg", "rb") as miniatura:
            bot.sendChatAction(chat,"upload_document")
            bot.sendDocument(chat_id=chat, parse_mode='HTML', document=db, caption='📋 Historial 📋\n🧬 User : @'+username, thumb=miniatura)
    except:
        bot.sendMessage(chat,'😬 Ups ....\n» Todavía no tienes un Historial de Proxys — Puertos — IP\no :\n» El bot se reinició y se borraron todos los datos (historial,database)')

def view_pr(bot,update):
    userid = update.effective_user.id
    ruta = 'pr_finds'
    archivo = f'{ruta}/{userid}.txt'
    file = open(f'{ruta}/{userid}.txt')
    try:
        with open(archivo, 'rb') as db, open("PR-FinderV2-Cuadrado.jpg", "rb") as miniatura:
            bot.sendChatAction(update.message.chat.id,"upload_document")
            linea=file.readlines()
            total_lines=len(linea)
            file.close()
            bot.sendDocument(chat_id=update.message.chat.id, parse_mode='HTML', document=db, caption='<b>📋 PUERTOS ABIERTOS: </b>{}'.format(total_lines), thumb=miniatura)
        os.remove(archivo)
    except Exception as ex:
        bot.sendMessage(update.message.chat.id,'😬 Ups ....\n» '+str(ex))

def get_db(isadmin,bot,chat,getUser):
    if isadmin:
        with open("database.jdb", "rb") as db, open("PR-FinderV2-Cuadrado.jpg", "rb") as miniatura:
            bot.sendChatAction(chat,"upload_document")
            bot.sendDocument(chat_id=chat, parse_mode="HTML", document=db, caption='🛰 BASE DE DATOS 🛰', thumb=miniatura)
    elif getUser:
        bot.sendMessage(chat,'✖️No Tiene Permiso✖️')

def start_i(username,userid,userdata,isadmin,listar,grupo):
    msg = 'Bienvenido al BOT PR-Finder V2 🛰\n'
    msg+= 'PR-FinderV2.2🛰 | Code by : @AresDza\n\n'
    msg+= '🧬 USERNAME : @' + str(username)+'\n\n'
    msg+= '🆔 ID : <pre>' + str(userid)+'</pre>\n\n'
    msg+= '🛰 IP : ' + str(userdata['ip'])+'\n'
    listado = '🗒 LISTAR : SI'
    if listar:listado = '🗒 LISTAR : NO'
    msg+= listado + '\n'
#    group = '👥 GRUPO [VIP]'
#    if grupo:group = '👥 GRUPO : @'+str(userdata['grupo'])+'\n'
#    msg+= group + '\n'
    msg+= '▶️ PUERTO INICIAL : ' + str(userdata['rango_minimo'])+'\n'
    msg+= '⏹ PUERTO FINAL : ' + str(userdata['rango_maximo'])+'\n\n'
    stat = '👤 [USER]'
    if isadmin:stat = '👑 [OWNER]'
    msg+= stat + '\n'
    return msg

def porcentaje(rango_max,rango_min,port,info,bot,chat,sms,ip):
    maxim = int(rango_max) - int(rango_min)
    actual = (int(port)+1) - int(rango_min)
    porcent = actual / maxim
    porcent *= 100
    porcent = int(str(porcent).split('.')[0])
    if porcent in range(0,10):
        n = '⬛️'*0
        b = '⬜️'*10
    elif porcent in range(10,20):
        n = '⬛️'*1
        b = '⬜️'*9
    elif porcent in range(20,30):
        n = '⬛️'*2
        b = '⬜️'*8
    elif porcent in range(30,40):
        n = '⬛️'*3
        b = '⬜️'*7
    elif porcent in range(40,50):
        n = '⬛️'*4
        b = '⬜️'*6
    elif porcent in range(50,60):
        n = '⬛️'*5
        b = '⬜️'*5
    elif porcent in range(60,70):
        n = '⬛️'*6
        b = '⬜️'*4
    elif porcent in range(70,80):
        n = '⬛️'*7
        b = '⬜️'*3
    elif porcent in range(80,90):
        n = '⬛️'*8
        b = '⬜️'*2
    elif porcent in range(90,100):
        n = '⬛️'*9
        b = '⬜️'*1
    elif porcent == 100:
        n = '⬛️'*10
        b = '⬜️'*0

    if porcent != 100 :porcente = '☑️'
    else :porcente = '✅'
    progress = n+b

    msg = '🛰 <b>Buscando Proxy</b>!!\n<b>🌐 IP : </b>'+str(ip)+'\n'
    msg+='<b>⏯ PUERTOS : </b>'+str(rango_min)+'-'+str(rango_max)
    msg+='\n'+progress
    msg+='\n'+porcente+'<b> PORCIENTO : </b>'+str(porcent)+'%\n➖➖➖➖➖➖➖\n'
    msg+=info+'\n➖➖➖➖➖➖➖'
    bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=msg)

def ip_finder(text,bot,chat,getUser,jdb,username):
    ip_range = (str(text).split(' ')[1]).split('-')[1]
    ip = ((str(text).split(' ')[1]).split('-')[0]).split('.')[3]
    ip_form = str(((str(text).split(' ')[1]).split('-')[0]).split('.')[0]+'.'+((str(text).split(' ')[1]).split('-')[0]).split('.')[1]+'.'+((str(text).split(' ')[1]).split('-')[0]).split('.')[2]+'.')
    msg_start = f"🛰 <b>Buscando IP!!\n▶️ IP INICIAL : </b>{ip_form+ip}\n⏸ <b>IP FINAL : </b>{ip_form+ip_range}\n\n<i>⏳ Por favor espere .....</i>"
    msg_start1 = "\n➖➖➖➖➖➖➖\n\n\n➖➖➖➖➖➖➖"
    error_ip_find = f"🛰 No Hubo Éxito Buscando IP!!\n\n❌ IP INICIAL : {ip_form+ip}\n\n❌ IP FINAL : {ip_form+ip_range}"
    lf = msg_start+"\n➖➖➖➖➖➖➖\n"
    rg = "\n➖➖➖➖➖➖➖"
    info = "Buscando IP...\n"
    sms = bot.sendMessage(chat_id=chat,parse_mode="HTML",text=msg_start+msg_start1)
    time.sleep(1.5)
    bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=lf+info+rg)
    listado = '<b>LISTADO DE IP VERIFICADAS </b>🛰 !!\n'
    listar = jdb.listar(username)
    for ips in range(int(ip),int(ip_range)+1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect_ex((ip_form+str(ips),1))
            info = f"IP Válida ✅ !!\nIP: {ip_form+str(ips)}"
            bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=lf+info+rg)
            listado += '\nIP: '+ip_form+str(ips)+' ✅'
            sock.close()
            if listar == True:break
        except:
            info = f"IP Inválida ❌ !!\nIP: {ip_form+str(ips)}"
            bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=lf+info+rg)
            listado += '\nIP: '+ip_form+str(ips)+' ❌'
            sock.close()
    if listar == True:bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=info)
    else:bot.editMessageText(chat_id=chat,message_id=sms.message_id,parse_mode="HTML",text=listado)


#def pr_check(text,chat,bot,result):
#    proxy_sms = str(text).split(' ')[1]
#    if text.__contains__ ('socks5://'):proxy_sms = str(proxy_sms).split('socks5://')[1]
#    else:pass
#    proxy_de = S5Crypto.decrypt(f'{proxy_sms}')
#    ip = str(proxy_de).split(':')[0]
#    port = str(proxy_de).split(':')[1]
#    sms = bot.sendMessage(chat_id=chat,text=f'''
#🛰 Comprobando Proxy!!
#{ip}:{port}
#⏳ Por favor espere .....''')
#    try:
#        for i in range(-1,int(len(str(proxy_de).split('.'))-2)) :
#            i+=1
#            nma = int(str(proxy_de).split('.')[i])
#        for i in range(-1,1):
#            i+=1
#            nmb = int(str(str(proxy_de).split('.')[int(len(str(proxy_de).split('.'))-1)]).split(':')[i])
#    except:
#        bot.sendMessage(chat_id=chat,text="⚠️ PROXY NO VÁLIDO ❗️")
#        return
#    try:
#        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        result1 = sock.connect_ex((ip,int(port)))
#        print('RESULT1 :'+result1)
#        if result == 0:proxy_stat = '🌐 PROXY ACTIVO !!'
#        bot.editMessageText(chat_id=chat,message_id=sms.message_id,text=proxy_stat)
#    except Exception as ex:
#        print(str(ex))
#        print('RESULTADO: '+ip+':'+port)
#        print(proxy_de)
#        proxy_stat = '❌ PROXY INHABILITADO !!'
#        bot.editMessageText(chat_id=chat,message_id=sms.message_id,text=proxy_stat)
#    return