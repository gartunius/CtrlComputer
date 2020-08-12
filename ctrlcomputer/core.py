#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

import Computer

def main():
	process_dir = "/proc"
	pattern = re.compile("\d")

	with os.scandir(process_dir) as directories:
		for entry in directories:
			if pattern.search(entry.name) != None :
				file_name = process_dir + "/" + entry.name
				p = Computer.Process(file_name)

	c = Computer.Cpu()
	m = Computer.Ram()
	operationalsistem = Computer.OperationalSistem()


if __name__ == "__main__":
	main()
