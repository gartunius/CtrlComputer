#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from os import scandir, geteuid
from getpass import getuser


class Process():
	"""docstring for Process."""

	def __init__(self, file_name):
		self.file_name = file_name
		self.process_pid = file_name.split("/")[2]
		self.process_name = None
		self.process_user = None
		self.process_user_uid = None

		current_user = {getuser() : str(geteuid())}

		with open(file_name + "/cmdline") as cmdline_file:
			self.process_name = cmdline_file.read()

		if self.process_name == "":
			self.process_name = "Not acessible"

		with open(file_name + "/status") as environ_file:
			pattern = re.compile("Uid:")
			for line in environ_file:
				if pattern.search(line) != None:
					uid = line.split()[1]
					self.process_user_uid = uid

					if uid == current_user.get(getuser()):
						self.process_user = getuser()
					elif uid == '0':
						self.process_user = "root"

	def print_process(self):
		print("PID      : {0}\nUSER UID : {1}\nUSER     : {2}\nCMD/NAME : {3}\n".format(self.process_pid, self.process_user_uid, self.process_user, self.process_name))


class Cpu():
	"""docstring for Cpu"""

	def __init__(self):
		self.file_name = "/proc/cpuinfo"
		self.cpu_model = None
		self.cpu_cores = {}

		with open(self.file_name) as cpuinfo:
			cpu_model_pattern = re.compile("model name")
			cpu_core_pattern = re.compile("processor")
			for line in cpuinfo.readlines():

				if cpu_model_pattern.search(line) != None:
					self.cpu_model = line.split(":")[1].strip()

				elif cpu_core_pattern.search(line) != None:
					core = line.split(":")[1].rstrip()[1]
					self.cpu_cores[core] = ""

		self.update_cores_freq_value()

	def update_cores_freq_value(self):
		cpu_freq_pattern = re.compile("cpu MHz")

		with open(self.file_name) as cpuinfo:
			counter = 0
			for line in cpuinfo.readlines():
				if cpu_freq_pattern.search(line) != None:
					self.cpu_cores[str(counter)] = line.split(":")[1].rstrip().strip()
					counter += 1


class Ram():
	"""docstring for Ram"""

	def __init__(self):
		self.file_name = "/proc/meminfo"
		self.mem_total = None
		self.mem_available = None
		self.mem_swap_total = None
		self.mem_swap_available = None

		mem_total_pattern = re.compile("MemTotal")
		mem_available_pattern = re.compile("MemAvailable")
		mem_swap_total_pattern = re.compile("SwapTotal")
		mem_swap_avaiable_pattern = re.compile("SwapFree")

		with open(self.file_name) as meminfo:
			for line in meminfo.readlines():

				if mem_total_pattern.search(line) != None:
					self.mem_total = line.split(":")[1].rstrip().strip()

				elif mem_available_pattern.search(line) != None:
					self.mem_available = line.split(":")[1].rstrip().strip()

				elif mem_swap_total_pattern.search(line) != None:
					self.mem_swap_total = line.split(":")[1].rstrip().strip()

				elif mem_swap_avaiable_pattern.search(line) != None:
					self.mem_swap_available = line.split(":")[1].rstrip().strip()


class OperationalSistem():
	"""docstring for ComputerStats"""

	def __init__(self):
		self.uptime_file_name = "/proc/uptime"
		self.sistem_uptime = None

		self.version_file_name = "/proc/version"
		self.sistem_version = None

		with open(self.uptime_file_name) as uptime:
			uptime_value_seconds = int(uptime.readline().rstrip().split(" ")[0].split(".")[0])
			uptime_hour = int(uptime_value_seconds / 3600)
			uptime_mins = int((uptime_value_seconds - (uptime_hour * 3600)) / 60)
			uptime_secs = int(uptime_value_seconds - (uptime_hour * 3600) - (uptime_mins * 60))
			self.sistem_uptime = str("{0:2}:{1:2}:{2:2}".format(uptime_hour, uptime_mins, uptime_secs))
			print(self.sistem_uptime)

		with open(self.version_file_name) as version:
			self.sistem_version = version.readline().strip()
