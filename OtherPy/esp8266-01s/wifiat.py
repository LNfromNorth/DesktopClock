import utime


class at(object):
    def __init__(self,uart):
        self.uart=uart
        
    def sendCMD_waitResp(self,cmd, timeout=2000):
        print("CMD: " + cmd)
        self.uart.write(cmd.encode('utf-8'))
        return self.waitResp(timeout)
    def waitResp(self,timeout=2000):
        prvMills = utime.ticks_ms()
        resp = b""
        while (utime.ticks_ms()-prvMills)<timeout:
            if self.uart.any():
                resp = b"".join([resp, self.uart.read(1)])
        print(resp)
        return resp
    
    def sendCMD_waitRespLine(self,cmd, timeout=2000):
        print("CMD: " + cmd)
        self.uart.write(cmd.encode('utf-8'))
        return self.waitRespLine(timeout) 
    def waitRespLine(self,timeout=2000):
        cl=[]
        prvMills = utime.ticks_ms()
        while (utime.ticks_ms()-prvMills)<timeout:
            if self.uart.any():
                li=self.uart.readline()
                print(li)
                cl.append(li)
        return cl
    # 重启模块
    def restart(self):
        self.sendCMD_waitResp('+++')
        return self.sendCMD_waitResp("AT+RST\r\n")
    # 选择wifi模式 加入AP
    def connect(self,name,password):
        self.sendCMD_waitResp('AT+CWMODE=1\r\n')
        cmd='AT+CWJAP="%s","%s"\r\n' % (name,password)
        return self.sendCMD_waitResp(cmd)
    # 获取本地IP地址
    def netinfo(self):
        return self.sendCMD_waitResp("AT+CIFSR\r\n")
    # 获取配置信息
    def info(self):
        return self.sendCMD_waitResp("AT+GMR\r\n")
    # 恢复出厂设置
    def restore(self):
        return self.sendCMD_waitResp("AT+RESTORE\r\n")
    # Ping命令
    def ping(self,doip):
        return self.sendCMD_waitResp('AT+PING="%s"\r\n' % (doip,))
    # 列出当前可用AP
    def disconnect(self):
        return self.sendCMD_waitResp("AT+CWQAP\r\n")
    # 拼接所需的命令
    def http(self,url,method="GET",ua=1,content=1,data='',timeout=6):
        # 当作分割符
        self.sendCMD_waitResp("+++")
        # 分割协议，域名，和之后的请求
        typ,edx,domain,rel= url.split("/",3)
        # 拼接出cs
        # 建立 TCP 连接 注册 UDP 端口号
        if "HTTP" == typ[0:-1].upper():
            # CIPSTART 的使用方式
            cs='AT+CIPSTART="TCP","%s",80\r\n' % (domain,)
        # 不是HTTP请求
        else:
            # 设置 SSL Buffer size
            self.sendCMD_waitResp("AT+CIPSSLSIZE=4096\r\n")
            cs='AT+CIPSTART="SSL","%s",443\r\n' % (domain,)
        # 建立连接
        self.sendCMD_waitResp(cs)
        # 设置模块传输模式
        self.sendCMD_waitResp('AT+CIPMODE=1\r\n')
        # 发送数据
        self.sendCMD_waitResp('AT+CIPSEND\r\n')
        # 配置user-Agent 列出四个可选项
        if ua==1:
            ua="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"
        elif ua==2:
            ua="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"
        elif ua==3:
            ua="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        elif ua==4:
            ua="Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        # 配置文本类型
        if content==1:
            content="text/html;charset=utf-8"
        elif content==2:
            content="text/xml"
        elif content==3:
            content="application/json"
        elif content==4:
            content="multipart/form-data"
        elif content==5:
            content="application/x-www-form-urlencoded"
        # 构造请求   
        c="%s %s HTTP/1.1\r\nHOST:%s \r\nContent-Type: %s\r\nUser-Agent:%s \r\n  \n %s \r\n\r\n " % (method,url,domain,content,ua,data)
        return self.sendCMD_waitRespLine(c,1000*timeout)
    def toString(self,ls):
        list = []
        for string in ls:
            str = string.decode("utf-8")
            list.append(str)
        str = "".join(list)
        return str