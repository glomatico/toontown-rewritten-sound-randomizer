from os import path, listdir, mkdir, chdir, remove
from tkinter.filedialog import askdirectory, askopenfilename
from shutil import which, rmtree, copy
from random import sample
from subprocess import run
from pathlib import Path

def main():
    # Welcome message
    print('Welcome to the Toontown Rewritten Sound Randomizer!')

    # Get Toontown Rewritten directory
    ttr_dir = ''
    if path.isdir('C:\\Program Files (x86)\\Toontown Rewritten'):
        ttr_dir = 'C:\\Program Files (x86)\\Toontown Rewritten'
    if path.isdir('C:\\Program Files\\Toontown Rewritten'):
        ttr_dir = 'C:\\Program Files\\Toontown Rewritten'
    if path.isdir('~/Library/Application Support/Toontown Rewritten'):
        ttr_dir = '~/Library/Application Support/Toontown Rewritten'
    if path.isdir('~/.var/app/xyz.xytime.Toontown/data/toontown-rewritten'):
        ttr_dir = '~/.var/app/xyz.xytime.Toontown/data/toontown-rewritten'
    if not ttr_dir:
        input('\nYou will be prompted to select your Toontown Rewritten directory. Press Enter to continue.')
        ttr_dir = askdirectory(title = 'Select Toontown Rewritten directory')
        if not ttr_dir:
            print('\nNo directory was selected.')
            return
    phase_files = [phase_file for phase_file in listdir(ttr_dir) if 'phase_' in phase_file and phase_file.endswith('.mf')]
    if not phase_files:
        print('\nNo phase files were found.')
        return
    
    # Get Multify path
    multify_exe = which('multify')
    if not multify_exe:
        input('\nYou will be prompted to select the Multify executable to extract the phase files. Press Enter to continue.')
        multify_exe = askopenfilename(title = 'Select Multify binary', filetypes = [('Multify executable', 'multify*')])
        if not multify_exe:
            print('\nNo file selected.')
            return
    
    # Final confirmaion
    print('\nThe content pack will be createad at "{}/resources/toontown_rewritten_sound_randomizer.mf" using the Multify executable at "{}".'.format(ttr_dir.replace("\\", "/"), multify_exe.replace("\\", "/")))
    input('\nPress Enter to start.')	

    # Create temporary directory
    temp_dir = Path(ttr_dir) / 'toontown_rewritten_sound_randomizer_temp'
    if path.exists(temp_dir):
        print('\nRemoving existing temporary directory...')
        rmtree(temp_dir)
    mkdir(temp_dir)

    # Extract phase files
    print('\nExtracting phase files...')
    chdir(temp_dir)
    for phase_file in phase_files:
        run([multify_exe, '-x', '-f', Path(ttr_dir) / phase_file])

    # Remove everything except audio files
    print('\nRemoving everything except audio...')
    for content in listdir():
        for subcontent in listdir(content):
            if path.isdir(Path(content) / subcontent):
                if subcontent != 'audio':
                    rmtree(Path(content) / subcontent)
            else:
                remove(Path(content) / subcontent)
        if path.isdir(content) and not listdir(content):
            rmtree(content)

    # Start randomizing
    to_randomize = ['bgm', 'sfx', 'dial']
    for item in to_randomize:
        print(f'\nRandomizing "{item}"...')
        audio_files_location = []
        for content in listdir():
            if path.exists(Path(content) / 'audio' / item):
                for subcontent in listdir(Path(content) / 'audio' / item):
                    audio_files_location.append(Path(content) / 'audio' / item / subcontent)
        random_indexes = sample(range(0, len(audio_files_location)), len(audio_files_location))
        for i in range(len(audio_files_location)):
            if audio_files_location[i] != audio_files_location[random_indexes[i]]:
                copy(audio_files_location[i], audio_files_location[random_indexes[i]])

    # Create ini file
    with open('info.ini', 'w') as f:
        f.write('[PackInfo]\nname=Toontown Rewritten Sound Randomizer\ndescription=Made with https://github.com/glomatico/toontown-rewritten-sound-randomizer')

    # Create content pack file
    print('\nCreating content pack file...')
    if not path.exists(Path(ttr_dir) / 'resources'):
        mkdir(Path(ttr_dir) / 'resources')
    resource_pack_path = Path(ttr_dir) / 'resources' / 'toontown_rewritten_sound_randomizer.mf'
    run([multify_exe, '-c', '-f', resource_pack_path] + listdir())

    # Remove temporary directory
    print('\nRemoving temporary directory...')
    chdir(ttr_dir)
    rmtree(temp_dir)

    # Done
    print('\nAll done! You can now play Toontown Rewritten with random sounds.')


if __name__ == '__main__':
    try:
        main()
        input('\nPress Enter to exit.')
    except KeyboardInterrupt:
        exit(0)
