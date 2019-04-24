#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gen_code
import glob
import os


enums = {
        'ENUM1': ['OPEN', 'CLOSE', 'ERR'],
        'ENUM2': ['OPEN2', 'CLOSE2', 'ERR2'],
        'ConnectStatusEnum': ['SUCCESS', 'CONNECTING', 'FAIL'],
        'UpdatePeriodEnum': ['UNKOWN','DAY','WEEK', 'MONTH'],
        'TableActionEnum': ['ADDCOLUMN', 'DELETECOLUMN', 'CHANGEFIELD', 'DELETEDATA', 'ADDRECORD'],
        'PlicyRuleEnum': ['RULETYPERANGE', 'RULETYPEEXACT', 'RULETYPENUMBER','RULETYPETIME'],
        'ReleaseStatusEnum': ['RELEASE', 'PENDING'],
        }


if __name__ == '__main__':
    env = os.environ
    api_dir = "cmd"
    gosrc = env['GOPATH'] + "/src/"
    gen_code.gen_code(
            api_dir=api_dir,
            filenames=[x for x in glob.glob(api_dir + "/*.json") if x not in glob.glob(api_dir + "/*_test.json")],
            mako_dir="go/graphql/mako",
            defines_out_dir=gosrc + "example/app/define",
            resolver_out_dir=gosrc + "example/app/resolver",
            schema_out_dir=gosrc + "example/cmd",
            go_test_dir=gosrc + "example/app/test",
            server=True,
            client=None,
            code_type='go',
            package='example',
            query_list=['getAllPermission', 'queryResourcePermission', 'judgePermission', 'login'],
            enums=enums,
            )
