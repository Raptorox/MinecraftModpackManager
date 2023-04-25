from zipfile import ZipFile
#from tqdm import tqdm
from glob import glob

import requests
import shutil
import json
import sys
import os

version = '1.0.0'
api_key = '$2a$10$bL4bIL5pUWqfcO7KQtnMReakwtfHbNKh6v1uTpKlzhwoueEJQnPnm'
mod_dir = 'mods'
mp_dir = 'modpacks'
app_dir = f'{os.environ["APPDATA"]}/.minecraft/mods'
conf_dir = f'{os.environ["APPDATA"]}/.minecraft'

# Create the mod directory if it doesn't exist
if not os.path.exists(mod_dir):
	os.mkdir(mod_dir)
	os.mkdir(mp_dir)
	print('First run detected. Run "python mmm.py import" to import your mods from your default Minecraft directory. If you don\'t, then goodbye installed mods!')
	exit()
if not os.path.exists(app_dir):
	os.makedirs(app_dir)

if len(sys.argv) < 2:
	print(f'''
Minecraft Mod Manager {version} by Raptorox
----------------------------------------
A tool to manage your Minecraft modpacks.
Created with hatred for instancing launchers and the CurseForge launcher.
I'm too lazy to download mods manually, sue me.
If you have any issues, remember: 'Future update' is a valid excuse.

Usage: mmm.py <command> [args]
Commands:
	set <file> - Set the modpack to the specified file.
	import [-debug] - Import all mods from the default Minecraft directory.
''')
	exit()

match sys.argv[1].lower():
	case 'set':	
		with ZipFile(sys.argv[2]) as zf:
			for file in zf.namelist():
				if file.startswith('overrides/') or file == 'manifest.json':
					zf.extract(file)

		with open('manifest.json', 'r') as f:
			manifest = json.load(f)
	
		mods = manifest['files']

		curr = 1
		total = len(mods)

		for modobj in mods:
			pid = modobj['projectID']
			fid = modobj['fileID']
			r = requests.get(f'https://api.curseforge.com/v1/mods/{pid}/files/{fid}/download-url', headers={'x-api-key': api_key})
			dl = json.loads(r.text)['data']
			mod = dl.split('/')[-1]

			if not os.path.exists(f'{mod_dir}/{mod}'):
				with open(f'{mod_dir}/{mod}', 'wb') as f:
					#data = requests.get(dl, stream=True)
					#total = len(data.content)
					#for byte in tqdm(data.iter_content(), total=total, unit='B', unit_scale=True, unit_divisor=1024, desc=f'{mod}'):
					print(f'Downloading {mod}... {curr}/{total}', end=' ')
					#for byte in data.iter_content():
					#	f.write(byte)
					f.write(requests.get(dl).content)
				print('DONE')
			else:
				print(f'Downloading {mod}... {curr}/{total} SKIPPED')
			curr+=1

		curr = 1

		print('Cleaning up...')
		for path in glob(f'{app_dir}/*', recursive=True):
			if os.path.isdir(path):
				shutil.rmtree(path)
			else:
				os.remove(path)
		shutil.rmtree(f'{conf_dir}/config', ignore_errors=True)
		shutil.rmtree(f'{conf_dir}/scripts', ignore_errors=True)
		print('Cleanup complete.')

		print('Installing mods...')
		for modobj in mods:
			pid = modobj['projectID']
			fid = modobj['fileID']
			r = requests.get(f'https://api.curseforge.com/v1/mods/{pid}/files/{fid}/download-url', headers={'x-api-key': api_key})
			dl = json.loads(r.text)['data']
			mod = dl.split('/')[-1]

			print(f'Installing {mod}... {curr}/{total}',end=' ')
			shutil.copy(f'{mod_dir}/{mod}', f'{app_dir}/{mod}')
			print('DONE')

			curr+=1
		
		print('Installing overrides...')
		for path in glob(f'overrides/**/*', recursive=True):
			if os.path.isdir(path):
				os.makedirs(path.replace('overrides', conf_dir), exist_ok=True)
			else:
				shutil.copy(path, path.replace('overrides', conf_dir))
		print('Overrides installed.')


		print('Destroying evidence...')
		os.remove('manifest.json')
		shutil.rmtree('overrides')
		shutil.move(sys.argv[2], f'{mp_dir}')
		print('Everything ready to go!')
	case 'import':
		newm = 0
		repeatm = 0
		for path in glob(f'{app_dir}/**/*.jar', recursive=True):
			file = path.split('\\')[-1]
			if len(sys.argv) >= 3 and sys.argv[2] == '-debug':
				print(path)
			if not os.path.exists(f'{mod_dir}/{file}'):
				shutil.copy(path, mod_dir)
				newm += 1
			else:
				repeatm += 1
		print(f'{newm} new mods imported, {repeatm} mods already exist, {newm + repeatm} total.')
	case _:
		print('Invalid command.')