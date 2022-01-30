import json
import os


class Modify:

    def __init__(self, config, player_map):
        self.__config = config
        self.__player_map = player_map

    def modify_json(self, file):
        prompt = f'[{file["name"]}]'
        # if filename change it's deactivated via __config it exits
        if not file['enable']:
            return print(f'{prompt} Skipped, {file["name"]}: {file["enable"]}')
        file_path = os.path.join(self.__config['server_directory'], file['name'])
        # if file doesn't exist, returns with error print
        if not os.path.isfile(file_path):
            return print(f'{prompt} ERROR file not found in directory: {file_path}')
        # open, loads & closes filename in read __mode
        read_file = open(file_path, 'r')
        file_json = json.load(read_file)
        read_file.close()
        # for each in file_json
        print(f'{prompt} Starting changing file: {file_path}')
        file_change = False
        for player in file_json:
            if player['uuid'] in self.__player_map:
                print(f'{prompt} {self.__player_map[player["uuid"]][1]} : {player["uuid"]} -> {self.__player_map[player["uuid"]][0]}')
                player['uuid'] = self.__player_map[player['uuid']][0]
                file_change = True
        # if something was changed
        if file_change:
            # open filename in write __mode
            write_file = open(file_path, 'w')
            # save changes into the file in the disk, then closes it
            json.dump(file_json, write_file, indent=4)
            write_file.close()
            print(f'{prompt} Successfully written json to file: {file_path}')
        else:
            print(f'{prompt} Nothing changed so file stays same: {file_path}')

    def modify_folder(self, folder):
        prompt = f'[{folder["name"]}]'
        # if folder change it's deactivated via __config it exits
        if not folder['enable']:
            return print(f'{prompt} Skipped, {folder["name"]}: {folder["enable"]}')
        folder_path = os.path.join(self.__config['server_directory'], self.__config['world_directory'], folder['name'])
        # if folder doesn't exist, returns with error print
        if not os.path.isdir(folder_path):
            return print(f'{prompt} ERROR not found directory: {folder_path}')
        # for each in folder_path
        print(f'{prompt} Starting changing folder files: {folder_path}')
        file_change = False
        for file in os.listdir(folder_path):
            file_split = str(file).split(".")
            file_uuid = file_split[0]
            if file_uuid in self.__player_map:
                old_name = os.path.abspath(os.path.join(folder_path, file))
                new_name = os.path.abspath(os.path.join(folder_path, f'{self.__player_map[file_uuid][0]}.{file_split[1]}'))
                try:
                    # changes filename
                    os.rename(old_name, new_name)
                    file_change = True
                    print(f'{prompt} {self.__player_map[file_uuid][1]} : {file} -> {self.__player_map[file_uuid][0]}.{file_split[1]}')
                    print(f'{prompt} oldpath: {old_name}')
                    print(f'{prompt} newpath: {new_name}')
                except:
                    print(f'{prompt} ERROR could not rename file: {file}')
        if not file_change:
            print(f'{prompt} Nothing changed so folder stays same: {folder_path}')
