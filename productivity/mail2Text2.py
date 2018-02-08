# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 12:10:13 2017

@author: user
"""

import poplib
#import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import os
from bs4 import BeautifulSoup
import re
import csv

 
 
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
 
 
def guess_charset(msg):
  # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
    # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset
 
 
def get_email_headers(msg):
  # 邮件的From, To, Subject存在于根对象上:
    headers = {}
    for header in ['From', 'To', 'Subject', 'Date']:
        value = msg.get(header, '')
        if value:
            if header == 'Date':
                headers['date'] = value
            if header == 'Subject':
        # 需要解码Subject字符串:
                subject = decode_str(value)
                headers['subject'] = subject
            else:
        # 需要解码Email地址:
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                value = '%s <%s>' % (name, addr)
                if header == 'From':
                    from_address = value
                    headers['from'] = from_address
                else:
                    to_address = value
                    headers['to'] = to_address
    content_type = msg.get_content_type()
    print(('head content_type: ', content_type))
    return headers
 
 
def get_email_cntent(message, base_save_path):
    j = 0
    content = ''
    attachment_files = []
    for part in message.walk():
        j = j + 1
#    file_name = part.get_filename()
        contentType = part.get_content_type()
    # 保存附件
        if False:
            pass
#    if file_name: # Attachment
#      # Decode filename
#      h = email.header.Header(file_name)
#      dh = email.header.decode_header(h)
#      filename = dh[0][0]
#      if dh[0][1]: # 如果包含编码的格式，则按照该格式解码
#        filename = str(filename, dh[0][1])
#        filename = filename.encode("utf-8")
#      data = part.get_payload(decode=True)
#      att_file = open(base_save_path + filename, 'wb')
#      attachment_files.append(filename)
#      att_file.write(data)
#      att_file.close()
        elif contentType == 'text/plain' or contentType == 'text/html':
      # 保存正文
            data = part.get_payload(decode=True)
            charset = guess_charset(part)
            if charset:
                charset = charset.strip().split(';')[0]
                print(('charset:', charset))
                data = data.decode(charset)
            if type(data) == bytes:
                data = data.decode('utf-8')
            content = data
    return content, attachment_files
 
#去掉列表中空字符或只有空格TAB的字符串
def lst_strip(lst):
    L=[]
    for v in lst:
        v = str.strip(v)
        if v:
            L.append(v)
    return L

#提取数字
def num_extract(str_lst):
    v = []
    ptt = r'[-+]?\d*\.\d+|\d+'
    for ss in str_lst:
        orz = re.findall(ptt,ss)
        if len(orz)==0:
            v.append(ss)
        else:
            v.append(orz)
    return v

#将字符串列表中的字符串合并为一串
def str_merger(str_lst):
       s = ''
       for ss in str_lst:
              s += ss
       return s

if __name__ == '__main__':
  # 输入邮件地址, 口令和POP3服务器地址:
#  emailaddress = 'glad2meetu@yeah.net'
#  # 注意使用开通POP，SMTP等的授权码
#  password = ''
#  pop3_server = 'pop.yeah.net'
#  
#  
  
    emailaddress = 'mailtestretrive@yeah.net'
  # 注意使用开通POP，SMTP等的授权码
    password = 'sqm123'
    pop3_server = 'pop.yeah.net'
  
  
  # 连接到POP3服务器:
    server = poplib.POP3(pop3_server)
  # 可以打开或关闭调试信息:
  # server.set_debuglevel(1)
  # POP3服务器的欢迎文字:
    print((server.getwelcome()))
  # 身份认证:
    server.user(emailaddress)
    server.pass_(password)
  # stat()返回邮件数量和占用空间:
    messagesCount, messagesSize = server.stat()
    print(('messagesCount:', messagesCount))
    print(('messagesSize:', messagesSize))
  # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    print('------ resp ------')
    print(resp) # +OK 46 964346 响应的状态 邮件数量 邮件占用的空间大小
    print('------ mails ------')
    print(mails) # 所有邮件的编号及大小的编号list，['1 2211', '2 29908', ...]
    print('------ octets ------')
    print(octets)
 
  # 获取最新一封邮件, 注意索引号从1开始:
    length = len(mails)
    for i in range(length):
        resp, lines, octets = server.retr(i + 1)
    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
        msg_content = '\n'.join(bytes.decode(line) for line in lines if line not in [None,''])
    # 把邮件内容解析为Message对象：
        msg = Parser().parsestr(msg_content)
 
    # 但是这个Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，
    # 嵌套可能还 不止一层。所以我们要递归地打印出Message对象的层次结构：
        print('---------- 解析之后 ----------')
        
        base_save_path = os.getcwd() + r'\outcomes'
        try:
            os.mkdir(base_save_path)
        except OSError as e:
            print(e)
            pass
    
        
        msg_headers = get_email_headers(msg)
        content, attachment_files = get_email_cntent(msg, base_save_path)
        bsObj = BeautifulSoup(content,'lxml')
        start_sub = '尊敬的李卓'
        end_sub = '贡献'
        content = bsObj.getText()
        content = content[content.find(start_sub):content.find(end_sub)+len(end_sub)]
#    sss = lst_strip(content.split('、'))
        sss = lst_strip(re.split('[、：        ]+',content))
#    for ss in sss:
#        if (re.sub('\D','',ss) == '') | (re.sub('.','',ss)== ''):
#            sss.remove(ss)
#    for ss in sss:
#        if (ss.isdigit()) or (ss == '其中'):
#            sss.remove(ss)
            
        for ss in sss:
            if ss.isdigit():
                sss.remove(ss)
        for ss in sss:
            if ss == '其中':
                sss.remove(ss)
#    [sss.remove() for ss in sss if len(ss) > 18]
        for ss in sss[8:87]:
            if (len(ss) > 16) or (len(ss) <2):
                sss.remove(ss)    
        sss = num_extract(sss)
        L = []
        for ss in sss:
            if  type(ss) == list:
                L.append(str_merger(ss))
            else:
                L.append(ss)
    
        sss = [L[i:i+2] for i in range(0,len(L),2)]
        if len(sss) > 0:
            sss.append(sss.pop()[::-1])
       
        os.chdir(base_save_path)
        os.getcwd()
        with open(re.split('：|:',msg_headers['subject'])[-1].strip() +'.txt','w',encoding='utf-8') as f:
            f.write('subject:'+ msg_headers['subject'])
            f.write('\n')
            f.write('from_address:'+ msg_headers['from'])
            f.write('\n')
            f.write('to_address:'+ msg_headers['to'])
            f.write('\n')
            f.write('date:'+ msg_headers['date'])
            f.write('\n')
#        print(type(content))
            f.write('content:'+'\n'+ content)
        
        with open(re.split('：|:',msg_headers['subject'])[-1] + '.csv','w',encoding = 'utf-8',newline = '') as f:
            csv_out = csv.writer(f)
            for row in sss:
                csv_out.writerow(row)
 
        print(('subject:', msg_headers['subject']))
        print(('from_address:', msg_headers['from']))
        print(('to_address:', msg_headers['to']))
        print(('date:', msg_headers['date']))
        print(('content:', content))
#    print(('attachment_files: ', attachment_files))
        print('----------解析完毕------------')
 
  # 关闭连接:
    server.quit()