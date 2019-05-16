#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gencode_pkg.go.graphql import gen
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
    gosrc = "go_example"  # env['GOPATH'] + "/src/"
    gen.gen_code(
            filenames=["json/newVersion.json", "json/newVersion2.json"],
            mako_dir="mako/go/graphql",
            data_type_out_dir=gosrc + "/app/define",
            resolver_out_dir=gosrc + "/app/resolver",
            schema_out_dir=gosrc + "/main",
            go_test_out_dir=gosrc + "/app/test",
            package='example',
            gen_server=True,
            gen_client=None,
            # query_list=['getAllPermission', 'queryResourcePermission', 'judgePermission', 'login'],
            )
