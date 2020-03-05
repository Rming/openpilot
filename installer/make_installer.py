#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-
import os
import requests

baseDir = os.path.split(os.path.realpath(__file__))[0]
githubApiToken = 'a1bdeee22c60fcde021c92add2760b2b1cce1ea1'
githubApiBase  = 'https://api.git.sdut.me'
forks = {
    'commaai':{
        'branch_url' :githubApiBase + '/repos/commaai/openpilot/branches',
        'cdn' :{
            'default' :'https://github.com/commaai/openpilot',
            'cn'      :'https://gitee.com/afaaa/openpilot',
        },
    },
    'afa':{
        'branch_url' :githubApiBase + '/repos/rming/openpilot/branches',
        'cdn' :{
            'default' :'https://github.com/rming/openpilot',
            'cn'      :'https://gitee.com/afaaa/openpilot-cn',
        },
    },
    'dragonpilot':{
        'branch_url' :githubApiBase + '/repos/dragonpilot-community/dragonpilot/branches',
        'cdn' :{
            'default' :'https://github.com/dragonpilot-community/dragonpilot',
            'cn'      :'https://gitee.com/afaaa/dragonpilot',
        },
    },
    'kegman':{
        'branch_url' :githubApiBase + '/repos/kegman/openpilot/branches',
        'cdn' :{
            'default' :'https://github.com/kegman/openpilot',
            'cn'      :'https://gitee.com/afaaa/kegman',
        },
    },
    'gernby':{
        'branch_url' :githubApiBase + '/repos/gernby/openpilot/branches',
        'cdn' :{
            'default' :'https://github.com/gernby/openpilot',
            'cn'      :'https://gitee.com/afaaa/gernby',
        },
    },
    'arne':{
        'branch_url' :githubApiBase + '/repos/arne182/openpilot/branches',
        'cdn' :{
            'default' :'https://github.com/arne182/openpilot',
            'cn'      :'https://gitee.com/afaaa/arne182',
        },
    },
}

def updateInstallerMakefile():
    depsStr = "DEPS := "
    makeAllStr = "all: "
    makeFileStr = ""
    ss = requests.Session()
    ss.headers.update({
        'Authorization' : 'token ' + githubApiToken,
        'User-Agent'    : 'requests',
    })
    for name in forks:
        forkData  = forks[name]
        branchUrl = forkData['branch_url']
        cdnData   = forkData['cdn']
        r = ss.get(branchUrl)
        if r.status_code != 200:
            print ("error: request github api error", branchUrl, r.status_code)
            return False

        branches = []
        rjson = r.json()
        for branch in rjson:
            branches.append(branch['name'])
        for region in cdnData:
            url = cdnData[region]
            for branch in branches:
                branch = branch.lower()
                fix = "%s_%s_%s" % (name, branch, region)
                objsName = "OPENPILOT_OBJS_%s" % fix
                ofileName = "installer_%s.o" % fix
                objsStr = "%s = %s continue_openpilot.o $(COMMON_OBJS)" % (objsName, ofileName)
                ofileStr = "%s: installer.c\n\t@echo \"[ CC ] $@\"\n\t$(CC) $(CFLAGS) -MMD -I.. -I../selfdrive -DBRAND=openpilot -DBRANCH=%s -DGITURL=%s -c -o '$@' '$<'" % (ofileName, branch, url)
                targetStr = "installers/installer_%s: $(%s)\n\t@echo \"[ LINK ] $@\"\n\t$(CXX) -fPIC -o '$@' $^ -s $(FRAMEBUFFER_LIBS) -L/system/vendor/lib64 $(OPENGL_LIBS) -lm -llog" % (fix, objsName)
                depsStr += "$(%s:.o=.d) " % objsName
                makeAllStr += "installers/installer_%s " % fix
                makeFileStr += "%s\n\n%s\n\n%s\n\n\n" % (objsStr, ofileStr, targetStr)
            # print name, region, url, branchUrl
    makeFileStr = "%s\n.PHONY: all\n%s\n" % (depsStr, makeAllStr) + makeFileStr

    with open(baseDir + '/MakefileTpl') as f:
        s = f.read()
        s = s.replace("{{MAKE_FILE_STR}}", makeFileStr)
        with open(baseDir + "/Makefile","w") as f:
            f.write(s)


if __name__ == '__main__':
    updateInstallerMakefile()
