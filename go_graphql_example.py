#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg.go.graphql import gen
# import glob
# import os


# enums = {
#         'ENUM1': ['OPEN', 'CLOSE', 'ERR'],
#         'ENUM2': ['OPEN2', 'CLOSE2', 'ERR2'],
#         'ConnectStatusEnum': ['SUCCESS', 'CONNECTING', 'FAIL'],
#         'UpdatePeriodEnum': ['UNKOWN', 'DAY', 'WEEK', 'MONTH'],
#         'TableActionEnum': ['ADDCOLUMN', 'DELETECOLUMN', 'CHANGEFIELD', 'DELETEDATA', 'ADDRECORD'],
#         'PlicyRuleEnum': ['RULETYPERANGE', 'RULETYPEEXACT', 'RULETYPENUMBER', 'RULETYPETIME'],
#         'ReleaseStatusEnum': ['RELEASE', 'PENDING'],
#         }


if __name__ == '__main__':
    # env = os.environ
    # json_dir = "json"
    gosrc = "./"  # env['GOPATH'] + "/src/"
    gen.gen_code(
            # json_dir=api_dir,
            filenames=["json/newVersion.json", "json/newVersion2.json"],
            mako_dir="mako/go/graphql",
            data_type_out_dir=gosrc + "go_example/app/define",
            resolver_out_dir=gosrc + "go_example/app/resolver",
            schema_out_dir=gosrc + "go_example/main",
            go_test_dir=gosrc + "go_example/app/test",
            gen_server=True,
            gen_client=None,
            # code_type='go_graphql',
            package='example',
            # query_list=['getAllPermission', 'queryResourcePermission', 'judgePermission', 'login'],
            # enums=enums,
            )
