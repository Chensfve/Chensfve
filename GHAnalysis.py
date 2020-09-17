import json
import os
import argparse

def SpiltFile(file_address) :

    json_load = []
    Users = {}
    Repos = {}
    UAR = {}

    for path, direct, files in os.walk(file_address) :
        for each_file in files :
            if each_file[-5:] == ".json" :
                f = open(file_address + "\\" + each_file, 'r' , encording="utf-8").read()
                for each_line in f.spilt("\n") :
                    if len(each_line) != 0 :
                        try:
                            json_load.append(json.loads(each_line))
                        except :
                            pass

    for each in json_load :
        EventType = each.get("type")
        EventUser = each.get("actor").get("login")
        EventRepo = each.get("repo").get("name")

        if not (Users.get("EventUser")) :
            Users.update({EventUser:{}})
        if not (Users[EventUser].get(EventType)) :
            Users[EventUser].update({EventType:0})
        Users[EventUser][EventType] += 1

        if not (Repos.get("EventRepo")) :
            Repos.update({EventRepo:{}})
        if not (Repos[EventRepo].get("EventType")) :
            Repos[EventRepo].update({EventType:0})
        Repos[EventRepo][EventType] += 1

        if not (UAR.get("EventUser")) :
            UAR.update({EventUser:{}})
        if not (UAR[EventUser].get("EventRepo")) :
            UAR[EventUser].update({EventRepo:{}})
        if not (UAR[EventUser][EventRepo].get("EventType")) :
            UAR[EventUser][EventRepo].update({EventType:0})
        UAR[EventUser][EventRepo][EventType] += 1

    with open("Users.json", 'w' , encoding="utf-8") as f :
        json.dump(Users, f)
    with open("Repos.json", 'w' , encoding="utf-8") as f :
        json.dump(Repos, f)
    with open("UAR.json", 'w' , encoding="utf-8") as f :
        json.dump(UAR, f)

def CountUsers(user, event) :
    f = open("Users.json" ,'r' , encoding="utf-8").read()
    file = json.loads(f)
    if not (file.get(user)) :
        print("none")
    else :
        print(file[user].get(event))

def CountRepo(repo, event) :
    f = open("Repos.json" , 'r' , encoding="utf-8").read()
    file = json.loads(f)
    if not (file.get(repo)) :
        print("none")
    else :
        print(file[repo].get(event))

def CountUAR(user, repo, event) :
    f = open("UAR.json" , 'r' , encoding="utf-8").read()
    file = json.loads(f)
    if not (file.get(user)) :
        print("none")
    elif not (file[user].get(repo)) :
        print("none")
    else :
        print(file[user][repo].get(event))


class Run_single :
    def __init__(self) :
        self.parser = argparse.ArgumentParser()
        #self.data = None
        self.argInit()
        self.analyse()

    def argInit(self) :
        self.parser.add_argument('-i' , '--init')
        self.parser.add_argument('-u' , '--user')
        self.parser.add_argument('-r' , '--repo')
        self.parser.add_argument('-e' , '--event')

    def analyse(self) :
        if self.parser.parse_args().init :
            self.data = Data(self.parser.parse_args().init, 1)
            return 0
        else:
            #if self.data is None :
                #self.data = Data()
            if self.parser.parse_args().event :
                if self.parser.parse_args().user :
                    if self.parser.parse_args().repo :
                        res = self.data.CountUAR(
                            self.parser.parse_args().user, self.parser.parse_args().repo, self.parser.parse_args().event)
                    else :
                        res = self.data.CountUsers(
                            self.parser.parse_args().user, self.parser.parse_args().event)
                elif self.parser.parse_args().repo :
                    res = self.data.CountRepos(
                        self.parser.parse_args().reop, self.parser.parse_args().event)
                else :
                    print('error: argument -l or -c are required')
                    return 0
            else :
                print('error: argument -e is required')
                return 0
        return res


if __name__ == '__main__':
    Run = Run_single
