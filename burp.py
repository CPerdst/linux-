import crypt
import argparse
import os
import string
import itertools
import time

parser = argparse.ArgumentParser(description="一款用于爆破linux用户密码的脚本工具")
parser.add_argument("-n","--name",help="指定爆破某个用户（ 不指定默认爆破所有",type=str,dest="name",required=False)
parser.add_argument("-s",'--shadow',help="指定shadow文件路径",type=str,dest='shadowPath',required=True)
parser.add_argument("-d","--dict",help="指定使用的爆破目录（ 留空则使用内置小字典",dest="dictPath",required=False)
parser.add_argument("-m","--method",help="指定爆破方法（ 1: 字典爆破，2: 完全爆破",dest="method",required=False)


def read_name_from_file(filename):
    with open(filename,'r') as f:
        for line in f:
            name = line.strip()
            yield name

def generate_letter_combinations(case):
    for r in range(1, 27):
        for combination in itertools.combinations(case, r):
            yield ''.join(combination)

def passwd_gen():
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = '0123456789'
    return generate_letter_combinations(lowercase)



def burpOne(userShadowInfo:str, dictPath:str, method:int):
    # *** 1: 字典爆破 2: 完全爆破 ***
    infos = userShadowInfo.split(':')
    userName = infos[0]
    miwen = infos[1]
    salt = '$'+miwen.split("$")[1]+'$'+miwen.split('$')[2]
    if method == 1:
        if not dictPath:
            gen = read_name_from_file('./passwdDict.txt')
        elif os.path.isfile(dictPath):
            gen = read_name_from_file(dictPath)
        else:
            print(f"Path: {dictPath} 出错.")
            exit()
    elif method == 2:
        gen = passwd_gen()
    else:
        gen = read_name_from_file('./passwdDict.txt')
    print(f'正在爆破 {userName} 密码中.')
    for mingwen in gen:
        if miwen == crypt.crypt(mingwen,salt):
            print(f"username:{userName} -> passwd:{mingwen}")
            return
    print(f"username: {userName} 密码未找到.")
    
def burpAll(availableUser:dict, dictPath:str, method:int):
    for name,userShadowInfo in availableUser.items():
        burpOne(userShadowInfo,dictPath,method)

def main(args):
    args=args.__dict__
    if not os.path.isfile(args['shadowPath']):
        print(f"Path: {args['shadowPath']} 出错.")
        exit()
    
    shadowContent=''
    availableUser={}

    with open(args['shadowPath'],'r') as f:
        shadowContent = f.read().strip()
        f.close()
    for user in shadowContent.split('\n'):
        if '$' in user.split(':')[1]:
            availableUser[user.split(':')[0]] = user
    if not args['name']:
        burpAll(availableUser,args['dictPath'],method=int(args['method']))
    else:
        if not availableUser.get(args['name']):
            print("shadow文件内未找到爆破用户.")
            exit()
        burpOne(availableUser[args['name']],args['dictPath'],method=int(args['method']))
        


if __name__ == '__main__':
    args=parser.parse_args()
    main(args)
