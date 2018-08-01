#!/usr/bin/python3

import os

if os.getuid() != 0:
    raise EnvironmentError("This script needs root privilages")

import subprocess as sp

USER = "miha"

def create_file_path(path):
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):        
        os.makedirs(dir_name)

def create_dir_path(path):    
    if not os.path.exists(path):        
        os.makedirs(path)

def file_and_write_data(file_path, data):
    create_file_path(file_path)
    mode = "x"
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            sp.run(["rm", "-rf", file_path])            
        elif os.path.isfile(file_path):
            mode = "w"
        else:
            sp.run(["rm", "-f", file_path])

    with open(file_path, mode) as file:
        file.write(data)

def execute(command):
    os.system(command)

def change_file(file_path, function):
    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist!")
    
    with open(file_path, "r") as file:
        file_data = file.read()
    
    for line_number, line_text in enumerate(file_data):
        file_data[line_number] = function(line_number, line_text)
    
    with open(file_path, "w") as file:
        file.write(file_data)

#modify sources.list to add contrib non-free
print("Modifying apt sources list...")

def sources_list_function(line_number, line_text):
    cnf = " contrib non-free\n"
    if line_text.startswith("deb") and not line_text.endswith(cnf):
        return line_text + cnf

sources_list_path = "/etc/apt/sources.list"
change_file(sources_list_path, sources_list_function)

print("-----------------------------")
print("Done!")

#install xorg, i3, snapd, arc-theme, unzip, network-manager, firmware-iwlwifi,
#apt_install = "sudo apt install xorg i3 snapd arc-theme unzip network-manager firmware-iwlwifi"

print("Installing updates and downloading programs...")

install_xorg = False
install_wayland = True

sp.run(["apt", "update", "-y"])
sp.run(["apt", "upgrade", "-y"])

install_array = [ "apt", "install" ]

install_array.append("snapd")
install_array.append("arc-theme")
install_array.append("unzip")
install_array.append("network-manager")
install_array.append("firmware-iwlwifi")
install_array.append("git")
install_array.append("ufw")
install_array.append("psmisc") #killall
install_array.append("alsa-utils") #alsa
install_array.append("pulseaudio")

if install_xorg:
    install_array.append("xorg")
    install_array.append("i3")

if install_wayland:
    wayland_packages = "libgles2-mesa-dev libdrm2 libdrm-dev libegl1-mesa-dev xwayland"
    install_array.extend(wayland_packages.split())
    wlc_packages = "cmake build-essential libinput10 libinput-dev libxkbcommon0 libxkbcommon-dev libudev-dev libxcb-image0 libxcb-image0-dev libxcb-composite0 libxcb-composite0-dev libxcb-xkb1 libxcb-xkb-dev libgbm1 libgbm-dev libdbus-1-dev libsystemd-dev zlib1g-dev libpixman-1-dev libxcb-ewmh-dev wayland-protocols"
    install_array.extend(wlc_packages.split())

install_array.append("-y")
sp.run(install_array)

# splited cuz some problem with 1GB optional downloads shit (dunnu if i use some optional stuff from the above packages. tldr: i don't wana break stuff)

if install_wayland:
    install_array = [ "apt", "install" ]
    sway_install = "-o APT::Install-Recommends=0 -o APT::Install-Suggests=0 libpcre3 libpcre3-dev libcairo2 libcairo2-dev libpango1.0-0 libpango1.0-dev asciidoc libjson-c3 libjson-c-dev libcap-dev xsltproc libpam0g-dev"
    install_array.append(sway_install.split())
    install_array.append("-y")
    sp.run(install_array)

print("-----------------------------")
print("Done!")

#setup firewall

print("Setting up firewall")

sp.run("ufw enable".split())

print("-----------------------------")
print("Done!")

#setup iwlwifi
print("Settingup iwlwifi")

sp.run("modprobe -r iwlwifi".split())
sp.run("modprobe iwlwifi".split())

print("-----------------------------")
print("Done!")

# mkfile .gtk-2.0  .config/gtk-3.0/settings.ini .xinitrc
print("creating gtk theme files...")

home_folder = os.path.join("/home", USER)
gtk2_path = os.path.join(home_folder, "/.gtkrc-2.0")
gtk3_path = os.path.join(home_folder, ".config", "gtk-3.0", "settings.ini")

# run chown on whole homefolder
#chown_gtk2 = "chown miha:miha " + gtk2_path
#sp.run(chown_gtk2.split())

file_and_write_data(gtk2_path, 'gtk-theme-name = "Arc-Dark"\n')
file_and_write_data(gtk3_path, "[Settings]\ngtk-theme-name = Arc-Dark\ngtk-application-prefer-dark-theme = true\n")

print("-----------------------------")
print("Done!")
# download fonts font-awsome system sanfrancisco

