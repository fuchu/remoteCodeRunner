#!/user/bin/env python3
##--coding:utf-8

import paramiko
import threading
import time
import io

class remote_host():
#需要控制的主机
	#host_username, host_ip, host_port, host_password = __remote_host_info
	#host_username = ''
	#host_ip = ''
	#host_port = ''
	#host_password = ''
	def __init__(self,each_host):
		self.each_host = each_host
		self.split_1 = self.each_host.split('@')
		self.split_2 = self.split_1[1].split(':')
		self.split_3 = self.split_2[1].split(' ')
	#def remote_host_info(self):
		#split_1 = self.each_host.split('@')
		#host_username = split_1[0]
		#split_2 = split_1[1].split(':')
		#host_ip = split_2[0] 
		#split_3 = split_2[1].split(' ')
		#host_port = split_3[0]
		#host_password = split_3[1]
		#return (host_username,host_ip,host_port,host_password)
	def get_host_username(self):
		host_username = self.split_1[0]
		return host_username
	def get_host_ip(self):
		host_ip = self.split_2[0]
		return host_ip
	def get_host_port(self):
		host_port = self.split_3[0]
		return host_port
	def get_host_password(self):
		host_password = self.split_3[1]
		return host_password

class cmd_runner(threading.Thread):
#运行线程类	
	#def __init__(self,host_ip,host_username,host_password,host_private_key_path,command_in):
	def __init__(self,host_ip,host_username,host_password,command_in,host_port):
		threading.Thread.__init__(self)
		self.host_ip = str(host_ip).strip()
		self.host_username = str(host_username).strip()
		self.host_password = str(host_password).strip()
		#self.host_private_key_path = host_private_key_path
		self.command_in = command_in
		self.host_port = int(host_port)
		#print(self.host_ip)
		#print(self.host_username)
		#print(self.host_password)
		#print(self.host_port)
		#print(self.command_in)
	def run(self):
		try:
			s = paramiko.SSHClient()
			s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			#s.connect(hostname=self.host_ip,port=self.host_port,username=self.host_username,password=self.host_password,timeout=5)
			#s.connect(hostname=hostip,port=port,username=username, password=password)
			s.connect(hostname=self.host_ip,port=self.host_port,username=self.host_username,password=self.host_password)
			#s.connect(hostname='192.168.0.234',port=22,username='zhou',password='123456')
			f = open(self.command_in,'r')
			command_input = f.readlines()
			f.close()
			for m in command_input:
				stdin, stdout, stderr = s.exec_command(m)
				stdin.write("Y")
				f = open('remote_cmd.log','a')
				f.writelines(stdout)
				f.close()
				#out = stdout.readlines()
				#for o in out:
					#print('%s' % o)
			s.close()
		#try:
			#s = paramiko.SSHClient()
			#s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			#s.connect(self.host_ip,self.host_port,self.host_username,self.host_password,timeout=5)
			#f = open(command_in,'r')
			#command_input = f.readlines()
			#f.close()
			#for m in command_input:
				#stdin, stdout, stderr = s.exec_command(m)
				#stdin.write("Y")
				#out = stdout.readlines()
				#for o in out:
					#print('%s' % o)
			#s.close()
		except Exception as e:
			command_run_errors = open('remote_runner.log','a')
			#command_run_errors.write('%s\t%s:\t%s\n'%(now,self.host_ip,e))
			command_run_errors.write('%s\t%s:\t%s\n'%(time.time(),self.host_ip,e))
			command_run_errors.close()
			pass
	def stop(self):
		self.thread_stop = True

def get_hosts(remote_host_list):
#获取所有主机
	f = open(remote_host_list,'r')
	a = f.readlines()
	f.close()
	all_hosts = []
	for each_host in a:
		one_host = remote_host(each_host)
		all_hosts.append(one_host)
	return all_hosts

def main_run():
	mythreads = []
	all_hosts = []
	all_hosts = get_hosts('remote_host.list')
	command_in = 'cmd.list'
	for x in all_hosts:
		#t = cmd_runner(x.host_ip,x.host_username,x.host_password,x.host_private_key_path,x.command_in,x.host_port)
		t = cmd_runner(x.get_host_ip(),x.get_host_username(),x.get_host_password(),command_in,x.get_host_port())
		mythreads.append(t)
	for i in range(len(mythreads)):
		mythreads[i].start()
	print('test!!! ok.')
	print('%s' % threading.activeCount())

if __name__ == '__main__':
	main_run()
