#!/usr/bin/python3

from subprocess import run
from os import path, getuid, mkdir

if getuid() != 0:    
    raise EnvironmentError("This script needs root privilages")

USER = "miha"

#modify sources.list to add contrib non-free
print("Modifying apt sources list...")
sources = open("/etc/apt/sources.list", "r+")
sources_lines = []

cnf = " contrib non-free\n"

for line in sources:
    sources_lines.append(line)
    if line.startswith("deb") and not line.endswith(cnf):
        sources_lines[-1] = sources_lines[-1][:-1] + cnf

sources.truncate()
sources.seek(0)

for line in sources_lines:
    sources.write(line)
    if line != "\n":
        print(line, end="")

sources.close()

print("-----------------------------")
print("Done!")

#install xorg, i3, snapd, arc-theme, unzip, network-manager, firmware-iwlwifi,
#apt_install = "sudo apt install xorg i3 snapd arc-theme unzip network-manager firmware-iwlwifi"

print("Installing updates and downloading programs...")

run(["apt", "update",])
run(["apt", "upgrade"])

install_array = [ "apt", "install" ]
install_array.append("xorg")
install_array.append("i3")
install_array.append("snapd")
install_array.append("arc-theme")
install_array.append("unzip")
install_array.append("network-manager")
install_array.append("firmware-iwlwifi")
install_array.append("git")
install_array.append("ufw")
# mybe add that pulseaudio

install_result = run(install_array)

print("-----------------------------")
print("Done!")

#setup firewall

print("Setting up firewall")

run("ufw enable".split())

print("-----------------------------")
print("Done!")

#setup iwlwifi
print("Settingup iwlwifi")

run("modprobe -r iwlwifi".split())
run("modprobe iwlwifi".split())


print("-----------------------------")
print("Done!")

# mkfile .gtk-2.0  .config/gtk-3.0/settings.ini .xinitrc
print("creating gtk theme files...")

home_folder = "/home/" + USER

gtk2_path = home_folder + "/.gtkrc-2.0"

config = home_folder + "/.config"
gtk3_folder_path = config + "/gtk-3.0"
gtk3_settings_path = gtk3_folder_path + "/settings.ini"

if not path.exists(home_folder):
    raise FileNotFoundError("such home folder does not exist!")

def create_gtk2(mode):    
    with open(gtk2_path, mode) as gtk2_file:
        #print("writing")
        gtk2_file.write('gtk-theme-name = "Arc-Dark"\n')
        gtk2_file.flush()        

if path.exists(gtk2_path):
    if path.isfile(gtk2_path):
        create_gtk2("w")
    elif path.isdir(gtk2_path):
        run(["rm", "-rf", gtk2_path])
        create_gtk2("x")
    else:
        run(["rm", "-f", gtk2_path])
        create_gtk2("x")
else:
    create_gtk2("x")

def create_gtk3(mode):
    with open(gtk3_settings_path, mode) as gkt3_file:
        gkt3_file.write("[Settings]\n")
        gkt3_file.write("gtk-theme-name = Arc-Dark\n")
        gkt3_file.write("gtk-application-prefer-dark-theme = true\n")
        gkt3_file.flush()

if path.exists(config):
    if path.isdir(config):
        pass
    else:
        run(["rm", "-f", config])
        mkdir(config)
else:
    mkdir(config)

if path.exists(gtk3_settings_path):
    if path.isfile(gtk3_settings_path):
        create_gtk3("w")
    elif path.isdir(gtk3_settings_path):
        run(["rm", "-rf", gtk3_settings_path])
        create_gtk3("x")
    else:
        run(["rm", "-f", gtk3_settings_path])
        create_gtk3("x")
else:
    create_gtk3("x")

print("-----------------------------")
print("Done!")
# download fonts font-awsome system sanfrancisco

print("Downloading fonts...")

command_font_awsome = 'wget https://github.com/FortAwesome/Font-Awesome/releases/download/5.2.0/fontawesome-free-5.2.0-web.zip -O /tmp/fontawsome.zip'
run(command_font_awsome.split())
command_san_francisco = 'wget https://github.com/supermarin/YosemiteSanFranciscoFont/archive/master.zip -O /tmp/sanfrancisco.zip'
run(command_san_francisco.split())

print("-----------------------------")
print("Done!")
# unzip and place fonts into right folder

print("Moving fonts files...")

command_font_awsome_unzip = "unzip -o /tmp/fontawsome.zip -d /tmp/"
run(command_font_awsome_unzip.split())

command_san_francisco_unzip = "unzip -o /tmp/sanfrancisco.zip -d /tmp/"
run(command_san_francisco_unzip.split())

local_folder = home_folder + "/.local"
share_folder = local_folder + "/share"
fonts_folder = share_folder + "/fonts"

# TODO: remove copy paste
# local folder
if path.exists(local_folder):
    if path.isdir(local_folder):
        pass
    else:
        run(["rm", "-f", local_folder])
        mkdir(local_folder)
else:
    mkdir(local_folder)

# share folder
if path.exists(share_folder):
    if path.isdir(share_folder):
        pass
    else:
        run(["rm", "-f", share_folder])
        mkdir(share_folder)
else:
    mkdir(share_folder)

# fonts folder
if path.exists(fonts_folder):
    if path.isdir(fonts_folder):
        pass
    else:
        run(["rm", "-f", fonts_folder])
        mkdir(fonts_folder)
else:
    mkdir(fonts_folder)

# cp /tmp/fontawesome-free-5.2.0-web/webfonts/*.ttf /home/miha/.local/share/fonts

def copy_font_awsome(filename):
    command_font_awsome_cp = "cp /tmp/fontawesome-free-5.2.0-web/webfonts/" + filename + " /home/" + USER + "/.local/share/fonts"    
    run(command_font_awsome_cp.split())

copy_font_awsome("fa-brands-400.ttf")
copy_font_awsome("fa-regular-400.ttf")
copy_font_awsome("fa-solid-900.ttf")

def copy_sf(filename):
    font_path="/tmp/YosemiteSanFranciscoFont-master/" + filename
    command_sf_cp = "cp temp /home/" + USER + "/.local/share/fonts"
    arry=command_sf_cp.split()
    arry[1]=font_path
    run(arry)

#command_san_francisco_cp = "cp /tmp/YosemiteSanFranciscoFont-master/*.ttf " + fonts_folder
#run(command_san_francisco_cp.split())

copy_sf("System San Francisco Display Bold.ttf")
copy_sf("System San Francisco Display Regular.ttf")
copy_sf("System San Francisco Display Thin.ttf")
copy_sf("System San Francisco Display Ultralight.ttf")

print("-----------------------------")
print("Done!")
# download i3 config file

print("Downloading i3 config file..")


command_config_i3 = "wget https://github.com/Jubast/Help/raw/master/i3/config -O /tmp/jubast_i3_config"
run(command_config_i3.split())

print("-----------------------------")
print("Done!")

# edit .config/i3/config

print("Moving config file...")

command_move_config = "mv /tmp/jubast_i3_config /home/" + USER + "/.config/i3/config"
run(command_move_config.split())

print("-----------------------------")
print("Done!")

print("-----------------------------")
print("-----------------------------")
print("-----------------------------")
print("-----------------------------")
print("dont forget to set up git!")
print("and network manager :)")
print("here is the status of ufw")
run("ufw status verbose".split())