print("Downloading fonts...")

command_font_awsome = 'wget https://github.com/FortAwesome/Font-Awesome/releases/download/5.2.0/fontawesome-free-5.2.0-web.zip -O /tmp/fontawsome.zip'
sp.run(command_font_awsome.split())
command_san_francisco = 'wget https://github.com/supermarin/YosemiteSanFranciscoFont/archive/master.zip -O /tmp/sanfrancisco.zip'
sp.run(command_san_francisco.split())

print("-----------------------------")
print("Done!")
# unzip and place fonts into right folder

print("Moving fonts files...")

command_font_awsome_unzip = "unzip -o /tmp/fontawsome.zip -d /tmp/"
sp.run(command_font_awsome_unzip.split())

command_san_francisco_unzip = "unzip -o /tmp/sanfrancisco.zip -d /tmp/"
sp.run(command_san_francisco_unzip.split())

#local_folder = home_folder + "/.local"
#share_folder = local_folder + "/share"
#fonts_folder = share_folder + "/fonts"

fonts_folder = os.path.join(home_folder, ".local", "share", "fonts")
create_dir_path(fonts_folder)

# cp /tmp/fontawesome-free-5.2.0-web/webfonts/*.ttf /home/miha/.local/share/fonts

def copy_font_awsome(filename):
    command_font_awsome_cp = "cp /tmp/fontawesome-free-5.2.0-web/webfonts/" + filename + " /home/" + USER + "/.local/share/fonts"    
    sp.run(command_font_awsome_cp.split())

copy_font_awsome("fa-brands-400.ttf")
copy_font_awsome("fa-regular-400.ttf")
copy_font_awsome("fa-solid-900.ttf")

def copy_sf(filename):
    font_path="/tmp/YosemiteSanFranciscoFont-master/" + filename
    command_sf_cp = "cp temp /home/" + USER + "/.local/share/fonts"
    arry=command_sf_cp.split()
    arry[1]=font_path
    sp.run(arry)

#command_san_francisco_cp = "cp /tmp/YosemiteSanFranciscoFont-master/*.ttf " + fonts_folder
#run(command_san_francisco_cp.split())

copy_sf("System San Francisco Display Bold.ttf")
copy_sf("System San Francisco Display Regular.ttf")
copy_sf("System San Francisco Display Thin.ttf")
copy_sf("System San Francisco Display Ultralight.ttf")

print("-----------------------------")
print("Done!")
# download wm config file

if install_xorg:
    print("Downloading i3 config file..")

    command_config_i3 = "wget https://github.com/Jubast/Help/raw/master/i3/config -O /tmp/jubast_wm_config"
    sp.run(command_config_i3.split())

if install_wayland:
    print("Downloading sway config file..")

    command_config_i3 = "wget https://github.com/Jubast/Help/raw/master/sway/config -O /tmp/jubast_wm_config"
    sp.run(command_config_i3.split())

print("-----------------------------")
print("Done!")

# edit .config/i3/config

print("Moving config file...")

if install_xorg:
    config_folder = "i3"

if install_wayland:
    config_folder = "sway"

wm_config_path = os.path.join(home_folder, ".config", config_folder, "config")
create_file_path(wm_config_path)
command_move_config = "mv /tmp/jubast_wm_config " + wm_config_path
sp.run(command_move_config.split())

print("-----------------------------")
print("Done!")

if install_xorg:
    print("Creating .xinitrc file")
    xinit_file = home_folder + "/.xinitrc"
    file_and_write_data(xinit_file, "#!/bin/sh\n\nexec i3\n")

if install_wayland:
    print("installing sway")

    print("downloading wlc")
    git_path = os.path.join(home_folder, "git")
    create_dir_path(git_path)
    clone_wlc = "git -C " + git_path + " clone https://github.com/Cloudef/wlc.git"
    sp.run(clone_wlc.split())

    git_wlc_path = os.path.join(git_path, "wlc")
    submodule_update = "git -C " + git_wlc_path + " submodule update --init --recursive"
    sp.run(submodule_update.split())

    target_path = os.path.join(git_wlc_path, "target")
    create_dir_path(target_path)

    cmake = "cmake -B" + target_path + " -H" + git_wlc_path + " -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local -DSOURCE_WLPROTO=ON"
    make = "make -C" +  


    
print("-----------------------------")
print("Done!")

print("fixing file ownage xd")
chown_on_home = "chown -R " + USER + ":" + USER + " " + home_folder
sp.run(chown_on_home.split())

print("-----------------------------")
print("Done!")

print("-----------------------------")
print("-----------------------------")
print("-----------------------------")
print("-----------------------------")
print("dont forget to set up git!")
print("and network manager :)")
print("here is the status of ufw")
sp.run("ufw status verbose".split())
